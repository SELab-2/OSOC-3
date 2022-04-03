import React, { useEffect, useState } from "react";
import {
    AdminsContainer,
    AdminsTable,
    ModalContentGreen,
    ModalContentRed,
    AddAdminButton,
    Warning,
} from "./styles";
import { getUsers, User } from "../../../utils/api/users/users";
import { Button, Modal, Spinner } from "react-bootstrap";
import {
    addAdmin,
    getAdmins,
    removeAdmin,
    removeAdminAndCoach,
} from "../../../utils/api/users/admins";
import { Error, SearchInput, SpinnerContainer } from "../../UsersPage/PendingRequests/styles";
import { Typeahead } from "react-bootstrap-typeahead";

function AdminFilter(props: {
    search: boolean;
    searchTerm: string;
    filter: (key: string) => void;
}) {
    return <SearchInput value={props.searchTerm} onChange={e => props.filter(e.target.value)} />;
}

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

function AddAdmin(props: { users: User[]; refresh: () => void }) {
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
                <ModalContentGreen>
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
                </ModalContentGreen>
            </Modal>
        </>
    );
}

function RemoveAdmin(props: { admin: User; refresh: () => void }) {
    const [show, setShow] = useState(false);
    const [error, setError] = useState("");

    const handleClose = () => setShow(false);
    const handleShow = () => {
        setShow(true);
        setError("");
    };

    async function removeUserAsAdmin(userId: number, removeCoach: boolean) {
        try {
            let removed;
            if (removeCoach) {
                removed = await removeAdminAndCoach(userId);
            } else {
                removed = await removeAdmin(userId);
            }

            if (removed) {
                props.refresh();
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
                <ModalContentRed>
                    <Modal.Header closeButton>
                        <Modal.Title>Remove Admin</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <h4>{props.admin.name}</h4>
                        <p>{props.admin.email}</p>
                        <p>
                            Remove admin: {props.admin.name} will stay coach for assigned editions
                        </p>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeUserAsAdmin(props.admin.userId, false);
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
                                removeUserAsAdmin(props.admin.userId, true);
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
                </ModalContentRed>
            </Modal>
        </>
    );
}

function AdminItem(props: { admin: User; refresh: () => void }) {
    return (
        <tr>
            <td>{props.admin.name}</td>
            <td>{props.admin.email}</td>
            <td>
                <RemoveAdmin admin={props.admin} refresh={props.refresh} />
            </td>
        </tr>
    );
}

function AdminsList(props: {
    admins: User[];
    loading: boolean;
    gotData: boolean;
    refresh: () => void;
}) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.admins.length === 0) {
        if (props.gotData) {
            return <div>No admins</div>;
        } else {
            return null;
        }
    }

    const body = (
        <tbody>
            {props.admins.map(admin => (
                <AdminItem key={admin.userId} admin={admin} refresh={props.refresh} />
            ))}
        </tbody>
    );

    return (
        <AdminsTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Remove</th>
                </tr>
            </thead>
            {body}
        </AdminsTable>
    );
}

export default function Admins() {
    const [allAdmins, setAllAdmins] = useState<User[]>([]);
    const [admins, setAdmins] = useState<User[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [gettingData, setGettingData] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");

    async function getData() {
        setGettingData(true);
        setGotData(false);
        try {
            const response = await getAdmins();
            setAllAdmins(response.users);
            setAdmins(response.users);

            const usersResponse = await getUsers();
            const users = [];
            for (const user of usersResponse.users) {
                if (!response.users.some(e => e.userId === user.userId)) {
                    users.push(user);
                }
            }
            setUsers(users);

            setGotData(true);
            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingData && !error) {
            getData();
        }
    }, [gotData, gettingData, error, getData]);

    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const admin of allAdmins) {
            if (admin.name.toUpperCase().includes(word.toUpperCase())) {
                newCoaches.push(admin);
            }
        }
        setAdmins(newCoaches);
    };

    return (
        <AdminsContainer>
            <AdminFilter
                search={allAdmins.length > 0}
                searchTerm={searchTerm}
                filter={word => filter(word)}
            />
            <AddAdmin users={users} refresh={getData} />
            <AdminsList admins={admins} loading={gettingData} gotData={gotData} refresh={getData} />
            <Error> {error} </Error>
        </AdminsContainer>
    );
}
