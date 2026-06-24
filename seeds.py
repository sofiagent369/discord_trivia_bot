from sqlalchemy import create_engine
from db import Base, Trivia, Question

DATABASE_URL = "sqlite:///./trivia.db"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Seed data for trivias
trivia_1 = Trivia(title="General Knowledge", description="A general knowledge trivia")
trivia_2 = Trivia(title="Science and Technology", description="A science and technology trivia")

session.add(trivia_1)
session.add(trivia_2)

# Seed data for questions
question_1 = Question(
    trivia_id=trivia_1.id,
    question_text="What is the capital of France?",
    options='["Paris", "London", "Berlin", "Madrid"]',
    correct_option="Paris"
)

question_2 = Question(
    trivia_id=trivia_1.id,
    question_text="What is the chemical symbol for water?",
    options='["H2O", "CO2", "N2", "O2"]',
    correct_option="H2O"
)

session.add(question_1)
session.add(question_2)

# Commit and close session
session.commit()
session.close()