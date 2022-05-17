import { axiosInstance } from "./api";
import { Conflicts } from "../../data/interfaces";

export async function getConflicts(edition: string): Promise<Conflicts> {
    const response = await axiosInstance.get(`/editions/${edition}/projects/conflicts`);
    return response.data;
}
