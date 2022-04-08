import axios from "axios";
import { BASE_URL } from "../../settings";

export const axiosInstance = axios.create();
axiosInstance.defaults.baseURL = BASE_URL;

/**
 * Function to set the default bearer token in the request headers.
 * Passing `null` as the value will remove the header instead.
 */
export function setBearerToken(value: string | null) {
    // Remove the header
    // Note: setting to "null" or "undefined" is not possible
    if (value === null) {
        delete axiosInstance.defaults.headers.common.Authorization;
        return;
    }

    axiosInstance.defaults.headers.common.Authorization = `Bearer ${value}`;
}
