from datetime import datetime
from sqlite3 import Date
from typing import Collection
from database import Base
from sqlalchemy import String, INTEGER, Column, Date, ForeignKey, TIMESTAMP, text


# Basic details class
class Basic_Details(Base):
    __tablename__ = "basic_details"
    basic_details_id = Column(INTEGER, primary_key=True)
    name = Column(String(25), nullable=False)
    email = Column(String(60), nullable=False)
    phone = Column(String(15), nullable=False)
    image = Column(String(250), nullable=True)
    summary = Column(String(500), nullable=True)
    applied_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                          nullable=False)


# Location details class
class Location(Base):
    __tablename__ = "location"
    location_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    address = Column(String(60), nullable=False)
    street = Column(String(50), nullable=False)
    city = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)
    pincode = Column(String(15), nullable=False)


# Education details class
class Education(Base):
    __tablename__ = "education_details"
    education_details_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    qualification = Column(String(50), nullable=False)
    course_name = Column(String(50), nullable=False)
    institute_name = Column(String(50), nullable=False)
    location = Column(String(30), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


# Project details class
class Project_Details(Base):
    __tablename__ = "project_details"
    project_details_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    project_title = Column(String(50), nullable=True)
    skills = Column(String(50), nullable=True)
    description = Column(String(150), nullable=True)


# Work experience details class
class Work_Experience(Base):
    __tablename__ = "experience_details"
    experience_details_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    organization = Column(String(50), nullable=True)
    job_role = Column(String(50), nullable=True)
    job_location = Column(String(30), nullable=True)
    key_roles = Column(String(50), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)


# Skills details class
class Skills(Base):
    __tablename__ = "skills"
    skills_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    skill_name = Column(String(50), nullable=False)
    skill_level = Column(String(50), nullable=False)


# Social media details class
class Social_Media(Base):
    __tablename__ = "social_media"
    social_media_id = Column(INTEGER, primary_key=True)
    basic_details_id = Column(INTEGER, ForeignKey(
        "basic_details.basic_details_id", ondelete="CASCADE"))
    network = Column(String(50), nullable=True)
    user_name = Column(String(50), nullable=True)
    url = Column(String(250), nullable=True)

