import { Request, acceptRequest, rejectRequest } from "../../../../utils/api/users/requests";
import React from "react";
import CreateButton from "../../../Common/Buttons/CreateButton";
import DeleteButton from "../../../Common/Buttons/DeleteButton";
import { Spacing } from "../styles";
import { toast } from "react-toastify";

/**
 * Component consisting of two buttons to accept or reject a coach request.
 * @param props.request The request which can be accepted/rejected.
 * @param props.removeRequest A function which will be called when a request is accepted/rejected.
 */
export default function AcceptReject(props: {
    request: Request;
    removeRequest: (coachAdded: boolean, request: Request) => void;
}) {
    async function accept() {
        const success = await toast.promise(acceptRequest(props.request.requestId), {
            error: "Failed to accept request",
            pending: "Accepting request",
        });
        if (!success) {
            toast.error("Failed to accept request", {
                toastId: "accept_request_failed",
            });
        }

        if (success) {
            props.removeRequest(true, props.request);
        }
    }

    async function reject() {
        const success = await toast.promise(rejectRequest(props.request.requestId), {
            error: "Failed to reject request",
            pending: "Rejecting request",
        });
        if (!success) {
            toast.error("Failed to reject request", {
                toastId: "reject_request_failed",
            });
        }

        if (success) {
            props.removeRequest(false, props.request);
        }
    }

    return (
        <div>
            <CreateButton onClick={accept} showIcon={false}>
                Accept
            </CreateButton>
            <Spacing />
            <DeleteButton onClick={reject} showIcon={false}>
                Reject
            </DeleteButton>
        </div>
    );
}
