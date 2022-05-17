import { Request } from "../../../../utils/api/users/requests";
import { AcceptRejectTh, RequestsTable } from "../styles";
import React from "react";
import RequestListItem from "./RequestListItem";
import InfiniteScroll from "react-infinite-scroller";
import LoadSpinner from "../../../Common/LoadSpinner";
import { ListDiv } from "../../../Common/Users/styles";

/**
 * A list of [[RequestListItem]]s.
 * @param props.requests A list of requests which need to be shown.
 * @param props.removeRequest A function which will be called when a request is accepted/rejected.
 * @param props.moreRequestsAvailable Boolean to indicate whether more requests can be fetched
 * @param props.getMoreRequests A function which will be called when more requests need to be loaded.
 */
export default function RequestList(props: {
    requests: Request[];
    removeRequest: (coachAdded: boolean, request: Request) => void;
    moreRequestsAvailable: boolean;
    getMoreRequests: () => void;
}) {
    return (
        <ListDiv>
            <InfiniteScroll
                pageStart={0}
                loadMore={props.getMoreRequests}
                hasMore={props.moreRequestsAvailable}
                loader={<LoadSpinner show={true} key="spinner" />}
                useWindow={false}
                initialLoad={true}
            >
                <RequestsTable>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <AcceptRejectTh>Accept/Reject</AcceptRejectTh>
                        </tr>
                    </thead>
                    <tbody>
                        {props.requests.map(request => (
                            <RequestListItem
                                key={request.requestId}
                                request={request}
                                removeRequest={props.removeRequest}
                            />
                        ))}
                    </tbody>
                </RequestsTable>
            </InfiniteScroll>
        </ListDiv>
    );
}
