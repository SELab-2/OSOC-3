import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { UsersPageDiv, UsersHeader } from "./styles";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/Requests";
import { User } from "../../utils/api/users/users";
import { getCoaches } from "../../utils/api/users/coaches";

/**
 * Page for admins to manage coach and admin settings.
 */
function UsersPage() {
    // Note: The coaches are not in the coaches component because accepting a request needs to refresh the coaches list.
    const [coaches, setCoaches] = useState<User[]>([]); // All coaches from the selected edition
    const [gettingData, setGettingData] = useState(false); // Waiting for data (used for spinner)
    const [gotData, setGotData] = useState(false); // Received data
    const [error, setError] = useState(""); // Error message
    const [moreCoachesAvailable, setMoreCoachesAvailable] = useState(true); // Endpoint has more coaches available
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter for coachlist

    const params = useParams();

    /**
     * Request a page from the list of coaches.
     * An optional filter can be used to filter the username.
     * If the filter is not used, the string saved in the "searchTerm" state will be used.
     * @param page The page to load.
     * @param filter Optional string to filter username.
     */
    async function getCoachesData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingData(true);
        setError("");
        try {
            const coachResponse = await getCoaches(params.editionId as string, filter, page);
            if (coachResponse.users.length === 0) {
                setMoreCoachesAvailable(false);
            }
            if (page === 0) {
                setCoaches(coachResponse.users);
            } else {
                setCoaches(coaches.concat(coachResponse.users));
            }

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

    /**
     * Set the searchTerm and request the first page with this filter.
     * The current list of coaches will be resetted.
     * @param searchTerm The string to filter coaches with by username.
     */
    function filterCoachesData(searchTerm: string) {
        setGotData(false);
        setSearchTerm(searchTerm);
        setCoaches([]);
        setMoreCoachesAvailable(true);
        getCoachesData(0, searchTerm);
    }

    /**
     * Reset the list of coaches and get the first page.
     * Used when a new coach is added.
     */
    function refreshCoaches() {
        setGotData(false);
        setCoaches([]);
        setMoreCoachesAvailable(true);
        getCoachesData(0);
    }

    /**
     * Remove a coach from the list of coaches.
     * @param coach The coach which needs to be deleted.
     */
    function removeCoach(coach: User) {
        setCoaches(
            coaches.filter(object => {
                return object !== coach;
            })
        );
    }

    if (params.editionId === undefined) {
        // If this happens, User should be redirected to error page
        return <div>Error</div>;
    } else {
        return (
            <UsersPageDiv>
                <div>
                    <UsersHeader>
                        <h1>Manage coaches from {params.editionId}</h1>
                    </UsersHeader>
                </div>
                <InviteUser edition={params.editionId} />
                <PendingRequests edition={params.editionId} refreshCoaches={refreshCoaches} />
                <Coaches
                    edition={params.editionId}
                    coaches={coaches}
                    gotData={gotData}
                    gettingData={gettingData}
                    error={error}
                    getMoreCoaches={getCoachesData}
                    searchCoaches={filterCoachesData}
                    moreCoachesAvailable={moreCoachesAvailable}
                    searchTerm={searchTerm}
                    refreshCoaches={refreshCoaches}
                    removeCoach={removeCoach}
                />
            </UsersPageDiv>
        );
    }
}

export default UsersPage;
