import { User } from "../../utils/api/users/users";
import React from "react";
import { RemoveAdmin } from "./index";
import { EmailAndAuth } from "../GeneralComponents";

/**
 * An item from [[AdminList]]. Contains the credentials of an admin and a button to remove the admin.
 * @param props.admin The user which is represented.
 * @param props.removeAdmin A function which will be called after removing an admin.
 */
export default function AdminItem(props: { admin: User; removeAdmin: (user: User) => void }) {
    return (
        <tr>
            <td>{props.admin.name}</td>
            <td>
                <EmailAndAuth user={props.admin} />
            </td>
            <td>
                <RemoveAdmin admin={props.admin} removeAdmin={props.removeAdmin} />
            </td>
        </tr>
    );
}
