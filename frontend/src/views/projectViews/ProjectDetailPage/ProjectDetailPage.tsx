import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { DragDropContext, DropResult } from "react-beautiful-dnd";
import {
    Project,
    CreateProject as EditProject,
    ProjectRole,
} from "../../../data/interfaces/projects";
import projectToEditProject from "../../../utils/logic/project";
import { deleteProject, getProject, patchProject } from "../../../utils/api/projects";
import { getStudent } from "../../../utils/api/students";
import { useAuth } from "../../../contexts/auth-context";
import { BiArrowBack } from "react-icons/bi";
import { BsPersonFill } from "react-icons/bs";
import {
    GoBack,
    ProjectContainer,
    ClientsContainer,
    NumberOfStudents,
    ProjectPageContainer,
} from "./styles";
import ConfirmDelete from "../../../components/ProjectsComponents/ConfirmDelete";
import {
    TitleAndEdit,
    ProjectRoles,
    ProjectCoaches,
    ProjectPartners,
    AddStudentModal,
    StudentList,
} from "../../../components/ProjectDetailComponents";
import { addStudentToProject, deleteStudentFromProject } from "../../../utils/api/projectStudents";
import { toast } from "react-toastify";
/**
 * @returns the detailed page of a project. Here you can add or remove students from the project.
 */

export default function ProjectDetailPage() {
    const params = useParams();
    const projectId = parseInt(params.projectId!);
    const editionId = params.editionId!;
    const [project, setProject] = useState<Project>();
    const [editedProject, setEditedProject] = useState<Project>();
    const [gotProject, setGotProject] = useState(false);
    const navigate = useNavigate();
    const { role } = useAuth(); // const [students, setStudents] = useState<StudentPlace[]>([]);

    const [editing, setEditing] = useState(false);

    const [projectRoles, setProjectRoles] = useState<ProjectRole[]>([]);
    useEffect(() => {
        async function callProjects(): Promise<void> {
            if (projectId) {
                setGotProject(true);
                const response = await getProject(editionId, projectId);

                if (response) {
                    setProject(response);
                    setProjectRoles(response.projectRoles);
                    setEditedProject(response);
                } else navigate("/404-not-found");
            }
        }

        if (!gotProject) {
            callProjects();
        }
    }, [editionId, gotProject, navigate, projectId]);

    // Used for the delete modal.
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const handleDeleteClose = () => setShowDeleteModal(false);
    const handleDeleteShow = () => setShowDeleteModal(true);
    const handleDelete = () => {
        // What to do when deleting a project.
        deleteProject(editionId, project!.projectId);
        setShowDeleteModal(false);
        navigate("/editions/" + editionId + "/projects/");
    };

    // Used for the Add modal.
    const [showAddModal, setShowAddModal] = useState(false);
    const [resultModal, setResult] = useState<DropResult>();
    const handleAddClose = () => setShowAddModal(false);
    const handleAddShow = (result: DropResult) => {
        setShowAddModal(true);
        setResult(result);
    };
    const handleAdd = async (motivation: string, result: DropResult) => {
        setShowAddModal(false);

        const newProjectRole = await toast.promise(
            addStudentToProject(
                editionId,
                projectId.toString(),
                result.destination!.droppableId,
                result.draggableId,
                motivation
            ),
            {
                pending: "Adding student",
                success: "Successfully added student",
                error: "Something went wrong",
            },
            { toastId: "addStudentToProject" }
        );
        if (!newProjectRole) return;
        setGotProject(false);
    };

    async function editProject() {
        const newProject: EditProject = projectToEditProject(editedProject!);
        await patchProject(
            editionId,
            projectId,
            newProject!.name,
            newProject!.partners,
            newProject!.coaches
        );
        setGotProject(false);
    }

    if (!project || !editedProject) return null;
    return (
        <DragDropContext onDragEnd={result => onDragDrop(result)}>
            <ProjectPageContainer>
                <StudentList />

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
                            10
                            <BsPersonFill />
                        </NumberOfStudents>
                    </ClientsContainer>

                    <ProjectCoaches
                        project={project}
                        editedProject={editedProject}
                        setEditedProject={setEditedProject}
                        editing={editing}
                    />

                    <ProjectRoles projectRoles={projectRoles} />
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
        const { source, destination } = result;

        if (!destination) {
            if (source.droppableId === "students") return;
            else {
                await deleteStudentFromProject(
                    editionId,
                    projectId.toString(),
                    source.droppableId,
                    result.draggableId.substring(
                        0,
                        result.draggableId.length - source.droppableId.length
                    )
                );
                setGotProject(false);
            }
        }

        if (destination?.droppableId === source.droppableId) return;

        if (source.droppableId === "students") {
            handleAddShow(result);
        } else {
            const student = await getStudent(
                editionId,
                parseInt(
                    result.draggableId.substring(
                        0,
                        result.draggableId.length - source.droppableId.length
                    )
                )
            );
            const newProjectRoles = projectRoles.map((projectRole, index) => {
                if (projectRole.projectRoleId.toString() === destination?.droppableId) {
                    const newSuggestions = [...projectRole.suggestions];
                    newSuggestions.splice(destination.index, 0, {
                        projectRoleSuggestionId: index,
                        argumentation: "arg",
                        drafter: { userId: 1, name: "Fix this" },
                        student: student,
                    });
                    return { ...projectRole, suggestions: newSuggestions };
                } else if (projectRole.projectRoleId.toString() === source.droppableId) {
                    const newSuggestions = [...projectRole.suggestions];
                    newSuggestions.splice(source.index, 1);
                    return { ...projectRole, suggestions: newSuggestions };
                } else return projectRole;
            });
            setProjectRoles(newProjectRoles);
        }
    }
}
