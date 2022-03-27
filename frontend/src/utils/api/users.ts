import axios from "axios";
import { axiosInstance } from "./api";

export interface User {
    id: Number;
    name: string;
    email: string;
    admin: boolean;
}

export interface Request {
    id: number;
    user: User;
}

export interface GetRequestsResponse {
    requests: Request[];
}

export async function getRequests(edition: string | undefined): Promise<GetRequestsResponse> {
    const data = {
        requests: [
            {
                id: 1,
                user: {
                    id: 1,
                    name: "Seppe",
                    email: "seppe@mail.be",
                    admin: false,
                },
            },
            {
                id: 2,
                user: {
                    id: 2,
                    name: "Stijn",
                    email: "stijn@mail.be",
                    admin: false,
                },
            },
        ],
    };

    // eslint-disable-next-line promise/param-names
    const delay = () => new Promise(res => setTimeout(res, 1000));
    await delay();

    return data;

    // try {
    //     await axiosInstance
    //         .get(`/users/requests/?edition=${edition}`)
    //         .then(response => {
    //             return response.data;
    //             }
    //         )
    // } catch (error) {
    //
    // }
}

/**
 * Get invite link for given email and edition
 */
export async function getInviteLink(edition: string | undefined, email: string): Promise<string> {
    try {
        await axiosInstance
            .post(`/editions/${edition}/invites/`, { email: email })
            .then(response => {
                return response.data.mailTo;
            });
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return error.message;
        } else {
            throw error;
        }
    }
    return "";
}

export async function acceptRequest(requestId: Number) {
    alert("Accept");
}

export async function rejectRequest(requestId: Number) {
    alert("Reject");
}
