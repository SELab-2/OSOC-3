import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    CoachText,
    NumberOfStudents,
    Delete,
    TitleContainer,
    Title,
    OpenIcon,
    ClientContainer,
    Client,
    Clients,
} from "./styles";

import { BsPersonFill } from "react-icons/bs";
import { HiOutlineTrash } from "react-icons/hi";

import { useState } from "react";

import ConfirmDelete from "../ConfirmDelete";
import { deleteProject } from "../../../utils/api/projects";
import { useNavigate, useParams } from "react-router-dom";

import { Project } from "../../../data/interfaces";
import { useAuth } from "../../../contexts";
import { Role } from "../../../data/enums";
import { toast } from "react-toastify";

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

    // What to do when deleting a project.
    async function handleDelete() {
        const success = await deleteProject(editionId, project.projectId);
        setShow(false);
        if (!success) {
            toast.error("Could not delete project", { toastId: "deleteProject" });
        } else {
            removeProject(project);
            toast.success("Deleted project", { toastId: "deletedProject" });
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

                {role === Role.ADMIN && (
                    <Delete onClick={handleShow}>
                        <HiOutlineTrash size={"20px"} />
                    </Delete>
                )}

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
                    {
                        // project.numberOfStudents
                    }
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
