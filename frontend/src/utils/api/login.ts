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
 * Set the tokens & context variables to authenticate yourself
 */
function setLogInTokens(response: LoginResponse, authCtx: AuthContextState) {
    setAccessToken(response.access_token);
    setRefreshToken(response.refresh_token);
    ctxLogIn(response.user, authCtx);
}

/**
 * Function that logs the user in via their email and password. If email/password were
 * valid, this will automatically set the [[AuthContextState]], and set the token in LocalStorage.
 * @param authCtx reference to the [[AuthContextState]]
 * @param email email entered
 * @param password password entered
 */
export async function logInEmail(
    authCtx: AuthContextState,
    email: string,
    password: string
): Promise<number> {
    const payload = new FormData();
    payload.append("username", email);
    payload.append("password", password);

    try {
        const response = await axiosInstance.post("/login/token/email", payload);
        const login = response.data as LoginResponse;

        setLogInTokens(login, authCtx);
        return response.status;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            authCtx.setIsLoggedIn(false);
            return error.response?.status || 500;
        } else {
            authCtx.setIsLoggedIn(null);
            throw error;
        }
    }
}

/**
 * Function that logs the user in via GitHub OAuth.
 */
export async function logInGitHub(authCtx: AuthContextState, code: string): Promise<boolean> {
    const payload = new FormData();
    payload.append("code", code);

    try {
        const response = await axiosInstance.post("/login/token/github", payload);
        const login = response.data as LoginResponse;

        setLogInTokens(login, authCtx);

        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            authCtx.setIsLoggedIn(false);
            return false;
        } else {
            throw error;
        }
    }
}
