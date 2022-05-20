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
import { toast } from "react-toastify";

/**
 *
 * @param project a Project object
 * @param removeProject what to do when a project is deleted.
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

    const params = useParams();
    const editionId = params.editionId!;
    const { role } = useAuth();

    const navigate = useNavigate();

    let assignedStudents = 0;
    let neededStudents = 0;
    project.projectRoles.forEach(projectRole => {
        neededStudents += projectRole.slots;
        assignedStudents += projectRole.suggestions.length;
    });

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
                    {assignedStudents + " / " + neededStudents}
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
