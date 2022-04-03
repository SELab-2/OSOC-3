import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { UsersPageDiv, AdminsButton, UsersHeader } from "./styles";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/PendingRequests";

/**
 * Page for admins to manage coach and admin settings.
 */
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
