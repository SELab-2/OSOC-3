import { getUsersNonAdmin, User } from "../../utils/api/users/users";
import { createRef, useEffect, useState } from "react";
import { addAdmin } from "../../utils/api/users/admins";
import { AddButtonDiv, EmailDiv, Warning } from "./styles";
import { Button, Modal, Spinner } from "react-bootstrap";
import { AsyncTypeahead, Menu } from "react-bootstrap-typeahead";
import { Error, StyledMenuItem } from "../Common/Users/styles";
import UserMenuItem from "../Common/Users/MenuItem";
import { EmailAndAuth } from "../Common/Users";
import CreateButton from "../Common/Buttons/CreateButton";
import { ModalContentConfirm } from "../Common/styles";
import Typeahead from "react-bootstrap-typeahead/types/core/Typeahead";

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
    const [clearRef, setClearRef] = useState(false); // The ref must be cleared

    const typeaheadRef = createRef<Typeahead>();

    useEffect(() => {
        // For some obscure reason the ref can only be cleared in here & not somewhere else
        if (clearRef) {
            // This triggers itself, but only once, so it doesn't really matter
            setClearRef(false);
            typeaheadRef.current?.clear();
        }
    }, [clearRef, typeaheadRef]);

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
            setSearchTerm("");
            getData(0, "");
            setSelected(undefined);
            setClearRef(true);
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
                Add admin
            </Button>
        );
    }

    let warning;
    if (selected !== undefined) {
        warning = (
            <Warning>
                Warning: This user will be able to edit/delete all data and manage admin roles.
            </Warning>
        );
    }

    return (
        <>
            <AddButtonDiv>
                <CreateButton showIcon={false} onClick={handleShow}>
                    Add admin
                </CreateButton>
            </AddButtonDiv>

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
                            ref={typeaheadRef}
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
                        {warning}
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
