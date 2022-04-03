import { AcceptButton, RejectButton } from "../styles";
import { acceptRequest, rejectRequest } from "../../../../utils/api/users/requests";
import React from "react";

export default function AcceptReject(props: { requestId: number }) {
    return (
        <div>
            <AcceptButton onClick={() => acceptRequest(props.requestId)}>Accept</AcceptButton>
            <RejectButton onClick={() => rejectRequest(props.requestId)}>Reject</RejectButton>
        </div>
    );
}
