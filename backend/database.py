"""
Database module for Trendsetter AI Resume Helper
SQLite database with tables for Jobs, Resumes, Keywords, and Analysis History
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Job(Base):
    """Saved job descriptions"""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255))
    description = Column(Text, nullable=False)
    role_type = Column(String(50))  # Full Stack, Frontend, Backend, Other
    keywords = Column(JSON)  # Stored as JSON array
    created_at = Column(DateTime, default=datetime.utcnow)

class Resume(Base):
    """Saved resume profiles"""
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    profile_type = Column(String(50))  # Full Stack, Frontend, Backend, etc.
    content = Column(Text, nullable=False)
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class Keyword(Base):
    """Keyword library built over time"""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(100), nullable=False)
    role_type = Column(String(50))
    frequency = Column(Integer, default=1)
    importance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisHistory(Base):
    """History of resume analyses"""
    __tablename__ = 'analysis_history'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    resume_name = Column(String(255))
    job_title = Column(String(255))
    score = Column(Float)
    ats_score = Column(Float)
    missing_keywords = Column(JSON)
    suggestions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./resume_helper.db')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database and create all tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
