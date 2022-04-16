/**
 * A sent email
 */
export interface Email {
    emailId: number;
    date: String;
    type: number;
}
/**
 * A list of sent emails
 */
export interface EmailHistoryList {
    emails: Email[];
}
