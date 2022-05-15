import { axiosInstance } from "../api";
import { AuthType } from "../../../data/enums";

/**
 *  Interface of a user.
 */
export interface User {
    userId: number;
    name: string;
    admin: boolean;
    auth: {
        authType: AuthType;
        email: string;
    };
}

/**
 * Interface of a list of users.
 */
export interface UsersList {
    users: User[];
}

/**
 * Interface of a mailto link.
 */
export interface MailTo {
    mailTo: string;
    inviteLink: string;
}

/**
 * Get an invite link for the given edition and email address.
 * @param edition The edition whereto the email address will be invited.
 * @param email The email address whereto the invite will be sent.
 */
export async function getInviteLink(edition: string, email: string): Promise<MailTo> {
    const response = await axiosInstance.post(`/editions/${edition}/invites/`, { email: email });
    return response.data as MailTo;
}

/**
 * Get a page of all users who are not coach of the given edition.
 * @param edition The edition which needs to be excluded.
 * @param name The name which every user's name must contain (can be empty).
 * @param page The requested page.
 */
export async function getUsersExcludeEdition(
    edition: string,
    name: string,
    page: number
): Promise<UsersList> {
    if (name) {
        const response = await axiosInstance.get(
            `/users?page=${page}&exclude_edition=${edition}&name=${name}`
        );
        return response.data as UsersList;
    }
    const response = await axiosInstance.get(`/users?exclude_edition=${edition}&page=${page}`);
    return response.data as UsersList;
}

/**
 * Get a page of all users who are not an admin.
 * @param name The name which every user's name must contain (can be empty).
 * @param page The requested page.
 */
export async function getUsersNonAdmin(name: string, page: number): Promise<UsersList> {
    if (name) {
        const response = await axiosInstance.get(`/users?page=${page}&admin=false&name=${name}`);
        return response.data as UsersList;
    }
    const response = await axiosInstance.get(`/users?admin=false&page=${page}`);
    return response.data as UsersList;
}
