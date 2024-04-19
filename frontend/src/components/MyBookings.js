import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import UserContext from './UserContext';
import './MyBookings.css';

function MyBookings() {
  const { user } = useContext(UserContext);
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
        try {
          const response = await axios.get(`/my-bookings?user_id=${user.id}`);
          setBookings(response.data.data.cars);
        } catch (error) {
          console.error('Failed to fetch bookings:', error);
          // You can set bookings to an empty array if the fetch fails
          setBookings([]);
        }
      };

    if (user) {
      fetchBookings();
    }
  }, [user]);

  if (!bookings) {
    return <div>Loading...</div>;
  }

  return (
    <div className="my-bookings">
      <h2>My Bookings</h2>
      {Array.isArray(bookings) && bookings.map((booking) => (
  <div key={booking.booking_id} className="booking">
    <p><strong>Booking Time:</strong> {booking.reservation_date}</p>
    <p><strong>Price:</strong> ${booking.total}</p>
    <p><strong>Status:</strong> {booking.status}</p>
    <p><strong>Passengers:</strong> {booking.num_of_travellers}</p>
    <p><strong>Pickup Date:</strong> {booking.pickup_date}</p>
    <p><strong>Return Date:</strong> {booking.return_date}</p>
  </div>
))}
    </div>
  );
}

export default MyBookings;
