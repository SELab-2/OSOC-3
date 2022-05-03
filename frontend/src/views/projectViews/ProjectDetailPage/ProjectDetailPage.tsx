import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Project } from "../../../data/interfaces";

import { deleteProject, getProject, patchProject } from "../../../utils/api/projects";
import {
    GoBack,
    ProjectContainer,
    Client,
    ClientContainer,
    NumberOfStudents,
    Title,
    TitleContainer,
    Save,
    Cancel,
    Delete,
} from "./styles";

import { BiArrowBack } from "react-icons/bi";
import { BsPersonFill } from "react-icons/bs";
import { MdOutlineEditNote } from "react-icons/md";

import { StudentPlace } from "../../../data/interfaces/projects";
import { StudentPlaceholder } from "../../../components/ProjectsComponents";
import {
    CoachContainer,
    CoachesContainer,
    CoachText,
} from "../../../components/ProjectsComponents/ProjectCard/styles";
import { Role } from "../../../data/enums/role";
import { useAuth } from "../../../contexts";
import { HiOutlineTrash } from "react-icons/hi";
import ConfirmDelete from "../../../components/ProjectsComponents/ConfirmDelete";

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

    const [students, setStudents] = useState<StudentPlace[]>([]);

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
                    setStudents(studentsTemplate);
                } else navigate("/404-not-found");
            }
        }
        if (!gotProject) {
            callProjects();
        }
    }, [editionId, gotProject, navigate, projectId]);

    async function editProject() {
        await patchProject(editionId, projectId, editedProject!.name, 10, [], [], []);
        setGotProject(false);
    }

    if (!project || !editedProject) return null;

    return (
        <div>
            <ProjectContainer>
                <GoBack onClick={() => navigate("/editions/" + editionId + "/projects/")}>
                    <BiArrowBack />
                    Overview
                </GoBack>

                <TitleContainer>
                    {!editing ? (
                        <Title>{project.name}</Title>
                    ) : (
                        <input
                            value={editedProject.name}
                            onChange={e => {
                                const newProject: Project = { ...project, name: e.target.value };
                                setEditedProject(newProject);
                            }}
                        ></input>
                    )}
                    {!editing ? (
                        <MdOutlineEditNote size={"25px"} onClick={() => setEditing(true)} />
                    ) : (
                        <>
                            <Save
                                onClick={async () => {
                                    await editProject();
                                    setEditing(false);
                                }}
                            >
                                Save
                            </Save>
                            <Cancel onClick={() => setEditing(false)}>Cancel</Cancel>
                        </>
                    )}
                    {role === Role.ADMIN && (
                        <Delete onClick={handleShow}>
                            <HiOutlineTrash size={"20px"} />
                        </Delete>
                    )}
                </TitleContainer>

                <ConfirmDelete
                    visible={show}
                    handleConfirm={handleDelete}
                    handleClose={handleClose}
                    name={project.name}
                ></ConfirmDelete>

                <ClientContainer>
                    {project.partners.map((element, _index) => (
                        <Client key={_index}>{element.name}</Client>
                    ))}
                    <NumberOfStudents>
                        {project.numberOfStudents}
                        <BsPersonFill />
                    </NumberOfStudents>
                </ClientContainer>

                <CoachesContainer>
                    {project.coaches.map((element, _index) => (
                        <CoachContainer key={_index}>
                            <CoachText>{element.name}</CoachText>
                        </CoachContainer>
                    ))}
                </CoachesContainer>

                <div>
                    {students.map((element: StudentPlace, _index) => (
                        <StudentPlaceholder studentPlace={element} key={_index} />
                    ))}
                </div>
            </ProjectContainer>
        </div>
    );
}
