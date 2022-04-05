import axios from "axios";
import { axiosInstance } from "./api";
import { User } from "../../data/interfaces";

/**
 * Check if a bearer token is valid.
 * @param token the token to validate.
 */
export async function validateBearerToken(token: string | null): Promise<User | null> {
    // No token stored -> can't validate anything
    if (token === null) return null;

    try {
        // Add header manually here instead of setting the default
        const config = {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        };

        const response = await axiosInstance.get("/users/current", config);
        return response.data as User;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * Function to check if a registration url exists by sending a GET request,
 * if this returns a 200 then we know the url is valid.
 */
export async function validateRegistrationUrl(edition: string, uuid: string): Promise<boolean> {
    try {
        await axiosInstance.get(`/editions/${edition}/invites/${uuid}`);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}