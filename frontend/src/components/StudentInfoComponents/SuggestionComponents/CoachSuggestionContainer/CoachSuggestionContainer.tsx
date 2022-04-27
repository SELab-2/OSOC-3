import {Button, ButtonGroup, Form, Modal} from "react-bootstrap";
import React, { useState } from "react";
import {Student} from "../../../../data/interfaces/students";

interface Props {
    student: Student;
}

export default function CoachSuggestionContainer(props: Props) {
    const [show, setShow] = useState(false);
    const [clickedButtonText, setClickedButtonText] = useState("")

    const handleClose = () => setShow(false);
    function handleShow(event: React.MouseEvent<HTMLButtonElement>) {
        event.preventDefault();
        const button: HTMLButtonElement = event.currentTarget;
        setClickedButtonText(button.innerText)
        setShow(true);
    }

    return (
        <div>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Suggestion "{clickedButtonText}" for {props.student.firstName + " " + props.student.lastName}</Modal.Title>
                </Modal.Header>
                <Modal.Body>Why are you giving this decision for this student?
                    <Form.Control
                    type="text"
                    name="nameFilter"
                    placeholder="Place your argumentation here..."/>
                    * This field isn't required
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleClose}>
                        Save Suggestion
                    </Button>
                </Modal.Footer>
            </Modal>
            <h4>Make a suggestion on this student</h4>
            <ButtonGroup className="grid gap-sm-1">
                <Button variant="success" size="lg" onClick={(e) => handleShow(e)}>
                    Yes
                </Button>
                <Button variant="warning" size="lg" onClick={(e) => handleShow(e)}>
                    Maybe
                </Button>
                <Button variant="danger" size="lg" onClick={(e) => handleShow(e)}>
                    No
                </Button>
            </ButtonGroup>
        </div>
    );
}
