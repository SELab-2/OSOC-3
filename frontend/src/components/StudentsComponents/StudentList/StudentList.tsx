import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";
import { Student } from "../../../data/interfaces/students";

interface Props {
    students: Student[];
}

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
