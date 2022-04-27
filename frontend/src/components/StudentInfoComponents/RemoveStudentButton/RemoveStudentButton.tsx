import React from "react";
import {StudentRemoveButton} from "../styles"
import {removeStudent} from "../../../utils/api/students";
import {useNavigate, useParams} from "react-router-dom";

export default function RemoveStudentButton() {

    const params = useParams()
    const navigate = useNavigate()

    function handleRemoveStudent() {
        removeStudent(params.editionId!, params.id!)
        navigate(`/editions/2022/students/`)
    }

    return (
        <StudentRemoveButton onClick={() => handleRemoveStudent()}>Remove Student</StudentRemoveButton>
    );
}