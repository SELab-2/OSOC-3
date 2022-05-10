import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Project, CreateProject as EditProject } from "../../../data/interfaces";

import { deleteProject, getProject, patchProject } from "../../../utils/api/projects";
import {
    GoBack,
    ProjectContainer,
    Client,
    ClientsContainer,
    NumberOfStudents,
    ClientContainer,
    ProjectPageContainer,
    SuggestionContainer,
    Suggestions,
} from "./styles";

import { BiArrowBack } from "react-icons/bi";
import { BsPersonFill } from "react-icons/bs";
import { TiDeleteOutline } from "react-icons/ti";

import { StudentPlace } from "../../../data/interfaces/projects";
import {
    CoachContainer,
    CoachesContainer,
    CoachText,
    ProjectRoleContainer,
} from "../../../components/ProjectsComponents/ProjectCard/styles";
import { useAuth } from "../../../contexts";
import ConfirmDelete from "../../../components/ProjectsComponents/ConfirmDelete";
import { RemoveButton } from "../CreateProjectPage/styles";
import {
    CoachInput,
    PartnerInput,
    TitleAndEdit,
    StudentList,
} from "../../../components/ProjectDetailComponents";
import projectToEditProject from "../../../utils/logic/project";

import { DragDropContext, Droppable, Draggable, DropResult } from "react-beautiful-dnd";
import { getStudent } from "../../../utils/api/students";

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

    const { role } = useAuth();

    // const [students, setStudents] = useState<StudentPlace[]>([]);

    const [editing, setEditing] = useState(false);

    // Used for the confirm screen.
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    // What to do when deleting a project.
    const handleDelete = () => {
        deleteProject(project!.editionName, project!.projectId);
        setShow(false);
        navigate("/editions/" + editionId + "/projects/");
    };

    const [projectRoles, setProjectRoles] = useState([
        { skill: "Frontend", slots: 5, suggestions: [{ name: "Tom" }] },
        { skill: "Backend", slots: 5, suggestions: [] },
    ]);

    useEffect(() => {
        async function callProjects(): Promise<void> {
            if (projectId) {
                setGotProject(true);
                const response = await getProject(editionId, projectId);
                if (response) {
                    setProject(response);
                    setEditedProject(response);

                    // TODO
                    // Generate student data
                    const studentsTemplate: StudentPlace[] = [];
                    for (let i = 0; i < response.numberOfStudents; i++) {
                        const student: StudentPlace = {
                            available: i % 2 === 0,
                            name: i % 2 === 0 ? undefined : "Tom",
                            skill: "Frontend",
                        };
                        studentsTemplate.push(student);
                    }
                    // setStudents(studentsTemplate);
                } else navigate("/404-not-found");
            }
        }
        if (!gotProject) {
            callProjects();
        }
    }, [editionId, gotProject, navigate, projectId]);

    async function editProject() {
        const newProject: EditProject = projectToEditProject(editedProject!);
        await patchProject(
            editionId,
            projectId,
            newProject!.name,
            newProject!.number_of_students,
            [], // TODO Skills
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
                        handleShow={handleShow}
                    />

                    <ConfirmDelete
                        visible={show}
                        handleConfirm={handleDelete}
                        handleClose={handleClose}
                        name={project.name}
                    ></ConfirmDelete>

                    <ClientsContainer>
                        {editedProject.partners.map((element, _index) => (
                            <ClientContainer key={_index}>
                                <Client>{element.name}</Client>
                                {editing && (
                                    <RemoveButton
                                        onClick={() => {
                                            const newPartners = [...editedProject.partners];
                                            newPartners.splice(_index, 1);
                                            const newProject: Project = {
                                                ...project,
                                                partners: newPartners,
                                            };
                                            setEditedProject(newProject);
                                        }}
                                    >
                                        <TiDeleteOutline size={"20px"} />
                                    </RemoveButton>
                                )}
                            </ClientContainer>
                        ))}
                        {editing && (
                            <PartnerInput project={editedProject!} setProject={setEditedProject} />
                        )}
                        <NumberOfStudents>
                            {project.numberOfStudents}
                            <BsPersonFill />
                        </NumberOfStudents>
                    </ClientsContainer>

                    <CoachesContainer>
                        {editedProject.coaches.map((element, _index) => (
                            <CoachContainer key={_index}>
                                <CoachText>{element.name}</CoachText>
                                {_index}
                                {editing && (
                                    <RemoveButton
                                        onClick={() => {
                                            const newCoaches = [...editedProject.coaches];
                                            console.log(_index);

                                            newCoaches.splice(_index, 1);
                                            const newProject: Project = {
                                                ...project,
                                                coaches: newCoaches,
                                            };
                                            setEditedProject(newProject);
                                        }}
                                    >
                                        <TiDeleteOutline size={"20px"} />
                                    </RemoveButton>
                                )}
                            </CoachContainer>
                        ))}
                        {editing && (
                            <CoachInput project={editedProject!} setProject={setEditedProject} />
                        )}
                    </CoachesContainer>

                    <div>
                        {projectRoles.map((projectRole, _index) => (
                            <ProjectRoleContainer key={_index}>
                                {projectRole.skill}
                                <br></br>
                                {projectRole.suggestions.length.toString() +
                                    " / " +
                                    projectRole.slots.toString()}
                                <Droppable droppableId={projectRole.skill}>
                                    {(provided, snapshot) => (
                                        <Suggestions
                                            ref={provided.innerRef}
                                            {...provided.droppableProps}
                                        >
                                            {projectRole.suggestions.map((sug, _index2) => (
                                                <Draggable
                                                    draggableId={sug.name}
                                                    index={_index2}
                                                    key={_index2}
                                                >
                                                    {(provided, snapshot) => (
                                                        <SuggestionContainer
                                                            ref={provided.innerRef}
                                                            {...provided.draggableProps}
                                                            {...provided.dragHandleProps}
                                                        >
                                                            {sug.name}
                                                        </SuggestionContainer>
                                                    )}
                                                </Draggable>
                                            ))}
                                            {provided.placeholder}
                                        </Suggestions>
                                    )}
                                </Droppable>
                            </ProjectRoleContainer>
                        ))}
                    </div>
                </ProjectContainer>
            </ProjectPageContainer>
        </DragDropContext>
    );

    async function onDragDrop(result: DropResult) {
        const { source, destination } = result;
        if (!destination || destination.droppableId === "student") {
            if (source.droppableId === "students") return;
            else {
                const newProjectRoles = projectRoles.map((projectRole, index) => {
                    if (projectRole.skill === source.droppableId) {
                        const newSuggestions = [...projectRole.suggestions];
                        newSuggestions.splice(source.index, 1);
                        return { ...projectRole, suggestions: newSuggestions };
                    } else return projectRole;
                });
                setProjectRoles(newProjectRoles);
            }
        }
        if (destination?.droppableId === source.droppableId) return;
        if (source.droppableId === "students") {
            const student = await getStudent(editionId, result.draggableId);
            const newProjectRoles = projectRoles.map((projectRole, index) => {
                if (projectRole.skill === destination?.droppableId) {
                    const newSuggestions = [...projectRole.suggestions];
                    newSuggestions.push({ name: student.lastName });
                    return { ...projectRole, suggestions: newSuggestions };
                } else return projectRole;
            });
            setProjectRoles(newProjectRoles);
        } else {
            const newProjectRoles = projectRoles.map((projectRole, index) => {
                if (projectRole.skill === destination?.droppableId) {
                    const newSuggestions = [...projectRole.suggestions];
                    newSuggestions.push({ name: result.draggableId });
                    return { ...projectRole, suggestions: newSuggestions };
                } else if (projectRole.skill === source.droppableId) {
                    const newSuggestions = [...projectRole.suggestions];
                    newSuggestions.splice(source.index, 1);
                    return { ...projectRole, suggestions: newSuggestions };
                } else return projectRole;
            });
            setProjectRoles(newProjectRoles);
        }
    }
}
