import React from "react";
import { StudentListFilters } from "../StudentsComponents";
import StudentInformation from "./StudentInformation/StudentInformation";
import { StudentRemoveButton, StudentInfoPageContent } from "./styles";
import {Student} from "../../data/interfaces/students";

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
            <StudentListFilters students={props.students} nameFilter={props.nameFilter} setNameFilter={props.setNameFilter} alumniFilter={props.alumniFilter} setAlumniFilter={props.setAlumniFilter} rolesFilter={props.rolesFilter} setRolesFilter={props.setRolesFilter} studentCoachVolunteerFilter={props.studentCoachVolunteerFilter} setStudentCoachVolunteerFilter={props.setStudentCoachVolunteerFilter} />
            <StudentRemoveButton>Remove Student</StudentRemoveButton>
            <StudentInformation currentStudent={props.currentStudent}/>
        </StudentInfoPageContent>
    );
}
