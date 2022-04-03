import { UsersList } from "./users";
import { axiosInstance } from "../api";

/**
 * Get all admins
 */
export async function getAdmins(): Promise<UsersList> {
    const response = await axiosInstance.get(`/users?admin=true`);
    return response.data as UsersList;
}

/**
 * Make the given user admin
 * @param {number} userId The id of the user
 */
export async function addAdmin(userId: number): Promise<boolean> {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: true });
    return response.status === 204;
}

/**
 * Remove the given user as admin
 * @param {number} userId The id of the user
 */
export async function removeAdmin(userId: number) {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: false });
    return response.status === 204;
}

/**
 * Remove the given user as admin and remove him as coach for every edition
 * @param {number} userId The id of the user
 */
export async function removeAdminAndCoach(userId: number) {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: false });
    // TODO: remove user from all editions
    return response.status === 204;
}
