import React, { useEffect, useState } from "react";
import Collapsible from "react-collapsible";
import { RequestsContainer, RequestListContainer } from "./styles";
import { getRequests, Request } from "../../../utils/api/users/requests";
import { RequestList, RequestsHeader } from "./RequestsComponents";
import SearchBar from "../../Common/Forms/SearchBar";
import { SearchFieldDiv } from "../../Common/Users/styles";
import { toast } from "react-toastify";
import { LoadSpinner } from "../../Common";

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
    const [requestedEdition, setRequestedEdition] = useState(props.edition);
    const [open, setOpen] = useState(false); // Collapsible is open
    const [moreRequestsAvailable, setMoreRequestsAvailable] = useState(true); // Endpoint has more requests available
    const [allRequestsFetched, setAllRequestsFetched] = useState(false);
    const [page, setPage] = useState(0); // The next page which needs to be fetched

    const [controller, setController] = useState<AbortController | undefined>(undefined);

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
    async function getData(requested: number) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
            return;
        }

        if (allRequestsFetched) {
            setRequests(
                allRequests.filter(request =>
                    request.user.name.toUpperCase().includes(searchTerm.toUpperCase())
                )
            );
            setMoreRequestsAvailable(false);
            return;
        }

        setLoading(true);

        if (controller !== undefined) {
            controller.abort();
        }
        const newController = new AbortController();
        setController(newController);

        const response = await toast.promise(
            getRequests(props.edition, searchTerm, page, newController),
            {
                error: "Failed to retrieve requests",
            }
        );

        if (response !== null) {
            if (response.requests.length === 0 && !filterChanged) {
                setMoreRequestsAvailable(false);
            }
            if (requestedPage === 0 || filterChanged) {
                setRequests(response.requests);
            } else {
                setRequests(requests.concat(response.requests));
            }

            if (searchTerm === "") {
                if (response.requests.length === 0) {
                    setAllRequestsFetched(true);
                }
                if (requestedPage === 0) {
                    setAllRequests(response.requests);
                } else {
                    setAllRequests(allRequests.concat(response.requests));
                }
            }

            setPage(page + 1);
        } else {
            setMoreRequestsAvailable(false);
        }
        setLoading(false);
    }

    useEffect(() => {
        setPage(0);
        setMoreRequestsAvailable(true);
        if (props.edition !== requestedEdition) {
            setAllRequestsFetched(false);
            setRequests([]);
        }
        getData(-1);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchTerm, props.edition]);

    let list;
    if (requests.length === 0) {
        if (loading) {
            list = <LoadSpinner show={true} />;
        }
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
                            setPage(0);
                            setSearchTerm(e.target.value);
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
