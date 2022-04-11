import { Edition } from "../../data/interfaces";
import Modal from "react-bootstrap/Modal";
import React from "react";
import Button from "react-bootstrap/Button";
import "./DeleteEditionModal.css";

interface Props {
    edition: Edition;
    show: boolean;
    setShow: (value: boolean) => void;
}

/**
 * Modal shown when trying to delete an edition
 */
export default function DeleteEditionModal(props: Props) {
    const disableConfirm = true;

    function handleClose() {
        props.setShow(false);
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
                <Modal.Body>You can't just walk around deleting editions like that!</Modal.Body>
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
