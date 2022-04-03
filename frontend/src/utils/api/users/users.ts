import { axiosInstance } from "../api";

/**
 *  Interface for a user
 */
export interface User {
    userId: number;
    name: string;
    email: string;
    admin: boolean;
}

export interface UsersList {
    users: User[];
}

/**
 * Interface for a mailto link
 */
export interface MailTo {
    mailTo: string;
    link: string;
}

/**
 * Get invite link for given email and edition
 */
export async function getInviteLink(edition: string, email: string): Promise<MailTo> {
    const response = await axiosInstance.post(`/editions/${edition}/invites/`, { email: email });
    console.log(response);
    return response.data as MailTo;
}

/**
 * Get all users
 */
export async function getUsers(): Promise<UsersList> {
    const response = await axiosInstance.get(`/users`);
    return response.data as UsersList;
}
