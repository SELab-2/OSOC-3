import { useEffect, useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { ProjectCard } from "../../../components/ProjectsComponents";
import { CardsGrid, CreateButton, SearchButton, SearchField, OwnProject } from "./styles";
import { useAuth } from "../../../contexts/auth-context";
import { Project } from "../../../data/interfaces";

function ProjectPage() {
    const [projectsAPI, setProjectsAPI] = useState<Array<Project>>([]);
    const [projects, setProjects] = useState<Array<Project>>([]);
    const [gotProjects, setGotProjects] = useState(false);

    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const { userId } = useAuth();

    /**
     * Uses to filter the results based onto search string and own projects
     */
    useEffect(() => {
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
    }, [projectsAPI, ownProjects, searchString, userId]);

    /**
     * Used to fetch the projects
     */
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
                    placeholder="project name"
                />
                <SearchButton>Search</SearchButton>
                <CreateButton>Create Project</CreateButton>
            </div>
            <OwnProject
                type="switch"
                id="custom-switch"
                label="Only own projects"
                checked={ownProjects}
                onChange={() => {
                    setOwnProjects(!ownProjects);
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
                        projectId={project.projectId}
                        refreshEditions={() => setGotProjects(false)}
                        key={_index}
                    />
                ))}
            </CardsGrid>
        </div>
    );
}

export default ProjectPage;