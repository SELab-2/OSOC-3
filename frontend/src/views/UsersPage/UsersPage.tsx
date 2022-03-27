import React from "react";
import { InviteUser } from "./InviteUser";
import { PendingRequests } from "./PendingRequests";
import { useParams } from "react-router-dom";

function UsersPage() {
    const params = useParams();
    return (
        <div>
            <InviteUser edition={params.edition} />
            <PendingRequests edition={params.edition} />
        </div>
    );
}

export default UsersPage;
