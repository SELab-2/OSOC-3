import { useEffect, useState } from "react";
import { getProject, getProjects } from "../../../utils/api/projects";
import { ControlContainer, OwnProject, SearchFieldDiv } from "./styles";
import { Project } from "../../../data/interfaces";
import ProjectTable from "../../../components/ProjectsComponents/ProjectTable";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth, useSockets } from "../../../contexts";

import { Role } from "../../../data/enums";
import ConflictsButton from "../../../components/ProjectsComponents/Conflicts/ConflictsButton";
import { EventType, RequestMethod, WebSocketEvent } from "../../../data/interfaces/websockets";
import { isReadonlyEdition } from "../../../utils/logic";
import { toast } from "react-toastify";
import { CreateButton } from "../../../components/Common/Buttons";
import { SearchBar } from "../../../components/Common/Forms";

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
    const { socket } = useSockets();

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
     * Remove a project with a specific id
     */
    function findAndRemoveProject(id: string, list: Project[]): Project[] {
        return list.filter(project => project.projectId.toString() !== id);
    }

    /**
     * Find a project with a specific id and update its data
     */
    function updateProject(project: Project, list: Project[]): Project[] {
        const index = list.findIndex(pr => pr.projectId === project.projectId);
        const copy = [...list];
        if (index > -1) {
            copy[index] = project;
        }

        return copy;
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

    /**
     * Websockets
     */
    useEffect(() => {
        function listener(event: MessageEvent) {
            const data = JSON.parse(event.data) as WebSocketEvent;

            // Ignore all events that aren't about projects
            if (data.eventType !== EventType.PROJECT) return;

            // If the project from the event hasn't been loaded in the list, ignore the event as well
            if (
                !allProjects.some(
                    project => project.projectId.toString() === data.pathIds.projectId
                )
            ) {
                return;
            }

            // Project was deleted: remove it from the list
            if (data.method === RequestMethod.DELETE) {
                setAllProjects(findAndRemoveProject(data.pathIds.projectId!, allProjects));
                setProjects(findAndRemoveProject(data.pathIds.projectId!, projects));
            } else if (data.method === RequestMethod.PATCH) {
                // Fetch the new version of the project & replace in the two lists
                getProject(editionId, parseInt(data.pathIds.projectId!)).then(project => {
                    setAllProjects(updateProject(project!, allProjects));
                    setProjects(updateProject(project!, projects));
                });
            }
        }

        socket?.addEventListener("message", listener);

        function removeListener() {
            if (socket) {
                socket.removeEventListener("message", listener);
            }
        }

        return removeListener;
    }, [socket, allProjects, projects, editionId]);

    return (
        <div>
            <ControlContainer>
                <div>
                    <SearchFieldDiv>
                        <SearchBar
                            onChange={e => {
                                setPage(0);
                                setSearchString(e.target.value);
                            }}
                            value={searchString}
                            placeholder="Search project..."
                        />
                    </SearchFieldDiv>

                    {role === Role.ADMIN && !isReadonlyEdition(editionId, editions) && (
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
                    setPage(0);
                    setOwnProjects(!ownProjects);
                }}
            />
            <ProjectTable
                projects={projects}
                loading={loading}
                getMoreProjects={loadProjects}
                moreProjectsAvailable={moreProjectsAvailable}
            />
        </div>
    );
}
