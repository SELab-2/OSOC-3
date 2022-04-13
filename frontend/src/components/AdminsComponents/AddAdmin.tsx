import { getUsersNonAdmin, User } from "../../utils/api/users/users";
import React, { useState } from "react";
import { addAdmin } from "../../utils/api/users/admins";
import { AddAdminButton, ModalContentConfirm, Warning } from "./styles";
import { Button, Modal, Spinner } from "react-bootstrap";
import { AsyncTypeahead, Menu } from "react-bootstrap-typeahead";
import { Error } from "../UsersComponents/Requests/styles";
import { StyledMenuItem } from "../GeneralComponents/styles";
import UserMenuItem from "../GeneralComponents/MenuItem";
import { EmailAndAuth } from "../GeneralComponents";

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
export default function AddAdmin(props: { adminAdded: (user: User) => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
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
            const response = await getUsersNonAdmin(filter, page);
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

    async function addUserAsAdmin(user: User) {
        setLoading(true);
        setError("");
        let success = false;
        try {
            success = await addAdmin(user.userId);
            if (!success) {
                setError("Something went wrong. Failed to add admin");
            }
        } catch (error) {
            setError("Something went wrong. Failed to add admin");
        }
        setLoading(false);
        if (success) {
            props.adminAdded(user);
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
                        addUserAsAdmin(selected);
                    }
                }}
                disabled={selected === undefined}
            >
                Add {selected?.name} as admin
            </Button>
        );
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
                        <AsyncTypeahead
                            filterBy={["name"]}
                            id="non-admin-users"
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
                        <EmailAndAuth user={selected} />
                        <AddWarning name={selected?.name} />
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
