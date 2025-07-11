import { useState } from "react";
import { userRegister } from "../../../api";

//styles
import "./LoginSignup.css";

//icons
import echomart_logo from "../assets/echomart_logo3.png";
import user_icon from "../assets/user.png";
import phone_icon from "../assets/phone.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";

const Signup = () => {
  const [formData, setFormData] = useState({
    fullName: "",
    phone: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const { fullName, phone, email, password, confirmPassword } = formData;

    //validation
    if (!fullName || !phone || !email || !password || !confirmPassword) {
      setError("All fields are required");
      return;
    }

    // Password validation
    if (password !== confirmPassword) {
      setError("Passwords do not match!!");
      return;
    }

    try {
      const response = await userRegister({
        full_name: fullName,
        phone_number: phone,
        email: email,
        password: password,
      });

      console.log("User is registered: ", response.data);
    } catch (error) {
      const errorMessage =
        error?.response?.data?.message ||
        JSON.stringify(error?.response?.data) ||
        "Registration failed. Try again.";
      setError(errorMessage);
      console.log(errorMessage);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <img src={echomart_logo} alt="" />
        <h1>Welcome to Echomart</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} alt="" />
            <input
              name="fullName"
              type="text"
              placeholder="Fullname"
              value={formData.fullName}
              onChange={handleChange}
            />
          </div>

          <div className="input">
            <img src={phone_icon} alt="" />
            <input
              name="phone"
              type="phone"
              placeholder="Phone Number"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          <div className="input">
            <img src={email_icon} alt="" />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              name="email"
              onChange={handleChange}
            />
          </div>

          <div className="input">
            <img src={password_icon} alt="" />
            <input
              type="password"
              placeholder="Password"
              value={formData.password}
              name="password"
              onChange={handleChange}
            />
          </div>

          <div className="input">
            <img src={password_icon} alt="" />
            <input
              type="password"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              name="confirmPassword"
              onChange={handleChange}
            />
          </div>
        </div>
        <div className="button">
          <button type="submit">Sign Up</button>
        </div>
      </form>

      <div className="text">
        <p>
          Do you have an Account?<a href="/login">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Signup;
