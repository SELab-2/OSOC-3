import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Coaches } from "../../components/UsersComponents/Coaches";
import { InviteUser } from "../../components/UsersComponents/InviteUser";
import { PendingRequests } from "../../components/UsersComponents/Requests";
import { User } from "../../utils/api/users/users";
import { getCoaches } from "../../utils/api/users/coaches";
import { toast } from "react-toastify";

/**
 * Page for admins to manage coach and admin settings.
 */
function UsersPage() {
    // Note: The coaches are not in the coaches component because accepting a request needs to refresh the coaches list.
    const [allCoaches, setAllCoaches] = useState<User[]>([]);
    const [coaches, setCoaches] = useState<User[]>([]); // All coaches from the selected edition
    const [loading, setLoading] = useState(false); // Waiting for data (used for spinner)
    const [moreCoachesAvailable, setMoreCoachesAvailable] = useState(true); // Endpoint has more coaches available
    const [allCoachesFetched, setAllCoachesFetched] = useState(false);
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter for coachlist
    const [page, setPage] = useState(0); // The next page to request

    const [controller, setController] = useState<AbortController | undefined>(undefined);

    const params = useParams();
    const navigate = useNavigate();

    /**
     * Request the next page from the list of coaches.
     * The set searchterm will be used.
     */
    async function getCoachesData(requested: number) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
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

        if (controller !== undefined) {
            controller.abort();
        }
        const newController = new AbortController();
        setController(newController);

        const response = await toast.promise(
            getCoaches(params.editionId as string, searchTerm, requestedPage, newController),
            { error: "Failed to retrieve coaches" }
        );

        if (response !== null) {
            if (response.users.length === 0 && !filterChanged) {
                setMoreCoachesAvailable(false);
            }
            if (requestedPage === 0 || filterChanged) {
                setCoaches(response.users);
            } else {
                setCoaches(coaches.concat(response.users));
            }

            if (searchTerm === "") {
                if (response.users.length === 0) {
                    setAllCoachesFetched(true);
                }
                if (requestedPage === 0) {
                    setAllCoaches(response.users);
                } else {
                    setAllCoaches(allCoaches.concat(response.users));
                }
            }

            setPage(page + 1);
        } else {
            setMoreCoachesAvailable(false);
        }

        setLoading(false);
    }

    useEffect(() => {
        setPage(0);
        setMoreCoachesAvailable(true);
        getCoachesData(-1);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchTerm]);

    /**
     * Reset the list of coaches and get the first page.
     * Used when a new coach is added.
     */
    function refreshCoaches() {
        setCoaches([]);
        setPage(0);
        setAllCoachesFetched(false);
        setMoreCoachesAvailable(true);
        getCoachesData(-1);
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
        setAllCoaches(
            allCoaches.filter(object => {
                return object !== coach;
            })
        );
    }

    if (params.editionId === undefined) {
        navigate("/404-not-found");
        return null;
    } else {
        return (
            <div>
                <InviteUser edition={params.editionId} />
                <PendingRequests edition={params.editionId} refreshCoaches={refreshCoaches} />
                <Coaches
                    edition={params.editionId}
                    coaches={coaches}
                    loading={loading}
                    getMoreCoaches={getCoachesData}
                    searchCoaches={setSearchTerm}
                    setPage={setPage}
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
