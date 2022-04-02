import React, { useEffect, useState } from "react";
import { getProjects } from "../../utils/api/projects";
import "./ProjectsPage.css";

import { ProjectCard } from "../../components/ProjectsComponents";

import { CardsGrid } from "./styles";

function ProjectPage() {
    const [projects, setProjects] = useState();

    useEffect(() => {
        async function callProjects() {
            const response = await getProjects("1");
            if (response) {
                console.log(response);
                setProjects(response);
            }
        }
        if (!projects) {
            callProjects();
        } else console.log("hello");
    });

    return (
        <div>
            <CardsGrid>
                <ProjectCard
                    name="Project 1"
                    client="client 1"
                    coaches={["PieterJanCornelis Delangeachternaam", "Bart"]}
                />
                <ProjectCard
                    name="Project 2"
                    client="client 2"
                    coaches={["Miet", "Bart", "Dirk de lange", "Jef de korte"]}
                />
                <ProjectCard name="Project 3" client="client 3" coaches={["Miet", "Bart"]} />
                <ProjectCard name="Project 4" client="client 4" coaches={["Miet"]} />
                <ProjectCard
                    name="This could be a long project name that has multiple lines"
                    client="client 1"
                    coaches={["Miet", "Bart"]}
                />
                <ProjectCard name="Project 5" client="client 5" coaches={["Miet", "Bart"]} />
                <ProjectCard name="Project 6" client="client 6" coaches={["Jef", "Carl"]} />
                <ProjectCard name="Project 7" client="client 7" coaches={["Miet", "Bart"]} />
                <ProjectCard name="Project 8" client="client 8" coaches={["Miet", "Carl"]} />
            </CardsGrid>
        </div>
    );
}

export default ProjectPage;
