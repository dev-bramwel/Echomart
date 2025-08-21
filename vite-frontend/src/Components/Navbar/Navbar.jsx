import { useRef, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Cookies from "js-cookie";
import { logout } from "../../../api";
import "./Navbar.css";
import Echomart_logo from "../assets/Echomart_logo.png";
import shopping_cart from "../assets/shopping_cart.png";

const Navbar = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!Cookies.get("token"));
  const [showProfileDropdown, setShowProfileDropdown] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const token = Cookies.get("token");
    setIsAuthenticated(!!token);

    const handleAuthChange = () => {
      setIsAuthenticated(!!Cookies.get("token"));
    };

    window.addEventListener("authChanged", handleAuthChange);

    return () => {
      window.removeEventListener("authChanged", handleAuthChange);
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowProfileDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleLogout = async () => {
    await logout();
    Cookies.remove("token");
    Cookies.remove("id");
    window.dispatchEvent(new Event("authChanged"));
    setIsAuthenticated(false);
    console.log("Logged out!!");
  };

  const handleProfileClick = () => {
    setShowProfileDropdown((prev) => !prev);
  };

  const handleDropdownLogout = async () => {
    await handleLogout();
    setShowProfileDropdown(false);
  };

  return (
    <div className="navbar-container">
      {/* Logo */}
      <div className="logo">
        <img src={Echomart_logo} alt="" />
        <h1>Echomart</h1>
      </div>

      {/* Navigation Links */}
      <div className="nav-links">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/shop">Shop</Link></li>
          <li><Link to="/about">About Us</Link></li>
          <li><Link to="/contact">Contact Us</Link></li>
          <li><Link to="/products">All Products</Link></li>
        </ul>
      </div>

      {/* Search */}
      <div className="search">
        <input type="text" placeholder="Search for products" />
        <button>Search</button>
      </div>

      {/* Cart */}
      <div className="cart">
        <a href="/">Cart</a>
        <img src={shopping_cart} alt="Cart" />
        <span>0</span>
      </div>

      {/* Profile Dropdown */}
      <div className="profile-dropdown-container" ref={dropdownRef}>
        <div className="profile-btn" onClick={handleProfileClick}>
          <img
            src="https://via.placeholder.com/30" // replace with actual profile image
            alt=""
            className="profile-image"
          />
          <span className="profile-name">Profile</span>
          <span className="arrow">&#9662;</span>
        </div>

        {showProfileDropdown && (
          <div className="profile-dropdown">
            <Link to="/login" onClick={() => setShowProfileDropdown(false)}>
              <div className="dropdown-item">Login</div>
            </Link>

            <Link to="/account" onClick={() => setShowProfileDropdown(false)}>
              <div className="dropdown-item">My Account</div>
            </Link>
            
            <div className="dropdown-item" onClick={handleDropdownLogout}>
              Logout
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
