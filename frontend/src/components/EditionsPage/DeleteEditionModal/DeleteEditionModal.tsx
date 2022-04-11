import { Edition } from "../../../data/interfaces";
import Modal from "react-bootstrap/Modal";
import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import "./DeleteEditionModal.css";
import Form from "react-bootstrap/Form";
import InfoMessage from "./InfoMessage";
import Spinner from "react-bootstrap/Spinner";

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

    function handleConfirm() {
        setConfirmed(true);

        // props.setShow(false);
        // // Force-reload the page to re-request all data related to editions
        // // (stored in various places such as auth, ...)
        // window.location.reload();
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
     * Function called when the input field for the name of the edition changes
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
                    <Modal.Title>Easy, partner!</Modal.Title>
                </Modal.Header>
                {/* Show checkbox screen if not clicked, else move on */}
                {!understandClicked ? (
                    <Modal.Body>
                        <Form onSubmit={() => {}}>
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
                        <Form onSubmit={() => {}}>
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
                        <h4>Deleting {props.edition.name}...</h4>
                        <p>
                            The request has been sent, there's no turning back now!
                            <br /> <br />
                            If you've changed your mind, all you can do now is hope the request
                            fails.
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
