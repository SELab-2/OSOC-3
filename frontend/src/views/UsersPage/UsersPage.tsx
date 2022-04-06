import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { UsersPageDiv, AdminsButton, UsersHeader } from "./styles";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/PendingRequests";
import { getUsers, User } from "../../utils/api/users/users";
import { getCoaches } from "../../utils/api/users/coaches";

/**
 * Page for admins to manage coach and admin settings.
 */
function UsersPage() {
    const [allCoaches, setAllCoaches] = useState<User[]>([]); // All coaches from the edition
    const [users, setUsers] = useState<User[]>([]); // All users which are not a coach
    const [gettingData, setGettingData] = useState(false); // Waiting for data
    const [gotData, setGotData] = useState(false); // Received data
    const [error, setError] = useState(""); // Error message

    const params = useParams();
    const navigate = useNavigate();

    async function getCoachesData() {
        setGettingData(true);
        setGotData(false);
        setError("");
        try {
            const coachResponse = await getCoaches(params.edition as string);
            setAllCoaches(coachResponse.users);

            const UsersResponse = await getUsers();
            const users = [];
            for (const user of UsersResponse.users) {
                if (!coachResponse.users.some(e => e.userId === user.userId)) {
                    users.push(user);
                }
            }
            setUsers(users);

            setGotData(true);
            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingData && !error && params.edition !== undefined) {
            getCoachesData();
        }
    }, [gotData, gettingData, error, getCoachesData, params.edition]);

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
                <PendingRequests edition={params.edition} refreshCoaches={getCoachesData} />
                <Coaches
                    edition={params.edition}
                    allCoaches={allCoaches}
                    users={users}
                    refresh={getCoachesData}
                    gotData={gotData}
                    gettingData={gettingData}
                    error={error}
                />
            </UsersPageDiv>
        );
    }
}

export default UsersPage;
