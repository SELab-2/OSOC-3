import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";
import { Student } from "../../../data/interfaces/students";
import InfiniteScroll from "react-infinite-scroller";
import { Draggable, Droppable } from "react-beautiful-dnd";
import LoadSpinner from "../../Common/LoadSpinner";
import { isReadonlyEdition } from "../../../utils/logic";
import { useParams } from "react-router-dom";
import { useAuth } from "../../../contexts";

interface Props {
    students: Student[];
    moreDataAvailable: boolean;
    getMoreData: (page: number) => void;
}

/**
 * Component that renders the list of students in the sidebar.
 * @param props the students that need to be rendered.
 */
export default function StudentList(props: Props) {
    const params = useParams();
    const editionId = params.editionId;
    const projectId = params.projectId;

    const { editions } = useAuth();

    const notDraggable = isReadonlyEdition(editionId, editions) || projectId === undefined;

    return (
        <StudentCardsList>
            <InfiniteScroll
                loadMore={props.getMoreData}
                hasMore={props.moreDataAvailable}
                loader={<LoadSpinner show={true} key="spinner" />}
                useWindow={false}
                initialLoad={true}
            >
                <Droppable droppableId="students" isDropDisabled={true}>
                    {(provided, snapshot) => (
                        <div ref={provided.innerRef} {...provided.droppableProps}>
                            {props.students.map((student, index) => (
                                <Draggable
                                    draggableId={student.studentId.toString()}
                                    index={index}
                                    key={index}
                                    isDragDisabled={notDraggable}
                                >
                                    {(provided, snapshot) => (
                                        <div
                                            key={student.studentId}
                                            ref={provided.innerRef}
                                            {...provided.draggableProps}
                                            {...provided.dragHandleProps}
                                        >
                                            <StudentCard
                                                key={student.studentId}
                                                student={student}
                                            />
                                        </div>
                                    )}
                                </Draggable>
                            ))}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </InfiniteScroll>
        </StudentCardsList>
    );
}
