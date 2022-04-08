/**
 * Data about a user using the application.
 * Contains a list of edition names so that we can quickly check if
 * they have access to a route or not.
 */
export interface User {
    userId: number;
    name: string;
    admin: boolean;
    editions: string[];
}
