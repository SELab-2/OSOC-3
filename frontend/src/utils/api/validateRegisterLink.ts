import axios from "axios";
import { axiosInstance } from "./api";
import { User } from "../../data/interfaces";

/**
 * Check if a bearer token is valid
 * @param token
 */
export async function validateBearerToken(token: string | null): Promise<User | null> {
    // No token stored -> can't validate anything
    if (token === null) return null;

    // TODO uncomment once it works
    // try {
    //     const response = await axiosInstance.get("/users/current");
    //     return response.data as User;
    // } catch (error) {
    //     if (axios.isAxiosError(error)) {
    //         return null;
    //     } else {
    //         throw error;
    //     }
    // }

    return {
        userId: 1,
        name: "admin",
        admin: false,
        editions: [],
    };
}

/**
 * Check if a registration url exists by sending a GET to it,
 * if it returns a 200 then we know the url is valid.
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
