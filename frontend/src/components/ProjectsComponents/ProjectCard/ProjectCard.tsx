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

import ConfirmDelete from "../ConfirmDelete";
import { deleteProject } from "../../../utils/api/projects";

interface Coach {
    name: string;
}

export default function ProjectCard({
    name,
    client,
    numberOfStudents,
    coaches,
    edition,
    projectId,
    refreshEditions,
}: {
    name: string;
    client: string;
    numberOfStudents: number;
    coaches: Coach[];
    edition: string;
    projectId: number;
    refreshEditions: () => void;
}) {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleDelete = () => {
        deleteProject(edition, projectId);
        setShow(false);
        refreshEditions();
    };
    const handleShow = () => setShow(true);

    return (
        <CardContainer>
            <TitleContainer>
                <Title>{name}</Title>

                <Delete onClick={handleShow}>
                    <TiDeleteOutline size={"20px"} />
                </Delete>

                <ConfirmDelete
                    visible={show}
                    handleConfirm={handleDelete}
                    handleClose={handleClose}
                    name={name}
                ></ConfirmDelete>
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
                        <CoachText>{element.name}</CoachText>
                    </CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
