from datetime import date
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.modelos import Libro, Usuario, Prestamo, EstadoDePrestamo

class ErrorBiblioteca(Exception):
    pass

def texto_requerido(valor: str, campo: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorBiblioteca(f"{campo} es obligatorio")
    return valor.strip()

def entero_no_negativo(valor: int, campo: str) -> int:
    if type(valor) is not int or valor < 0:
        raise ErrorBiblioteca(f"{campo} debe ser un entero no negativo")
    return valor

def guardar(db: Session):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ErrorBiblioteca("Conflicto de datos (correo duplicado o restricción de integridad)") from exc
    except Exception:
        db.rollback()
        raise

def crear_libro(db: Session, titulo: str, autor: str, ejemplares_disponibles: int):
    titulo = texto_requerido(titulo, "Título")
    autor = texto_requerido(autor, "Autor")
    entero_no_negativo(ejemplares_disponibles, "Ejemplares")
    libro = Libro(titulo=titulo, autor=autor, ejemplares_disponibles=ejemplares_disponibles)
    db.add(libro)
    guardar(db)
    db.refresh(libro)
    return libro

def listar_libros(db: Session):
    return db.scalars(select(Libro).order_by(Libro.id)).all()

def listar_libros_disponibles(db: Session):
    return db.scalars(
        select(Libro).where(Libro.ejemplares_disponibles > 0).order_by(Libro.id)
    ).all()

def buscar_libro_por_id(db: Session, libro_id: int):
    return db.get(Libro, libro_id)

def actualizar_libro(db: Session, libro_id: int, titulo: str, autor: str, ejemplares_disponibles: int):
    libro = buscar_libro_por_id(db, libro_id)
    if libro is None:
        raise ErrorBiblioteca("Libro inexistente")
    titulo = texto_requerido(titulo, "Título")
    autor = texto_requerido(autor, "Autor")
    entero_no_negativo(ejemplares_disponibles, "Ejemplares")
    libro.titulo = titulo
    libro.autor = autor
    libro.ejemplares_disponibles = ejemplares_disponibles
    guardar(db)
    db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = buscar_libro_por_id(db, libro_id)
    if libro is None:
        raise ErrorBiblioteca("Libro inexistente")
    if db.scalar(select(Prestamo.id).where(Prestamo.libro_id == libro_id).limit(1)) is not None:
        raise ErrorBiblioteca("No se puede eliminar un libro con historial de préstamos")
    db.delete(libro)
    guardar(db)
    return libro

def crear_usuario(db: Session, nombre: str, correo: str):
    nombre = texto_requerido(nombre, "Nombre")
    correo = texto_requerido(correo, "Correo")
    if "@" not in correo or correo.startswith("@") or correo.endswith("@"):
        raise ErrorBiblioteca("Correo inválido")
    usuario = Usuario(nombre=nombre, correo=correo)
    db.add(usuario)
    guardar(db)
    db.refresh(usuario)
    return usuario

def listar_usuarios(db: Session):
    return db.scalars(select(Usuario).order_by(Usuario.id)).all()

def buscar_usuario_por_id(db: Session, usuario_id: int):
    return db.get(Usuario, usuario_id)

def actualizar_usuario(db: Session, usuario_id: int, nombre: str, correo: str):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if usuario is None:
        raise ErrorBiblioteca("Usuario inexistente")
    nombre = texto_requerido(nombre, "Nombre")
    correo = texto_requerido(correo, "Correo")
    if "@" not in correo or correo.startswith("@") or correo.endswith("@"):
        raise ErrorBiblioteca("Correo inválido")
    usuario.nombre = nombre
    usuario.correo = correo
    guardar(db)
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario_id: int):
    usuario = buscar_usuario_por_id(db, usuario_id)
    if usuario is None:
        raise ErrorBiblioteca("Usuario inexistente")
    if db.scalar(select(Prestamo.id).where(Prestamo.usuario_id == usuario_id).limit(1)) is not None:
        raise ErrorBiblioteca("No se puede eliminar un usuario con historial de préstamos")
    db.delete(usuario)
    guardar(db)
    return usuario

def registrar_prestamo(db: Session, libro_id: int, usuario_id: int, cantidad: int, fecha: date):
    if type(cantidad) is not int or cantidad <= 0:
        raise ErrorBiblioteca("Cantidad debe ser un entero positivo")
    if not isinstance(fecha, date):
        raise ErrorBiblioteca("Fecha inválida")
    if buscar_usuario_por_id(db, usuario_id) is None:
        raise ErrorBiblioteca("Usuario inexistente")
    # UPDATE condicional evita sobreprestar unidades si hay solicitudes simultáneas.
    try:
        result = db.execute(
            update(Libro)
            .where(Libro.id == libro_id, Libro.ejemplares_disponibles >= cantidad)
            .values(ejemplares_disponibles=Libro.ejemplares_disponibles - cantidad)
        )
        if result.rowcount != 1:
            if buscar_libro_por_id(db, libro_id) is None:
                raise ErrorBiblioteca("Libro inexistente")
            raise ErrorBiblioteca("No hay ejemplares suficientes")
        prestamo = Prestamo(libro_id=libro_id, usuario_id=usuario_id, cantidad=cantidad, fecha=fecha, estado=EstadoDePrestamo.Activo)
        db.add(prestamo)
        guardar(db)
        db.refresh(prestamo)
        return prestamo
    except Exception:
        db.rollback()
        raise

def buscar_prestamo_por_id(db: Session, prestamo_id: int):
    return db.get(Prestamo, prestamo_id)

def listar_prestamos(db: Session):
    return db.scalars(select(Prestamo).order_by(Prestamo.id)).all()

def devolver_prestamo(db: Session, prestamo_id: int):
    try:
        # Solo una devolución puede cambiar Activo a Devuelto.
        result = db.execute(
            update(Prestamo)
            .where(Prestamo.id == prestamo_id, Prestamo.estado == EstadoDePrestamo.Activo)
            .values(estado=EstadoDePrestamo.Devuelto)
        )
        if result.rowcount != 1:
            if buscar_prestamo_por_id(db, prestamo_id) is None:
                raise ErrorBiblioteca("Préstamo inexistente")
            raise ErrorBiblioteca("Este préstamo ya fue devuelto")
        prestamo = buscar_prestamo_por_id(db, prestamo_id)
        db.execute(
            update(Libro)
            .where(Libro.id == prestamo.libro_id)
            .values(ejemplares_disponibles=Libro.ejemplares_disponibles + prestamo.cantidad)
        )
        guardar(db)
        db.refresh(prestamo)
        return prestamo
    except Exception:
        db.rollback()
        raise
