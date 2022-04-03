import { Request } from "../../../../utils/api/users/requests";
import { AcceptRejectTh, RequestsTable, SpinnerContainer } from "../styles";
import { Spinner } from "react-bootstrap";
import React from "react";
import RequestListItem from "./RequestListItem";

export default function RequestList(props: {
    requests: Request[];
    loading: boolean;
    gotData: boolean;
}) {
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.requests.length === 0) {
        if (props.gotData) {
            return <div>No requests</div>;
        } else {
            return null;
        }
    }

    const body = (
        <tbody>
            {props.requests.map(request => (
                <RequestListItem key={request.requestId} request={request} />
            ))}
        </tbody>
    );

    return (
        <RequestsTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <AcceptRejectTh>Accept/Reject</AcceptRejectTh>
                </tr>
            </thead>
            {body}
        </RequestsTable>
    );
}
