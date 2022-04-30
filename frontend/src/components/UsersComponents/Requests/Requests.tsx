import React, { useState } from "react";
import Collapsible from "react-collapsible";
import { RequestsContainer, Error, RequestListContainer, SearchButton } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./RequestsComponents";
import { SearchInput } from "../../styles";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 * @param props.refreshCoaches A function which will be called when a new coach is added
 */
export default function Requests(props: { edition: string; refreshCoaches: () => void }) {
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [loading, setLoading] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in the filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [error, setError] = useState(""); // Error message
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true); // Endpoint has more requests available
    const [page, setPage] = useState(0); // The next page which needs to be fetched

    /**
     * Remove a request from the list of requests (Request is accepter or rejected).
     * When the request was accepted, the refreshCoaches will be called.
     * @param accepted Boolean to say if a coach was accepted.
     * @param request The request which was accepter or rejected.
     */
    function removeRequest(accepted: boolean, request: Request) {
        setRequests(
            requests.filter(object => {
                return object !== request;
            })
        );
        if (accepted) {
            props.refreshCoaches();
        }
    }

    /**
     * Request the next page from the list of requests.
     * The set searchterm will be used.
     */
    async function getData() {
        if (loading) {
            return;
        }
        setLoading(true);
        setError("");
        try {
            const response = await getRequests(props.edition, searchTerm, page);
            if (response.requests.length === 0) {
                setMoreRequestsAvailable(false);
            }
            if (page === 0) {
                setRequests(response.requests);
            } else {
                setRequests(requests.concat(response.requests));
            }
            setPage(page + 1);
            setGotData(true);
        } catch (exception) {
            setError("Oops, something went wrong...");
        }
        setLoading(false);
    }

    /**
     * Delete all found request and reset searching
     */
    function refresh() {
        setRequests([]);
        setPage(0);
        setMoreRequestsAvailable(true);
        setGotData(false);
    }

    let list;
    if (error) {
        list = <Error>{error}</Error>;
    } else if (gotData && requests.length === 0) {
        list = <div>No requests found</div>;
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
        <RequestsContainer>
            <Collapsible
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <SearchInput
                    value={searchTerm}
                    onChange={e => {
                        setSearchTerm(e.target.value);
                        if (e.target.value === "") {
                            refresh();
                        }
                    }}
                    onKeyDown={e => {
                        if (e.key === "Enter") refresh();
                    }}
                />
                <SearchButton onClick={refresh}>Search</SearchButton>
                <RequestListContainer>{list}</RequestListContainer>
            </Collapsible>
        </RequestsContainer>
    );
}
