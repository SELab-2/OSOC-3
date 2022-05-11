import { User } from "../../utils/api/users/users";
import { SpinnerContainer } from "../UsersComponents/Requests/styles";
import { Spinner } from "react-bootstrap";
import { AdminsTable } from "./styles";
import React from "react";
import { AdminListItem } from "./index";

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
    if (props.loading) {
        return (
            <SpinnerContainer>
                <Spinner animation="border" />
            </SpinnerContainer>
        );
    } else if (props.admins.length === 0) {
        if (props.gotData) {
            return <div>No admins</div>;
        } else {
            return null;
        }
    }

    return (
        <AdminsTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Remove</th>
                </tr>
            </thead>
        <tbody>
            {props.admins.map(admin => (
                <AdminListItem key={admin.userId} admin={admin} removeAdmin={props.removeAdmin} />
            ))}
        </tbody>
        </AdminsTable>
    );
}
