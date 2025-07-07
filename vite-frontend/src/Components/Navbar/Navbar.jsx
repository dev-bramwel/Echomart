

import React from 'react';
import './Navbar.css';
import Echomart_logo from '../assets/Echomart_logo.png';
import shopping_cart from '../assets/shopping_cart.png';
import { Link } from 'react-router-dom';


const Navbar = () => {
  return (
    <div className='navbar-container'>
        <div className="logo">
          <h1>Echomart</h1>
          <img src={Echomart_logo} alt="" />
        </div>
        <div className="nav-links">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/">Shop</a></li>
            <li><a href="/">About Us</a></li>
            <li><a href="/">Contact Us</a></li>
            <li><a href="/">All Products</a></li>
          </ul>
        </div>
        <div className="search">
          <input type="text" placeholder='Search for products' />
          <button>Search</button>
        </div>
        <div className="cart">
          <a href="/">Cart</a>
          <img src={shopping_cart} alt="Cart" />
          <span>0</span>
        </div>
        <div className="login">
          <Link to="/login"><button>Login</button></Link>
          <Link to="/signup"><button>Signup</button></Link>
        </div>
    </div>

    
  )
}

export default Navbar
