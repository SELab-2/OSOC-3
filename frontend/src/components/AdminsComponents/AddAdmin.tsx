import { User } from "../../utils/api/users/users";
import React, { useState } from "react";
import { addAdmin } from "../../utils/api/users/admins";
import { AddAdminButton, ModalContentConfirm, Warning } from "./styles";
import { Button, Modal } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import { Error } from "../UsersComponents/PendingRequests/styles";

/**
 * Warning that the user will get all persmissions.
 * @param props.name The name of the user.
 */
function AddWarning(props: { name: string | undefined }) {
    if (props.name !== undefined) {
        return (
            <Warning>
                Warning: {props.name} will be able to edit/delete all data and manage admin roles.
            </Warning>
        );
    }
    return null;
}

/**
 * Button and popup to add an existing user as admin.
 * @param props.users All users which can be added as admin.
 * @param props.refresh A function which is called when a new admin is added.
 */
export default function AddAdmin(props: { users: User[]; refresh: () => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
    const [error, setError] = useState("");

    const handleClose = () => {
        setSelected(undefined);
        setShow(false);
    };
    const handleShow = () => {
        setShow(true);
        setError("");
    };

    async function addUserAsAdmin(userId: number) {
        try {
            const added = await addAdmin(userId);
            if (added) {
                props.refresh();
                handleClose();
            } else {
                setError("Something went wrong. Failed to add admin");
            }
        } catch (error) {
            setError("Something went wrong. Failed to add admin");
        }
    }

    return (
        <>
            <AddAdminButton variant="primary" onClick={handleShow}>
                Add admin
            </AddAdminButton>

            <Modal show={show} onHide={handleClose}>
                <ModalContentConfirm>
                    <Modal.Header closeButton>
                        <Modal.Title>Add Admin</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Typeahead
                            onChange={selected => {
                                setSelected(selected[0] as User);
                            }}
                            id="non-admin-users"
                            options={props.users}
                            labelKey="name"
                            emptyLabel="No users found."
                            placeholder={"name"}
                        />
                        <AddWarning name={selected?.name} />
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                if (selected !== undefined) {
                                    addUserAsAdmin(selected.userId);
                                }
                            }}
                            disabled={selected === undefined}
                        >
                            Add {selected?.name} as admin
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                        <Error> {error} </Error>
                    </Modal.Footer>
                </ModalContentConfirm>
            </Modal>
        </>
    );
}
