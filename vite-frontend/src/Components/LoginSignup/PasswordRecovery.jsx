import react from "react";
import "./LoginSignup.css";
import echomart_logo from "../Assets/Echomart_logo3.png";

const PasswordRecovery = () => {
  return (
    <div className="container">
      <div className="header">
        <img src={echomart_logo} alt="" />
        <h1>Password Recovery</h1>
        <p>Request to reset Password below. A security code will be sent to your Email Address.</p>
      </div>
      <div className="input">
        <input type="email" placeholder="Email Address" />
      </div>
      <div className="button">
        <button><a href="/Passcode">Request Security Code</a></button>
      </div>
      <div className="ending">
        <p>Need any Help. Contact Customer support or visit the help centre</p>
      </div>
      <div className="end">
        <p>Echomart</p>
      </div>
    </div>
  );
};

export default PasswordRecovery;
