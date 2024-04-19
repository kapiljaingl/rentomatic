import React, { useState, useContext } from 'react';
import axios from 'axios';
import backgroundImage from './images/background.jpg';
import './Login.css';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import UserContext from './UserContext';



function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);


  const handleSubmit = e => {
    e.preventDefault();
    axios.post('/login', { email, password })
      .then(res => {
        console.log(res.data);
        // handle successful login here
        if (res.data.status === 'success') {
          setUser(res.data.data);
          console.log('Login successful');
          navigate('/cars'); // redirect to the cars page
          return;
        }
      })
      .catch(err => {
        console.error(err);
        // handle login error here
      });
  };

  return (
    <div className="login-container" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
        <p className="register-link">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
