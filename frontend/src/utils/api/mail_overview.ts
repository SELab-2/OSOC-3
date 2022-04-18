import { Email, Student } from "../../data/interfaces";
import { ChangeEvent } from "react";
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
            {
                student: { studentId: 2, firstName: "Test", lastName: "Person" },
                emails: [
                    { emailId: 1, date: "2022-04-13T08:25:46.641337", type: 4 },
                    { emailId: 2, date: "2022-04-14T12:36:28.641337", type: 1 },
                    { emailId: 3, date: "2022-04-15T13:38:38.641337", type: 2 },
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
 */
export function handleSetState(eventKey: string | null) {
    console.log(eventKey);
    console.log(selectedRows);
    // TODO do post request with selected data

    // update table contents ?
}

let selectedFilters: string[] = [];
/**
 * Filters the table
 * @param selectedList
 */
export function handleFilterSelect(selectedList: string[]) {
    selectedFilters = selectedList;
}

let searchTerm: string = "";
export function handleSetSearch(event: ChangeEvent<{ value: string }>) {
    searchTerm = event.target.value;
}

export function handleDoSearch() {
    console.log(selectedFilters);
    console.log(searchTerm);
    // TODO: make get request with filters and searchterm
}
