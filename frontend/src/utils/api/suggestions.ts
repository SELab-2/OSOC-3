import axios from "axios";
import {axiosInstance} from "./api";
import {Suggestions} from "../../data/interfaces/suggestions";

export async function getSuggestions(edition: string, studentId: string){
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/students/" + studentId.toString() + "/suggestions");
        return response.data as Suggestions;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

export async function confirmStudent(edition: string, studentId: string, confirmValue: number) {
    try {
        const response = await axiosInstance.put("/editions/" + edition + "/students/" + studentId.toString() + "/decision", { decision: confirmValue });
        return response.status === 204
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}