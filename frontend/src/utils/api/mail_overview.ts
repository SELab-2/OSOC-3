import { Email, Student } from "../../data/interfaces";

/**
 * A student together with its email history
 */
interface StudentEmail {
    student: Student;
    emails: Email[];
}

export interface StudentEmails {
    studentEmails: StudentEmail[];
}

export async function getMailOverview(): Promise<StudentEmails> {
    // const response = await axiosInstance.get("/editions/1/emails/");
    // return response.data as StudentEmails;

    // placeholder while the real API call is not available
    const data = {
        studentEmails: [
            {
                student: { studentId: 1, firstName: "Bert", lastName: "Guillemyn" },
                emails: [
                    { emailId: 1, date: "2022-04-13T11:46:28.641337", type: 0 },
                    { emailId: 2, date: "2022-04-14T12:36:28.641337", type: 1 },
                    { emailId: 3, date: "2022-04-15T13:38:38.641337", type: 2 },
                ],
            },
        ],
    };
    return data as StudentEmails;
}
