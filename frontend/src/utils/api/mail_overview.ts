import { Email, Student } from "../../data/interfaces";
import { EmailType } from "../../data/enums";
import { axiosInstance } from "./api";

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
    filters: EmailType[]
): Promise<StudentEmails> {
    const FormatFilters: string[] = filters.map(filter => {
        return `&email_status=${Object.values(EmailType).indexOf(filter)}`;
    });
    const concatted: string = FormatFilters.join("");

    const response = await axiosInstance.get(
        `/editions/${edition}/students/emails?page=${page}&name=${name}${concatted}`
    );
    return response.data as StudentEmails;
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
