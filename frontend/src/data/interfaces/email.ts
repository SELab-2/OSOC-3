import { EmailType } from "../enums";
/**
 * A sent email
 */
export interface Email {
    email_id: number;
    date: String;
    type: EmailType;
}
