import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getStudent, getStudents } from "../../utils/api/students";
import StudentInfo from "../../components/StudentInfoComponents/StudentInfo";
import { Student } from "../../data/interfaces/students";

/**
 * @returns the detailed page of a student. Here you can make a suggestion and admins
 *          can make definitive decisions on students. You can also remove the currently selected student.
 */
function StudentInfoPage() {
    const params = useParams();
    const [students, setStudents] = useState<Student[]>([]);
    const [nameFilter, setNameFilter] = useState("");
    const [rolesFilter, setRolesFilter] = useState<number[]>([]);
    const [alumniFilter, setAlumniFilter] = useState(false);
    const [studentCoachVolunteerFilter, setStudentCoachVolunteerFilter] = useState(false);
    const [currentStudent, setCurrentStudent] = useState<Student>();

    /**
     * Request all students with selected filters.
     */
    async function callGetStudents() {
        try {
            const response = await getStudents(
                params.editionId!,
                nameFilter,
                rolesFilter,
                alumniFilter,
                studentCoachVolunteerFilter
            );
            setStudents(response.students);
        } catch (error) {
            console.log(error);
        }
    }

    /**
     * Request the currently selected student.
     */
    async function callGetStudent() {
        try {
            const response = await getStudent(params.editionId!, params.id!);
            setCurrentStudent(response);
        } catch (error) {
            console.log(error);
        }
    }

    /**
     * fetch students when a filter changes
     */
    useEffect(() => {
        callGetStudents();
    }, [nameFilter, rolesFilter, alumniFilter, studentCoachVolunteerFilter]);

    /**
     * fetch student when the student id changes
     */
    useEffect(() => {
        callGetStudent();
    }, [params.id!]);

    if (!currentStudent) {
        return (
            <div>
                <h1>loading</h1>
            </div>
        );
    } else {
        return (
            <div>
                <StudentInfo
                    students={students}
                    currentStudent={currentStudent!}
                    nameFilter={nameFilter}
                    setNameFilter={setNameFilter}
                    alumniFilter={alumniFilter}
                    setAlumniFilter={setAlumniFilter}
                    rolesFilter={rolesFilter}
                    setRolesFilter={setRolesFilter}
                    studentCoachVolunteerFilter={studentCoachVolunteerFilter}
                    setStudentCoachVolunteerFilter={setStudentCoachVolunteerFilter}
                />
            </div>
        );
    }
}

export default StudentInfoPage;
