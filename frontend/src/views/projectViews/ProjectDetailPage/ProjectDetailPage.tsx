import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { DragDropContext, DropResult } from "react-beautiful-dnd";
import {
    Project,
    CreateProject as EditProject,
    AddStudentRole,
} from "../../../data/interfaces/projects";
import projectToEditProject from "../../../utils/logic/project";
import { deleteProject, getProject, patchProject } from "../../../utils/api/projects";
import { useAuth } from "../../../contexts";
import { BiArrowBack } from "react-icons/bi";
import { BsPersonFill } from "react-icons/bs";
import {
    GoBack,
    ProjectContainer,
    ClientsContainer,
    NumberOfStudents,
    ProjectPageContainer,
    MoreInfoLink,
} from "./styles";
import ConfirmDelete from "../../../components/ProjectsComponents/ConfirmDelete";
import {
    TitleAndEdit,
    ProjectRoles,
    ProjectCoaches,
    ProjectPartners,
    AddStudentModal,
} from "../../../components/ProjectDetailComponents";
import { addStudentToProject, deleteStudentFromProject } from "../../../utils/api/projectStudents";
import { toast } from "react-toastify";
import { StudentListFilters } from "../../../components/StudentsComponents";
import { CreateButton } from "../../../components/Common/Buttons";
import { useSockets } from "../../../contexts";
import { EventType, RequestMethod, WebSocketEvent } from "../../../data/interfaces/websockets";


// Types of events accepted by this websocket
const wsEventTypes = [EventType.PROJECT, EventType.PROJECT_ROLE, EventType.PROJECT_ROLE_SUGGESTION];

/**
 * @returns the detailed page of a project. Here you can add or remove students from the project.
 */
