from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./molecules.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

class Molecule(Base):
    __tablename__ = "molecules"
    id = Column(Integer, primary_key=True, index=True)
    smiles = Column(String, unique=True, index=True)
    mw = Column(Float)
    logp = Column(Float)
    qed = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)