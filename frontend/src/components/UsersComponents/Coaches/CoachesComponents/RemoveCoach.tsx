import { User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import {
    removeCoachFromAllEditions,
    removeCoachFromEdition,
} from "../../../../utils/api/users/coaches";
import { Modal } from "react-bootstrap";
import {
    CancelButton,
    CredsDiv,
    DialogButtonContainer,
    DialogButtonDiv,
    ModalContent,
} from "../styles";
import LoadSpinner from "../../../Common/LoadSpinner";
import DeleteButton from "../../../Common/Buttons/DeleteButton";
import { toast } from "react-toastify";

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
    const [loading, setLoading] = useState(false);

    const handleClose = () => setShow(false);

    const handleShow = () => {
        setShow(true);
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
                toast.error("Failed to remove coach", {
                    toastId: "remove_coach_failed",
                });
                setLoading(false);
            }
        } catch (error) {
            toast.error("Failed to remove coach", {
                toastId: "remove_coach_failed",
            });
            setLoading(false);
        }
    }

    let buttons;
    if (loading) {
        buttons = <LoadSpinner show={true} />;
    } else {
        buttons = (
            <DialogButtonContainer>
                <DialogButtonDiv>
                    <DeleteButton
                        onClick={() => {
                            removeCoach(props.coach.userId, true);
                        }}
                        showIcon={false}
                    >
                        Remove from all editions
                    </DeleteButton>
                </DialogButtonDiv>
                <DialogButtonDiv>
                    <DeleteButton
                        onClick={() => {
                            removeCoach(props.coach.userId, false);
                        }}
                        showIcon={false}
                    >
                        Remove from current edition
                    </DeleteButton>
                    <CancelButton variant="secondary" onClick={handleClose}>
                        Cancel
                    </CancelButton>
                </DialogButtonDiv>
            </DialogButtonContainer>
        );
    }

    return (
        <>
            <DeleteButton onClick={handleShow} showIcon={false}>
                Remove
            </DeleteButton>

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
                    <Modal.Footer>{buttons}</Modal.Footer>
                </ModalContent>
            </Modal>
        </>
    );
}
