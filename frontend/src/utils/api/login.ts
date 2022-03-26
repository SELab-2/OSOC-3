import axios from "axios";
import { axiosInstance } from "./api";

export async function logIn({ setToken }: any, email: any, password: any) {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);
    try {
        await axiosInstance.post("/login/token", payload).then((response: any) => {
            setToken(response.data.accessToken);
        });
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}
