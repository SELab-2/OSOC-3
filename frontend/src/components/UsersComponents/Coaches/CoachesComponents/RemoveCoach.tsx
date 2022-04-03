import { User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import {
    removeCoachFromAllEditions,
    removeCoachFromEdition,
} from "../../../../utils/api/users/coaches";
import { Button, Modal } from "react-bootstrap";
import { ModalContent } from "../styles";
import { Error } from "../../PendingRequests/styles";

export default function RemoveCoach(props: { coach: User; edition: string; refresh: () => void }) {
    const [show, setShow] = useState(false);
    const [error, setError] = useState("");

    const handleClose = () => setShow(false);
    const handleShow = () => {
        setShow(true);
        setError("");
    };

    async function removeCoach(userId: number, allEditions: boolean) {
        try {
            let removed;
            if (allEditions) {
                removed = await removeCoachFromAllEditions(userId);
            } else {
                removed = await removeCoachFromEdition(userId, props.edition);
            }

            if (removed) {
                props.refresh();
                handleClose();
            } else {
                setError("Something went wrong. Failed to remove coach");
            }
        } catch (error) {
            setError("Something went wrong. Failed to remove coach");
        }
    }

    return (
        <>
            <Button variant="primary" size="sm" onClick={handleShow}>
                Remove
            </Button>

            <Modal show={show} onHide={handleClose}>
                <ModalContent>
                    <Modal.Header closeButton>
                        <Modal.Title>Remove Coach</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <h4>{props.coach.name}</h4>
                        {props.coach.email}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeCoach(props.coach.userId, true);
                            }}
                        >
                            Remove from all editions
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeCoach(props.coach.userId, false);
                            }}
                        >
                            Remove from {props.edition}
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                        <Error> {error} </Error>
                    </Modal.Footer>
                </ModalContent>
            </Modal>
        </>
    );
}
