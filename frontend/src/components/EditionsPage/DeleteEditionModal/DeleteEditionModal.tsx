import { Edition } from "../../../data/interfaces";
import Modal from "react-bootstrap/Modal";
import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import "./DeleteEditionModal.css";
import Form from "react-bootstrap/Form";
import InfoMessage from "./InfoMessage";
import Spinner from "react-bootstrap/Spinner";
import { deleteEdition } from "../../../utils/api/editions";
import { getCurrentEdition, setCurrentEdition } from "../../../utils/session-storage";

interface Props {
    edition: Edition;
    show: boolean;
    setShow: (value: boolean) => void;
}

/**
 * Modal shown when trying to delete an edition
 */
export default function DeleteEditionModal(props: Props) {
    const [disableConfirm, setDisableConfirm] = useState(true);
    const [understandClicked, setUnderstandClicked] = useState(false);
    const [confirmed, setConfirmed] = useState(false);

    function handleClose() {
        props.setShow(false);
        setUnderstandClicked(false);
    }

    /**
     * Confirm the deletion of this edition
     */
    async function handleConfirm() {
        // Show confirmation text while the request is being sent
        setConfirmed(true);

        // Delete the request
        const statusCode = await deleteEdition(props.edition.name);

        // Hide the modal
        props.setShow(false);

        if (statusCode === 204) {
            // Remove the edition as current
            if (getCurrentEdition() === props.edition.name) {
                setCurrentEdition(null);
            }

            // Force-reload the page to re-request all data related to editions
            // (stored in various places such as auth, ...)
            window.location.reload();
        }
    }

    /**
     * Validate the data entered into the form
     */
    function checkFormValid(name: string) {
        if (name !== props.edition.name) {
            setDisableConfirm(true);
        } else {
            setDisableConfirm(false);
        }
    }

    /**
     * Called when the input field for the name of the edition changes
     */
    function handleTextfieldChange(value: string) {
        checkFormValid(value);
    }

    return (
        // Obscure JS thing: clicking "close" on the modal propagates the "onClick" up
        // to the open button, which re-opens it
        // Explicitly deny propagation to stop this
        <div onClick={e => e.stopPropagation()}>
            <Modal show={props.show} backdrop={"static"} onHide={handleClose} variant={"dark"}>
                <Modal.Header>
                    <Modal.Title>
                        {confirmed ? `Deleting ${props.edition.name}...` : "Not so fast!"}
                    </Modal.Title>
                </Modal.Header>
                {!understandClicked ? (
                    // Show checkbox screen/information text
                    <Modal.Body>
                        <Form>
                            <InfoMessage editionName={props.edition.name} />
                            <Form.Group>
                                <Form.Check
                                    type={"checkbox"}
                                    label={"I understand."}
                                    checked={understandClicked}
                                    onChange={e => setUnderstandClicked(e.target.checked)}
                                />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                ) : !confirmed ? (
                    // Checkbox screen was passed, show the other screen now
                    <Modal.Body>
                        <Form>
                            <Form.Label>
                                You didn't think it would be <i>that</i> easy, did you?
                            </Form.Label>
                            <br />
                            <br />
                            <Form.Group>
                                <Form.Label>
                                    Type the name of the edition in the field below
                                </Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder={"Edition name"}
                                    required
                                    onChange={e => handleTextfieldChange(e.target.value)}
                                />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                ) : (
                    // Delete request is being sent
                    <Modal.Body>
                        <h4>There's no turning back now!</h4>
                        <p>
                            The request has been sent. If you've changed your mind, all you can do
                            now is hope the request fails.
                        </p>
                        <Spinner animation={"border"} role={"status"} className={"mx-auto my-3"} />
                    </Modal.Body>
                )}
                {/* Only show footer if not yet confirmed */}
                {!confirmed && (
                    <Modal.Footer>
                        <Button onClick={handleClose} variant={"secondary"}>
                            Close
                        </Button>
                        <Button
                            onClick={handleConfirm}
                            variant={"danger"}
                            disabled={disableConfirm}
                        >
                            Delete Edition
                        </Button>
                    </Modal.Footer>
                )}
            </Modal>
        </div>
    );
}
