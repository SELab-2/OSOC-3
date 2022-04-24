import React, { useEffect, useState } from "react";
import { StudentListFilters } from "../../components/StudentsComponents";
import { getStudents } from "../../utils/api/students";
import {Student} from "../../data/interfaces/students";

function StudentsPage() {
    const [students, setStudents] = useState<Student[]>([]);
    const [nameFilter, setNameFilter] = useState("");
    const [rolesFilter, setRolesFilter] = useState<number[]>([]);
    const [alumniFilter, setAlumniFilter] = useState(false);
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(false);

    async function callGetStudents() {
        try {
            const response = await getStudents("OSOC_2022", nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter);
            if (response) {
                setStudents(response.students);
                console.log(students);
            }
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        callGetStudents();
        console.log("changed")
    }, [nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter]);

    return (
        <div>
            <StudentListFilters students={students} nameFilter={nameFilter} setNameFilter={setNameFilter} alumniFilter={alumniFilter} setAlumniFilter={setAlumniFilter} rolesFilter={rolesFilter} setRolesFilter={setRolesFilter} studentCoachVolunteerFilter={studentCoachVolunteerFilter} setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}/>
        </div>
    );
}

export default StudentsPage;
