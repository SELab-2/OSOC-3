import { getUsersExcludeEdition, User } from "../../../../utils/api/users/users";
import React, { useState } from "react";
import { addCoachToEdition } from "../../../../utils/api/users/coaches";
import { Button, Modal, Spinner } from "react-bootstrap";
import { AddButtonDiv } from "../../../AdminsComponents/styles";
import { AsyncTypeahead, Menu } from "react-bootstrap-typeahead";
import UserMenuItem from "../../../Common/Users/MenuItem";
import { Error, StyledMenuItem } from "../../../Common/Users/styles";
import { EmailAndAuth } from "../../../Common/Users";
import { EmailDiv } from "../styles";
import CreateButton from "../../../Common/Buttons/CreateButton";
import { ModalContentConfirm } from "../../../Common/styles";

/**
 * A button and popup to add a new coach to the given edition.
 * The popup consists of a field to search for a user.
 * @param props.edition The edition to which users need to be added.
 * @param props.coachAdded A function which will be called when a user is added as coach.
 */
export default function AddCoach(props: { edition: string; refreshCoaches: () => void }) {
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
            props.refreshCoaches();
            handleClose();
        }
    }

    let addButton;
    if (loading) {
        addButton = <Spinner animation="border" />;
    } else {
        addButton = (
            <CreateButton
                showIcon={false}
                onClick={() => {
                    if (selected !== undefined) {
                        addCoach(selected);
                    }
                }}
                disabled={selected === undefined}
            >
                Add coach
            </CreateButton>
        );
    }

    return (
        <>
            <AddButtonDiv>
                <CreateButton showIcon={false} onClick={handleShow}>
                    Add coach
                </CreateButton>
            </AddButtonDiv>

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
                            renderMenu={(results, menuProps) => {
                                const {
                                    newSelectionPrefix,
                                    paginationText,
                                    renderMenuItemChildren,
                                    ...props
                                } = menuProps;
                                return (
                                    <Menu {...props}>
                                        {results.map((result, index) => {
                                            const user = result as User;
                                            return (
                                                <StyledMenuItem
                                                    option={result}
                                                    position={index}
                                                    key={user.userId}
                                                >
                                                    <UserMenuItem user={user} />
                                                    <br />
                                                </StyledMenuItem>
                                            );
                                        })}
                                    </Menu>
                                );
                            }}
                        />
                        <EmailDiv>
                            <EmailAndAuth user={selected} />
                        </EmailDiv>
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
