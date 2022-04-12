import { EmailType } from "../enums";
/**
 * A sent email
 */
export interface Email {
    date: String;
    type: EmailType;
}
