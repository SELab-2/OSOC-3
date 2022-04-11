import { Edition } from "../../../data/interfaces";
import Modal from "react-bootstrap/Modal";
import React, { useState } from "react";
import Button from "react-bootstrap/Button";
import "./DeleteEditionModal.css";
import Form from "react-bootstrap/Form";
import InfoMessage from "./InfoMessage";

interface Props {
    edition: Edition;
    show: boolean;
    setShow: (value: boolean) => void;
}

/**
 * Create a value for the slider to be on
 */
function createSliderValue(): number {
    return Math.floor(Math.random() * 100);
}

/**
 * Modal shown when trying to delete an edition
 */
export default function DeleteEditionModal(props: Props) {
    const [requiredSliderValue, setRequiredSliderValue] = useState(createSliderValue());
    const [understandClicked, setUnderstandClicked] = useState(false);
    const [sliderValue, setSliderValue] = useState(0);
    const disableConfirm = true;

    function handleClose() {
        props.setShow(false);
        setUnderstandClicked(false);

        // Create a new slider value
        setRequiredSliderValue(createSliderValue());
    }

    function handleConfirm() {
        props.setShow(false);
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
                ) : (
                    <Modal.Body>
                        <Form>
                            <Form.Text>
                                You didn't think it would be <i>that</i> easy, did you?
                            </Form.Text>
                            <Form.Label>
                                Set the value of the slider below to {requiredSliderValue}%
                            </Form.Label>
                            <Form.Group>
                                <Form.Range
                                    onChange={e => setSliderValue(Number(e.target.value))}
                                />
                                <Form.Text>{sliderValue}%</Form.Text>
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                )}
                <Modal.Footer>
                    <Button onClick={handleClose} variant={"secondary"}>
                        Close
                    </Button>
                    <Button onClick={handleConfirm} variant={"danger"} disabled={disableConfirm}>
                        Delete Edition
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
