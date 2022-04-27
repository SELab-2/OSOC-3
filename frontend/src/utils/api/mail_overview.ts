import { Email, Student } from "../../data/interfaces";
import { ChangeEvent } from "react";
import { EmailType } from "../../data/enums";
import { axiosInstance } from "./api";
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
    const FormatFilters: string[] = finalFilters.map(filter => {
        return `&email_status=${Object.values(EmailType).indexOf(filter)}`;
    });
    const concatted: string = FormatFilters.join("");
    const response = await axiosInstance.get(
        `/editions/${edition}/students/emails?page=${page}&name=${finalSearch}${concatted}`
    );
    return response.data as StudentEmails;
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
export async function setStateRequest(eventKey: string | null, edition: string | undefined) {
    // post request with selected data
    await axiosInstance.post(`/editions/${edition}/students/emails`, {
        students_id: selectedRows,
        email_status: eventKey,
    });
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

let finalFilters: EmailType[] = [];
let finalSearch: string = "";

/**
 * Sets the definitive search term and filters to be sent
 */
export function setFinalFilters() {
    finalFilters = selectedFilters;
    finalSearch = searchTerm;
}
