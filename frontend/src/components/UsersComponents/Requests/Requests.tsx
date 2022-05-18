import React, { useState } from "react";
import Collapsible from "react-collapsible";
import { RequestsContainer, RequestListContainer } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./RequestsComponents";
import SearchBar from "../../Common/Forms/SearchBar";
import { SearchFieldDiv } from "../../Common/Users/styles";
import { toast } from "react-toastify";

/**
 * A collapsible component which contains all coach requests for a given edition.
 * Every request can be accepted or rejected.
 * @param props.edition The edition.
 * @param props.refreshCoaches A function which will be called when a new coach is added
 */
export default function Requests(props: { edition: string; refreshCoaches: () => void }) {
    const [allRequests, setAllRequests] = useState<Request[]>([]);
    const [requests, setRequests] = useState<Request[]>([]); // All requests after filter
    const [loading, setLoading] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in the filter
    const [gotData, setGotData] = useState(false); // Received data
    const [open, setOpen] = useState(false); // Collapsible is open
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true); // Endpoint has more requests available
    const [allRequestsFetched, setAllRequestsFetched] = useState(false);
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
        setAllRequests(
            allRequests.filter(object => {
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

        if (allRequestsFetched) {
            setGotData(true);
            setRequests(
                allRequests.filter(request =>
                    request.user.name.toUpperCase().includes(searchTerm.toUpperCase())
                )
            );
            setMoreRequestsAvailable(false);
            return;
        }

        setLoading(true);

        const response = await toast.promise(getRequests(props.edition, searchTerm, page), {
            error: "Failed to retrieve requests",
        });

        if (response.requests.length === 0) {
            setMoreRequestsAvailable(false);
        }
        if (page === 0) {
            setRequests(response.requests);
        } else {
            setRequests(requests.concat(response.requests));
        }

        if (searchTerm === "") {
            if (response.requests.length === 0) {
                setAllRequestsFetched(true);
            }
            if (page === 0) {
                setAllRequests(response.requests);
            } else {
                setAllRequests(allRequests.concat(response.requests));
            }
        }

        setPage(page + 1);

        setGotData(true);
        setLoading(false);
    }

    function filter(searchTerm: string) {
        setPage(0);
        setGotData(false);
        setMoreRequestsAvailable(true);
        setSearchTerm(searchTerm);
        setRequests([]);
    }

    let list;
    if (gotData && requests.length === 0) {
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
                <SearchFieldDiv>
                    <SearchBar
                        onChange={e => {
                            filter(e.target.value);
                        }}
                        value={searchTerm}
                        placeholder="Search name..."
                    />
                </SearchFieldDiv>
                <RequestListContainer>{list}</RequestListContainer>
            </Collapsible>
        </RequestsContainer>
    );
}
