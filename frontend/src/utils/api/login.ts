import axios from "axios";
import { axiosInstance } from "./api";

interface LoginResponse {
    accessToken: string;
}

export async function logIn({ setToken }: any, email: string, password: string) {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);
    try {
        const response = await axiosInstance.post("/login/token", payload);
        const login = response.data as LoginResponse;
        await setToken(login.accessToken);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}
