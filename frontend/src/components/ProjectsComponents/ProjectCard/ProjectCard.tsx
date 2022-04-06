import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    CoachText,
    NumberOfStudents,
    Delete,
    TitleContainer,
    Title,
    ClientContainer,
    Client,
} from "./styles";

import { BsPersonFill } from "react-icons/bs";
import { TiDeleteOutline } from "react-icons/ti";

import { Modal, Button } from "react-bootstrap";
import { useState } from "react";

export default function ProjectCard({
    name,
    client,
    numberOfStudents,
    coaches,
}: {
    name: string;
    client: string;
    numberOfStudents: number;
    coaches: string[];
}) {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <CardContainer>
            <TitleContainer>
                <Title>{name}</Title>
                <Delete onClick={handleShow}>
                    <TiDeleteOutline size={"20px"} />
                </Delete>

                <>
                    <Modal show={show} onHide={handleClose}>
                        <Modal.Header closeButton>
                            <Modal.Title>Confirm delete</Modal.Title>
                        </Modal.Header>

                        <Modal.Body>Are you sure you want to delete {name}?</Modal.Body>

                        <Modal.Footer>
                            <Button variant={"secondary"} onClick={handleClose}>
                                Close
                            </Button>
                            <Button variant={"primary"} onClick={handleClose}>
                                Submit
                            </Button>
                        </Modal.Footer>
                    </Modal>
                </>
            </TitleContainer>
            <ClientContainer>
                <Client>{client}</Client>
                <NumberOfStudents>
                    {numberOfStudents}
                    <BsPersonFill />
                </NumberOfStudents>
            </ClientContainer>

            <CoachesContainer>
                {coaches.map((element, _index) => (
                    <CoachContainer key={_index}>
                        <CoachText>{element}</CoachText>
                    </CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
