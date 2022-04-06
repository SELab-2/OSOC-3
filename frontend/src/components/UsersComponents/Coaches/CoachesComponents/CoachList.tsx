import { User } from "../../../../utils/api/users/users";
import { SpinnerContainer } from "../../PendingRequests/styles";
import { Spinner } from "react-bootstrap";
import { CoachesTable, RemoveTh } from "../styles";
import React from "react";
import { CoachListItem } from "./index";

/**
 * A list of [[CoachListItem]]s.
 * @param props.coaches The list of coaches which needs to be shown.
 * @param props.loading Data is not available yet.
 * @param props.edition The edition.
 * @param props.gotData All data is received.
 * @param props.refresh A function which will be called when a coach is removed.
 */
export default function CoachList(props: {
    coaches: User[];
    loading: boolean;
    edition: string;
    gotData: boolean;
    refresh: () => void;
}) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.coaches.length === 0) {
        if (props.gotData) {
            return <div>No coaches for this edition</div>;
        } else {
            return null;
        }
    }

    const body = (
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
    );

    return (
        <CoachesTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <RemoveTh>Remove from edition</RemoveTh>
                </tr>
            </thead>
            {body}
        </CoachesTable>
    );
}
