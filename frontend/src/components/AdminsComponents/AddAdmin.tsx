import { getUsersNonAdmin, User } from "../../utils/api/users/users";
import { createRef, useEffect, useState } from "react";
import { addAdmin } from "../../utils/api/users/admins";
import { AddButtonDiv, EmailDiv, Warning } from "./styles";
import { Button, Modal } from "react-bootstrap";
import { AsyncTypeahead, Menu } from "react-bootstrap-typeahead";
import { StyledMenuItem } from "../Common/Users/styles";
import UserMenuItem from "../Common/Users/MenuItem";
import { EmailAndAuth } from "../Common/Users";
import CreateButton from "../Common/Buttons/CreateButton";
import { ModalContentConfirm } from "../Common/styles";
import Typeahead from "react-bootstrap-typeahead/types/core/Typeahead";
import { toast } from "react-toastify";
import { StyledInput } from "../Common/Forms/styles";

/**
 * Button and popup to add an existing user as admin.
 * @param props.users All users which can be added as admin.
 * @param props.refresh A function which is called when a new admin is added.
 */
export default function AddAdmin(props: { adminAdded: (user: User) => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
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
        const response = await toast.promise(getUsersNonAdmin(filter, page), {
            error: "Failed to retrieve users",
        });
        if (page === 0) {
            setUsers(response.users);
        } else {
            setUsers(users.concat(response.users));
        }

        setGettingData(false);
    }

    function filterData(searchTerm: string) {
        setSearchTerm(searchTerm);
        setUsers([]);
        getData(0, searchTerm);
    }

    const handleClose = () => {
        setSelected(undefined);
        setShow(false);
    };
    const handleShow = () => {
        setShow(true);
    };

    async function addUserAsAdmin(user: User) {
        await toast.promise(addAdmin(user.userId), {
            pending: "Adding admin",
            success: "Admin successfully added",
            error: "Failed to add admin",
        });

        props.adminAdded(user);
        setSearchTerm("");
        setSelected(undefined);
        setClearRef(true);
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
                            placeholder={"Username"}
                            onChange={selected => {
                                setSelected(selected[0] as User);
                            }}
                            renderInput={({ inputRef, referenceElementRef, ...inputProps }) => (
                                <StyledInput
                                    {...inputProps}
                                    ref={input => {
                                        inputRef(input);
                                        referenceElementRef(input);
                                    }}
                                />
                            )}
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
                        <CreateButton
                            showIcon={false}
                            onClick={() => {
                                if (selected !== undefined) {
                                    addUserAsAdmin(selected);
                                }
                            }}
                            disabled={selected === undefined}
                        >
                            Add admin
                        </CreateButton>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContentConfirm>
            </Modal>
        </>
    );
}
