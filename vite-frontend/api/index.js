import axios from "axios";
import Cookies from "js-cookie";

const API = axios.create({ baseURL: "http://127.0.0.1:8000/" });

// Attach token from cookies
API.interceptors.request.use((req) => {
  const token = Cookies.get("token");
  if (token) req.headers.Authorization = `Bearer ${token}`;
  return req;
});

//API calls

//Register
export const userRegister = (formData) => {
  return API.post("/api/accounts/register/", formData);
};

//Login
export const userLogin = (formData) => {
  return API.post("api/accounts/login/", formData);
};

//Logout
export const logout = () => {
  return API.post("/api/accounts/logout/");
};
