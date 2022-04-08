import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Project } from "../../../data/interfaces";

import { getProject } from "../../../utils/api/projects";
import { GoBack, ProjectContainer } from "./styles";

import { BiArrowBack } from "react-icons/bi";

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

                    <h2>{project.name}</h2>
                    {project.editionName}
                </ProjectContainer>
            </div>
        );
    } else return <div></div>;
}
