import axios from "axios";

const api = axios.create({
  baseURL: "http://ssems.net:8000",
  headers: {
    "Content-Type": "application/json"
  }
});
console.log(">>> API BASE URL =", api.defaults.baseURL);
export default api;
