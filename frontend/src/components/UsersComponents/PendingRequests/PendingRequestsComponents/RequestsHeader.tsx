import { ClosedArrow, OpenArrow, RequestHeaderDiv, RequestHeaderTitle } from "../styles";
import React from "react";

/**
 * Arrow to indicate the status of the collapsible component.
 * @param props.open Boolean to indicate if the collapsible is open.
 */
function Arrow(props: { open: boolean }) {
    if (props.open) {
        return <OpenArrow />;
    } else {
        return <ClosedArrow />;
    }
}

/**
 * The header of [[PendingRequests]].
 * @param props.open Boolean to indicate if the collapsible is open.
 */
export default function RequestsHeader(props: { open: boolean }) {
    return (
        <RequestHeaderDiv>
            <RequestHeaderTitle>Requests</RequestHeaderTitle>
            <Arrow open={props.open} />
        </RequestHeaderDiv>
    );
}
