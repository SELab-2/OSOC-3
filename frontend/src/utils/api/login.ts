import axios from "axios";
import { axiosInstance } from "./api";
import { AuthContextState } from "../../contexts";
import { Role } from "../../data/enums";

interface LoginResponse {
    accessToken: string;
    user: {
        admin: boolean;
        editions: number[];
    };
}

export async function logIn(auth: AuthContextState, email: string, password: string) {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);

    try {
        const response = await axiosInstance.post("/login/token", payload);
        const login = response.data as LoginResponse;
        auth.setToken(login.accessToken);
        auth.setIsLoggedIn(true);
        auth.setRole(login.user.admin ? Role.ADMIN : Role.COACH);

        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            auth.setIsLoggedIn(false);
            return false;
        } else {
            auth.setIsLoggedIn(null);
            throw error;
        }
    }
}
