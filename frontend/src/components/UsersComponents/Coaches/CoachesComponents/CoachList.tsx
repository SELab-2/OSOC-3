import { User } from "../../../../utils/api/users/users";
import { CoachesTable, ListDiv, RemoveTh } from "../styles";
import React from "react";
import InfiniteScroll from "react-infinite-scroller";
import { CoachListItem } from "./index";

/**
 * A list of [[CoachListItem]]s.
 * @param props.coaches The list of coaches which needs to be shown.
 * @param props.loading Data is not available yet.
 * @param props.edition The edition.
 * @param props.gotData All data is received.
 * @param props.refresh A function which will be called when a coach is removed.
 * @param props.getMoreCoaches A function to load more coaches.
 */
export default function CoachList(props: {
    coaches: User[];
    loading: boolean;
    edition: string;
    gotData: boolean;
    refresh: () => void;
    getMoreCoaches: (page: number) => void;
    moreCoachesAvailable: boolean;
}) {
    return (
        <ListDiv>
            <InfiniteScroll
                pageStart={-1}
                loadMore={props.getMoreCoaches}
                hasMore={props.moreCoachesAvailable}
                loader={
                    <div className="loader" key={0}>
                        Loading ...
                    </div>
                }
                useWindow={true}
                initialLoad={true}
            >
                <CoachesTable variant="dark">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <RemoveTh>Remove from edition</RemoveTh>
                        </tr>
                    </thead>
                    <tbody>
                        {props.coaches.map(coach => (
                            <CoachListItem
                                key={coach.userId}
                                coach={coach}
                                edition={props.edition}
                                refresh={props.refresh}
                            />
                        ))}
                    </tbody>
                </CoachesTable>
            </InfiniteScroll>
        </ListDiv>
    );
}
