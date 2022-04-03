import { User } from "../../../../utils/api/users/users";
import React from "react";
import RemoveCoach from "./RemoveCoach";

export default function CoachListItem(props: {
    coach: User;
    edition: string;
    refresh: () => void;
}) {
    return (
        <tr>
            <td>{props.coach.name}</td>
            <td>{props.coach.email}</td>
            <td>
                <RemoveCoach coach={props.coach} edition={props.edition} refresh={props.refresh} />
            </td>
        </tr>
    );
}
