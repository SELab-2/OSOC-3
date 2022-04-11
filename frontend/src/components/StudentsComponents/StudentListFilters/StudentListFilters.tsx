import React, { useState } from "react";
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
import ApplyFilterButton from "./ApplyFilterButton/ApplyFilterButton";

interface Student {
    name: string;
    amountOfSuggestions: number;
}

interface Props {
    students: Student[];
}

export default function StudentListFilters(props: Props) {
    const [nameFilter, setNameFilter] = useState("");
    const [rolesFilter, setRolesFilter] = useState<number[]>([]);
    const [alumniFilter, setAlumniFilter] = useState(false);
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(false);

    return (
        <StudentListSideMenu>
            <StudentListTitle>Students</StudentListTitle>
            <StudentListLinebreak />
            <NameFilter nameFilter={nameFilter} setNameFilter={setNameFilter} />
            <RolesFilter rolesFilter={rolesFilter} setRolesFilter={setRolesFilter} />
            <Form.Group>
                <AlumniFilter alumniFilter={alumniFilter} setAlumniFilter={setAlumniFilter} />
                <Form.Check type="checkbox" label="Only students you've suggested for" />
                <StudentCoachVolunteerFilter
                    studentCoachVolunteerFilter={studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                />
                <Form.Check type="checkbox" label="Only available students" />
            </Form.Group>
            <FilterControls>
                <ApplyFilterButton />
                <ResetFiltersButton
                    setNameFilter={setNameFilter}
                    setAlumniFilter={setAlumniFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                />
            </FilterControls>
            <StudentList students={props.students} />
        </StudentListSideMenu>
    );
}
