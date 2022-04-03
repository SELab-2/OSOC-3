import React, { useEffect, useState } from "react";
import { CoachesTitle, CoachesContainer, CoachesTable, ModalContent } from "./styles";
import { getUsers, User } from "../../../utils/api/users/users";
import { Error, SearchInput, SpinnerContainer } from "../PendingRequests/styles";
import { Button, Modal, Spinner } from "react-bootstrap";
import {
    getCoaches,
    removeCoachFromAllEditions,
    removeCoachFromEdition,
    addCoachToEdition,
} from "../../../utils/api/users/coaches";
import { AddAdminButton, ModalContentGreen } from "../../AdminsPage/Admins/styles";
import { Typeahead } from "react-bootstrap-typeahead";

function CoachesHeader() {
    return <CoachesTitle>Coaches</CoachesTitle>;
}

function CoachFilter(props: {
    search: boolean;
    searchTerm: string;
    filter: (key: string) => void;
}) {
    return <SearchInput value={props.searchTerm} onChange={e => props.filter(e.target.value)} />;
}

function AddCoach(props: { users: User[]; edition: string }) {
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
                            options={props.users}
                            labelKey="email"
                            filterBy={["email", "name"]}
                            emptyLabel="No users found."
                            placeholder={"user's email address"}
                        />
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                if (selected !== undefined) {
                                    addCoachToEdition(selected.id, props.edition);
                                }
                                handleClose();
                            }}
                            disabled={selected === undefined}
                        >
                            Add {selected?.name} as coach
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

function RemoveCoach(props: { coach: User; edition: string }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Button variant="primary" size="sm" onClick={handleShow}>
                Remove
            </Button>

            <Modal show={show} onHide={handleClose}>
                <ModalContent>
                    <Modal.Header closeButton>
                        <Modal.Title>Remove Coach</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <h4>{props.coach.name}</h4>
                        {props.coach.email}
                    </Modal.Body>
                    <Modal.Footer>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeCoachFromAllEditions(props.coach.id);
                                handleClose();
                            }}
                        >
                            Remove from all editions
                        </Button>
                        <Button
                            variant="primary"
                            onClick={() => {
                                removeCoachFromEdition(props.coach.id, props.edition);
                                handleClose();
                            }}
                        >
                            Remove from {props.edition}
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContent>
            </Modal>
        </>
    );
}

function CoachItem(props: { coach: User; edition: string }) {
    return (
        <tr>
            <td>{props.coach.name}</td>
            <td>{props.coach.email}</td>
            <td>
                <RemoveCoach coach={props.coach} edition={props.edition} />
            </td>
        </tr>
    );
}

function CoachesList(props: {
    coaches: User[];
    loading: boolean;
    edition: string;
    gotData: boolean;
}) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.coaches.length === 0) {
        if (props.gotData) {
            return <div>No coaches for this edition</div>;
        } else {
            return null;
        }
    }

    const body = (
        <tbody>
            {props.coaches.map(coach => (
                <CoachItem key={coach.id} coach={coach} edition={props.edition} />
            ))}
        </tbody>
    );

    return (
        <CoachesTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Remove from edition</th>
                </tr>
            </thead>
            {body}
        </CoachesTable>
    );
}

export default function Coaches(props: { edition: string }) {
    const [allCoaches, setAllCoaches] = useState<User[]>([]);
    const [coaches, setCoaches] = useState<User[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [gettingData, setGettingData] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");

    async function getData() {
        try {
            const coachResponse = await getCoaches(props.edition);
            setAllCoaches(coachResponse.coaches);
            setCoaches(coachResponse.coaches);

            const UsersResponse = await getUsers();
            const users = [];
            for (const user of UsersResponse.users) {
                if (!allCoaches.some(e => e.id === user.id)) {
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
            setGettingData(true);
            getData();
        }
    });

    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const coach of allCoaches) {
            if (
                coach.name.toUpperCase().includes(word.toUpperCase()) ||
                coach.email.toUpperCase().includes(word.toUpperCase())
            ) {
                newCoaches.push(coach);
            }
        }
        setCoaches(newCoaches);
    };

    return (
        <CoachesContainer>
            <CoachesHeader />
            <CoachFilter
                search={coaches.length > 0}
                searchTerm={searchTerm}
                filter={word => filter(word)}
            />
            <AddCoach users={users} edition={props.edition} />
            <CoachesList
                coaches={coaches}
                loading={gettingData}
                edition={props.edition}
                gotData={gotData}
            />
            <Error> {error} </Error>
        </CoachesContainer>
    );
}
