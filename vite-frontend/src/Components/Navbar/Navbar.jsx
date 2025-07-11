import { Link } from "react-router-dom";
import Cookies from "js-cookie";
import { logout } from "../../../api";
import { useEffect, useState } from "react";

//styles
import "./Navbar.css";

//images
import Echomart_logo from "../assets/Echomart_logo.png";
import shopping_cart from "../assets/shopping_cart.png";

const Navbar = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!Cookies.get("token")
  );

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

  const handleLogout = async () => {
    await logout();
    Cookies.remove("token");
    Cookies.remove("id");
    window.dispatchEvent(new Event("authChanged"));
    setIsAuthenticated(false);
    console.log("Logged out!!");
  };

  return (
    <div className="navbar-container">
      <div className="logo">
        <img src={Echomart_logo} alt="" />
        <h1>Echomart</h1>
      </div>

      <div className="nav-links">
        <ul>
          <li>
            <a href="/">Home</a>
          </li>

          <li>
            <a href="/">Shop</a>
          </li>

          <li>
            <a href="/">About Us</a>
          </li>

          <li>
            <a href="/">Contact Us</a>
          </li>

          <li>
            <a href="/">All Products</a>
          </li>
        </ul>
      </div>

      <div className="search">
        <input type="text" placeholder="Search for products" />
        <button>Search</button>
      </div>

      <div className="cart">
        <a href="/">Cart</a>
        <img src={shopping_cart} alt="Cart" />
        <span>0</span>
      </div>

      {!isAuthenticated ? (
        <div className="login">
          <Link to="/login">
            <button>Login</button>
          </Link>

          <Link to="/signup">
            <button>Signup</button>
          </Link>
        </div>
      ) : (
        <div className="flex justify-end mt-4">
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded shadow transition duration-300 ease-in-out"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default Navbar;
