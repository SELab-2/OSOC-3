import axios, { AxiosError } from "axios";
import { BE_BASE_URL } from "../../settings";
import {
    getAccessToken,
    getRefreshTokenLock,
    setAccessToken,
    setRefreshToken,
    setRefreshTokenLock,
} from "../local-storage/auth";
import { refreshTokens } from "./auth";

export const axiosInstance = axios.create();

axiosInstance.defaults.baseURL = BE_BASE_URL;

axiosInstance.interceptors.request.use(async config => {
    // If the request is sent when a token is being refreshed, delay it for 100ms.
    while (getRefreshTokenLock()) {
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    const accessToken = getAccessToken();
    if (accessToken) {
        if (config.headers) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
    }
    return config;
});

axiosInstance.interceptors.response.use(undefined, async (error: AxiosError) => {
    if (error.response?.status === 401) {
        if (getRefreshTokenLock()) {
            // If the token is already being refreshed, resend it (will be delayed until the token has been refreshed)
            return axiosInstance(error.config);
        } else {
            // If the user is on the login page, don't try to refresh their token as
            // they don't have one yet
            // Instead just raise the error so we can show a message
            if (window.location.pathname === "/") {
                throw error;
            }

            setRefreshTokenLock(true);
            try {
                const tokens = await refreshTokens();

                setAccessToken(tokens.access_token);
                setRefreshToken(tokens.refresh_token);

                setRefreshTokenLock(false);

                return axiosInstance(error.config);
            } catch (refreshError) {
                if (axios.isAxiosError(refreshError)) {
                    const axiosError: AxiosError = refreshError;
                    if (axiosError.response?.status === 401) {
                        // refreshing failed with an unauthorized status
                        localStorage.clear();
                        window.location.replace("/");
                    }
                }
            }
            setRefreshTokenLock(false);
        }
    }

    throw error;
});
