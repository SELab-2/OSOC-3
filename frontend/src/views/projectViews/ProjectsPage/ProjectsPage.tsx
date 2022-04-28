import { useEffect, useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { CreateButton, SearchButton, SearchField, OwnProject } from "./styles";
import { Project } from "../../../data/interfaces";
import { useParams } from "react-router-dom";
import ProjectTable from "../../../components/ProjectsComponents/ProjectTable";

/**
 * @returns The projects overview page where you can see all the projects.
 * You can filter on your own projects or filter on project name.
 */
export default function ProjectPage() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [gotProjects, setGotProjects] = useState(false);
    const [loading, setLoading] = useState(false);
    const [moreProjectsAvailable, setMoreProjectsAvailable] = useState(true); // Endpoint has more coaches available

    // Keep track of the set filters
    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const [page, setPage] = useState(0);

    const params = useParams();
    const editionId = params.editionId!;

    /**
     * Used to fetch the projects
     */
    async function callProjects() {
        if (loading) {
            return;
        }
        setLoading(true);
        const response = await getProjects(editionId, searchString, ownProjects, page);
        if (response) {
            if (response.projects.length === 0) {
                setMoreProjectsAvailable(false);
            }
            if (page === 0) {
                setProjects(response.projects);
            } else {
                setProjects(projects.concat(response.projects));
            }
            setPage(page + 1);
        }
        setGotProjects(true);
        setLoading(false);
    }

    async function refreshProjects() {
        setProjects([]);
        setPage(0);
        setMoreProjectsAvailable(true);
        setGotProjects(false);
    }

    useEffect(() => {
        if (moreProjectsAvailable && !gotProjects) {
            callProjects();
        }
    });

    /**
     * Remove a project in local list.
     * @param project The project to remove.
     */
    function removeProject(project: Project) {
        setProjects(
            projects.filter(object => {
                return object !== project;
            })
        );
    }

    return (
        <div>
            <div>
                <SearchField
                    value={searchString}
                    onChange={e => setSearchString(e.target.value)}
                    placeholder="project name"
                    onKeyDown={e => {
                        if (e.key === "Enter") refreshProjects();
                    }}
                />
                <SearchButton onClick={refreshProjects}>Search</SearchButton>
                <CreateButton>Create Project</CreateButton>
            </div>
            <OwnProject
                type="switch"
                id="custom-switch"
                label="Only own projects"
                checked={ownProjects}
                onChange={() => {
                    setOwnProjects(!ownProjects);
                    refreshProjects();
                }}
            />
            <ProjectTable
                projects={projects}
                loading={loading}
                gotData={gotProjects}
                getMoreProjects={callProjects}
                moreProjectsAvailable={moreProjectsAvailable}
                removeProject={removeProject}
            />
        </div>
    );
}
