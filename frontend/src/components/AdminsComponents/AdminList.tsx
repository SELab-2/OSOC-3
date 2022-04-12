import { User } from "../../utils/api/users/users";
import { SpinnerContainer } from "../UsersComponents/PendingRequests/styles";
import { Spinner } from "react-bootstrap";
import { AdminsTable } from "./styles";
import React from "react";
import { AdminListItem } from "./index";

/**
 * List of [[AdminListItem]]s which represents all admins.
 * @param props.admins List of all users who are admin.
 * @param props.loading Data is being fetched.
 * @param props.gotData Data is received.
 * @param props.refresh Function which will be called after deleting an admin.
 * @constructor
 */
export default function AdminList(props: {
    admins: User[];
    loading: boolean;
    gotData: boolean;
    refresh: () => void;
    getMoreAdmins: (page: number) => void;
    moreAdminsAvailable: boolean;
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

    const body = (
        <tbody>
            {props.admins.map(admin => (
                <AdminListItem key={admin.userId} admin={admin} refresh={props.refresh} />
            ))}
        </tbody>
    );

    return (
        <AdminsTable variant="dark">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Remove</th>
                </tr>
            </thead>
            {body}
        </AdminsTable>
    );
}
