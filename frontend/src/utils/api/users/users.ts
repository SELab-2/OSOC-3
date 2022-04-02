import axios from "axios";
import { axiosInstance } from "../api";

export interface User {
    id: number;
    name: string;
    email: string;
    admin: boolean;
}

/**
 * Get invite link for given email and edition
 */
export async function getInviteLink(edition: string, email: string): Promise<string> {
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

export interface GetUsersResponse {
    users: User[];
}

export async function getUsers(): Promise<GetUsersResponse> {
    const data = {
        users: [
            {
                id: 1,
                name: "Seppe",
                email: "seppe@mail.be",
                admin: false,
            },
            {
                id: 2,
                name: "Stijn",
                email: "stijn@mail.be",
                admin: false,
            },
            {
                id: 3,
                name: "Bert",
                email: "bert@mail.be",
                admin: false,
            },
            {
                id: 4,
                name: "Tiebe",
                email: "tiebe@mail.be",
                admin: false,
            },
            {
                id: 5,
                name: "Ward",
                email: "ward@mail.be",
                admin: true,
            },
            {
                id: 6,
                name: "Francis",
                email: "francis@mail.be",
                admin: true,
            },
            {
                id: 7,
                name: "Clement",
                email: "clement@mail.be",
                admin: true,
            },
        ],
    };

    // eslint-disable-next-line promise/param-names
    const delay = () => new Promise(res => setTimeout(res, 100));
    await delay();

    return data;
}
