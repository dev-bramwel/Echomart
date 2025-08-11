import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Components/Navbar/Navbar.jsx";
import Categorybar from "./Components/Categorybar/Categorybar.jsx";

import Login from "./Components/LoginSignup/Login.jsx";
import Signup from "./Components/LoginSignup/Signup.jsx";
import PasswordRecovery from "./Components/LoginSignup/PasswordRecovery.jsx";
import Passcode from "./Components/LoginSignup/Passcode.jsx";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Categorybar />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/password-recovery" element={<PasswordRecovery />} />
        <Route path="/passcode" element={<Passcode />} />
      </Routes>
    </Router>
  );
};

export default App;
