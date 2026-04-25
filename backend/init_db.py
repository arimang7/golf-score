import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import Base, engine
from backend.models.user import User
from backend.models.course import GolfCourse
from backend.models.round import Round, RoundScore

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
