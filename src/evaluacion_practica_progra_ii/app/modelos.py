import enum
from datetime import date

from sqlalchemy import (
    ForeignKey,
    String,
    CheckConstraint,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base_datos import Base


class EstadoDePrestamo(enum.Enum):
    Activo = "Activo"
    Devuelto = "Devuelto"


class Libro(Base):
    __tablename__ = "Libro"

    __table_args__ = (
        CheckConstraint(
            "ejemplares_disponibles >= 0",
            name="ck_libro_stock"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    titulo: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    autor: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    ejemplares_disponibles: Mapped[int] = mapped_column(
        default=0, nullable=False
    )

    prestamos: Mapped[list["Prestamo"]] = relationship(
        "Prestamo",
        back_populates="libro"
    )

    def __repr__(self):
        return (
            f"Libro(id={self.id}, titulo={self.titulo!r}, "
            f"autor={self.autor!r}, "
            f"disponibles={self.ejemplares_disponibles})"
        )


class Usuario(Base):
    __tablename__ = "Usuario"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    correo: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    prestamos: Mapped[list["Prestamo"]] = relationship(
        "Prestamo",
        back_populates="usuario"
    )

    def __repr__(self):
        return (
            f"Usuario(id={self.id}, "
            f"nombre={self.nombre!r}, "
            f"correo={self.correo!r})"
        )


class Prestamo(Base):
    __tablename__ = "Prestamo"

    __table_args__ = (
        CheckConstraint(
            "cantidad > 0",
            name="ck_prestamo_cantidad"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    libro_id: Mapped[int] = mapped_column(
        ForeignKey("Libro.id"),
        nullable=False
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("Usuario.id"),
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        nullable=False,
        default=date.today
    )

    cantidad: Mapped[int] = mapped_column(nullable=False)

    estado: Mapped[EstadoDePrestamo] = mapped_column(
        Enum(EstadoDePrestamo),
        default=EstadoDePrestamo.Activo,
        nullable=False
    )

    libro: Mapped["Libro"] = relationship(
        "Libro",
        back_populates="prestamos"
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="prestamos"
    )

    def __repr__(self):
        return (
            f"Prestamo(id={self.id}, "
            f"libro_id={self.libro_id}, "
            f"usuario_id={self.usuario_id}, "
            f"cantidad={self.cantidad}, "
            f"fecha={self.fecha}, "
            f"estado={self.estado.value})"
        )

