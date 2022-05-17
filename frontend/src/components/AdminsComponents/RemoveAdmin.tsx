import { User } from "../../utils/api/users/users";
import React, { useState } from "react";
import { removeAdmin, removeAdminAndCoach } from "../../utils/api/users/admins";
import { Button, Modal } from "react-bootstrap";
import { RemoveAdminBody } from "./styles";
import { ModalContentWarning } from "../Common/styles";
import { toast } from "react-toastify";

/**
 * Button and popup to remove a user as admin (and as coach).
 * @param props.admin The user which can be removed.
 * @param props.removeAdmin A function which is called when the user is removed as admin.
 */
export default function RemoveAdmin(props: { admin: User; removeAdmin: (user: User) => void }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => {
        setShow(true);
    };

    async function removeUserAsAdmin(removeCoach: boolean) {
        let removed;
        if (removeCoach) {
            removed = await toast.promise(removeAdminAndCoach(props.admin.userId), {
                pending: "Removing admin",
                success: "Admin successfully removed",
                error: "Failed to remove admin",
            });
        } else {
            removed = await toast.promise(removeAdmin(props.admin.userId), {
                pending: "Removing admin",
                success: "Admin successfully removed",
                error: "Failed to remove admin",
            });
        }

        if (removed) {
            props.removeAdmin(props.admin);
        } else {
            toast.error("Failed to remove admin", {
                toastId: "remove_admin_failed",
            });
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
                            }}
                        >
                            Remove admin
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeUserAsAdmin(true);
                            }}
                        >
                            Remove as admin and coach
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContentWarning>
            </Modal>
        </>
    );
}
