import { Button, ButtonGroup, Modal } from "react-bootstrap";
import React, { useState } from "react";
import { Student } from "../../../../data/interfaces/students";
import { makeSuggestion } from "../../../../utils/api/students";
import { useParams } from "react-router-dom";
import { SuggestionActionTitle, YesButton, MaybeButton, NoButton } from "./styles";
import { CreateButton } from "../../../Common/Buttons";
import { FormControl } from "../../../Common/Forms";

interface Props {
    student: Student;
}

/**
 * Component for functionality of suggestions.
 * @param props current student
 */
export default function CoachSuggestionContainer(props: Props) {
    const params = useParams();
    const [show, setShow] = useState(false);
    const [argumentation, setArgumentation] = useState("");
    const [clickedButtonText, setClickedButtonText] = useState("");

    /**
     * Close the modal.
     */
    const handleClose = () => setShow(false);

    /**
     * Show the modal.
     */
    function handleShow(event: React.MouseEvent<HTMLButtonElement>) {
        event.preventDefault();
        const button: HTMLButtonElement = event.currentTarget;
        setClickedButtonText(button.innerText);
        setShow(true);
    }

    /**
     * Make suggestion on the current student based on the selected suggestion value.
     */
    async function doSuggestion() {
        let suggestionNum: number;
        if (clickedButtonText === "Yes") {
            suggestionNum = 1;
        } else if (clickedButtonText === "Maybe") {
            suggestionNum = 2;
        } else {
            suggestionNum = 3;
        }
        await makeSuggestion(params.editionId!, params.id!, suggestionNum, argumentation);
        setArgumentation("");
        setShow(false);
    }

    return (
        <div>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Suggestion "{clickedButtonText}" for{" "}
                        {props.student.firstName + " " + props.student.lastName}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Why are you giving this decision for this student?
                    <FormControl
                        type="text"
                        value={argumentation}
                        onChange={e => {
                            setArgumentation(e.target.value);
                        }}
                        placeholder="Place your argumentation here..."
                    />
                    * This field isn't required
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="info" onClick={handleClose}>
                        Close
                    </Button>
                    <CreateButton onClick={doSuggestion}>Save Suggestion</CreateButton>
                </Modal.Footer>
            </Modal>
            <SuggestionActionTitle>Make a suggestion on this student</SuggestionActionTitle>

            <ButtonGroup className="grid gap-sm-1">
                <YesButton
                    variant="success"
                    size="lg"
                    onClick={(e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => handleShow(e)}
                >
                    Yes
                </YesButton>
                <MaybeButton
                    variant="warning"
                    size="lg"
                    onClick={(e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => handleShow(e)}
                >
                    Maybe
                </MaybeButton>
                <NoButton
                    variant="danger"
                    size="lg"
                    onClick={(e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => handleShow(e)}
                >
                    No
                </NoButton>
            </ButtonGroup>
        </div>
    );
}
