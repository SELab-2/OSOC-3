import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import {
    RequestHeaderTitle,
    RequestHeaderDiv,
    OpenArrow,
    ClosedArrow,
    RequestsTable,
    PendingRequestsContainer,
    AcceptButton,
    RejectButton,
    SpinnerContainer,
    SearchInput,
    AcceptRejectTh,
    Error,
} from "./styles";
import {
    acceptRequest,
    getRequests,
    rejectRequest,
    Request,
} from "../../../utils/api/users/requests";
import { Spinner } from "react-bootstrap";

function Arrow(props: { open: boolean }) {
    if (props.open) {
        return <OpenArrow />;
    } else {
        return <ClosedArrow />;
    }
}

function RequestHeader(props: { open: boolean }) {
    return (
        <RequestHeaderDiv>
            <RequestHeaderTitle>Requests</RequestHeaderTitle>
            <Arrow open={props.open} />
        </RequestHeaderDiv>
    );
}

function RequestFilter(props: {
    searchTerm: string;
    filter: (key: string) => void;
    show: boolean;
}) {
    if (props.show) {
        return (
            <SearchInput value={props.searchTerm} onChange={e => props.filter(e.target.value)} />
        );
    } else {
        return null;
    }
}

function AcceptReject(props: { requestId: number }) {
    return (
        <div>
            <AcceptButton onClick={() => acceptRequest(props.requestId)}>Accept</AcceptButton>
            <RejectButton onClick={() => rejectRequest(props.requestId)}>Reject</RejectButton>
        </div>
    );
}

function RequestItem(props: { request: Request }) {
    return (
        <tr>
            <td>{props.request.user.name}</td>
            <td>{props.request.user.email}</td>
            <td>
                <AcceptReject requestId={props.request.requestId} />
            </td>
        </tr>
    );
}

function RequestsList(props: { requests: Request[]; loading: boolean; gotData: boolean }) {
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
                <RequestItem key={request.requestId} request={request} />
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

export default function PendingRequests(props: { edition: string }) {
    const [allRequests, setAllRequests] = useState<Request[]>([]);
    const [requests, setRequests] = useState<Request[]>([]);
    const [gettingRequests, setGettingRequests] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [open, setOpen] = useState(false);
    const [error, setError] = useState("");

    async function getData() {
        try {
            const response = await getRequests(props.edition);
            setAllRequests(response.requests);
            setRequests(response.requests);
            setGotData(true);
            setGettingRequests(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingRequests(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingRequests && !error) {
            setGettingRequests(true);
            getData();
        }
    }, [gotData, gettingRequests, error, getData]);

    const filter = (word: string) => {
        setSearchTerm(word);
        const newRequests: Request[] = [];
        for (const request of allRequests) {
            if (request.user.name.toUpperCase().includes(word.toUpperCase())) {
                newRequests.push(request);
            }
        }
        setRequests(newRequests);
    };

    return (
        <PendingRequestsContainer>
            <Collapsible
                trigger={<RequestHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <RequestFilter
                    searchTerm={searchTerm}
                    filter={word => filter(word)}
                    show={allRequests.length > 0}
                />
                <RequestsList requests={requests} loading={gettingRequests} gotData={gotData} />
                <Error> {error} </Error>
            </Collapsible>
        </PendingRequestsContainer>
    );
}
