import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './Cars.css';

const Cars = () => {
    const [cars, setCars] = useState([]);

    useEffect(() => {
        fetch('/cars')
          .then(response => response.json())
          .then(data => {
            console.log(data);
            setCars(data);
          });
      }, []);

    return (
      <div className="cars-container">
        {cars.map(car => (
          <div key={car.id} className="car-card">
            <img src={car.thumbnail} alt={car.model} />
            <h3>{car.model}</h3>
            <p>{car.brand}</p>
            <p>${car.price_per_hour}</p>
            <Link to={`/cars/${car.id}`}>View Details</Link>
          </div>
        ))}
      </div>
    );
  };

  export default Cars;
