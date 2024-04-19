// // This is the main component of the application. It contains the routes for the different pages of the application.
// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Register from './components/Register';
// import Login from './components/Login';
// import Cars from './components/Cars';
// import CarDetail from './components/CarDetail';
// import Profile from './components/Profile';
// import Navigation from './components/Navigation';

// function App() {
//   return (
//     <Router>
//       <Navigation /> {/* add the Navigation component here */}
//       <Routes>
//         <Route path="/login" element={<Login />} />
//         <Route path="/register" element={<Register />} />
//         <Route path="/cars" element={<Cars />} />
//         <Route path="/cars/:id" element={<CarDetail />} />
//         <Route path="/profile" element={<Profile />} />
//         {/* other routes go here */}
//       </Routes>
//     </Router>
//   );
// }

// export default App;

import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserContext from './components/UserContext';
import Register from './components/Register';
import Login from './components/Login';
import Cars from './components/Cars';
import CarDetail from './components/CarDetail';
import Profile from './components/Profile';
import Navigation from './components/Navigation';
import MyBookings from './components/MyBookings';

function App() {
  const [user, setUser] = useState(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Router>
      <Navigation /> {/* add the Navigation component here */}
        <Routes>
         <Route path="/login" element={<Login />} />
         <Route path="/register" element={<Register />} />
         <Route path="/cars" element={<Cars />} />
         <Route path="/cars/:id" element={<CarDetail />} />
         <Route path="/profile" element={<Profile />} />
         <Route path="/my-bookings" element={<MyBookings />} />
        </Routes>
      </Router>
    </UserContext.Provider>
  );
}

export default App;
