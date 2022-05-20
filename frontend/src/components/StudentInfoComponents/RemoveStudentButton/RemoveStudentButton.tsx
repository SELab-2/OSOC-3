import React from "react";
import { removeStudent } from "../../../utils/api/students";
import { useNavigate } from "react-router-dom";
import { DeleteButton } from "../../Common/Buttons";

/**
 * Component that removes the current student.
 */
export default function RemoveStudentButton(props: { editionId: string; studentId: number }) {
    const navigate = useNavigate();

    /**
     * Remove the current selected student and navigate back to the students page.
     */
    async function handleRemoveStudent() {
        await removeStudent(props.editionId, props.studentId);
        navigate(`/editions/${props.editionId}/students/`);
    }

    return <DeleteButton onClick={() => handleRemoveStudent()}>Remove Student</DeleteButton>;
}
