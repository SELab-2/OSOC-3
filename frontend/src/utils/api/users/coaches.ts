import { User } from "./users";
import { axiosInstance } from "../api";

export interface GetCoachesResponse {
    coaches: User[];
}

export async function getCoaches(edition: string): Promise<GetCoachesResponse> {
    const response = await axiosInstance.get(`/users/?admin=false&edition=${edition}`);
    return response.data as GetCoachesResponse;
}

export async function removeCoachFromEdition(userId: number, edition: string) {
    alert("remove " + userId + " from " + edition);
}

export async function removeCoachFromAllEditions(userId: number) {
    alert("remove " + userId + " from all editions");
}

export async function addCoachToEdition(userId: number, edition: string) {
    alert("add " + userId + " to " + edition);
}
