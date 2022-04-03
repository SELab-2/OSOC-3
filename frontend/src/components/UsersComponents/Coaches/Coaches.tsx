import React, { useEffect, useState } from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { getUsers, User } from "../../../utils/api/users/users";
import { Error, SearchInput } from "../PendingRequests/styles";
import { getCoaches } from "../../../utils/api/users/coaches";
import { CoachList, AddCoach } from "./CoachesComponents";

/**
 *
 * @param props
 * @constructor
 */
export default function Coaches(props: { edition: string }) {
    const [allCoaches, setAllCoaches] = useState<User[]>([]);
    const [coaches, setCoaches] = useState<User[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [gettingData, setGettingData] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");

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
