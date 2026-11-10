from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASEURL = f"sqlite:///{BASE_DIR / 'reservas.db'}"

engine = create_engine(
    DATABASEURL,
    echo=False
)



SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass