import axios from "axios";
import { axiosInstance } from "./api";

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
