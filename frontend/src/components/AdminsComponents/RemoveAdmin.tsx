import { User } from "../../utils/api/users/users";
import React, { useState } from "react";
import { removeAdmin, removeAdminAndCoach } from "../../utils/api/users/admins";
import { Button, Modal } from "react-bootstrap";
import { ModalContentWarning, RemoveAdminBody } from "./styles";
import { Error } from "../UsersComponents/Requests/styles";

/**
 * Button and popup to remove a user as admin (and as coach).
 * @param props.admin The user which can be removed.
 * @param props.removeAdmin A function which is called when the user is removed as admin.
 */
export default function RemoveAdmin(props: { admin: User; removeAdmin: (user: User) => void }) {
    const [show, setShow] = useState(false);
    const [error, setError] = useState("");

    const handleClose = () => setShow(false);
    const handleShow = () => {
        setShow(true);
        setError("");
    };

    async function removeUserAsAdmin(removeCoach: boolean) {
        try {
            let removed;
            if (removeCoach) {
                removed = await removeAdminAndCoach(props.admin.userId);
            } else {
                removed = await removeAdmin(props.admin.userId);
            }

            if (removed) {
                props.removeAdmin(props.admin);
            } else {
                setError("Something went wrong. Failed to remove admin");
            }
        } catch (error) {
            setError("Something went wrong. Failed to remove admin");
        }
    }

    return (
        <>
            <Button variant="primary" size="sm" onClick={handleShow}>
                Remove
            </Button>

            <Modal show={show} onHide={handleClose}>
                <ModalContentWarning>
                    <Modal.Header closeButton>
                        <Modal.Title>Remove Admin</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <RemoveAdminBody>
                            <h4>{props.admin.name}</h4>
                            <p>{props.admin.auth.email}</p>
                            <p>Remove admin: This admin will stay coach for assigned editions</p>
                        </RemoveAdminBody>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeUserAsAdmin(false);
                                if (!error) {
                                    handleClose();
                                }
                            }}
                        >
                            Remove admin
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeUserAsAdmin(true);
                                if (!error) {
                                    handleClose();
                                }
                            }}
                        >
                            Remove as admin and coach
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                        <Error> {error} </Error>
                    </Modal.Footer>
                </ModalContentWarning>
            </Modal>
        </>
    );
}
