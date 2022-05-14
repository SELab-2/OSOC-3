import React from "react";
import StudentList from "../StudentList";
import { Form } from "react-bootstrap";
import {
    StudentListSideMenu,
    StudentListTitle,
    StudentListLinebreak,
    FilterControls,
} from "./styles";
import AlumniFilter from "./AlumniFilter/AlumniFilter";
import StudentCoachVolunteerFilter from "./StudentCoachVolunteerFilter/StudentCoachVolunteerFilter";
import NameFilter from "./NameFilter/NameFilter";
import RolesFilter from "./RolesFilter/RolesFilter";
import "./StudentListFilters.css";
import ResetFiltersButton from "./ResetFiltersButton/ResetFiltersButton";
import { Student } from "../../../data/interfaces/students";

interface Props {
    students: Student[];
    nameFilter: string;
    setNameFilter: (value: string) => void;
    rolesFilter: number[];
    setRolesFilter: (value: number[]) => void;
    alumniFilter: boolean;
    setAlumniFilter: (value: boolean) => void;
    studentCoachVolunteerFilter: boolean;
    setStudentCoachVolunteerFilter: (value: boolean) => void;
}

/**
 * Component that shows the sidebar with all the filters and student list.
 * @param props All students and filters currently selected.
 */
export default function StudentListFilters(props: Props) {
    return (
        <StudentListSideMenu>
            <StudentListTitle>Students</StudentListTitle>
            <StudentListLinebreak />
            <NameFilter nameFilter={props.nameFilter} setNameFilter={props.setNameFilter} />
            <RolesFilter setRolesFilter={props.setRolesFilter} />
            <Form.Group>
                <AlumniFilter
                    alumniFilter={props.alumniFilter}
                    setAlumniFilter={props.setAlumniFilter}
                />
                <Form.Check type="checkbox" label="Only students you've suggested for" />
                <StudentCoachVolunteerFilter
                    studentCoachVolunteerFilter={props.studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={props.setStudentCoachVolunteerFilter}
                />
                <Form.Check type="checkbox" label="Only available students" />
            </Form.Group>
            <FilterControls>
                <ResetFiltersButton
                    setNameFilter={props.setNameFilter}
                    setAlumniFilter={props.setAlumniFilter}
                    setStudentCoachVolunteerFilter={props.setStudentCoachVolunteerFilter}
                />
            </FilterControls>
            <StudentList students={props.students} />
        </StudentListSideMenu>
    );
}
