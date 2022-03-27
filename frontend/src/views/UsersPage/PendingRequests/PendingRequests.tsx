import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import {
    RequestHeader,
    RequestsTable,
    PendingRequestsContainer,
    AcceptButton,
    RejectButton,
} from "./styles";
import { acceptRequest, getRequests, rejectRequest, Request } from "../../../utils/api/users";
import { Spinner } from "react-bootstrap";

function RequestsHeader() {
    // TODO: Search field when out-folded
    return <RequestHeader>Requests</RequestHeader>;
}

function AcceptReject(props: { request_id: number }) {
    return (
        <div>
            <AcceptButton onClick={() => acceptRequest(props.request_id)}>Accept</AcceptButton>
            <RejectButton onClick={() => rejectRequest(props.request_id)}>Reject</RejectButton>
        </div>
    );
}

function RequestItem(props: { request: Request }) {
    return (
        <tr>
            <td>{props.request.user.name}</td>
            <td>{props.request.user.email}</td>
            <td>
                <AcceptReject request_id={props.request.id} />
            </td>
        </tr>
    );
}

function RequestsList(props: { requests: Request[]; loading: boolean }) {
    if (props.loading) {
        return <Spinner animation="border" />;
    } else if (props.requests.length === 0) {
        return <div>No requests</div>;
    }

    const body = (
        <tbody>
            {props.requests.map(request => (
                <RequestItem request={request} />
            ))}
        </tbody>
    );
    props.requests.map(request => <RequestItem request={request} />);

    return (
        <RequestsTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Accept/Reject</th>
                </tr>
            </thead>
            {body}
        </RequestsTable>
    );
}

export default function PendingRequests(props: { edition: string | undefined }) {
    const [requests, setRequests] = useState<Request[]>([]);
    const [gettingRequests, setGettingRequests] = useState(true);

    useEffect(() => {
        getRequests(props.edition)
            .then(response => {
                setRequests(response.requests);
                setGettingRequests(false);
            })
            .catch(function (error: any) {
                console.log(error);
                setGettingRequests(false);
            });
    });

    return (
        <PendingRequestsContainer>
            <Collapsible trigger={<RequestsHeader />}>
                <RequestsList requests={requests} loading={gettingRequests} />
            </Collapsible>
        </PendingRequestsContainer>
    );
}
