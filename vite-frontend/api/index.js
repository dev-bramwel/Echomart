import axios from "axios"

const API = axios.create({baseURL: "http://127.0.0.1:8000/"})

//API calls

//Register
export const userRegister = (formData) => {
    return API.post("/api/accounts/register/", formData)
}

//Login
export const userLogin = (formData) => {
    return API.post("api/accounts/login/", formData)
}