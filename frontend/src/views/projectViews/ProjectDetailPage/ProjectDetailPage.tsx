import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Project } from "../../../data/interfaces";

import { getProject } from "../../../utils/api/projects";
import {
    GoBack,
    ProjectContainer,
    Client,
    ClientContainer,
    NumberOfStudents,
    Title,
} from "./styles";

import { BiArrowBack } from "react-icons/bi";
import { BsPersonFill } from "react-icons/bs";

import { StudentPlace } from "../../../data/interfaces/projects";
import { StudentPlaceholder } from "../../../components/ProjectsComponents";
import {
    CoachContainer,
    CoachesContainer,
    CoachText,
} from "../../../components/ProjectsComponents/ProjectCard/styles";

/**
 * @returns the detailed page of a project. Here you can add or remove students from the project.
 */
export default function ProjectDetailPage() {
    const params = useParams();
    const projectId = parseInt(params.projectId!);

    const [project, setProject] = useState<Project>();
    const [gotProject, setGotProject] = useState(false);

    const navigate = useNavigate();

    const [students, setStudents] = useState<StudentPlace[]>([]);

    useEffect(() => {
        async function callProjects() {
            if (projectId) {
                setGotProject(true);
                const response = await getProject("2022", projectId);
                if (response) {
                    setProject(response);

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
    }, [gotProject, navigate, projectId]);

    if (!project) return null;

    return (
        <div>
            <ProjectContainer>
                <GoBack onClick={() => navigate("/editions/2022/projects/")}>
                    <BiArrowBack />
                    Overview
                </GoBack>

                <Title>{project.name}</Title>

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
