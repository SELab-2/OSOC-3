import React, { useEffect, useState } from "react";
import { CoachesTitle, CoachesContainer, CoachesTable, ModalContent } from "./styles";
import { User } from "../../../utils/api/users/users";
import { SearchInput, SpinnerContainer } from "../PendingRequests/styles";
import { Button, Modal, Spinner } from "react-bootstrap";
import {
    getCoaches,
    removeCoachFromAllEditions,
    removeCoachFromEdition,
} from "../../../utils/api/users/coaches";

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

function RemoveCoach(props: { coach: User; edition: string }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
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

function CoachesList(props: { coaches: User[]; loading: boolean; edition: string }) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.coaches.length === 0) {
        return <div>No coaches for this edition</div>;
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
    const [gettingCoaches, setGettingCoaches] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);

    useEffect(() => {
        if (!gotData) {
            getCoaches(props.edition)
                .then(response => {
                    setCoaches(response.coaches);
                    setAllCoaches(response.coaches);
                    setGettingCoaches(false);
                    setGotData(true);
                })
                .catch(function (error: any) {
                    console.log(error);
                    setGettingCoaches(false);
                });
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
            <CoachesList coaches={coaches} loading={gettingCoaches} edition={props.edition} />
        </CoachesContainer>
    );
}
