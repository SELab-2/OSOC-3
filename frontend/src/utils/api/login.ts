import axios from "axios";
import { axiosInstance } from "./api";
import { AuthContextState, logIn as ctxLogIn } from "../../contexts";
import { User } from "../../data/interfaces";

interface LoginResponse {
    accessToken: string;
    user: User;
}

/**
 * Function that logs the user in via their email and password. If email/password were
 * valid, this will automatically set the [[AuthContextState]], and set the token in LocalStorage.
 * @param auth reference to the [[AuthContextState]]
 * @param email email entered
 * @param password password entered
 */
export async function logIn(auth: AuthContextState, email: string, password: string) {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);

    try {
        const response = await axiosInstance.post("/login/token", payload);
        const login = response.data as LoginResponse;
        ctxLogIn(login.user, login.accessToken, auth);

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
