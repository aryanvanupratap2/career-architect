from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# User model for storing user details in database and showing the roadmaps
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    qualification: str
    aim: str

    career_paths: List["CareerPath"] = Relationship(back_populates="user")

# Career model for taking the inputs related to career and showing the final roadmap required as output
class CareerPath(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    career_goal: str
    current_skills: str
    recommended_path: str

    user: Optional[User] = Relationship(back_populates="career_paths")

