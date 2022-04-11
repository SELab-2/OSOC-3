import { AcceptButton, RejectButton } from "../styles";
import { Request, acceptRequest, rejectRequest } from "../../../../utils/api/users/requests";
import React, { useState } from "react";
import { Spinner } from "react-bootstrap";

/**
 * Component consisting of two buttons to accept or reject a coach request.
 * @param props.requestId The id of the request.
 * @param props.refresh A function which will be called when a request is accepted/rejected.
 */
export default function AcceptReject(props: {
    request: Request;
    refresh: (coachAdded: boolean, request: Request) => void;
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
            props.refresh(true, props.request);
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
            props.refresh(false, props.request);
        }
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (loading) {
        return <Spinner animation="border" />;
    }

    return (
        <div>
            <AcceptButton onClick={accept}>Accept</AcceptButton>
            <RejectButton onClick={reject}>Reject</RejectButton>
        </div>
    );
}
