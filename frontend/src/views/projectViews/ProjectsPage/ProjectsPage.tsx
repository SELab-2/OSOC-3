import { useEffect, useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { ProjectCard } from "../../../components/ProjectsComponents";
import { CardsGrid, CreateButton, SearchButton, SearchField, OwnProject } from "./styles";
import { useAuth } from "../../../contexts/auth-context";
import { Project } from "../../../data/interfaces";
import { useParams } from "react-router-dom";

/**
 * @returns The projects overview page where you can see all the projects.
 * You can filter on your own projects or filter on project name.
 */
export default function ProjectPage() {
    const [projectsAPI, setProjectsAPI] = useState<Project[]>([]);
    const [gotProjects, setGotProjects] = useState(false);

    // To filter projects we need to keep a separate list to avoid calling the API every time we change te filters.
    const [projects, setProjects] = useState<Project[]>([]);

    // Keep track of the set filters
    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const { userId } = useAuth();

    const params = useParams();
    const editionId = params.editionId!;

    /**
     * Uses to filter the results based onto search string and own projects
     */
    useEffect(() => {
        const results: Project[] = [];
        projectsAPI.forEach(project => {
            let filterOut = false;
            if (ownProjects) {
                // If the user doesn't coach this project it will be filtered out.
                filterOut = !project.coaches.some(coach => {
                    return coach.userId === userId;
                });
            }
            if (
                project.name.toLocaleLowerCase().includes(searchString.toLocaleLowerCase()) &&
                !filterOut
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
            const response = await getProjects(editionId);
            if (response) {
                setProjectsAPI(response.projects);
                setProjects(response.projects);
            }
        }
        if (!gotProjects) {
            callProjects();
        }
    }, [editionId, gotProjects]);

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
                        project={project}
                        refreshProjects={() => setGotProjects(false)}
                        key={_index}
                    />
                ))}
            </CardsGrid>
        </div>
    );
}
