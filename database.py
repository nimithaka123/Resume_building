from curses import echo
from email.mime import base
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine=create_engine("postgresql://postgres:Nimi123@localhost/resume",
echo=True)

Base=declarative_base()

Session=sessionmaker(autocommit=False, autoflush=False, bind=engine)


