from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

# pattern for clear URL: "postgresql://<username>:<password>@<ip-address>/<database-name>"
SQLALCHMY_DATABASE_URL = "postgresql://postgres:123@localhost/postgres"

#* create `sqlalchemy` engine
engine = create_engine(SQLALCHMY_DATABASE_URL)

#* create `sqlalchemy` session
SessionLocal = sessionmaker(bind=engine, autoflush=False)

#* define `Base` for Models
Base = declarative_base()