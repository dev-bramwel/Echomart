import React from 'react'
import "./LoginSignup.css";
import echomart_logo from "../Assets/Echomart_logo3.png";

const Passcode = () => {
  return (
    <div className='container'>
      <div className="header">
        <img src={echomart_logo} alt="" />
        <h1>Enter Security Code</h1>
      </div>
      <div className="formbox">
        <p>Enter the Security Code sent to your Email Address.</p>
        <div className="input">
          <input type="text" placeholder="Security Code" />
        </div>
        <div className="button">
          <button>Verify Code</button>
        </div>
        <div className="ending">
            <p>Return to Login</p>
            <a href="/Login">LOGIN</a>
        </div>
              <div className="end">
        <p>&copy; 2025 Echomart</p>
      </div>
      </div>
    </div>
  )
}

export default Passcode
