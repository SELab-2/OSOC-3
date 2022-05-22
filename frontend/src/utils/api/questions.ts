import axios from "axios";
import { axiosInstance } from "./api";
import { Questions } from "../../data/interfaces/questions";

/**
 * API call to fetch all questions and answers of a student.
 * @param edition The edition name.
 * @param studentId The ID of the student which answers need to be fetched.
 */
export async function getQuestions(edition: string, studentId: number) {
    try {
        const response = await axiosInstance.get(
            "/editions/" + edition + "/students/" + studentId.toString() + "/answers"
        );
        return response.data as Questions;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            throw error;
        } else {
            throw error;
        }
    }
}
