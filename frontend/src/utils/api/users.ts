import axios from "axios";
import { axiosInstance } from "./api";

/**
 * Get invite link for given email and edition
 */
export async function getInviteLink(edition: string, email: string): Promise<string> {
    try {
        await axiosInstance
            .post(`/editions/${edition}/invites/`, { email: email })
            .then(response => {
                return response.data.mailTo;
            });
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return error.message;
        } else {
            throw error;
        }
    }
    return "";
}
