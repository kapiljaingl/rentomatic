// Register.js
import './Register.css';
import React, { useState } from 'react';
import axios from 'axios';
import backgroundImage from './images/background.jpg'; // replace with the path to your image
import { Link } from 'react-router-dom';

function Register() {
  const [user, setUser] = useState({
    fullname: '',
    email: '',
    mobile: '',
    password: '',
    confirm_password: '',
    license_number: ''
  });

  const [termsAccepted, setTermsAccepted] = useState(false);

  const handleChange = e => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  const handleTermsChange = e => {
    setTermsAccepted(e.target.checked);
  };

  const [registrationStatus, setRegistrationStatus] = useState(null);

  const handleSubmit = e => {
    e.preventDefault();
    axios.post('/register', user)
      .then(res => {
        console.log(res.data);
        if (res.data.status === 'success') {
            setRegistrationStatus(res.data.message); // set the status message
            return;
            }
        setRegistrationStatus('Registration Failed!'); // set the status message
      })
      .catch(err => {
        console.error(err);
        setRegistrationStatus('Registration failed. Please try again.'); // set the status message
      });
  };

  if (registrationStatus) {
    return (
      <div className="register-container" style={{ backgroundImage: `url(${backgroundImage})` }}>
        <h2 className="registration-message success-message">{registrationStatus}</h2>
        {registrationStatus === 'User registered successfully' && (
          <Link to="/login" className="login-button">Login</Link>
        )}
        {registrationStatus === 'Registration failed. Please try again.' && (
          <button onClick={() => setRegistrationStatus(null)} className="try-again-button">Try again</button>
        )}
      </div>
    );
  }
  return (
    <div className="register-container" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <form onSubmit={handleSubmit} className="register-form">
        <h2 className="centered-title">Register</h2>
        <input type="text" name="fullname" onChange={handleChange} placeholder="Full Name" required />
        <input type="email" name="email" onChange={handleChange} placeholder="Email" required />
        <input type="tel" name="mobile" onChange={handleChange} placeholder="Mobile" required />
        <input type="password" name="password" onChange={handleChange} placeholder="Password" required />
        <input type="password" name="confirm_password" onChange={handleChange} placeholder="Confirm Password" required />
        <input type="text" name="license_number" onChange={handleChange} placeholder="License Number" required />
        <label className="terms">
          <input type="checkbox" checked={termsAccepted} onChange={handleTermsChange} />
          I accept the Terms and Conditions
        </label>
        <button type="submit" className="register-button" disabled={!termsAccepted}>Register</button>
        <p className="login-link">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </form>
    </div>
  );
}

export default Register;
