from airflow.models import Variable
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

USERNAME = Variable.get('USERNAME_DB')
PASSWORD = Variable.get('PASSWORD_DB')
DATABASE = Variable.get('DATABASE_DB')
HOST = Variable.get('HOST_DB')
PORT = Variable.get('PORT_DB')

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    echo=True,
    connect_args={"options": "-csearch_path=etl"}
)

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS etl"))

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()