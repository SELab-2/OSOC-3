import { axiosInstance } from "./api";
import { Edition } from "../../data/interfaces";
import axios, { AxiosResponse } from "axios";

interface EditionsResponse {
    editions: Edition[];
}

/**
 * Get all editions the user can see.
 */
export async function getEditions(): Promise<EditionsResponse> {
    const response = await axiosInstance.get("/editions");
    return response.data as EditionsResponse;
}

/**
 * Get all edition names sorted the user can see
 */
export async function getSortedEditions(): Promise<string[]> {
    const response = await axiosInstance.get("/users/current");
    return response.data.editions;
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
export async function createEdition(name: string, year: number): Promise<AxiosResponse> {
    const payload = { name: name, year: year };
    try {
        return await axiosInstance.post("/editions", payload);
    } catch (error) {
        if (axios.isAxiosError(error) && error.response !== undefined) {
            return error.response;
        } else {
            throw error;
        }
    }
}

/**
 * Change the readonly status of an edition
 */
export async function patchEdition(name: string, readonly: boolean): Promise<AxiosResponse> {
    const payload = { readonly: readonly };
    return await axiosInstance.patch(`/editions/${name}`, payload);
}