export default function ProjectDetailPage() {
    const { socket } = useSockets();

    const params = useParams();
    const projectId = parseInt(params.projectId!);
    const editionId = params.editionId!;

    const [project, setProject] = useState<Project>();
    const [editedProject, setEditedProject] = useState<Project>();
    const [gotProject, setGotProject] = useState(false);
    const [editing, setEditing] = useState(false);
    const [studentAmount, setStudentAmount] = useState(0);
    const [assignedAmount, setAssignedAmount] = useState(0);

    const navigate = useNavigate();
    const { role } = useAuth();

    // WebSocket listener
    useEffect(() => {
        function listener(event: MessageEvent) {
            const data = JSON.parse(event.data) as WebSocketEvent;

            // Ignore events that aren't targeted towards projects
            if (!wsEventTypes.includes(data.eventType)) return;

            const idString = projectId.toString();

            // Ignore events targeted towards other projects
            if (data.pathIds.projectId !== idString) return;

            // This project was deleted
            if (data.method === RequestMethod.DELETE) {
                if (data.eventType === EventType.PROJECT) {
                    toast.info("This project was deleted by an admin.");
                    navigate(`/editions/${editionId}/projects`);
                    return;
                }
            }

            // Project was edited in some way (either a PATCH or adding/deleting suggestions)
            // By setting this one to False we force the other useEffect
            // to fetch the project again
            setGotProject(false);
        }

        socket?.addEventListener("message", listener);

        function removeListener() {
            if (socket) {
                socket.removeEventListener("message", listener);
            }
        }

        return removeListener;
    }, [socket, editionId, projectId, navigate]);

    // Get project details
    useEffect(() => {
        async function callProjects(): Promise<void> {
            if (projectId) {
                setGotProject(true);
                const response = await getProject(editionId, projectId);
                if (response) {
                    setProject(response);
                    setEditedProject(response);
                    let countStudents = 0;
                    let countAssigned = 0;
                    response.projectRoles.forEach(projectRole => {
                        countStudents += projectRole.slots;
                        countAssigned += projectRole.suggestions.length;
                    });
                    setStudentAmount(countStudents);
                    setAssignedAmount(countAssigned);
                } else navigate("/404-not-found");
            }
        }
        if (!gotProject) {
            callProjects();
        }

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [editionId, gotProject, projectId]);

    // Used for the delete modal.
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const handleDeleteClose = () => setShowDeleteModal(false);
    const handleDeleteShow = () => setShowDeleteModal(true);
    const handleDelete = () => {
        // What to do when deleting a project.
        toast.promise(
            deleteProject(editionId, project!.projectId),
            {
                pending: "Deleting project",
                success: "Successfully deleted project",
                error: "Something went wrong",
            },
            { toastId: "deleteProject" }
        );
        setShowDeleteModal(false);
        navigate("/editions/" + editionId + "/projects/");
    };

    // Used for the Add modal.
    const [showAddModal, setShowAddModal] = useState(false);
    const [resultModal, setResult] = useState<AddStudentRole>();
    const handleAddClose = () => setShowAddModal(false);
    const handleAddShow = (
        projectRoleId: string,
        studentId: string,
        switchProjectRoleId: string | undefined
    ) => {
        setResult({
            projectRoleId: projectRoleId,
            studentId: studentId,
            switchProjectRoleId: switchProjectRoleId,
        });
        setShowAddModal(true);
    };

    const handleAdd = async (motivation: string, addStudent: AddStudentRole) => {
        setShowAddModal(false);
        if (addStudent.switchProjectRoleId) {
            await deleteStudentFromProject(
                editionId,
                projectId.toString(),
                addStudent.switchProjectRoleId,
                addStudent.studentId
            );
        }
        await toast.promise(
            addStudentToProject(
                editionId,
                projectId.toString(),
                addStudent.projectRoleId,
                addStudent.studentId,
                motivation
            ),
            {
                pending: "Adding student",
                success: "Successfully added student",
                error: "Something went wrong",
            },
            { toastId: "addStudentToProject" }
        );
        setGotProject(false);
    };

    async function editProject() {
        const newProject: EditProject = projectToEditProject(editedProject!);
        if (newProject.name === "") {
            toast.error("Project name must be filled in", {
                toastId: "createProjectNoName",
            });
            return;
        }
        await toast.promise(
            patchProject(
                editionId,
                projectId,
                newProject!.name,
                newProject.info_url || null,
                newProject!.partners,
                newProject!.coaches
            ),
            {
                pending: "Updating project",
                success: "Successfully updated project",
                error: "Something went wrong",
            },
            { toastId: "UpdateProject" }
        );
        setGotProject(false);
    }

    if (!project || !editedProject) return null;
    return (
        <DragDropContext onDragEnd={result => onDragDrop(result)}>
            <ProjectPageContainer>
                <StudentListFilters />

                <ProjectContainer>
                    <GoBack onClick={() => navigate("/editions/" + editionId + "/projects/")}>
                        <BiArrowBack />
                        Overview
                    </GoBack>

                    <TitleAndEdit
                        editing={editing}
                        project={project}
                        editedProject={editedProject}
                        setEditedProject={setEditedProject}
                        setEditing={setEditing}
                        editProject={editProject}
                        role={role!}
                        handleShow={handleDeleteShow}
                    />

                    <ConfirmDelete
                        visible={showDeleteModal}
                        handleConfirm={handleDelete}
                        handleClose={handleDeleteClose}
                        name={project.name}
                    ></ConfirmDelete>

                    <ClientsContainer>
                        <ProjectPartners
                            project={project}
                            editedProject={editedProject}
                            setEditedProject={setEditedProject}
                            editing={editing}
                        />
                        <NumberOfStudents>
                            {assignedAmount + " / " + studentAmount}
                            <BsPersonFill />
                        </NumberOfStudents>
                    </ClientsContainer>

                    <ProjectCoaches
                        project={project}
                        editedProject={editedProject}
                        setEditedProject={setEditedProject}
                        editing={editing}
                    />

                    {project.infoUrl !== null && (
                        <MoreInfoLink>
                            <CreateButton
                                showIcon={false}
                                label="More info about this project"
                                onClick={() => window.open(project.infoUrl!)}
                            />
                        </MoreInfoLink>
                    )}

                    <ProjectRoles
                        projectRoles={project.projectRoles}
                        setGotProject={setGotProject}
                    />
                    <AddStudentModal
                        visible={showAddModal}
                        handleConfirm={handleAdd}
                        handleClose={handleAddClose}
                        result={resultModal!}
                    />
                </ProjectContainer>
            </ProjectPageContainer>
        </DragDropContext>
    );

    async function onDragDrop(result: DropResult) {
        const { source, destination, draggableId } = result;
        if (destination) {
            if (source.droppableId === "students") {
                handleAddShow(destination.droppableId, draggableId, undefined);
            } else if (source.droppableId !== destination.droppableId) {
                handleAddShow(
                    destination.droppableId,
                    draggableId.substring(0, draggableId.length - source.droppableId.length),
                    source.droppableId
                );
            }
        }
    }
}
