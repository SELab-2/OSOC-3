import React, { useState } from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { User } from "../../../utils/api/users/users";
import { Error, SearchInput } from "../PendingRequests/styles";
import { CoachList, AddCoach } from "./CoachesComponents";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches need to be shown.
 * @param props.allCoaches The list of all coaches of the current edition.
 * @param props.users A list of all users who can be added as coach.
 * @param props.refresh A function which will be called when a coach is added/removed.
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.gotData All data is received.
 * @param props.gettingData Data is not available yet.
 * @param props.error An error message.
 */
export default function Coaches(props: {
    edition: string;
    allCoaches: User[];
    users: User[];
    refresh: () => void;
    getMoreCoaches: (page: number) => void;
    gotData: boolean;
    gettingData: boolean;
    error: string;
    moreCoachesAvailable: boolean;
}) {
    // const [coaches, setCoaches] = useState<User[]>([]); // All coaches after filter
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter

    /**
     * Apply a filter to the coach list.
     * Only keep coaches who's name contain the searchterm.
     * @param {string} word a searchterm which a coach needs to contain
     */
    const filter = (word: string) => {
        setSearchTerm(word);
        const newCoaches: User[] = [];
        for (const coach of props.allCoaches) {
            if (coach.name.toUpperCase().includes(word.toUpperCase())) {
                newCoaches.push(coach);
            }
        }
        // setCoaches(newCoaches);
    };

    return (
        <CoachesContainer>
            <CoachesTitle>Coaches</CoachesTitle>
            <SearchInput value={searchTerm} onChange={e => filter(e.target.value)} />
            <AddCoach users={props.users} edition={props.edition} refresh={props.refresh} />
            <CoachList
                coaches={props.allCoaches}
                loading={props.gettingData}
                edition={props.edition}
                gotData={props.gotData}
                refresh={props.refresh}
                getMoreCoaches={props.getMoreCoaches}
                moreCoachesAvailable={props.moreCoachesAvailable}
            />
            <Error> {props.error} </Error>
        </CoachesContainer>
    );
}
