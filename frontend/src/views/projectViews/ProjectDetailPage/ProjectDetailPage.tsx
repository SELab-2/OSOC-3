import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Project } from "../../../data/interfaces";

import { getProject } from "../../../utils/api/projects";

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
        return <div>{project.name}</div>;
    } else return <div></div>;
}
