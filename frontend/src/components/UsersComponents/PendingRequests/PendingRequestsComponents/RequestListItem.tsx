import { Request } from "../../../../utils/api/users/requests";
import React from "react";
import AcceptReject from "./AcceptReject";

export default function RequestListItem(props: { request: Request }) {
    return (
        <tr>
            <td>{props.request.user.name}</td>
            <td>{props.request.user.email}</td>
            <td>
                <AcceptReject requestId={props.request.requestId} />
            </td>
        </tr>
    );
}
