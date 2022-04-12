import { getUsersExcludeEdition, User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import { addCoachToEdition } from "../../../../utils/api/users/coaches";
import { Button, Modal, Spinner } from "react-bootstrap";
import { AsyncTypeahead } from "react-bootstrap-typeahead";
import { Error } from "../../PendingRequests/styles";
import { AddAdminButton, ModalContentConfirm } from "../../../AdminsComponents/styles";

/**
 * A button and popup to add a new coach to the given edition.
 * The popup consists of a field to search for a user.
 * @param props.edition The edition to which users need to be added.
 * @param props.coachAdded A function which will be called when a user is added as coach.
 */
export default function AddCoach(props: { edition: string; coachAdded: (user: User) => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [gettingData, setGettingData] = useState(false); // Waiting for data
    const [users, setUsers] = useState<User[]>([]); // All users which are not a coach
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter

    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingData(true);
        setError("");
        try {
            const response = await getUsersExcludeEdition(props.edition, filter, page);
            if (page === 0) {
                setUsers(response.users);
            } else {
                setUsers(users.concat(response.users));
            }

            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    function filterData(searchTerm: string) {
        setSearchTerm(searchTerm);
        setUsers([]);
        getData(0, searchTerm);
    }

    const handleClose = () => {
        setSelected(undefined);
        setError("");
        setShow(false);
    };
    const handleShow = () => {
        setShow(true);
    };

    async function addCoach(user: User) {
        setLoading(true);
        setError("");
        let success = false;
        try {
            success = await addCoachToEdition(user.userId, props.edition);
            if (!success) {
                setError("Something went wrong. Failed to add coach");
            }
        } catch (error) {
            setError("Something went wrong. Failed to add coach");
        }
        setLoading(false);
        if (success) {
            props.coachAdded(user);
            handleClose();
        }
    }

    let addButton;
    if (loading) {
        addButton = <Spinner animation="border" />;
    } else {
        addButton = (
            <Button
                variant="primary"
                onClick={() => {
                    if (selected !== undefined) {
                        addCoach(selected);
                    }
                }}
                disabled={selected === undefined}
            >
                Add {selected?.name} as coach
            </Button>
        );
    }

    return (
        <>
            <AddAdminButton variant="primary" onClick={handleShow}>
                Add coach
            </AddAdminButton>

            <Modal show={show} onHide={handleClose}>
                <ModalContentConfirm>
                    <Modal.Header closeButton>
                        <Modal.Title>Add Coach</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <AsyncTypeahead
                            filterBy={["name"]}
                            id="non-coach-users"
                            isLoading={gettingData}
                            labelKey="name"
                            minLength={1}
                            onSearch={filterData}
                            options={users}
                            placeholder={"user's name"}
                            onChange={selected => {
                                setSelected(selected[0] as User);
                                setError("");
                            }}
                        />
                    </Modal.Body>
                    <Modal.Footer>
                        {addButton}
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
