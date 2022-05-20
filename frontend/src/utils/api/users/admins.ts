import { UsersList } from "./users";
import { axiosInstance } from "../api";

/**
 * Get a page from all admins.
 * @param page The requested page.
 * @param name A string which every username should contain (can be empty).
 */
export async function getAdmins(page: number, name: string): Promise<UsersList> {
    if (name) {
        const response = await axiosInstance.get(`/users?page=${page}&admin=true&name=${name}`);
        return response.data as UsersList;
    }
    const response = await axiosInstance.get(`/users?page=${page}&admin=true`);
    return response.data as UsersList;
}

/**
 * Make the given user admin.
 * @param {number} userId The id of the user.
 */
export async function addAdmin(userId: number) {
    await axiosInstance.patch(`/users/${userId}`, { admin: true });
}

/**
 * Remove the given user as admin.
 * @param {number} userId The id of the user.
 */
export async function removeAdmin(userId: number) {
    await axiosInstance.patch(`/users/${userId}`, { admin: false });
}

/**
 * Remove the given user as admin and remove him as coach for every edition.
 * @param {number} userId The id of the user.
 */
export async function removeAdminAndCoach(userId: number) {
    await axiosInstance.delete(`/users/${userId}/editions`);
    await axiosInstance.patch(`/users/${userId}`, { admin: false });
}
