import { UsersList } from "./users";
import { axiosInstance } from "../api";
import axios from "axios";

/**
 * Get a page from all coaches from the given edition.
 * @param edition The edition name.
 * @param name The username to filter.
 * @param page The requested page.
 * @param controller An optional AbortController to cancel the request
 */
export async function getCoaches(
    edition: string,
    name: string,
    page: number,
    controller: AbortController | null = null
): Promise<UsersList | null> {
    if (controller === null) {
        const response = await axiosInstance.get(
            `/users?edition=${edition}&page=${page}&name=${name}`
        );
        return response.data as UsersList;
    } else {
        try {
            const response = await axiosInstance.get(
                `/users?edition=${edition}&page=${page}&name=${name}`,
                { signal: controller.signal }
            );
            return response.data as UsersList;
        } catch (error) {
            if (axios.isAxiosError(error) && error.code === "ERR_CANCELED") {
                return null;
            } else {
                throw error;
            }
        }
    }
}

/**
 * Remove a user as coach from the given edition.
 * @param {number} userId The user's id.
 * @param {string} edition The edition's name.
 */
export async function removeCoachFromEdition(userId: number, edition: string) {
    await axiosInstance.delete(`/users/${userId}/editions/${edition}`);
}

/**
 * Remove a user as coach from all editions.
 * @param {number} userId The user's id.
 */
export async function removeCoachFromAllEditions(userId: number) {
    await axiosInstance.delete(`/users/${userId}/editions`);
}

/**
 * Add a user as coach to an edition.
 * @param {number} userId The user's id.
 * @param {string} edition The edition's name.
 */
export async function addCoachToEdition(userId: number, edition: string) {
    await axiosInstance.post(`/users/${userId}/editions/${edition}`);
}
