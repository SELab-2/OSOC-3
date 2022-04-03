import { User } from "./users";
import { axiosInstance } from "../api";

export interface GetCoachesResponse {
    users: User[];
}

export async function getCoaches(edition: string): Promise<GetCoachesResponse> {
    const response = await axiosInstance.get(`/users/?edition=${edition}`);
    return response.data as GetCoachesResponse;
}

export async function removeCoachFromEdition(userId: number, edition: string): Promise<boolean> {
    const response = await axiosInstance.delete(`/users/${userId}/editions/${edition}`);
    return response.status === 204;
}

export async function removeCoachFromAllEditions(userId: number): Promise<boolean> {
    // TODO: sent correct DELETE
    return false;
}

export async function addCoachToEdition(userId: number, edition: string): Promise<boolean> {
    const response = await axiosInstance.post(`/users/${userId}/editions/${edition}`);
    return response.status === 204;
}
