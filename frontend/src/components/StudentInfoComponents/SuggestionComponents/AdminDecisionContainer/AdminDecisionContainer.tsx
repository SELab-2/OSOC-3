import React, { useState } from "react";
import { Button, Modal } from "react-bootstrap";
import { DefinitiveDecisionContainer } from "../../StudentInformation/styles";
import { SuggestionButtons, ConfirmButton } from "./styles";

/**
 * Make definitive decision on the current student based on the selected decision value.
 * Only admins can see this component.
 */
export default function AdminDecisionContainer() {
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
                            <Button variant="primary" onClick={handleClose}>
                                Confirm {clickedButtonText}?
                            </Button>
                        ) : (
                            <Button variant="primary" onClick={handleClose} disabled={true}>
                                Confirm
                            </Button>
                        )}
                    </div>
                </Modal.Footer>
            </Modal>
            <h4>Definitive decision by admin</h4>
            <DefinitiveDecisionContainer>
                <Button onClick={e => handleShow(e)} variant="success" size="lg">
                    Confirm
                </Button>
            </DefinitiveDecisionContainer>
        </div>
    );
}
