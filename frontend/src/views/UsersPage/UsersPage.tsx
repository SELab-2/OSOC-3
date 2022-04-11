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
    const [coaches, setCoaches] = useState<User[]>([]); // All coaches from the edition
    const [users, setUsers] = useState<User[]>([]); // All users which are not a coach
    const [gettingData, setGettingData] = useState(false); // Waiting for data
    const [gotData, setGotData] = useState(false); // Received data
    const [error, setError] = useState(""); // Error message
    const [moreCoachesAvailable, setMoreCoachesAvailable] = useState(true);
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter

    const params = useParams();
    const navigate = useNavigate();

    async function getCoachesData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingData(true);
        setError("");
        try {
            const coachResponse = await getCoaches(params.editionId as string, filter, page);
            if (coachResponse.users.length !== 25) {
                setMoreCoachesAvailable(false);
            }
            if (page === 0) {
                setCoaches(coachResponse.users);
            } else {
                setCoaches(coaches.concat(coachResponse.users));
            }

            const usersResponse = await getUsers();
            const users: User[] = [];
            for (const user of usersResponse.users) {
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
        if (!gotData && !gettingData && !error) {
            getCoachesData(0);
        }
    });

    function filterCoachesData(searchTerm: string) {
        setGettingData(true);
        setGotData(false);
        setSearchTerm(searchTerm);
        setCoaches([]);
        setMoreCoachesAvailable(true);
        getCoachesData(0, searchTerm);
    }

    function coachAdded(coach: User) {
        if (coach.name.includes(searchTerm)) {
            setCoaches([coach].concat(coaches));
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
                <PendingRequests edition={params.editionId} coachAdded={coachAdded} />
                <Coaches
                    edition={params.editionId}
                    coaches={coaches}
                    users={users}
                    refresh={() => getCoachesData(0)}
                    gotData={gotData}
                    gettingData={gettingData}
                    error={error}
                    getMoreCoaches={getCoachesData}
                    searchCoaches={filterCoachesData}
                    moreCoachesAvailable={moreCoachesAvailable}
                    searchTerm={searchTerm}
                />
            </UsersPageDiv>
        );
    }
}

export default UsersPage;
