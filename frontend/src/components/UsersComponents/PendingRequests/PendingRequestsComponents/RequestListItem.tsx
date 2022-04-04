import { Request } from "../../../../utils/api/users/requests";
import React from "react";
import AcceptReject from "./AcceptReject";

/**
 * An item from [[RequestList]] which represents one request.
 * This includes two buttons to accept and reject the request.
 * @param props.request The request which is represented.
 */
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
