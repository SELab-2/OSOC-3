import React from "react";
import { StudentRemoveButton } from "../styles";
import { removeStudent } from "../../../utils/api/students";
import { useNavigate, useParams } from "react-router-dom";

/**
 * Component that removes the current student.
 */
export default function RemoveStudentButton() {
    const params = useParams();
    const navigate = useNavigate();

    /**
     * Remove the current selected student and navigate back to the students page.
     */
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
