import { CardsGrid, ProjectsContainer } from "../../views/projectViews/ProjectsPage/styles";
import { ProjectCard } from "./index";
import InfiniteScroll from "react-infinite-scroller";
import { Project } from "../../data/interfaces";
import { SpinnerContainer, Error } from "../UsersComponents/Requests/styles";
import { Spinner } from "react-bootstrap";
import React from "react";
import { MessageDiv } from "./styles";

/**
 * A table of [[ProjectCard]]s.
 * @param props.projects A list of projects which needs to be shown.
 * @param props.loading Data is not available yet.
 * @param props.gotData All data is received.
 * @param props.getMoreProjects A function to load more projects.
 * @param props.moreProjectsAvailable More unfetched projects available.
 * @param props.removeProject A function which will be called when a project is removed.
 */
export default function ProjectTable(props: {
    projects: Project[];
    loading: boolean;
    gotData: boolean;
    getMoreProjects: () => void;
    moreProjectsAvailable: boolean;
    removeProject: (project: Project) => void;
    error: string | undefined;
}) {
    if (props.error) {
        return (
            <MessageDiv>
                <Error>{props.error}</Error>
            </MessageDiv>
        );
    } else if (props.gotData && props.projects.length === 0) {
        return (
            <MessageDiv>
                <div>No projects found.</div>
            </MessageDiv>
        );
    }

    return (
        <InfiniteScroll
            loadMore={props.getMoreProjects}
            hasMore={props.moreProjectsAvailable}
            loader={
                <SpinnerContainer key={"spinner"}>
                    <Spinner animation="border" />
                </SpinnerContainer>
            }
            initialLoad={true}
            useWindow={false}
            getScrollParent={() => document.getElementById("root")}
        >
            <ProjectsContainer>
                <CardsGrid>
                    {props.projects.map((project, _index) => (
                        <ProjectCard
                            project={project}
                            removeProject={props.removeProject}
                            key={_index}
                        />
                    ))}
                </CardsGrid>
            </ProjectsContainer>
        </InfiniteScroll>
    );
}