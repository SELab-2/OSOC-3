import React from "react";
import { StudentRemoveButton } from "../styles";
import { removeStudent } from "../../../utils/api/students";
import { useNavigate, useParams } from "react-router-dom";

export default function RemoveStudentButton() {
    const params = useParams();
    const navigate = useNavigate();

    async function handleRemoveStudent() {
        await removeStudent(params.editionId!, params.id!);
        navigate(`/editions/${params.editionId}/students/`);
    }

    return (
        <StudentRemoveButton onClick={() => handleRemoveStudent()}>
            Remove Student
        </StudentRemoveButton>
    );
}
