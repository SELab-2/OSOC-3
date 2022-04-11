import React from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { User } from "../../../utils/api/users/users";
import { Error, SearchInput, SpinnerContainer } from "../PendingRequests/styles";
import { CoachList, AddCoach } from "./CoachesComponents";
import { Spinner } from "react-bootstrap";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches need to be shown.
 * @param props.coaches The list of all coaches of the current edition.
 * @param props.refresh A function which will be called when a coach is added/removed.
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.gotData All data is received.
 * @param props.gettingData Data is not available yet.
 * @param props.error An error message.
 * @param props.moreCoachesAvailable More unfetched coaches available.
 * @param props.searchTerm Current filter for coaches' names.
 */
export default function Coaches(props: {
    edition: string;
    coaches: User[];
    refresh: () => void;
    getMoreCoaches: (page: number) => void;
    searchCoaches: (word: string) => void;
    gotData: boolean;
    gettingData: boolean;
    error: string;
    moreCoachesAvailable: boolean;
    searchTerm: string;
    coachAdded: (user: User) => void;
}) {
    let table;
    if (props.coaches.length === 0) {
        if (props.gettingData) {
            table = (
                <SpinnerContainer>
                    <Spinner animation="border" />
                </SpinnerContainer>
            );
        } else if (props.gotData) {
            table = <div>No coaches found</div>;
        } else {
            table = <Error> {props.error} </Error>;
        }
    } else {
        table = (
            <CoachList
                coaches={props.coaches}
                loading={props.gettingData}
                edition={props.edition}
                gotData={props.gotData}
                refresh={props.refresh}
                getMoreCoaches={props.getMoreCoaches}
                moreCoachesAvailable={props.moreCoachesAvailable}
            />
        );
    }

    return (
        <CoachesContainer>
            <CoachesTitle>Coaches</CoachesTitle>
            <SearchInput
                value={props.searchTerm}
                onChange={e => props.searchCoaches(e.target.value)}
            />
            <AddCoach edition={props.edition} coachAdded={props.coachAdded} />
            {table}
        </CoachesContainer>
    );
}
