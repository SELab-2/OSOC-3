import { CardsGrid, ProjectsContainer } from "../../views/projectViews/ProjectsPage/styles";
import { ProjectCard } from "./index";
import InfiniteScroll from "react-infinite-scroller";
import { Project } from "../../data/interfaces";
import { MessageDiv } from "./styles";
import LoadSpinner from "../Common/LoadSpinner";

/**
 * A table of [[ProjectCard]]s.
 * @param props.projects A list of projects which needs to be shown.
 * @param props.loading Data is not available yet.
 * @param props.getMoreProjects A function to load more projects.
 * @param props.moreProjectsAvailable More unfetched projects available.
 */
export default function ProjectTable(props: {
    projects: Project[];
    loading: boolean;
    getMoreProjects: (page: number, reset: boolean) => void;
    moreProjectsAvailable: boolean;
}) {
    if (props.projects.length === 0) {
        if (props.loading) {
            return <LoadSpinner show={true} />;
        }
        return (
            <MessageDiv>
                <div>No projects found.</div>
            </MessageDiv>
        );
    }

    return (
        <InfiniteScroll
            loadMore={page => props.getMoreProjects(page, false)}
            hasMore={props.moreProjectsAvailable}
            loader={<LoadSpinner show={true} key="Spinner" />}
            initialLoad={true}
            useWindow={false}
            getScrollParent={() => document.getElementById("root")}
        >
            <ProjectsContainer>
                <CardsGrid>
                    {props.projects.map((project, _index) => (
                        <ProjectCard project={project} key={_index} />
                    ))}
                </CardsGrid>
            </ProjectsContainer>
        </InfiniteScroll>
    );
}
