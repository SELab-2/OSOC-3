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
import { Project } from "../../../data/interfaces";
import { useParams } from "react-router-dom";
import InfiniteScroll from "react-infinite-scroller";
import { useAuth } from "../../../contexts";
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

    const { role } = useAuth();

    /**
     * Used to fetch the projects
     */
    async function callProjects(newPage: number) {
        if (loading) return;
        setLoading(true);
        const response = await getProjects(editionId, searchString, ownProjects, newPage);
        setGotProjects(true);

        if (response) {
            if (response.projects.length === 0) {
                setMoreProjectsAvailable(false);
            } else {
                setPage(page + 1);
                setProjects(projects.concat(response.projects));
            }
        }
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
                    onKeyDown={e => {
                        if (e.key === "Enter") refreshProjects();
                    }}
                />
                <SearchButton onClick={refreshProjects}>Search</SearchButton>
                {!role && <CreateButton>Create Project</CreateButton>}
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
                                refreshProjects={refreshProjects}
                                key={_index}
                            />
                        ))}
                    </CardsGrid>
                </ProjectsContainer>
            </InfiniteScroll>

            <LoadSpinner show={loading} />

            {moreProjectsAvailable && (
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
            )}
        </div>
    );
}
