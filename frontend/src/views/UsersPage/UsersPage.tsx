import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { UsersPageDiv, AdminsButton, UsersHeader } from "./styles";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/PendingRequests";
import { User } from "../../utils/api/users/users";
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
    const [moreCoachesAvailable, setMoreCoachesAvailable] = useState(true);

    const params = useParams();
    const navigate = useNavigate();

    async function getCoachesData(page: number) {
        setGettingData(true);
        setGotData(false);
        setError("");
        try {
            const coachResponse = await getCoaches(params.editionId as string, page);
            if (coachResponse.users.length === 0) {
                setMoreCoachesAvailable(false);
            } else {
                console.log(allCoaches.length);
                setAllCoaches(allCoaches.concat(coachResponse.users));
                console.log(allCoaches.concat(coachResponse.users).length);
            }

            // const usersResponse = await getUsers();
            const users: User[] = [];
            // for (const user of usersResponse.users) {
            //     if (!coachResponse.users.some(e => e.userId === user.userId)) {
            //         users.push(user);
            //     }
            // }
            setUsers(users);

            setGotData(true);
            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    if (params.editionId === undefined) {
        return <div>Error</div>;
    } else {
        return (
            <UsersPageDiv>
                <div>
                    <UsersHeader>
                        <h1>Manage coaches from {params.editionId}</h1>
                    </UsersHeader>
                    <AdminsButton onClick={() => navigate("/admins")}>Edit Admins</AdminsButton>
                </div>
                <InviteUser edition={params.editionId} />
                <PendingRequests
                    edition={params.editionId}
                    refreshCoaches={() => getCoachesData(0)}
                />
                <Coaches
                    edition={params.editionId}
                    allCoaches={allCoaches}
                    users={users}
                    refresh={() => getCoachesData(0)}
                    gotData={gotData}
                    gettingData={gettingData}
                    error={error}
                    getMoreCoaches={getCoachesData}
                    moreCoachesAvailable={moreCoachesAvailable}
                />
            </UsersPageDiv>
        );
    }
}

export default UsersPage;
