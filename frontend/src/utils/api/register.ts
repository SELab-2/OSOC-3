import axios, { AxiosResponse } from "axios";
import { axiosInstance } from "./api";

interface RegisterFields {
    email: string;
    name: string;
    uuid: string;
    pw: string;
}

/**
 * Function to register a user in the backend.
 * @param edition the name of the edition that the user is registering for
 * @param email the email entered
 * @param name the name entered
 * @param uuid the uuid of the invitation link that was used
 * @param password the password entered
 */
export async function register(
    edition: string,
    email: string,
    name: string,
    uuid: string,
    password: string
) {
    const payload: RegisterFields = { email: email, name: name, uuid: uuid, pw: password };
    try {
        await axiosInstance.post("/editions/" + edition + "/register/email", payload);
        return true;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}

/**
 * Function to register a user using GitHub OAuth
 */
export async function registerGithub(
    edition: string,
    uuid: string,
    code: string
): Promise<AxiosResponse> {
    const payload = {
        uuid: uuid,
        code: code,
    };

    return await axiosInstance.post(`/editions/${edition}/register/github`, payload);
}
