import React from 'react'
import './LoginSignup.css';

import echomart_logo from '../assets/echomart_logo3.png';

import user_icon from '../assets/user.png';
import phone_icon from '../assets/phone.png';
import email_icon from '../assets/email.png';
import password_icon from '../assets/password.png';

const Signup = () => {
  return (
    <div className="container">
            <div className="header">
                <img src={echomart_logo} alt="" />
                <h1>Welcome to Echomart</h1>
            </div>
            <div className="inputs">
                <div className="input">
                    <img src={user_icon} alt="" />
                    <input type="text" placeholder='Username' />
                </div>
                <div className="input">
                    <img src={phone_icon} alt="" />
                    <input type="number" placeholder='Phone Number' />
                </div>
                <div className="input">
                    <img src={email_icon} alt="" />
                    <input type="email" placeholder='Email' />
                </div>
                <div className="input">
                    <img src={password_icon} alt="" />
                    <input type="password" placeholder='Password' />
                </div>
                <div className="input">
                    <img src={password_icon} alt="" />
                    <input type="password" placeholder='Confirm Password' />
                </div>
                
            </div>
            <div className="button">
                <button>Sign Up</button>
            </div>
            
            <div className="text">
                <p>Do you have an Account?<a href="/login">Login</a></p>
            </div>
        </div>
  )
}

export default Signup
