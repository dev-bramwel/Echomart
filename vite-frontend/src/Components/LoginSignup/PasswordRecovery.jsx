import react from "react";
import { Link } from "react-router-dom";
import "./LoginSignup.css";
import echomart_logo from "../Assets/Echomart_logo3.png";

const PasswordRecovery = () => {
  return (
    <div className="container">
      <div className="header">
        <img src={echomart_logo} alt="" />
        <h1>Password Recovery</h1>
        <p>Request to reset Password below. A Security Code will be sent to your Email Address.</p>
      </div>
      <div className="input">
        <input type="email" placeholder="Email Address" />
      </div>
      <div className="button">
        <button><Link to="/Passcode">Request Security Code</Link></button>
      </div>
      <div className="ending">
        <p>Need any Help. Contact Customer support or visit the help centre</p>
      </div>
      <div className="end">
        <p>&copy; 2025 Echomart</p>
      </div>
    </div>
  );
};

export default PasswordRecovery;
