import axios from "axios";
import { axiosInstance } from "./api";

interface RegisterFields {
    email: string;
    name: string;
    uuid: string;
    pw: string;
}

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
