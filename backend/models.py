from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class CarAvailabilityEnum(PyEnum):
    available = "available"
    booked = "booked"


class ReservationStatusEnum(PyEnum):
    booked = "booked"
    cancelled = "cancelled"
    completed = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    license_number = Column(String, unique=True)

    reservations = relationship("Reservation", back_populates="user")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)
    availability = Column(
        Enum(CarAvailabilityEnum), nullable=False, default=CarAvailabilityEnum.available
    )
    brand = Column(String, nullable=False)
    price_per_hour = Column(Float, nullable=False)
    thumbnail = Column(String)

    reservations = relationship("Reservation", back_populates="car")


class Reservation(Base):
    __tablename__ = "reservations"

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    pickup_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    num_of_travellers = Column(Integer, nullable=False)
    status = Column(
        Enum(ReservationStatusEnum),
        nullable=False,
        default=ReservationStatusEnum.booked,
    )
    # car = Column(String, nullable=False)
    # img = Column(String, nullable=False)
    total = Column(Float, nullable=False)

    user = relationship("User", back_populates="reservations")
    car = relationship("Car", back_populates="reservations")
