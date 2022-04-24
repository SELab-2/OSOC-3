import { useEffect, useState } from "react";
import { getProjects } from "../../../utils/api/projects";
import { ProjectCard, LoadSpinner } from "../../../components/ProjectsComponents";
import {
    CardsGrid,
    CreateButton,
    SearchButton,
    SearchField,
    OwnProject,
    ProjectsContainer,
    LoadMoreContainer,
    LoadMoreButton,
} from "./styles";
import { useAuth } from "../../../contexts/auth-context";
import { Project } from "../../../data/interfaces";
import { useParams } from "react-router-dom";
import InfiniteScroll from "react-infinite-scroller";
/**
 * @returns The projects overview page where you can see all the projects.
 * You can filter on your own projects or filter on project name.
 */
export default function ProjectPage() {
    const [projectsAPI, setProjectsAPI] = useState<Project[]>([]);
    const [gotProjects, setGotProjects] = useState(false);
    const [loading, setLoading] = useState(false);
    const [moreProjectsAvailable, setMoreProjectsAvailable] = useState(true); // Endpoint has more coaches available

    // To filter projects we need to keep a separate list to avoid calling the API every time we change te filters.
    const [projects, setProjects] = useState<Project[]>([]);

    // Keep track of the set filters
    const [searchString, setSearchString] = useState("");
    const [ownProjects, setOwnProjects] = useState(false);

    const [page, setPage] = useState(0);

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
    async function callProjects(newPage: number) {
        if (loading) return;
        setLoading(true);
        const response = await getProjects(editionId, newPage);
        setGotProjects(true);

        if (response) {
            if (response.projects.length === 0) {
                setMoreProjectsAvailable(false);
            } else {
                setPage(page + 1);
                setProjectsAPI(projectsAPI.concat(response.projects));
                setProjects(projects.concat(response.projects));
            }
        }
        setLoading(false);
    }

    useEffect(() => {
        if (moreProjectsAvailable && !gotProjects) {
            callProjects(0);
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

            <InfiniteScroll
                pageStart={0}
                loadMore={(newPage: number) => {
                    console.log("loading more" + newPage);
                }}
                hasMore={moreProjectsAvailable}
                useWindow={false}
                initialLoad={true}
            >
                <ProjectsContainer>
                    <CardsGrid>
                        {projects.map((project, _index) => (
                            <ProjectCard
                                project={project}
                                refreshProjects={() => {
                                    setProjectsAPI([]);
                                    setProjects([]);
                                    setGotProjects(false);
                                    setPage(0);
                                    setMoreProjectsAvailable(true);
                                }}
                                key={_index}
                            />
                        ))}
                    </CardsGrid>
                </ProjectsContainer>
            </InfiniteScroll>

            <LoadSpinner show={loading} />

            <LoadMoreContainer>
                <LoadMoreButton
                    onClick={() => {
                        if (moreProjectsAvailable) {
                            callProjects(page);
                        }
                    }}
                >
                    Load more projects
                </LoadMoreButton>
            </LoadMoreContainer>
        </div>
    );
}
