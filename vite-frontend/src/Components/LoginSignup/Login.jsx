import React from 'react'
import './LoginSignup.css';

import echomart_logo from '../Assets/Echomart_logo3.png';
import email_icon from '../Assets/email.png';
import password_icon from '../Assets/password.png';

const Login = () => {
  return (
    <div className="container">
        <div className="header">
            <img src={echomart_logo} alt="" />
            <p>Affordable Online Shopping</p>
            <h1>Login with Password</h1>
        </div>
        <div className="inputs">
            <div className="input">
                <img src={email_icon} alt="" />
                <input type="email" placeholder='Email or Phone' />
            </div>
            <div className="input">
                <img src={password_icon} alt="" />
                <input type="password" placeholder='Password' />
            </div>
            
        </div>
        <div className="button">
            <button>Login</button>
        </div>

        <div className="text">
                <p>Don't have an Account?<a href="/signup">Signup</a></p>
            </div>
    </div>
  )
}

export default Login
