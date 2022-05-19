import React, { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { DefinitiveDecisionContainer } from "../../StudentInformation/styles";
import { SuggestionButtons, ConfirmActionTitle } from "./styles";
import { YesButton, MaybeButton, NoButton } from "../CoachSuggestionContainer/styles";
import { confirmStudent } from "../../../../utils/api/suggestions";
import { useParams } from "react-router-dom";
import { CreateButton } from "../../../Common/Buttons";

/**
 * Make definitive decision on the current student based on the selected decision value.
 * Only admins can see this component.
 */
export default function AdminDecisionContainer() {
    const params = useParams();
    const [show, setShow] = useState(false);
    const [clickedButtonText, setClickedButtonText] = useState("");

    /**
     * Close the modal.
     */
    function handleClose() {
        setShow(false);
        setClickedButtonText("");
    }

    /**
     * Show the modal.
     */
    function handleShow(event: React.MouseEvent<HTMLButtonElement>) {
        event.preventDefault();
        setShow(true);
    }

    /**
     * Make definitive decision on the current student based on the selected decision value.
     */
    function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
        event.preventDefault();
        const button: HTMLButtonElement = event.currentTarget;
        setClickedButtonText(button.innerText);
    }

    async function makeDecision() {
        let decisionNum: number;
        if (clickedButtonText === "Undecided") {
            decisionNum = 0;
        } else if (clickedButtonText === "Yes") {
            decisionNum = 1;
        } else if (clickedButtonText === "Maybe") {
            decisionNum = 2;
        } else {
            decisionNum = 3;
        }
        await confirmStudent(params.editionId!, params.id!, decisionNum);
        setClickedButtonText("");
        setShow(false);
    }

    return (
        <div>
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Definitive decision on student</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Click on one of the buttons to mark your decision
                    <SuggestionButtons>
                        <YesButton
                            value={0}
                            variant="success"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            Yes
                        </YesButton>
                        <MaybeButton
                            value={1}
                            variant="warning"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            Maybe
                        </MaybeButton>
                        <NoButton
                            value={2}
                            variant="danger"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            No
                        </NoButton>
                    </SuggestionButtons>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="info" onClick={handleClose}>
                        Close
                    </Button>
                    <div>
                        {clickedButtonText ? (
                            <CreateButton onClick={makeDecision}>
                                Confirm {clickedButtonText}?
                            </CreateButton>
                        ) : (
                            <CreateButton onClick={makeDecision} disabled={true}>
                                Confirm
                            </CreateButton>
                        )}
                    </div>
                </Modal.Footer>
            </Modal>
            <ConfirmActionTitle>Definitive decision by admin</ConfirmActionTitle>
            <DefinitiveDecisionContainer>
                <CreateButton onClick={handleShow} variant="success" size="lg">
                    Confirm
                </CreateButton>
            </DefinitiveDecisionContainer>
        </div>
    );
}
