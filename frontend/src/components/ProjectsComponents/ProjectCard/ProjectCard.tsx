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

import { useState } from "react";

import Modal from "../Modal"

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
                <Modal show={show} handleClose={handleClose} name={name}></Modal>
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
