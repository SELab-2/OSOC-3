import React from "react";
import { InviteUser } from "./InviteUser";
import { PendingRequests } from "./PendingRequests";
import { Coaches } from "./Coaches";
import { useParams, useNavigate } from "react-router-dom";
import { UsersPageDiv, AdminsButton, UsersHeader } from "./styles";

function UsersPage() {
    const params = useParams();
    const navigate = useNavigate();

    if (params.edition === undefined) {
        return <div>Error</div>;
    } else {
        return (
            <UsersPageDiv>
                <div>
                    <UsersHeader>
                        <h1>Manage coaches from {params.edition}</h1>
                    </UsersHeader>
                    <AdminsButton onClick={() => navigate("/admins")}>Edit Admins</AdminsButton>
                </div>
                <InviteUser edition={params.edition} />
                <PendingRequests edition={params.edition} />
                <Coaches edition={params.edition} />
            </UsersPageDiv>
        );
    }
}

export default UsersPage;
