from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, EmailStr, Field


# Base Schemas
class UserBase(BaseModel):
    email: EmailStr
    fullname: str
    mobile: str = Field(..., pattern=r"^\+91[0-9]{10}$")
    license_number: str


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class BaseResponse(BaseModel):
    status: str
    message: str


# Register Request and Response Schema
class UserRegisterRequest(UserBase):
    password: str
    confirm_password: str


class UserRegisterResponse(BaseResponse):
    pass


# Login Request and Response Schema
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseResponse):
    data: UserResponse


# Car Request and Response Schema
class CarBase(BaseModel):
    model: str
    registration_number: str
    brand: str
    price_per_hour: float


class CarRequest(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    availability: str
    thumbnail: str


class AllCarsResponse(BaseModel):
    status: str
    results: int
    data: Dict[str, List[CarResponse]]


# Resevation Request and Response Schema
class ReservationBase(BaseModel):
    user_id: int
    car_id: int
    pickup_date: datetime
    return_date: datetime
    num_of_travellers: int


class ReservationRequest(ReservationBase):
    pass


class ReservationResponse(BaseResponse):
    booking_id: int


# Booking Request and Response Schema
class BookingBase(ReservationBase):
    booking_id: int
    reservation_date: datetime
    status: str
    total: float

    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    user_email: EmailStr


class BookingResponse(BaseModel):
    status: str
    data: Dict[str, List[BookingBase]]


# Cancel Booking Request Schema
class CancelBookingRequest(BaseModel):
    booking_id: int


class CancelBookingResponse(BaseResponse):
    pass


# Complete Booking Request Schema
class CompleteBookingRequest(BaseModel):
    booking_id: int


class CompleteBookingResponse(BaseResponse):
    pass


# class Car(CarBase):
#     id: int
#     class Config:
#         from_attributes = True
