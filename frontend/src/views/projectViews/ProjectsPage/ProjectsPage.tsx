import { useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { ControlContainer, OwnProject, SearchFieldDiv } from "./styles";
import { Project } from "../../../data/interfaces";
import ProjectTable from "../../../components/ProjectsComponents/ProjectTable";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../../../contexts";

import { Role } from "../../../data/enums";
import ConflictsButton from "../../../components/ProjectsComponents/Conflicts/ConflictsButton";
import { toast } from "react-toastify";
import { CreateButton } from "../../../components/Common/Buttons";
import { SearchBar } from "../../../components/Common/Forms";
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

    const [controller, setController] = useState<AbortController | undefined>(undefined);

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

        if (controller !== undefined) {
            controller.abort();
        }
        const newController = new AbortController();
        setController(newController);

        const response = await toast.promise(
            getProjects(editionId, searchString, ownProjects, page, newController),
            { error: "Failed to retrieve projects" }
        );
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
        setLoading(false);
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
            <ControlContainer>
                <div>
                    <SearchFieldDiv>
                        <SearchBar
                            onChange={e => filter(e.target.value)}
                            value={searchString}
                            placeholder="Search project..."
                        />
                    </SearchFieldDiv>

                    {role === Role.ADMIN && editionId === editions[0] && (
                        <CreateButton
                            label="Create Project"
                            onClick={() => navigate("/editions/" + editionId + "/projects/new")}
                        />
                    )}
                </div>
                <ConflictsButton editionId={editionId} />
            </ControlContainer>

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
            />
        </div>
    );
}
