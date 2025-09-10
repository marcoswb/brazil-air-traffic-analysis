from airflow.models import Variable
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

USERNAME = Variable.get('USERNAME_DB')
PASSWORD = Variable.get('PASSWORD_DB')
DATABASE = Variable.get('DATABASE_DB')
HOST = Variable.get('HOST_DB')
PORT = Variable.get('PORT_DB')
SCHEMA_NAME = 'etl'

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    echo=True,
    connect_args={"options": f"-csearch_path={SCHEMA_NAME}"}
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_connection():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_schema():
    metadata = MetaData(schema=SCHEMA_NAME)
    metadata.reflect(bind=engine)
    metadata.drop_all(engine)
    with engine.begin() as conn:
        conn.execute(text(f'DROP SCHEMA IF EXISTS {SCHEMA_NAME}'))

    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))