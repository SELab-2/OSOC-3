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
import { SearchInput, SpinnerContainer } from "../../UsersPage/PendingRequests/styles";
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

function AddAdmin(props: { users: User[] }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);

    const handleClose = () => {
        setSelected(undefined);
        setShow(false);
    };
    const handleShow = () => setShow(true);

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
                            options={props.users}
                            labelKey="email"
                            filterBy={["email", "name"]}
                            emptyLabel="No users found."
                            placeholder={"email"}
                        />
                        <AddWarning name={selected?.name} />
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                if (selected !== undefined) {
                                    addAdmin(selected.id);
                                }
                                handleClose();
                            }}
                            disabled={selected === undefined}
                        >
                            Add {selected?.name} as admin
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContentGreen>
            </Modal>
        </>
    );
}

function RemoveAdmin(props: { admin: User }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
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
                                removeAdmin(props.admin.id);
                                handleClose();
                            }}
                        >
                            Remove admin
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeAdminAndCoach(props.admin.id);
                                handleClose();
                            }}
                        >
                            Remove as admin and coach
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContentRed>
            </Modal>
        </>
    );
}

function AdminItem(props: { admin: User }) {
    return (
        <tr>
            <td>{props.admin.name}</td>
            <td>{props.admin.email}</td>
            <td>
                <RemoveAdmin admin={props.admin} />
            </td>
        </tr>
    );
}

function AdminsList(props: { admins: User[]; loading: boolean }) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.admins.length === 0) {
        return <div>No admins? #rip</div>;
    }

    const body = (
        <tbody>
            {props.admins.map(admin => (
                <AdminItem key={admin.id} admin={admin} />
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
    const [gettingAdmins, setGettingAdmins] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);

    useEffect(() => {
        if (!gotData) {
            getAdmins()
                .then(response => {
                    setAdmins(response.admins);
                    setAllAdmins(response.admins);
                    setGettingAdmins(false);
                    setGotData(true);
                })
                .catch(function (error: any) {
                    console.log(error);
                    setGettingAdmins(false);
                });
            getUsers()
                .then(response => {
                    const users = [];
                    for (const user of response.users) {
                        if (!allAdmins.some(e => e.id === user.id)) {
                            users.push(user);
                        }
                    }
                    setUsers(users);
                })
                .catch(function (error: any) {
                    console.log(error);
                });
        }
    });

    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const admin of allAdmins) {
            if (
                admin.name.toUpperCase().includes(word.toUpperCase()) ||
                admin.email.toUpperCase().includes(word.toUpperCase())
            ) {
                newCoaches.push(admin);
            }
        }
        setAdmins(newCoaches);
    };

    return (
        <AdminsContainer>
            <AdminFilter
                search={admins.length > 0}
                searchTerm={searchTerm}
                filter={word => filter(word)}
            />
            <AddAdmin users={users} />
            <AdminsList admins={admins} loading={gettingAdmins} />
        </AdminsContainer>
    );
}
