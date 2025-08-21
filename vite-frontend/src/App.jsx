import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./Components/Navbar/Navbar.jsx";
import Categorybar from "./Components/Categorybar/Categorybar.jsx";

import Login from "./Components/LoginSignup/Login.jsx";
import Signup from "./Components/LoginSignup/Signup.jsx";
import PasswordRecovery from "./Components/LoginSignup/PasswordRecovery.jsx";
import Passcode from "./Components/LoginSignup/Passcode.jsx";
import Account from "./Components/LoginSignup/Account.jsx";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Categorybar />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/PasswordRecovery" element={<PasswordRecovery />} />
        <Route path="/passcode" element={<Passcode />} />
        <Route path="/account" element={<Account />} />
      </Routes>
    </Router>
  );
};

export default App;
