import { User } from "../../../../utils/api/users/users";
import { SpinnerContainer } from "../../PendingRequests/styles";
import { Spinner } from "react-bootstrap";
import { CoachesTable } from "../styles";
import React from "react";
import { CoachItem } from "./index";

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
                <CoachItem
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
                    <th>Remove from edition</th>
                </tr>
            </thead>
            {body}
        </CoachesTable>
    );
}
