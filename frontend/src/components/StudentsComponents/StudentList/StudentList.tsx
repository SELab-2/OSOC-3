import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";
import { Student } from "../../../data/interfaces/students";
import { SpinnerContainer } from "../../UsersComponents/Requests/styles";
import { Spinner } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroller";

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
    return (
        <StudentCardsList>
            <InfiniteScroll
                loadMore={props.getMoreData}
                hasMore={props.moreDataAvailable}
                loader={
                    <SpinnerContainer key={"spinner"}>
                        <Spinner animation="border" />
                    </SpinnerContainer>
                }
                useWindow={false}
                initialLoad={true}
            >
                {props.students.map(student => (
                    <StudentCard key={student.studentId} student={student} />
                ))}
            </InfiniteScroll>
        </StudentCardsList>
    );
}
