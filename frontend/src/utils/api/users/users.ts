import { axiosInstance } from "../api";

/**
 *  Interface for a user
 */
export interface User {
    userId: number;
    name: string;
    admin: boolean;
    auth: {
        autType: string;
        email: string;
    };
}

export interface UsersList {
    users: User[];
}

/**
 * Interface for a mailto link
 */
export interface MailTo {
    mailTo: string;
    inviteLink: string;
}

/**
 * Get invite link for given email and edition
 */
export async function getInviteLink(edition: string, email: string): Promise<MailTo> {
    const response = await axiosInstance.post(`/editions/${edition}/invites/`, { email: email });
    return response.data as MailTo;
}

/**
 * Get all users who are not coach in edition
 */
export async function getUsers(edition: string, name: string, page: number): Promise<UsersList> {
    // eslint-disable-next-line promise/param-names
    // await new Promise(r => setTimeout(r, 2000));
    if (name) {
        console.log(`/users/?page=${page}&exclude_edition=${edition}&name=${name}`);
        const response = await axiosInstance.get(
            `/users/?page=${page}&exclude_edition=${edition}&name=${name}`
        );
        console.log(`|page: ${page}  Search:${name}  Found: ${response.data.users.length}`);
        return response.data as UsersList;
    }
    const response = await axiosInstance.get(`/users/?exclude_edition=${edition}&page=${page}`);
    console.log(`|page: ${page}  Search:${name}  Found: ${response.data.users.length}`);
    return response.data as UsersList;
}
