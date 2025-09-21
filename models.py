from sqlalchemy import Column, Integer, String, Date, Enum, Text, TIMESTAMP, ForeignKey, DateTime, DECIMAL, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum
from sqlalchemy.sql import func

class RoleEnum(enum.Enum):
    admin = "admin"
    provider = "provider"
    reception = "reception"

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class StatusEnum(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.reception)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date)
    gender = Column(Enum(GenderEnum), default=GenderEnum.female)
    phone = Column(String(20), unique=True)
    email = Column(String(150), unique=True)
    address = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete")

class Provider(Base):
    __tablename__ = "providers"
    provider_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialty = Column(String(100))
    phone = Column(String(20))
    email = Column(String(150), unique=True)
    license_no = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    appointments = relationship("Appointment", back_populates="provider", cascade="all, delete")
    services = relationship("ProviderService", back_populates="provider", cascade="all, delete")

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    providers = relationship("ProviderService", back_populates="service", cascade="all, delete")

class ProviderService(Base):
    __tablename__ = "provider_services"
    provider_id = Column(Integer, ForeignKey("providers.provider_id", ondelete="CASCADE"), primary_key=True)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"), primary_key=True)
    provider = relationship("Provider", back_populates="services")
    service = relationship("Service", back_populates="providers")

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.provider_id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.service_id", ondelete="CASCADE"), nullable=False)
    room = Column(String(50))
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.scheduled)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    patient = relationship("Patient", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
    __table_args__ = (
        UniqueConstraint('provider_id', 'start_datetime', name='uniq_provider_start'),
        CheckConstraint('end_datetime > start_datetime', name='chk_end_after_start'),
    )

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id", ondelete="CASCADE"), unique=True, nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    method = Column(Enum('cash','card','mpesa','insurance', name='method_enum'), default='cash')
    paid_at = Column(TIMESTAMP, server_default=func.now())
