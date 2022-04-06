import React, { useEffect, useState } from "react";
import { getProjects } from "../../utils/api/projects";
import "./ProjectsPage.css";

import  {ProjectCard}  from "../../components/ProjectsComponents";

import { CardsGrid } from "./styles";

interface Partner {
    name: string
}

interface Project {
    name: string;
    partners: Partner[];
}

function ProjectPage() {
    const [projects, setProjects] = useState<Array<Project>>([]);
    const [gotProjects, setGotProjects] = useState(false);

    useEffect(() => {
        async function callProjects() {
            const response = await getProjects("summerof2022");
            if (response) {
                setGotProjects(true);
                setProjects(response.projects);
            }
        }
        if (!gotProjects) {
            callProjects();
        }
    });

    return (
        <div>
            <div>
                <input placeholder="project name"></input>
                <button>Search</button>
                <button>Create Project</button>
            </div>

            <CardsGrid>
                {projects.map((project, _index) => (
                    <ProjectCard
                        name={project.name}
                        client={project.partners[0].name}
                        coaches={["Langemietnaamdielangis", "Bart"]}
                        key={_index}
                    />
                ))}
                
            </CardsGrid>
        </div>
    );
}

export default ProjectPage;
