import axios from "axios";
import { BASE_URL } from "../../settings";

export const axiosInstance = axios.create();
axiosInstance.defaults.baseURL = BASE_URL;
