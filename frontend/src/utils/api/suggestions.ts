import axios from "axios";
import { axiosInstance } from "./api";
import { Suggestions } from "../../data/interfaces/suggestions";

/**
 * API call to fetch all suggestion on a student.
 * @param edition The edition name.
 * @param studentId The ID of the student which suggestions need to be fetched.
 */
export async function getSuggestions(edition: string, studentId: number) {
    try {
        const response = await axiosInstance.get(
            "/editions/" + edition + "/students/" + studentId.toString() + "/suggestions"
        );
        return response.data as Suggestions;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}

/**
 * API call for admins to make a definitive decision on a student.
 * @param edition The edition name.
 * @param studentId The ID of the student to make a decision on.
 * @param confirmValue The decision to give this student.
 */
export async function confirmStudent(edition: string, studentId: string, confirmValue: number) {
    const response = await axiosInstance.put(
        "/editions/" + edition + "/students/" + studentId.toString() + "/decision",
        { decision: confirmValue }
    );
    return response.status === 204;
}
