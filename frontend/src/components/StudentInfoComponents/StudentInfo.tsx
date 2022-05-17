import React from "react";
import { StudentListFilters } from "../StudentsComponents";
import StudentInformation from "./StudentInformation/StudentInformation";
import { StudentInfoPageContent } from "./styles";

/**
 * Component that renders the students list and the information about the currently selected student.
 * @param props all student, current student and all filters to handle the student information page.
 */
export default function StudentInfo(props: { studentId: number; editionId: string }) {
    return (
        <StudentInfoPageContent>
            <StudentListFilters />
            <StudentInformation studentId={props.studentId} editionId={props.editionId} />
        </StudentInfoPageContent>
    );
}
