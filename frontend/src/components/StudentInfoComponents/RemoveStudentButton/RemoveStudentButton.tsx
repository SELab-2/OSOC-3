import React, { useState } from "react";
import { removeStudent } from "../../../utils/api/students";
import { useNavigate } from "react-router-dom";
import { DeleteButton } from "../../Common/Buttons";
import { Button, Modal } from "react-bootstrap";
import { Student } from "../../../data/interfaces/students";

/**
 * Component that removes the current student.
 */
export default function RemoveStudentButton(props: {
    editionId: string;
    studentId: number;
    student: Student;
}) {
    const navigate = useNavigate();
    const [show, setShow] = useState(false);

    /**
     * Close the modal.
     */
    const handleClose = () => setShow(false);

    /**
     * Show the modal.
     */
    const handleShow = () => setShow(true);

    /**
     * Remove the current selected student and navigate back to the students page.
     */
    async function handleRemoveStudent() {
        await removeStudent(props.editionId, props.studentId);
        navigate(`/editions/${props.editionId}/students/`);
    }

    return (
        <div>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Are you sure you want to delete {props.student.firstName}{" "}
                        {props.student.lastName}?
                    </Modal.Title>
                </Modal.Header>
                <Modal.Footer>
                    <Button variant="info" onClick={handleClose}>
                        Close
                    </Button>
                    <DeleteButton onClick={handleRemoveStudent}>
                        Remove {props.student.firstName}
                    </DeleteButton>
                </Modal.Footer>
            </Modal>
            <DeleteButton onClick={handleShow}>Remove Student</DeleteButton>
        </div>
    );
}
