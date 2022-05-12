import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";
import { Student } from "../../../data/interfaces/students";

interface Props {
    students: Student[];
}

/**
 * Component that renders the list of students in the sidebar.
 * @param props the students that need to be rendered.
 */
export default function StudentList(props: Props) {
    return (
        <StudentCardsList>
            {props.students.map(student => (
                <StudentCard
                    key={student.studentId}
                    studentId={student.studentId}
                    firstName={student.firstName}
                    nrOfSuggestions={student.nrOfSuggestions}
                />
            ))}
        </StudentCardsList>
    );
}
