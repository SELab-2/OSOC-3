import { UsersList } from "./users";
import { axiosInstance } from "../api";

/**
 * Get all coaches from the given edition
 * @param {string} edition The edition name
 */
export async function getCoaches(edition: string): Promise<UsersList> {
    const response = await axiosInstance.get(`/users/?edition=${edition}`);
    return response.data as UsersList;
}

/**
 * Remove a user as coach from the given edition
 * @param {number} userId The user's id
 * @param {string} edition The edition's name
 */
export async function removeCoachFromEdition(userId: number, edition: string): Promise<boolean> {
    const response = await axiosInstance.delete(`/users/${userId}/editions/${edition}`);
    return response.status === 204;
}

/**
 * Remove a user as coach from all editions
 * @param {number} userId The user's id
 */
export async function removeCoachFromAllEditions(userId: number): Promise<boolean> {
    const response = await axiosInstance.delete(`/users/${userId}/editions`);
    return response.status === 204;
}

/**
 * Add a user as coach to an edition
 * @param {number} userId The user's id
 * @param {string} edition The edition's name
 */
export async function addCoachToEdition(userId: number, edition: string): Promise<boolean> {
    const response = await axiosInstance.post(`/users/${userId}/editions/${edition}`);
    return response.status === 204;
}
