import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import { PendingRequestsContainer, Error } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestFilter, RequestList, RequestsHeader } from "./PendingRequestsComponents";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 */
export default function PendingRequests(props: { edition: string; refreshCoaches: () => void }) {
    const [allRequests, setAllRequests] = useState<Request[]>([]); // All requests for the given edition
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [gettingRequests, setGettingRequests] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [error, setError] = useState(""); // Error message

    function refresh(coachAdded: boolean) {
        getData();
        if (coachAdded) {
            props.refreshCoaches();
        }
    }

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
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <RequestFilter
                    searchTerm={searchTerm}
                    filter={word => filter(word)}
                    show={allRequests.length > 0}
                />
                <RequestList
                    requests={requests}
                    loading={gettingRequests}
                    gotData={gotData}
                    refresh={refresh}
                />
                <Error> {error} </Error>
            </Collapsible>
        </PendingRequestsContainer>
    );
}
