import { User } from "../../../../utils/api/users/users";
import React from "react";
import RemoveCoach from "./RemoveCoach";
import { RemoveTd } from "../styles";
import { EmailAndAuth } from "../../../Common/Users";

/**
 * An item from [[CoachList]] which represents one coach.
 * This includes a button te remove the coach.
 * @param props.coach The coach which is represented.
 * @param props.edition The edition whereof the user is coach.
 * @param props.removeCoach A function which will be called when the coach is removed.
 */
export default function CoachListItem(props: {
    coach: User;
    edition: string;
    removeCoach: (coach: User) => void;
}) {
    return (
        <tr>
            <td>{props.coach.name}</td>
            <td>
                <EmailAndAuth user={props.coach} />
            </td>
            <RemoveTd>
                <RemoveCoach
                    coach={props.coach}
                    edition={props.edition}
                    removeCoach={() => props.removeCoach(props.coach)}
                />
            </RemoveTd>
        </tr>
    );
}
