import React, { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { DefinitiveDecisionContainer } from "../../StudentInformation/styles";
import { SuggestionButtons, ConfirmButton } from "./styles";
import { confirmStudent } from "../../../../utils/api/suggestions";
import { useParams } from "react-router-dom";

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
                        <ConfirmButton
                            value={0}
                            variant="success"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            Yes
                        </ConfirmButton>
                        <ConfirmButton
                            value={1}
                            variant="warning"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            Maybe
                        </ConfirmButton>
                        <ConfirmButton
                            value={2}
                            variant="danger"
                            onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick(e)}
                        >
                            No
                        </ConfirmButton>
                    </SuggestionButtons>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    <div>
                        {clickedButtonText ? (
                            <Button variant="primary" onClick={makeDecision}>
                                Confirm {clickedButtonText}?
                            </Button>
                        ) : (
                            <Button variant="primary" onClick={makeDecision} disabled={true}>
                                Confirm
                            </Button>
                        )}
                    </div>
                </Modal.Footer>
            </Modal>
            <h4>Definitive decision by admin</h4>
            <DefinitiveDecisionContainer>
                <Button onClick={handleShow} variant="success" size="lg">
                    Confirm
                </Button>
            </DefinitiveDecisionContainer>
        </div>
    );
}