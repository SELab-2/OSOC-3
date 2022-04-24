import React, { useEffect, useState } from "react";
import {useParams} from 'react-router-dom';
import {getStudent, getStudents} from "../../utils/api/students";
import StudentInfo from "../../components/StudentInfoComponents/StudentInfo";
import {Student} from "../../data/interfaces/students";

function StudentInfoPage() {
    const params = useParams()
    const [students, setStudents] = useState<Student[]>([]);
    const [nameFilter, setNameFilter] = useState("");
    const [rolesFilter, setRolesFilter] = useState<number[]>([]);
    const [alumniFilter, setAlumniFilter] = useState(false);
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(false);
    const [currentStudent, setCurrentStudent] = useState<Student>();
    async function callGetStudents() {
        try {
            const response = await getStudents("OSOC_2022", nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter);
            setStudents(response.students);
        } catch (error) {
            console.log(error);
        }
    }

    async function callGetStudent() {
        try {
            const response = await getStudent("OSOC_2022", params.id!);
            setCurrentStudent(response);
            console.log(currentStudent)
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        callGetStudent();
        callGetStudents();
    }, []);

    return (
        <div>
            <StudentInfo students={students} currentStudent={currentStudent!} nameFilter={nameFilter} setNameFilter={setNameFilter} alumniFilter={alumniFilter} setAlumniFilter={setAlumniFilter} rolesFilter={rolesFilter} setRolesFilter={setRolesFilter} studentCoachVolunteerFilter={studentCoachVolunteerFilter} setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter} />
        </div>
    );
}

export default StudentInfoPage;
