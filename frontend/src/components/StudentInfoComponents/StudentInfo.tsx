import React from "react";
import { StudentListFilters } from "../StudentsComponents";
import StudentInformation from "./StudentInformation/StudentInformation";
import { StudentInfoPageContent } from "./styles";
import { Student } from "../../data/interfaces/students";

interface Props {
    students: Student[];
    currentStudent: Student;
    nameFilter: string;
    setNameFilter: (value: string) => void;
    rolesFilter: number[];
    setRolesFilter: (value: number[]) => void;
    alumniFilter: boolean;
    setAlumniFilter: (value: boolean) => void;
    studentCoachVolunteerFilter: boolean;
    setStudentCoachVolunteerFilter: (value: boolean) => void;
}

export default function StudentInfo(props: Props) {
    return (
        <StudentInfoPageContent>
            <StudentListFilters {...props} />
            <StudentInformation currentStudent={props.currentStudent} />
        </StudentInfoPageContent>
    );
}