import { Email } from "../../data/interfaces";
import { EmailType } from "../../data/enums";

/**
 * A list of emails
 */
export interface EmailHistoryList {
    emails: Email[];
}
/**
 * Get the full email history for a student
 */
export async function getEmails(): Promise<EmailHistoryList> {
    // const response = await axiosInstance.get("/edition/student/1/");
    // return response.data as EmailHistoryList;

    // placeholder while the real API call is not available
    return {
        emails: [
            { email_id: 1, date: "Tuesday, 12-Apr-22 13:52:31", type: EmailType.YES },
            { email_id: 2, date: "Monday, 11-Apr-22 12:52:31", type: EmailType.MAYBE },
            { email_id: 3, date: "Sunday, 10-Apr-22 12:51:01", type: EmailType.NO },
        ],
    };
}
