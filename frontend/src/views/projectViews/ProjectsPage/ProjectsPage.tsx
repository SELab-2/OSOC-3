import { useEffect, useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { CreateButton, SearchField, OwnProject } from "./styles";
import { Project } from "../../../data/interfaces";
import ProjectTable from "../../../components/ProjectsComponents/ProjectTable";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../../../contexts";

import { Role } from "../../../data/enums";
import ConflictsButton from "../../../components/ProjectsComponents/Conflicts/ConflictsButton";
import { isReadonlyEdition } from "../../../utils/logic";
import { toast } from "react-toastify";
/**
 * @returns The projects overview page where you can see all the projects.
 * You can filter on your own projects or filter on project name.
 */
export default function ProjectPage() {
    const params = useParams();

    const [allProjects, setAllProjects] = useState<Project[]>([]);
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(false);
    const [requestedEdition, setRequestedEdition] = useState(params.editionId);
    const [moreProjectsAvailable, setMoreProjectsAvailable] = useState(true); // Endpoint has more coaches available
    const [allProjectsFetched, setAllProjectsFetched] = useState(false);

    const [controller, setController] = useState<AbortController | undefined>(undefined);

    // Keep track of the set filters
    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const navigate = useNavigate();
    const [page, setPage] = useState(0);

    const editionId = params.editionId!;

    const { role, editions, userId } = useAuth();

    /**
     * Used to fetch the projects
     */
    async function loadProjects(requested: number, reset: boolean) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
            return;
        }

        if (allProjectsFetched && !reset) {
            const newUserId: number = userId === null ? -1 : userId;

            setProjects(
                allProjects
                    .filter(project =>
                        project.name.toUpperCase().includes(searchString.toUpperCase())
                    )
                    .filter(
                        project =>
                            !ownProjects ||
                            project.coaches.map(coach => coach.userId).includes(newUserId)
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
            getProjects(editionId, searchString, ownProjects, requestedPage, newController),
            { error: "Failed to retrieve projects" }
        );

        if (response !== null) {
            if (response.projects.length === 0 && !filterChanged) {
                setMoreProjectsAvailable(false);
            }
            if (requestedPage === 0 || filterChanged) {
                setProjects(response.projects);
            } else {
                setProjects(projects.concat(response.projects));
            }

            if (searchString === "" && !ownProjects) {
                if (response.projects.length === 0) {
                    setAllProjectsFetched(true);
                }
                if (requestedPage === 0) {
                    setAllProjects(response.projects);
                } else {
                    setAllProjects(allProjects.concat(response.projects));
                }
            }

            setPage(requestedPage + 1);
        } else {
            setMoreProjectsAvailable(false);
        }
        setLoading(false);
    }

    useEffect(() => {
        if (params.editionId !== requestedEdition) {
            setProjects([]);
            setPage(0);
            setAllProjectsFetched(false);
            setMoreProjectsAvailable(true);
            loadProjects(-1, true);
            setRequestedEdition(params.editionId);
        } else {
            setPage(0);
            setMoreProjectsAvailable(true);
            loadProjects(-1, false);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchString, ownProjects, params.editionId]);

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
                    onChange={e => {
                        setPage(0);
                        setSearchString(e.target.value);
                    }}
                    placeholder="project name"
                />

                {role === Role.ADMIN && !isReadonlyEdition(editionId, editions) && (
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
                    setPage(0);
                    setOwnProjects(!ownProjects);
                }}
            />
            <ProjectTable
                projects={projects}
                loading={loading}
                getMoreProjects={loadProjects}
                moreProjectsAvailable={moreProjectsAvailable}
                removeProject={removeProject}
            />
        </div>
    );
}
