import { Request } from "../../../../utils/api/users/requests";
import React from "react";
import AcceptReject from "./AcceptReject";
import { AcceptRejectTd } from "../styles";

/**
 * An item from [[RequestList]] which represents one request.
 * This includes two buttons to accept and reject the request.
 * @param props.request The request which is represented.
 * @param props.removeRequest A function which will be called when a request is accepted/rejected.
 */
export default function RequestListItem(props: {
    request: Request;
    removeRequest: (coachAdded: boolean, request: Request) => void;
}) {
    return (
        <tr>
            <td>{props.request.user.name}</td>
            <td>{props.request.user.auth.email}</td>
            <AcceptRejectTd>
                <AcceptReject request={props.request} refresh={props.removeRequest} />
            </AcceptRejectTd>
        </tr>
    );
}
