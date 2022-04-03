import { User } from "./users";
import { axiosInstance } from "../api";

export interface Request {
    requestId: number;
    user: User;
}

export interface GetRequestsResponse {
    requests: Request[];
}

export async function getRequests(edition: string): Promise<GetRequestsResponse> {
    const response = await axiosInstance.get(`/users/requests?edition=${edition}`);
    return response.data as GetRequestsResponse;
}

export async function acceptRequest(requestId: number) {
    alert("Accept " + requestId);
}

export async function rejectRequest(requestId: number) {
    alert("Reject " + requestId);
}
