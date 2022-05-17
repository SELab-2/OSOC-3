import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import StudentInfo from "../../components/StudentInfoComponents/StudentInfo";

/**
 * @returns the detailed page of a student. Here you can make a suggestion and admins
 *          can make definitive decisions on students. You can also remove the currently selected student.
 */
function StudentInfoPage() {
    const params = useParams();
    const studentId = params.id;
    const editionId = params.editionId;

    const navigate = useNavigate();

    if (studentId === undefined || (isNaN(+studentId) && editionId === undefined)) {
        navigate("/404-not-found");
    }

    return <StudentInfo studentId={Number(studentId)} editionId={editionId as string} />;
}

export default StudentInfoPage;
