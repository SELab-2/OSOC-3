import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import { PendingRequestsContainer, Error, SearchInput } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./PendingRequestsComponents";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 */
export default function PendingRequests(props: { edition: string; refreshCoaches: () => void }) {
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [gettingRequests, setGettingRequests] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [error, setError] = useState(""); // Error message
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true);

    function refresh(coachAdded: boolean) {
        // TODO
        getData(0);
        if (coachAdded) {
            props.refreshCoaches();
        }
    }

    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
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
            setGettingRequests(true);
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

    return (
        <PendingRequestsContainer>
            <Collapsible
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <SearchInput value={searchTerm} onChange={e => searchRequests(e.target.value)} />
                <RequestList
                    requests={requests}
                    loading={gettingRequests}
                    gotData={gotData}
                    refresh={refresh}
                    moreRequestAvailable={moreRequestsAvailable}
                    getMoreRequests={getData}
                />
                <Error> {error} </Error>
            </Collapsible>
        </PendingRequestsContainer>
    );
}
