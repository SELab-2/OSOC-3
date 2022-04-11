import { axiosInstance } from "./api";
import { Edition } from "../../data/interfaces";

interface EditionsResponse {
    editions: Edition[];
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
