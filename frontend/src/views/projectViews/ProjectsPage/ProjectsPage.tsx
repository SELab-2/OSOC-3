import { useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { CreateButton, SearchField, OwnProject } from "./styles";
import { Project } from "../../../data/interfaces";
import ProjectTable from "../../../components/ProjectsComponents/ProjectTable";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../../../contexts";

import { Role } from "../../../data/enums";
import ConflictsButton from "../../../components/ProjectsComponents/Conflicts/ConflictsButton";
import axios from "axios";
/**
 * @returns The projects overview page where you can see all the projects.
 * You can filter on your own projects or filter on project name.
 */
export default function ProjectPage() {
    const [allProjects, setAllProjects] = useState<Project[]>([]);
    const [projects, setProjects] = useState<Project[]>([]);
    const [gotProjects, setGotProjects] = useState(false);
    const [loading, setLoading] = useState(false);
    const [moreProjectsAvailable, setMoreProjectsAvailable] = useState(true); // Endpoint has more coaches available
    const [allProjectsFetched, setAllProjectsFetched] = useState(false);
    const [error, setError] = useState<string | undefined>(undefined);

    // Keep track of the set filters
    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const navigate = useNavigate();
    const [page, setPage] = useState(0);

    const params = useParams();
    const editionId = params.editionId!;

    const { role, editions } = useAuth();

    /**
     * Used to fetch the projects
     */
    async function loadProjects() {
        if (loading) {
            return;
        }

        if (allProjectsFetched) {
            setProjects(
                allProjects.filter(project =>
                    project.name.toUpperCase().includes(searchString.toUpperCase())
                )
            );
            setMoreProjectsAvailable(false);
            return;
        }

        setLoading(true);
        let notFoundError = false;

        try {
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

                if (searchString === "") {
                    if (response.projects.length === 0) {
                        setAllProjectsFetched(true);
                    }
                    if (page === 0) {
                        setAllProjects(response.projects);
                    } else {
                        setAllProjects(allProjects.concat(response.projects));
                    }
                }

                setPage(page + 1);
                setGotProjects(true);
            } else {
                setError("Oops, something went wrong...");
            }
        } catch (error) {
            setError("Oops, something went wrong...");

            if (axios.isAxiosError(error) && error.response?.status === 404) {
                notFoundError = true;
            }
        }
        setLoading(false);
        if (notFoundError) {
            // Navigate must be at end of function
            navigate("/404-not-found");
        }
    }

    /**
     * Reset fetched projects
     */
    function refreshProjects() {
        setProjects([]);
        setPage(0);
        setMoreProjectsAvailable(true);
        setAllProjectsFetched(false);
        setGotProjects(false);
    }

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

    /**
     * Filter the projects by name
     * @param searchTerm
     */
    function filter(searchTerm: string) {
        setPage(0);
        setGotProjects(false);
        setMoreProjectsAvailable(true);
        setSearchString(searchTerm);
        setProjects([]);
    }

    return (
        <div>
            <div>
                <SearchField
                    value={searchString}
                    onChange={e => {
                        filter(e.target.value);
                    }}
                    placeholder="project name"
                />

                {role === Role.ADMIN && editionId === editions[0] && (
                    <CreateButton
                        onClick={() => navigate("/editions/" + editionId + "/projects/new")}
                    >
                        Create Project
                    </CreateButton>
                )}
                <ConflictsButton editionId={editionId} />
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
                getMoreProjects={loadProjects}
                moreProjectsAvailable={moreProjectsAvailable}
                removeProject={removeProject}
                error={error}
            />
        </div>
    );
}
