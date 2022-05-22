/**
 * A sent email
 */
import { Student } from "./students";

export interface Email {
    emailId: number;
    studentId: number;
    decision: number;
    date: String;
}
/**
 * A list of sent emails
 */
export interface EmailHistoryList {
    emails: Email[];
    student: Student;
}
