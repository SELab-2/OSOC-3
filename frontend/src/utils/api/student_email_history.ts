import { axiosInstance } from "./api";
import { Email } from "../../data/interfaces";

/**
 * A list of emails
 */
interface EmailHistoryList {
    emails: Email[];
}
/**
 * Get the full email history for a student
 */
export async function getEmails(): Promise<EmailHistoryList> {
    const response = await axiosInstance.get("/edition/student/1/");
    return response as unknown as EmailHistoryList;
}
