import React, { useCallback, useEffect, useState } from "react";
import { getProjects } from "../../utils/api/projects";
import "./ProjectsPage.css";

import { ProjectCard } from "../../components/ProjectsComponents";

import { CardsGrid, CreateButton, SearchButton, SearchField, OwnProject } from "./styles";

import { useAuth } from "../../contexts/auth-context";

interface Partner {
    name: string;
}

interface Coach {
    name: string;
    userId: number;
}

interface Project {
    name: string;
    numberOfStudents: number;
    partners: Partner[];
    coaches: Coach[];
    editionName: string;
    projectId: string;
}

function ProjectPage() {
    const [projectsAPI, setProjectsAPI] = useState<Array<Project>>([]);
    const [projects, setProjects] = useState<Array<Project>>([]);
    const [gotProjects, setGotProjects] = useState(false);

    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const { userId } = useAuth();

    const searchProjects = useCallback(() => {
        const results: Project[] = [];
        projectsAPI.forEach(project => {
            let ownsProject = true;
            if (ownProjects) {
                ownsProject = false;
                project.coaches.forEach(coach => {
                    if (coach.userId === userId) {
                        ownsProject = true;
                    }
                });
            }
            if (
                project.name.toLocaleLowerCase().includes(searchString.toLocaleLowerCase()) &&
                ownsProject
            ) {
                results.push(project);
            }
        });
        setProjects(results);
    }, [ownProjects, projectsAPI, searchString, userId]);

    useEffect(() => {
        searchProjects();
    }, [ownProjects, searchProjects]);

    useEffect(() => {
        async function callProjects() {
            setGotProjects(true);
            const response = await getProjects("summerof2022");
            if (response) {
                setProjectsAPI(response.projects);
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
                <SearchField
                    value={searchString}
                    onChange={e => setSearchString(e.target.value)}
                    onKeyPress={e => {
                        if (e.key === "Enter") {
                            searchProjects();
                        }
                    }}
                    placeholder="project name"
                ></SearchField>
                <SearchButton onClick={searchProjects}>Search</SearchButton>
                <CreateButton>Create Project</CreateButton>
            </div>
            <OwnProject
                type="switch"
                id="custom-switch"
                label="Only own projects"
                checked={ownProjects}
                onChange={() => {
                    setOwnProjects(!ownProjects);
                    searchProjects();
                }}
            />

            <CardsGrid>
                {projects.map((project, _index) => (
                    <ProjectCard
                        name={project.name}
                        client={project.partners[0].name}
                        numberOfStudents={project.numberOfStudents}
                        coaches={project.coaches}
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
