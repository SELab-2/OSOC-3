import { User } from "./users";

export interface GetAdminsResponse {
    admins: User[];
}

export async function getAdmins(): Promise<GetAdminsResponse> {
    const data = {
        admins: [
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

export async function addAdmin(userId: number) {
    alert("add " + userId + " as admin");
}

export async function removeAdmin(userId: number) {
    alert("remove " + userId + " as admin");
}
