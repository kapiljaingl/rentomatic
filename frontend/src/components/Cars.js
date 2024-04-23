import React, { useEffect, useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import './Cars.css';
import UserContext from './UserContext';

const Cars = () => {
    const [cars, setCars] = useState([]);
    const [reservation, setReservation] = useState({ pickup_date: '', return_date: '', passengers: '' });
    const [showModal, setShowModal] = useState(false);
    const { user } = useContext(UserContext);

    const handleReservation = (carId, user_id) => {
      fetch('/reservation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          car_id: carId,
          user_id: user_id,
          pickup_date: reservation.pickup_date,
          return_date: reservation.return_date,
          num_of_travellers: reservation.passengers,
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Handle the response here
        });
    };
    useEffect(() => {
        fetch('/cars')
          .then(response => response.json())
          .then(data => {
            console.log(data);
            setCars(data);
          });
      }, []);

      const handleDateChange = (dateString, type) => {
        const date = new Date(dateString);
        const isoString = date.toISOString();
        setReservation({ ...reservation, [type]: isoString });
      };

      return (
        <div className="cars-container">
          {cars.map(car => (
            <div key={car.id} className="car-card">
              <img src={car.thumbnail} alt={car.model} />
              <h3>{car.model}</h3>
              <p>{car.brand}</p>
              <p className="price">₹{car.price_per_hour}/Hour</p>
              <p className="availability">{car.availability}</p>
              <div className="button-container">
              <Link to={`/cars/${car.id}`} className="button">View Details</Link>
              <button className="button" onClick={() => { setReservation({ ...reservation, carId: car.id }); setShowModal(true); }}>Book Now</button>
              </div>
            </div>
          ))}
        {showModal && reservation.carId && (
          <div className="dialog">
            <div className="dialog-content">
              <h2>Reservation</h2>
            <button className="close-button" onClick={() => setShowModal(false)}>X</button>
                <input type="datetime-local" onChange={e => handleDateChange(e.target.value, 'pickup_date')} />
                <input type="datetime-local" onChange={e => handleDateChange(e.target.value, 'return_date')} />
                <input type="number" value={reservation.passengers} onChange={e => setReservation({ ...reservation, passengers: parseInt(e.target.value) })} />
                <div className="button-container">
                <button className="button" onClick={() => {
                  if (user) {
                    handleReservation(reservation.carId, user.id)
                  } else {
                    // Handle the case where user is null or undefined
                    console.error('User is not defined');
                  }
                }}>Book</button>
                <button className="button" onClick={() => setShowModal(false)}>Close</button>
              </div>
            </div>
          </div>
        )}
        </div>
      );
  };

  export default Cars;
