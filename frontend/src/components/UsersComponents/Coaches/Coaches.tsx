import React, { useEffect, useState } from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { getUsers, User } from "../../../utils/api/users/users";
import { Error, SearchInput } from "../PendingRequests/styles";
import { getCoaches } from "../../../utils/api/users/coaches";
import { CoachList, AddCoach } from "./CoachesComponents";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches need to be shown.
 */
export default function Coaches(props: { edition: string }) {
    const [allCoaches, setAllCoaches] = useState<User[]>([]); // All coaches from the edition
    const [coaches, setCoaches] = useState<User[]>([]); // All coaches after filter
    const [users, setUsers] = useState<User[]>([]); // All users which are not a coach
    const [gettingData, setGettingData] = useState(false); // Waiting for data
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter
    const [gotData, setGotData] = useState(false); // Received data
    const [error, setError] = useState(""); // Error message

    async function getData() {
        setGettingData(true);
        setGotData(false);
        try {
            const coachResponse = await getCoaches(props.edition);
            setAllCoaches(coachResponse.users);
            setCoaches(coachResponse.users);

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
        if (!gotData && !gettingData && !error) {
            getData();
        }
    }, [gotData, gettingData, error, getData]);

    /**
     * Apply a filter to the coach list.
     * Only keep coaches who's name contain the searchterm.
     * @param {string} word a searchterm which a coach needs to contain
     */
    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const coach of allCoaches) {
            if (coach.name.toUpperCase().includes(word.toUpperCase())) {
                newCoaches.push(coach);
            }
        }
        setCoaches(newCoaches);
    };

    return (
        <CoachesContainer>
            <CoachesTitle>Coaches</CoachesTitle>
            <SearchInput value={searchTerm} onChange={e => filter(e.target.value)} />
            <AddCoach users={users} edition={props.edition} refresh={getData} />
            <CoachList
                coaches={coaches}
                loading={gettingData}
                edition={props.edition}
                gotData={gotData}
                refresh={getData}
            />
            <Error> {error} </Error>
        </CoachesContainer>
    );
}
