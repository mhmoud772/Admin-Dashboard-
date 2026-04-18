from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class System(Base):
    __tablename__ = "systems"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    api_url = Column(String)
    system_type = Column(String, default="Microservice") # e.g. "Microservice", "Database", "External"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    metrics = relationship("SystemMetric", back_populates="system", cascade="all, delete-orphan")
    logs = relationship("SystemLog", back_populates="system", cascade="all, delete-orphan")

class SystemMetric(Base):
    __tablename__ = "system_metrics"
    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String) # "optimal", "degraded", "offline"
    latency_ms = Column(Float, nullable=True)
    active_users = Column(Integer, nullable=True)
    queue_size = Column(Integer, nullable=True)
    cpu_load = Column(String, nullable=True)
    memory_usage = Column(String, nullable=True)
    
    system = relationship("System", back_populates="metrics")

class SystemLog(Base):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    level = Column(String)
    message = Column(String)
    
    system = relationship("System", back_populates="logs")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    system_id = Column(Integer, ForeignKey("systems.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String)
    is_read = Column(Integer, default=0) # 0 for false, 1 for true

