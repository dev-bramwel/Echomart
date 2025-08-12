import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { userLogin } from "../../../api";
import Cookies from "js-cookie";

//styles
import "./LoginSignup.css";

//images
import echomart_logo from "../Assets/Echomart_logo3.png";
import email_icon from "../Assets/email.png";
import password_icon from "../Assets/password.png";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    setError("");
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const formData = { email, password };
      let response;

      //validation
      if (!email || !password) {
        setError("All fields are required");
        return;
      }

      response = await userLogin(formData);
      setSuccess("You have logged in succesfully!");

      // Store user token in cookies (valid for 1 day)
      Cookies.set("token", response.data.access, {
        expires: 1,
        secure: true,
        sameSite: "Strict",
      });
      Cookies.set("id", response.data.id, {
        expires: 1,
        secure: true,
        sameSite: "Strict",
      });

      window.dispatchEvent(new Event("authChanged"));
      navigate("/");
    } catch (error) {
      let errorMessage = "Email or Password failed. Try again.";

      const data = error?.response?.data;
      if (data && typeof data === "object") {
        // Turn error object into readable lines
        errorMessage = Object.entries(data)
          .map(
            ([key, value]) =>
              `${key
                .replace("_", " ")
                .replace(/\b\w/g, (c) => c.toUpperCase())}: ${
                Array.isArray(value) ? value.join(", ") : value
              }`
          )
          .join("\n");
      } else if (error?.response?.data?.message) {
        errorMessage = error.response.data.message;
      }

      setError(errorMessage);
      setSuccess("");
      console.log(errorMessage);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <img src={echomart_logo} alt="" />
        <p>Affordable Online Shopping</p>
        <h1>Login with Password</h1>
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 border border-red-400 px-4 py-3 rounded mt-4 text-sm whitespace-pre-line mb-4">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-100 text-green-700 border border-green-400 px-4 py-3 rounded mt-4 text-sm mb-4">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="inputs">
          <div className="input">
            <img src={email_icon} alt="" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="input">
            <img src={password_icon} alt="" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>

        <div className="button">
          <button>Login</button>
        </div>
      </form>

      <div className="text">
        <p>
          <Link to="/change-password">Forgot password</Link>
        </p>
      </div>

      <div className="text">
        <p>
          Don't have an Account?<Link to="/signup">Signup</Link>
        </p>
      </div>
      <div className="end">
        <p>&copy; 2025 Echomart</p>
      </div>
    </div>
  );
};

export default Login;
