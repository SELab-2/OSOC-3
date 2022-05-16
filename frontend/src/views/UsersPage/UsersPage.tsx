import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/Requests";
import { User } from "../../utils/api/users/users";
import { getCoaches } from "../../utils/api/users/coaches";
import axios from "axios";

/**
 * Page for admins to manage coach and admin settings.
 */
function UsersPage() {
    // Note: The coaches are not in the coaches component because accepting a request needs to refresh the coaches list.
    const [allCoaches, setAllCoaches] = useState<User[]>([]);
    const [coaches, setCoaches] = useState<User[]>([]); // All coaches from the selected edition
    const [loading, setLoading] = useState(false); // Waiting for data (used for spinner)
    const [gotData, setGotData] = useState(false); // Received data
    const [error, setError] = useState(""); // Error message
    const [moreCoachesAvailable, setMoreCoachesAvailable] = useState(true); // Endpoint has more coaches available
    const [allCoachesFetched, setAllCoachesFetched] = useState(false);
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter for coachlist
    const [page, setPage] = useState(0); // The next page to request

    const params = useParams();
    const navigate = useNavigate();

    /**
     * Request the next page from the list of coaches.
     * The set searchterm will be used.
     */
    async function getCoachesData() {
        if (loading) {
            return;
        }

        if (allCoachesFetched) {
            setCoaches(
                allCoaches.filter(coach =>
                    coach.name.toUpperCase().includes(searchTerm.toUpperCase())
                )
            );
            setMoreCoachesAvailable(false);
            return;
        }

        setLoading(true);
        setError("");

        let notFoundError = false;

        try {
            const response = await getCoaches(params.editionId as string, searchTerm, page);
            if (response.users.length === 0) {
                setMoreCoachesAvailable(false);
            }
            if (page === 0) {
                setCoaches(response.users);
            } else {
                setCoaches(coaches.concat(response.users));
            }

            if (searchTerm === "") {
                if (response.users.length === 0) {
                    setAllCoachesFetched(true);
                }
                if (page === 0) {
                    setAllCoaches(response.users);
                } else {
                    setAllCoaches(allCoaches.concat(response.users));
                }
            }

            setPage(page + 1);
            setGotData(true);
        } catch (error) {
            setError("Oops, something went wrong...");

            if (axios.isAxiosError(error) && error.response?.status === 404) {
                notFoundError = true;
            }
        }
        setLoading(false);
        if (notFoundError) {
            // Navigate must be at end of function
            navigate("/404-not-found");
        }
    }

    /**
     * Set the searchTerm and request the first page with this filter.
     * The current list of coaches will be resetted.
     * @param searchTerm The string to filter coaches with by username.
     */
    function filterCoachesData(searchTerm: string) {
        setPage(0);
        setGotData(false);
        setMoreCoachesAvailable(true);
        setSearchTerm(searchTerm);
        setCoaches([]);
    }

    /**
     * Reset the list of coaches and get the first page.
     * Used when a new coach is added.
     */
    function refreshCoaches() {
        setCoaches([]);
        setPage(0);
        setAllCoachesFetched(false);
        setGotData(false);
        setMoreCoachesAvailable(true);
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
            <div>
                <InviteUser edition={params.editionId} />
                <PendingRequests edition={params.editionId} refreshCoaches={refreshCoaches} />
                <Coaches
                    edition={params.editionId}
                    coaches={coaches}
                    gotData={gotData}
                    error={error}
                    getMoreCoaches={getCoachesData}
                    searchCoaches={filterCoachesData}
                    moreCoachesAvailable={moreCoachesAvailable}
                    searchTerm={searchTerm}
                    refreshCoaches={refreshCoaches}
                    removeCoach={removeCoach}
                />
            </div>
        );
    }
}

export default UsersPage;
