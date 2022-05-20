import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    CoachText,
    NumberOfStudents,
    TitleContainer,
    Title,
    OpenIcon,
    ClientContainer,
    Client,
    Clients,
} from "./styles";

import { BsPersonFill } from "react-icons/bs";

import { useState } from "react";

import ConfirmDelete from "../ConfirmDelete";
import { deleteProject } from "../../../utils/api/projects";
import { useNavigate, useParams } from "react-router-dom";

import { Project } from "../../../data/interfaces";
import { useAuth } from "../../../contexts";
import { Role } from "../../../data/enums";
import { DeleteButton } from "../../Common/Buttons";

/**
 *
 * @param project a Project object
 * @param refreshProjects what to do when a project is deleted.
 * @returns a project card which is a small overview of a project.
 */
export default function ProjectCard({
    project,
    removeProject,
}: {
    project: Project;
    removeProject: (project: Project) => void;
}) {
    // Used for the confirm screen.
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();
    const params = useParams();
    const editionId = params.editionId!;

    // What to do when deleting a project.
    async function handleDelete() {
        const success = await deleteProject(editionId, project.projectId);
        setShow(false);
        if (!success) {
            alert("Failed to delete the project");
        } else {
            removeProject(project);
        }
    }

    const { role } = useAuth();

    return (
        <CardContainer>
            <TitleContainer>
                <Title
                    onClick={() =>
                        navigate("/editions/" + editionId + "/projects/" + project.projectId)
                    }
                >
                    {project.name}
                    <OpenIcon />
                </Title>

                {role === Role.ADMIN && <DeleteButton onClick={handleShow} />}

                <ConfirmDelete
                    visible={show}
                    handleConfirm={handleDelete}
                    handleClose={handleClose}
                    name={project.name}
                />
            </TitleContainer>

            <ClientContainer>
                <Clients>
                    {project.partners.map((partner, _index) => (
                        <Client key={_index}>{partner.name}</Client>
                    ))}
                </Clients>
                <NumberOfStudents>
                    {project.numberOfStudents}
                    <BsPersonFill />
                </NumberOfStudents>
            </ClientContainer>

            <CoachesContainer>
                {project.coaches.map((coach, _index) => (
                    <CoachContainer key={_index}>
                        <CoachText>{coach.name}</CoachText>
                    </CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
