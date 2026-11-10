from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from app.base_datos import Base, engine, SessionLocal
from app import modelos, crud


def leer_entero(mensaje: str, minimo: int = 0) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"Debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingresa un número entero válido.")


def leer_fecha() -> date:
    while True:
        texto = input("Fecha AAAA-MM-DD (Enter = hoy): ").strip()
        if not texto:
            return date.today()
        try:
            if len(texto) != 10 or texto[4] != '-' or texto[7] != '-':
                raise ValueError
            return date.fromisoformat(texto)
        except ValueError:
            print("Fecha inválida. Ejemplo: 2026-11-10")


def ejecutar_opcion(db, opcion: str):
    if opcion == '1':
        print(crud.crear_libro(db, input('Título: '), input('Autor: '), leer_entero('Ejemplares disponibles: ')))
    elif opcion == '2':
        for libro in crud.listar_libros(db):
            print(libro)
    elif opcion == '3':
        print(crud.buscar_libro_por_id(db, leer_entero('ID libro: ', 1)) or 'Libro inexistente')
    elif opcion == '4':
        libro_id = leer_entero('ID libro: ', 1)
        print(crud.actualizar_libro(db, libro_id, input('Nuevo título: '), input('Nuevo autor: '), leer_entero('Ejemplares disponibles: ')))
    elif opcion == '5':
        print('Eliminado:', crud.eliminar_libro(db, leer_entero('ID libro: ', 1)))
    elif opcion == '6':
        print(crud.crear_usuario(db, input('Nombre: '), input('Correo: ')))
    elif opcion == '7':
        for usuario in crud.listar_usuarios(db):
            print(usuario)
    elif opcion == '8':
        print(crud.buscar_usuario_por_id(db, leer_entero('ID usuario: ', 1)) or 'Usuario inexistente')
    elif opcion == '9':
        usuario_id = leer_entero('ID usuario: ', 1)
        print(crud.actualizar_usuario(db, usuario_id, input('Nuevo nombre: '), input('Nuevo correo: ')))
    elif opcion == '10':
        print('Eliminado:', crud.eliminar_usuario(db, leer_entero('ID usuario: ', 1)))
    elif opcion == '11':
        libro_id = leer_entero('ID libro: ', 1)
        usuario_id = leer_entero('ID usuario: ', 1)
        cantidad = leer_entero('Cantidad: ', 1)
        fecha = leer_fecha()
        print('Préstamo registrado:', crud.registrar_prestamo(db, libro_id, usuario_id, cantidad, fecha))
    elif opcion == '12':
        for prestamo in crud.listar_prestamos(db):
            print(prestamo)
    elif opcion == '13':
        print(crud.buscar_prestamo_por_id(db, leer_entero('ID préstamo: ', 1)) or 'Préstamo inexistente')
    elif opcion == '14':
        print('Devuelto:', crud.devolver_prestamo(db, leer_entero('ID préstamo: ', 1)))
    else:
        print('Opción inválida.')


def main():
    Base.metadata.create_all(engine)
    menu = '''\n=== BIBLIOTECA ===
1. Crear libro          2. Listar libros
3. Buscar libro         4. Actualizar libro
5. Eliminar libro       6. Crear usuario
7. Listar usuarios      8. Buscar usuario
9. Actualizar usuario  10. Eliminar usuario
11. Registrar préstamo 12. Listar préstamos
13. Buscar préstamo    14. Devolver préstamo
0. Salir'''
    while True:
        print(menu)
        try:
            opcion = input('Opción: ').strip()
            if opcion == '0':
                print('Hasta luego.')
                break
            with SessionLocal() as db:
                try:
                    ejecutar_opcion(db, opcion)
                except crud.ErrorBiblioteca as exc:
                    db.rollback()
                    print('Error:', exc)
                except SQLAlchemyError as exc:
                    db.rollback()
                    print('Error de base de datos:', exc)
        except (KeyboardInterrupt, EOFError):
            print('\nSaliendo...')
            break

if __name__ == '__main__':
    main()
