import { User } from "../../../../utils/api/users/users";
import { CoachesTable, ListDiv, RemoveTh } from "../styles";
import React from "react";
import InfiniteScroll from "react-infinite-scroller";
import { CoachListItem } from "./index";
import LoadSpinner from "../../../Common/LoadSpinner";

/**
 * A list of [[CoachListItem]]s.
 * @param props.coaches The list of coaches which needs to be shown.
 * @param props.edition The edition.
 * @param props.removeCoach A function which will be called when a coach is removed.
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.moreCoachesAvailable More unfetched coaches available.
 */
export default function CoachList(props: {
    coaches: User[];
    edition: string;
    removeCoach: (coach: User) => void;
    getMoreCoaches: () => void;
    moreCoachesAvailable: boolean;
}) {
    return (
        <ListDiv>
            <InfiniteScroll
                pageStart={0}
                loadMore={props.getMoreCoaches}
                hasMore={props.moreCoachesAvailable}
                loader={<LoadSpinner show={true} />}
                useWindow={false}
                initialLoad={true}
            >
                <CoachesTable>
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
                                removeCoach={props.removeCoach}
                            />
                        ))}
                    </tbody>
                </CoachesTable>
            </InfiniteScroll>
        </ListDiv>
    );
}
