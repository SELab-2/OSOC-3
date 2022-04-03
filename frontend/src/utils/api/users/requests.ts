import { User } from "./users";
import { axiosInstance } from "../api";

/**
 * Interface for a request
 */
export interface Request {
    requestId: number;
    user: User;
}

/**
 * Interface for a list of requests
 */
export interface GetRequestsResponse {
    requests: Request[];
}

/**
 * Get all pending requests of a given edition
 * @param {string} edition The edition's name
 */
export async function getRequests(edition: string): Promise<GetRequestsResponse> {
    const response = await axiosInstance.get(`/users/requests?edition=${edition}`);
    return response.data as GetRequestsResponse;
}

/**
 * Accept a coach request
 * @param {number} requestId The id of the request
 */
export async function acceptRequest(requestId: number) {
    alert("Accept " + requestId);
}

/**
 * Reject a coach request
 * @param {number} requestId The id of the request
 */
export async function rejectRequest(requestId: number) {
    alert("Reject " + requestId);
}
