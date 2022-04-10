import React, { useState } from "react";
import StudentList from "../StudentList";
import { Form } from "react-bootstrap";
import {
    StudentListSideMenu,
    FilterResetButton,
    StudentListTitle,
    StudentListLinebreak,
} from "./styles";
import AlumniFilter from "./AlumniFilter/AlumniFilter";
import StudentCoachVolunteerFilter from "./StudentCoachVolunteerFilter/StudentCoachVolunteerFilter";
import NameFilter from "./NameFilter/NameFilter";
import RolesFilter from "./RolesFilter/RolesFilter";

export default function StudentListFilters() {
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
            <FilterResetButton>Reset filters</FilterResetButton>
            <StudentList />
        </StudentListSideMenu>
    );
}
