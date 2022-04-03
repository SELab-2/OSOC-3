import { ClosedArrow, OpenArrow, RequestHeaderDiv, RequestHeaderTitle } from "../styles";
import React from "react";

function Arrow(props: { open: boolean }) {
    if (props.open) {
        return <OpenArrow />;
    } else {
        return <ClosedArrow />;
    }
}

export default function RequestsHeader(props: { open: boolean }) {
    return (
        <RequestHeaderDiv>
            <RequestHeaderTitle>Requests</RequestHeaderTitle>
            <Arrow open={props.open} />
        </RequestHeaderDiv>
    );
}
