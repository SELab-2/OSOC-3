import { Email } from "../../data/interfaces";
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
    const data = {
        emails: [
            { emailId: 1, date: "2022-04-13T11:46:28.641337", type: 0 },
            { emailId: 2, date: "2022-04-14T12:36:28.641337", type: 1 },
            { emailId: 3, date: "2022-04-15T13:38:38.641337", type: 2 },
        ],
    };
    return data as EmailHistoryList;
}
