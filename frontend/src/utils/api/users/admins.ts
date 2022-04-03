import { User } from "./users";
import { axiosInstance } from "../api";

export interface GetAdminsResponse {
    users: User[];
}

export async function getAdmins(): Promise<GetAdminsResponse> {
    const response = await axiosInstance.get(`/users?admin=true`);
    return response.data as GetAdminsResponse;
}

export async function addAdmin(userId: number): Promise<boolean> {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: true });
    return response.status === 204;
}

export async function removeAdmin(userId: number) {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: false });
    return response.status === 204;
}

export async function removeAdminAndCoach(userId: number) {
    const response = await axiosInstance.patch(`/users/${userId}`, { admin: false });
    // TODO: remove user from all editions
    return response.status === 204;
}
