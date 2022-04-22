import { Email, Student } from "../../data/interfaces";
import { ChangeEvent } from "react";
import { EmailType } from "../../data/enums";
/**
 * A student together with its email history
 */
interface StudentEmail {
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
    page: number
): Promise<StudentEmails> {
    // const FormatFilters: number[] = finalFilters.map(filter => {
    //     return Object.values(EmailType).indexOf(filter);
    // });
    // const response = await axiosInstance.get(
    //    `/editions/${edition}/emails/?page=${page}&first_name=${finalSearch}&email_status=${FormatFilters}`
    // );
    // return response.data as StudentEmails;
    console.log(finalFilters);
    console.log(finalSearch);
    // placeholder while the real API call is not available
    if (page > 0) {
        return { studentEmails: [] } as StudentEmails;
    }
    const data = {
        studentEmails: [
            {
                student: { studentId: 1, firstName: "Bert", lastName: "Guillemyn" },
                emails: [
                    { emailId: 1, studentId: 1, date: "2022-04-13T11:46:28.641337", decision: 0 },
                    { emailId: 2, studentId: 1, date: "2022-04-14T12:36:28.641337", decision: 1 },
                    { emailId: 3, studentId: 1, date: "2022-04-15T13:38:38.641337", decision: 2 },
                ],
            },
            {
                student: { studentId: 2, firstName: "Test", lastName: "Person" },
                emails: [
                    { emailId: 1, studentId: 2, date: "2022-04-13T08:25:46.641337", decision: 4 },
                    { emailId: 2, studentId: 2, date: "2022-04-14T12:36:28.641337", decision: 1 },
                    { emailId: 3, studentId: 2, date: "2022-04-15T13:38:38.641337", decision: 2 },
                ],
            },
        ],
    };
    return data as StudentEmails;
}

const selectedRows: number[] = [];

/**
 * Keeps the selectedRows list up-to-date when a student is selected/unselected in the table
 * @param row
 * @param isSelect
 */
export function handleSelect(row: StudentEmail, isSelect: boolean) {
    if (isSelect) {
        selectedRows.push(row.student.studentId);
    } else {
        selectedRows.splice(
            selectedRows.findIndex(item => item === row.student.studentId),
            1
        );
    }
}

/**
 * Does the same as handleSelect, but for multiple rows at the same time
 * @param isSelect
 * @param rows
 */
export function handleSelectAll(isSelect: boolean, rows: StudentEmail[]) {
    for (const row of rows) {
        handleSelect(row, isSelect);
    }
}

/**
 * Updates the Email state of the currently selected students in the table to the selected state
 * from the dropdown menu
 * @param eventKey
 * @param edition
 */
export function setStateRequest(eventKey: string | null, edition: string | undefined) {
    console.log(eventKey);
    console.log(selectedRows);
    // TODO do post request with selected data
    // const response = await axiosInstance.post(`/editions/${edition}/emails/`,
    // {student_ids: selectedRows, email_status: eventKey});
}

let selectedFilters: EmailType[] = [];
/**
 * Keeps track of the selected filters
 * @param selectedList
 */
export function handleFilterSelect(selectedList: EmailType[]) {
    selectedFilters = selectedList;
}

let searchTerm: string = "";

/**
 * Keeps track of the search value
 * @param event
 */
export function handleSetSearch(event: ChangeEvent<{ value: string }>) {
    searchTerm = event.target.value;
}

let finalFilters: string[] = [];
let finalSearch: string = "";

/**
 * Sets the definitive search term and filters to be sent
 */
export function setFinalFilters() {
    finalFilters = selectedFilters;
    finalSearch = searchTerm;
}
