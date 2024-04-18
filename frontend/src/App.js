// App.js
import React from 'react';

import Register from './components/Register';
import Login from './components/Login';
import Cars from './components/Cars';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/cars" element={<Cars />} />
        {/* other routes go here */}
      </Routes>
    </Router>
  );
}

export default App;
