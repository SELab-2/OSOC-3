import { User } from "./users";
import { axiosInstance } from "../api";
import axios from "axios";

/**
 * Interface of a request
 */
export interface Request {
    requestId: number;
    user: User;
}

/**
 * Interface of a list of requests
 */
export interface GetRequestsResponse {
    requests: Request[];
}

/**
 * Get a page from all pending requests of a given edition.
 * @param edition The edition's name.
 * @param name String which every request's user's name needs to contain
 * @param page The pagenumber to fetch.
 * @param controller An optional AbortController to cancel the request
 */
export async function getRequests(
    edition: string,
    name: string,
    page: number,
    controller: AbortController
): Promise<GetRequestsResponse | null> {
    try {
        const response = await axiosInstance.get(
            `/users/requests?edition=${edition}&page=${page}&user=${name}`,
            { signal: controller.signal }
        );
        return response.data as GetRequestsResponse;
    } catch (error) {
        if (axios.isAxiosError(error) && error.code === "ERR_CANCELED") {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * Accept a coach request.
 * @param {number} requestId The id of the request.
 */
export async function acceptRequest(requestId: number) {
    await axiosInstance.post(`/users/requests/${requestId}/accept`);
}

/**
 * Reject a coach request.
 * @param {number} requestId The id of the request.s
 */
export async function rejectRequest(requestId: number) {
    await axiosInstance.post(`/users/requests/${requestId}/reject`);
}
