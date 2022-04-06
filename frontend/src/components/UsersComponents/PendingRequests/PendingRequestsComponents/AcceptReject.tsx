import { AcceptButton, RejectButton } from "../styles";
import { acceptRequest, rejectRequest } from "../../../../utils/api/users/requests";
import React from "react";

/**
 * Component consisting of two buttons to accept or reject a coach request.
 * @param props.requestId The id of the request.
 * @param props.refresh A function which will be called when a request is accepted/rejected.
 */
export default function AcceptReject(props: {
    requestId: number;
    refresh: (coachAdded: boolean) => void;
}) {
    async function accept() {
        await acceptRequest(props.requestId);
        props.refresh(true);
    }

    async function reject() {
        await rejectRequest(props.requestId);
        props.refresh(false);
    }

    return (
        <div>
            <AcceptButton onClick={accept}>Accept</AcceptButton>
            <RejectButton onClick={reject}>Reject</RejectButton>
        </div>
    );
}
