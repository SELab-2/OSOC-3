import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";

interface Student {
    name: string;
    amountOfSuggestions: number;
}

interface Props {
    students: Student[];
}

export default function StudentList(props: Props) {
    return (
        <StudentCardsList>
            {props.students.map(student => (
                <StudentCard
                    key={student.name}
                    name={student.name}
                    amountOfSuggestions={student.amountOfSuggestions}
                />
            ))}
        </StudentCardsList>
    );
}
