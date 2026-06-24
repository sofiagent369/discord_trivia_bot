from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./trivia.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Trivia(Base):
    __tablename__ = "trivias"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    trivia_id = Column(Integer, ForeignKey("trivias.id"), index=True)
    question_text = Column(String, index=True)
    options = Column(String)  # JSON string with options
    correct_option = Column(String)

Base.metadata.create_all(bind=engine)