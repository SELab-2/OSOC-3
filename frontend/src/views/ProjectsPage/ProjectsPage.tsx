import React, { useEffect, useState } from "react";
import { getProjects } from "../../utils/api/projects";
import "./ProjectsPage.css";

import { ProjectCard } from "../../components/ProjectsComponents";

import { CardsGrid, CreateButton, SearchButton, SearchField } from "./styles";

interface Partner {
    name: string;
}

interface Project {
    name: string;
    numberOfStudents: number;
    partners: Partner[];
    editionName: string;
    projectId: string;
}

function ProjectPage() {
    const [projects, setProjects] = useState<Array<Project>>([]);
    const [gotProjects, setGotProjects] = useState(false);

    useEffect(() => {
        async function callProjects() {
            setGotProjects(true);
            const response = await getProjects("summerof2022");
            if (response) {
                setProjects(response.projects);
            } else setGotProjects(false);
        }
        if (!gotProjects) {
            callProjects();
        }
    });

    return (
        <div>
            <div>
                <SearchField placeholder="project name"></SearchField>
                <SearchButton>Search</SearchButton>
                <CreateButton>Create Project</CreateButton>
            </div>

            <CardsGrid>
                {projects.map((project, _index) => (
                    <ProjectCard
                        name={project.name}
                        client={project.partners[0].name}
                        numberOfStudents={project.numberOfStudents}
                        coaches={[
                            "Langemietnaamdielangis",
                            "Bart met een lange naam",
                            "dfjdf",
                            "kdjfdif",
                            "kfjdif",
                        ]}
                        edition={project.editionName}
                        id={project.projectId}
                        refreshEditions={() => setGotProjects(false)}
                        key={_index}
                    />
                ))}
            </CardsGrid>
        </div>
    );
}

export default ProjectPage;
