import datetime
from typing import List  # , Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import database, models, schemas
from backend.models import CarAvailabilityEnum, ReservationStatusEnum

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@router.post("/register", response_model=schemas.UserRegisterResponse)
def register(req_user: schemas.UserRegisterRequest, db: Session = Depends(get_db)):
    if req_user.password != req_user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and Confirm Password do not match",
        )
    try:
        create_user(req_user, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Mobile already registered",
        )
    return schemas.UserRegisterResponse(
        status="success", message="User registered successfully"
    )


def create_user(req_user: schemas.UserRegisterRequest, db: Session):
    hashed_password = pwd_context.hash(req_user.password)
    user = models.User(
        fullname=req_user.fullname,
        email=req_user.email,
        mobile=req_user.mobile,
        hashed_password=hashed_password,
        license_number=req_user.license_number,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise e


@router.post("/login", response_model=schemas.UserLoginResponse)
def login(req_user: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req_user.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not pwd_context.verify(req_user.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    # assuming UserResponse is a Pydantic model that represents a User
    user_data = schemas.UserResponse.model_validate(user)
    return schemas.UserLoginResponse(
        status="success", message="Logged in successfully", data=user_data
    )


@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.Car.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/cars", response_model=schemas.CarResponse)
def create_car(
    model: str = Form(),
    registration_number: str = Form(),
    brand: str = Form(),
    price_per_hour: float = Form(),
    thumbnail: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    with open(f"images/{thumbnail.filename}", "wb") as image_file:
        image_file.write(thumbnail.file.read())

    car = models.Car(
        model=model,
        registration_number=registration_number,
        brand=brand,
        price_per_hour=price_per_hour,
        thumbnail=f"images/{thumbnail.filename}",
    )
    try:
        db.add(car)
        db.commit()
        db.refresh(car)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Car already registered"
        )
    return car


@router.get("/cars", response_model=List[schemas.CarResponse])
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(models.Car).all()
    return cars


@router.get("/cars/available", response_model=List[schemas.CarResponse])
def get_available_cars(db: Session = Depends(get_db)):
    cars = (
        db.query(models.Car)
        .filter(models.Car.availability == CarAvailabilityEnum.available)
        .all()
    )
    return cars


@router.get("/cars/{car_id}", response_model=schemas.CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    return car


@router.post("/reservation", response_model=schemas.ReservationResponse)
def create_reservation(
    req_reservation: schemas.ReservationRequest, db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.id == req_reservation.user_id).first()
    )
    car = db.query(models.Car).filter(models.Car.id == req_reservation.car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    if car.availability == CarAvailabilityEnum.booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Car is already booked"
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Calculate the total cost based on the car's price_per_hour and the duration of the reservation
    duration = (
        req_reservation.return_date - req_reservation.pickup_date
    ).total_seconds() / 3600
    total = car.price_per_hour * duration

    reservation = models.Reservation(
        car=car,
        user=user,
        car_id=req_reservation.car_id,
        user_id=req_reservation.user_id,
        pickup_date=req_reservation.pickup_date,
        return_date=req_reservation.return_date,
        num_of_travellers=req_reservation.num_of_travellers,
        reservation_date=datetime.datetime.now(),
        total=total,
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    # Update car availability to booked
    car.availability = CarAvailabilityEnum.booked
    db.add(car)
    db.commit()
    return schemas.ReservationResponse(
        status="success",
        message="Reservation successful",
        booking_id=reservation.booking_id,
    )


@router.get("/reservation/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.booking_id == booking_id)
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    booking_data = schemas.BookingBase.model_validate(reservation)
    return schemas.BookingResponse(status="success", data={"car": [booking_data]})


@router.get("/my-bookings", response_model=schemas.BookingResponse)
def get_bookings(user_id: str, db: Session = Depends(get_db)):
    reservations = (
        db.query(models.Reservation).filter(models.Reservation.user_id == user_id).all()
    )
    # assuming BookingBase is a Pydantic model that represents a Booking
    booking_data = [
        schemas.BookingBase.model_validate(reservation) for reservation in reservations
    ]
    return schemas.BookingResponse(status="success", data={"cars": booking_data})


@router.put("/cancel-booking", response_model=schemas.CancelBookingResponse)
def cancel_booking(
    req_cancel_booking: schemas.CancelBookingRequest, db: Session = Depends(get_db)
):
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.booking_id == req_cancel_booking.booking_id)
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    reservation.status = ReservationStatusEnum.cancelled
    db.add(reservation)
    db.commit()
    # db.refresh(reservation)
    car = db.query(models.Car).filter(models.Car.id == reservation.car_id).first()
    # Update car availability to available
    car.availability = CarAvailabilityEnum.available
    db.add(car)
    db.commit()
    return schemas.CancelBookingResponse(
        status="success", message="Your reservation is cancelled successfully"
    )


@router.put("/complete-booking", response_model=schemas.CompleteBookingResponse)
def complete_booking(
    req_cancel_booking: schemas.CompleteBookingRequest, db: Session = Depends(get_db)
):
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.booking_id == req_cancel_booking.booking_id)
        .first()
    )
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found"
        )
    reservation.status = ReservationStatusEnum.completed
    db.add(reservation)
    db.commit()
    # db.refresh(reservation)
    car = db.query(models.Car).filter(models.Car.id == reservation.car_id).first()
    # Update car availability to available
    car.availability = CarAvailabilityEnum.available
    db.add(car)
    db.commit()
    return schemas.CancelBookingResponse(
        status="success", message="Your reservation is completed successfully"
    )
