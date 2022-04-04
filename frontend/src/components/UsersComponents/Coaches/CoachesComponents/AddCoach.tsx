import { User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import { addCoachToEdition } from "../../../../utils/api/users/coaches";
import { AddAdminButton, ModalContentGreen } from "../../../../views/AdminsPage/Admins/styles";
import { Button, Modal } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import { Error } from "../../PendingRequests/styles";

/**
 * A button and popup to add a new coach to the given edition.
 * The popup consists of a field to search for a user.
 * @param props.users A list of all users which can be added as coach to the edition.
 * @param props.edition The edition to which users need to be added.
 * @param props.refresh A function which will be called when a user is added as coach.
 */
export default function AddCoach(props: { users: User[]; edition: string; refresh: () => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
    const [error, setError] = useState("");

    const handleClose = () => {
        setSelected(undefined);
        setShow(false);
    };
    const handleShow = () => setShow(true);

    async function addCoach(userId: number) {
        try {
            const added = await addCoachToEdition(userId, props.edition);
            if (added) {
                props.refresh();
                handleClose();
            } else {
                setError("Something went wrong. Failed to add coach");
            }
        } catch (error) {
            setError("Something went wrong. Failed to add coach");
        }
    }

    return (
        <>
            <AddAdminButton variant="primary" onClick={handleShow}>
                Add coach
            </AddAdminButton>

            <Modal show={show} onHide={handleClose}>
                <ModalContentGreen>
                    <Modal.Header closeButton>
                        <Modal.Title>Add Coach</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Typeahead
                            onChange={selected => {
                                setSelected(selected[0] as User);
                            }}
                            id="non-coach-users"
                            options={props.users}
                            labelKey="name"
                            filterBy={["name"]}
                            emptyLabel="No users found."
                            placeholder={"user's name"}
                        />
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                if (selected !== undefined) {
                                    addCoach(selected.userId);
                                }
                            }}
                            disabled={selected === undefined}
                        >
                            Add {selected?.name} as coach
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                        <Error> {error} </Error>
                    </Modal.Footer>
                </ModalContentGreen>
            </Modal>
        </>
    );
}
