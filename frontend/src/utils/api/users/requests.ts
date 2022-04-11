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
export async function getRequests(
    edition: string,
    name: string,
    page: number
): Promise<GetRequestsResponse> {
    if (name) {
        const response = await axiosInstance.get(
            `/users/requests?edition=${edition}&page=${page}&name=${name}`
        );
        console.log(`|page: ${page}  Search:${name}  Found: ${response.data.requests.length}`);
        console.log(response.data.requests);
        return response.data as GetRequestsResponse;
    }
    const response = await axiosInstance.get(`/users/requests?edition=${edition}&page=${page}`);
    console.log(`|page: ${page}  Search:${name}  Found: ${response.data.requests.length}`);
    return response.data as GetRequestsResponse;
}

/**
 * Accept a coach request
 * @param {number} requestId The id of the request
 */
export async function acceptRequest(requestId: number): Promise<Boolean> {
    const response = await axiosInstance.post(`/users/requests/${requestId}/accept`);
    return response.status === 204;
}

/**
 * Reject a coach request
 * @param {number} requestId The id of the request
 */
export async function rejectRequest(requestId: number) {
    const response = await axiosInstance.post(`/users/requests/${requestId}/reject`);
    return response.status === 204;
}
