import React, { useState } from 'react'
import './Login.css';

import user_icon from '../Assets/person.png';
import email_icon from '../Assets/email.png';
import password_icon from '../Assets/password.png';

const Login = () => {

  const [action, setAction] = useState('Signup')
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    // Replace with real signup logic
    alert(`Signup\nUsername: ${username}\nEmail: ${email}\nPassword: ${password}`);
  };

  const handleLogin = () => {
    // Replace with real login logic
    alert(`Login\nEmail: ${email}\nPassword: ${password}`);
  };

  return (
    <div className='container'>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <div className="inputs">
        {action === "Login" ? <div></div> : (
          <div className="input">
            <img src={user_icon} alt="" />
            <input type="text" placeholder='Username' value={username} onChange={e => setUsername(e.target.value)} />
          </div>
        )}
        <div className="input">
          <img src={email_icon} alt="" />
          <input type="email" placeholder='Email' value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="input">
          <img src={password_icon} alt="" />
          <input type="password" placeholder='Password' value={password} onChange={e => setPassword(e.target.value)} />
        </div>
      </div>

      {action === "Signup" ?<div></div>:<div className="forgot-password">Don't have an Account? <span>Click Here</span></div>}
      
      <div className="submit-container">
        <div className={action === "Login" ? "submit gray" : "submit"} onClick={action === "Signup" ? handleSignup : () => setAction("Signup")}>Signup</div>
        <div className={action === "Signup" ? "submit gray" : "submit"} onClick={action === "Login" ? handleLogin : () => setAction("Login")}>Login</div>
      </div>
    </div>
  )
}

export default Login

