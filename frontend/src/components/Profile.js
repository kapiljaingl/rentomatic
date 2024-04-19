import React, { useContext } from 'react';
import UserContext from './UserContext';
import './Profile.css';

function Profile() {
  const { user } = useContext(UserContext);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile">
      <h2>User Profile</h2>
      {user && (
        <>
          <p><strong>Name:</strong> {user.fullname}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Mobile:</strong> {user.mobile}</p>
          <p><strong>Licence Number:</strong> {user.license_number}</p>
        </>
      )}
    </div>
  );
}

export default Profile;
