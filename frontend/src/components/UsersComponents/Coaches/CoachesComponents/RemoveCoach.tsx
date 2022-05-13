import { User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import {
    removeCoachFromAllEditions,
    removeCoachFromEdition,
} from "../../../../utils/api/users/coaches";
import { Button, Modal, Spinner } from "react-bootstrap";
import {
    CancelButton,
    CredsDiv,
    DialogButton,
    DialogButtonContainer,
    ModalContent,
} from "../styles";
import { Error } from "../../Requests/styles";

/**
 * A button (part of [[CoachListItem]]) and popup to remove a user as coach from the given edition or all editions.
 * The popup gives the choice between removing the user as coach from this edition or all editions.
 * @param props.coach The coach which can be removed.
 * @param props.edition The edition of which the coach can be removed.
 * @param props.removeCoach A function which will be called when a user is removed as coach.
 */
export default function RemoveCoach(props: {
    coach: User;
    edition: string;
    removeCoach: () => void;
}) {
    const [show, setShow] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleClose = () => setShow(false);

    const handleShow = () => {
        setShow(true);
        setError("");
    };

    /**
     * Remove a coach from the current edition or all editions.
     * @param userId The id of the coach
     * @param allEditions Boolean whether the coach should be removed from all editions he's coach from.
     */
    async function removeCoach(userId: number, allEditions: boolean) {
        setLoading(true);
        let removed = false;
        try {
            if (allEditions) {
                removed = await removeCoachFromAllEditions(userId);
            } else {
                removed = await removeCoachFromEdition(userId, props.edition);
            }

            if (removed) {
                props.removeCoach();
            } else {
                setError("Something went wrong. Failed to remove coach");
                setLoading(false);
            }
        } catch (error) {
            setError("Something went wrong. Failed to remove coach");
            setLoading(false);
        }
    }

    let buttons;
    if (loading) {
        buttons = <Spinner animation="border" />;
    } else {
        buttons = (
            <DialogButtonContainer>
                <div>
                    <DialogButton
                        variant="primary"
                        onClick={() => {
                            removeCoach(props.coach.userId, true);
                        }}
                    >
                        Remove from all editions
                    </DialogButton>
                </div>
                <div>
                    <DialogButton
                        variant="primary"
                        onClick={() => {
                            removeCoach(props.coach.userId, false);
                        }}
                    >
                        Remove from current edition
                    </DialogButton>
                    <CancelButton variant="secondary" onClick={handleClose}>
                        Cancel
                    </CancelButton>
                </div>
            </DialogButtonContainer>
        );
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
                        <CredsDiv>
                            <h4>{props.coach.name}</h4>
                            {props.coach.auth.email}
                        </CredsDiv>
                    </Modal.Body>
                    <Modal.Footer>
                        {buttons}
                        <Error> {error} </Error>
                    </Modal.Footer>
                </ModalContent>
            </Modal>
        </>
    );
}
