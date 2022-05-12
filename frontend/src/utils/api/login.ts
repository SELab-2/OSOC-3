import axios from "axios";
import { axiosInstance } from "./api";
import { AuthContextState, logIn as ctxLogIn } from "../../contexts";
import { User } from "../../data/interfaces";
import { setAccessToken, setRefreshToken } from "../local-storage";

interface LoginResponse {
    access_token: string;
    refresh_token: string;
    user: User;
}

/**
 * Function that logs the user in via their email and password. If email/password were
 * valid, this will automatically set the [[AuthContextState]], and set the token in LocalStorage.
 * @param auth reference to the [[AuthContextState]]
 * @param email email entered
 * @param password password entered
 */
export async function logIn(
    auth: AuthContextState,
    email: string,
    password: string
): Promise<number> {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);

    try {
        const response = await axiosInstance.post("/login/token", payload);
        const login = response.data as LoginResponse;

        setAccessToken(login.access_token);
        setRefreshToken(login.refresh_token);

        ctxLogIn(login.user, auth);
        return response.status;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            auth.setIsLoggedIn(false);
            return error.response?.status || 500;
        } else {
            auth.setIsLoggedIn(null);
            throw error;
        }
    }
}
