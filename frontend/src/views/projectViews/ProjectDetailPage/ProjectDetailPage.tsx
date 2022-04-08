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

export default function ProjectDetailPage() {
    const params = useParams();
    const projectId = parseInt(params.projectId!);

    const [project, setProject] = useState<Project>();
    const [gotProject, setGotProject] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        async function callProjects() {
            if (projectId) {
                setGotProject(true);
                const response = await getProject("summerof2022", projectId);
                if (response) {
                    setProject(response);
                } else navigate("/404-not-found");
            }
        }
        if (!gotProject) {
            callProjects();
        }
    });
    if (project) {
        return (
            <div>
                <ProjectContainer>
                    <GoBack onClick={() => navigate("/editions/summerof2022/projects/")}>
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
                </ProjectContainer>
            </div>
        );
    } else return <div></div>;
}
