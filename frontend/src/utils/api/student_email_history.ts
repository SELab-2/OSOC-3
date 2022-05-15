import { EmailHistoryList } from "../../data/interfaces";
import { axiosInstance } from "./api";
/**
 * Get the full email history for a student
 */
export async function getEmails(
    editionId: string | undefined,
    studentId: string | undefined
): Promise<EmailHistoryList> {
    const response = await axiosInstance.get(`/editions/${editionId}/students/${studentId}/emails`);
    return response.data as EmailHistoryList;
}
