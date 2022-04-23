import { axiosInstance } from "./api";
import { Edition } from "../../data/interfaces";
import axios from "axios";

interface EditionsResponse {
    editions: Edition[];
}

interface EditionFields {
    name: string;
    year: number;
}

/**
 * Get all editions the user can see.
 */
export async function getEditions(): Promise<EditionsResponse> {
    const response = await axiosInstance.get("/editions/");
    return response.data as EditionsResponse;
}

/**
 * Delete an edition by name
 */
export async function deleteEdition(name: string): Promise<number> {
    const response = await axiosInstance.delete(`/editions/${name}`);
    return response.status;
}

/**
 * Create a new edition with the given name and year
 */
export async function createEdition(name: string, year: number): Promise<number> {
    const payload: EditionFields = { name: name, year: year };
    try {
        const response = await axiosInstance.post("/editions/", payload);
        return response.status;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response !== undefined) {
            return error.response.status;
        } else {
            return -1;
        }
    }
}
