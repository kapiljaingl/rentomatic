import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './CarDetail.css'; // Import the CSS file

const CarDetail = () => {
  const [car, setCar] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    fetch(`/cars/${id}`)
      .then(response => response.json())
      .then(data => setCar(data));
  }, [id]);

  if (!car) {
    return <div>Loading...</div>;
  }

  return (
    <div className="car-detail">
      <img className="car-image" src={process.env.PUBLIC_URL + '/' + car.thumbnail} alt={car.model} />
      <div className="car-info">
        <h1>Model: {car.model}</h1>
        <p>Brand: {car.brand}</p>
        <p>Hourly Charge: ${car.price_per_hour}/hour</p>
        <p>Registration Number: {car.registration_number}</p>
        <p>Availability: {car.availability === "available" ? 'Available' : 'Unavailable'}</p>
      </div>
    </div>
  );
};

export default CarDetail;
