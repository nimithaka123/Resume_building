from database import Base,engine
from models import Basic_Details

print("creating database")

Base.metadata.create_all(engine)