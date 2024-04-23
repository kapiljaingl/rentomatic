import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import UserContext from './UserContext';
import './MyBookings.css';

function MyBookings() {
  const { user } = useContext(UserContext);
  const [bookings, setBookings] = useState([]);
  const [reload, setReload] = useState(false);

  const cancelRide = async (booking_id) => {
    fetch('/cancel-booking', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "booking_id": booking_id }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setReload(!reload);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await axios.get(`/my-bookings?user_id=${user.id}`);
        setBookings(response.data.data.cars);
      } catch (error) {
        console.error('Error:', error);
      }
    };
    fetchBookings();
  }, [user.id, reload]);

  return (
    <div className="my-bookings">
      {Array.isArray(bookings) && bookings.map((booking) => (
        <div key={booking.booking_id} className="booking">
          <img src={booking.thumbnail} alt={booking.model} />
          <h3>{booking.model}</h3>
          <p><strong>Booking Time:</strong> {booking.reservation_date}</p>
          <p><strong>Price:</strong> ₹{booking.total}</p>
          <p><strong>Status:</strong> {booking.status}</p>
          <p><strong>Passengers:</strong> {booking.num_of_travellers}</p>
          <p><strong>Pickup Date:</strong> {booking.pickup_date}</p>
          <p><strong>Return Date:</strong> {booking.return_date}</p>
          {booking.status === 'booked' ? (
            <button className="button" onClick={() => cancelRide(booking.booking_id)}>Cancel Ride</button>
          ) : (
            <button className="button" disabled>Cancel Ride</button>
          )}
        </div>
      ))}
    </div>
  );
}

export default MyBookings;
