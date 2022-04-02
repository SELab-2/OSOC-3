import { User } from "./users";

export interface Request {
    id: number;
    user: User;
}

export interface GetRequestsResponse {
    requests: Request[];
}

export async function getRequests(edition: string): Promise<GetRequestsResponse> {
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

export async function acceptRequest(requestId: number) {
    alert("Accept " + requestId);
}

export async function rejectRequest(requestId: number) {
    alert("Reject " + requestId);
}
