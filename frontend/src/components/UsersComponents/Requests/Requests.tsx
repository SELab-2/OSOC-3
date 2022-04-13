import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import { RequestsContainer, Error, SpinnerContainer, RequestListContainer } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./RequestsComponents";
import { Spinner } from "react-bootstrap";
import { SearchInput } from "../../styles";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 * @param props.refreshCoaches A function which will be called when a new coach is added
 */
export default function Requests(props: { edition: string; refreshCoaches: () => void }) {
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [gettingRequests, setGettingRequests] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in the filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [error, setError] = useState(""); // Error message
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true); // Endpoint has more requests available

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
     * Request a page from the list of requests.
     * An optional filter can be used to filter the username.
     * If the filter is not used, the string saved in the "searchTerm" state will be used.
     * @param page The page to load.
     * @param filter Optional string to filter username.
     */
    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingRequests(true);
        setError("");
        try {
            const response = await getRequests(props.edition, filter, page);
            if (response.requests.length === 0) {
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
    });

    /**
     * Set the searchTerm and request the first page with this filter.
     * The current list of requests will be resetted.
     * @param searchTerm The string to filter coaches with by username.
     */
    function filterRequests(searchTerm: string) {
        setGotData(false);
        setSearchTerm(searchTerm);
        setRequests([]);
        setMoreRequestsAvailable(true);
        getData(0, searchTerm);
    }

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
        <RequestsContainer>
            <Collapsible
                trigger={<RequestsHeader open={open} />}
                onOpening={() => setOpen(true)}
                onClosing={() => setOpen(false)}
            >
                <SearchInput value={searchTerm} onChange={e => filterRequests(e.target.value)} />
                <RequestListContainer>{list}</RequestListContainer>
            </Collapsible>
        </RequestsContainer>
    );
}
