import { User } from "./users";

export interface GetCoachesResponse {
    coaches: User[];
}

export async function getCoaches(edition: string): Promise<GetCoachesResponse> {
    const data = {
        coaches: [
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
        ],
    };

    // eslint-disable-next-line promise/param-names
    const delay = () => new Promise(res => setTimeout(res, 100));
    await delay();

    return data;
}

export async function removeCoachFromEdition(userId: number, edition: string) {
    alert("remove " + userId + " from " + edition);
}

export async function removeCoachFromAllEditions(userId: Number) {
    alert("remove " + userId + " from all editions");
}
