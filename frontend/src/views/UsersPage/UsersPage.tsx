import React from "react";
import { InviteUser } from "./InviteUser";
import { PendingRequests } from "./PendingRequests";
import { Coaches } from "./Coaches";
import { useParams } from "react-router-dom";

function UsersPage() {
    const params = useParams();

    if (params.edition === undefined) {
        return <div>Error</div>;
    } else {
        return (
            <div>
                <InviteUser edition={params.edition} />
                <PendingRequests edition={params.edition} />
                <Coaches edition={params.edition} />
            </div>
        );
    }
}

export default UsersPage;
