import { Request, acceptRequest, rejectRequest } from "../../../../utils/api/users/requests";
import React, { useState } from "react";
import LoadSpinner from "../../../Common/LoadSpinner";
import CreateButton from "../../../Common/Buttons/CreateButton";
import DeleteButton from "../../../Common/Buttons/DeleteButton";
import { Spacing } from "../styles";

/**
 * Component consisting of two buttons to accept or reject a coach request.
 * @param props.request The request which can be accepted/rejected.
 * @param props.removeRequest A function which will be called when a request is accepted/rejected.
 */
export default function AcceptReject(props: {
    request: Request;
    removeRequest: (coachAdded: boolean, request: Request) => void;
}) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function accept() {
        setLoading(true);
        let success = false;
        try {
            success = await acceptRequest(props.request.requestId);
            if (!success) {
                setError("Failed to accept");
            }
        } catch (exception) {
            setError("Failed to accept");
        }
        setLoading(false);
        if (success) {
            props.removeRequest(true, props.request);
        }
    }

    async function reject() {
        setLoading(true);
        let success = false;
        try {
            success = await rejectRequest(props.request.requestId);
            if (!success) {
                setError("Failed to reject");
            }
        } catch (exception) {
            setError("Failed to reject");
        }
        setLoading(false);
        if (success) {
            props.removeRequest(false, props.request);
        }
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (loading) {
        return <LoadSpinner show={true} />;
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
