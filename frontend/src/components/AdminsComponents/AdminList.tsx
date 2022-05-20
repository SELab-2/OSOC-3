import { User } from "../../utils/api/users/users";
import { AdminsTable } from "./styles";
import React from "react";
import { AdminListItem } from "./index";
import { ListDiv } from "../Common/Users/styles";
import { RemoveTh } from "../Common/Tables/styles";

/**
 * List of [[AdminListItem]]s which represents all admins.
 * @param props.admins List of all users who are admin.
 * @param props.loading Data is being fetched.
 * @param props.gotData Data is received.
 * @param props.removeAdmin Function which will be called after deleting an admin.
 * @constructor
 */
export default function AdminList(props: {
    admins: User[];
    loading: boolean;
    gotData: boolean;
    removeAdmin: (user: User) => void;
}) {
    return (
        <ListDiv>
            <AdminsTable>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <RemoveTh>Remove</RemoveTh>
                    </tr>
                </thead>
                <tbody>
                    {props.admins.map(admin => (
                        <AdminListItem
                            key={admin.userId}
                            admin={admin}
                            removeAdmin={props.removeAdmin}
                        />
                    ))}
                </tbody>
            </AdminsTable>
        </ListDiv>
    );
}
