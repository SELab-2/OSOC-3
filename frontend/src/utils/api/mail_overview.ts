import { Email, Student } from "../../data/interfaces";
import { EmailType } from "../../data/enums";
import { axiosInstance } from "./api";
import axios from "axios";

/**
 * A student together with its email history
 */
export interface StudentEmail {
    student: Student;
    emails: Email[];
}

/**
 * Multiple studentEmails in a list
 */
export interface StudentEmails {
    studentEmails: StudentEmail[];
}

/**
 * Get the sent emails of all students
 */
export async function getMailOverview(
    edition: string | undefined,
    page: number,
    name: string,
    filters: EmailType[],
    controller: AbortController
): Promise<StudentEmails | null> {
    try {
        const FormatFilters: string[] = filters.map(filter => {
            return `&email_status=${Object.values(EmailType).indexOf(filter)}`;
        });
        const concatted: string = FormatFilters.join("");

        const response = await axiosInstance.get(
            `/editions/${edition}/students/emails?page=${page}&name=${name}${concatted}`,
            { signal: controller.signal }
        );
        return response.data as StudentEmails;
    } catch (error) {
        if (axios.isAxiosError(error) && error.code === "ERR_CANCELED") {
            return null;
        } else {
            throw error;
        }
    }
}

/**
 * Updates the Email state of the currently selected students in the table to the selected state
 * from the dropdown menu
 */
export async function setStateRequest(
    eventKey: string,
    edition: string | undefined,
    selectedStudents: number[]
) {
    // post request with selected data
    await axiosInstance.post(`/editions/${edition}/students/emails`, {
        students_id: selectedStudents,
        email_status: eventKey,
    });
}
