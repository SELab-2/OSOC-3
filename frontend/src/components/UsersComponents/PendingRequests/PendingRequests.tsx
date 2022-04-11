import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import {
    PendingRequestsContainer,
    Error,
    SearchInput,
    SpinnerContainer,
    RequestListContainer,
} from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./PendingRequestsComponents";
import { User } from "../../../utils/api/users/users";
import { Spinner } from "react-bootstrap";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 * @param props.coachAdded A funciton to call when a new coach is added
 */
export default function PendingRequests(props: {
    edition: string;
    coachAdded: (user: User) => void;
}) {
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [gettingRequests, setGettingRequests] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [error, setError] = useState(""); // Error message
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true);

    function removeRequest(coachAdded: boolean, request: Request) {
        setRequests(
            requests.filter(object => {
                return object !== request;
            })
        );
        if (coachAdded) {
            props.coachAdded(request.user);
        }
    }

    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingRequests(true);
        setError("");
        try {
            const response = await getRequests(props.edition, filter, page);
            if (response.requests.length !== 25) {
                setMoreRequestsAvailable(false);
            }
            if (page === 0) {
                setRequests(response.requests);
            } else {
                setRequests(requests.concat(response.requests));
            }

            setGotData(true);
            setGettingRequests(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingRequests(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingRequests && !error) {
            getData(0);
        }
    }, [gotData, gettingRequests, error, getData]);

    const searchRequests = (searchTerm: string) => {
        setGettingRequests(true);
        setGotData(false);
        setSearchTerm(searchTerm);
        setRequests([]);
        setMoreRequestsAvailable(true);
        getData(0, searchTerm);
    };

    let list;
    if (requests.length === 0) {
        if (gettingRequests) {
            list = (
                <SpinnerContainer>
                    <Spinner animation="border" />
                </SpinnerContainer>
            );
        } else if (gotData) {
            list = <div>No requests found</div>;
        } else {
            list = <Error>{error}</Error>;
        }
    } else {
        list = (
            <RequestList
                requests={requests}
                removeRequest={removeRequest}
                moreRequestsAvailable={moreRequestsAvailable}
                getMoreRequests={getData}
            />
        );
    }

    return (
        <PendingRequestsContainer>
            <Collapsible
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <SearchInput value={searchTerm} onChange={e => searchRequests(e.target.value)} />
                <RequestListContainer>{list}</RequestListContainer>
            </Collapsible>
        </PendingRequestsContainer>
    );
}
