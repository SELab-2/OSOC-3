import React from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { User } from "../../../utils/api/users/users";
import { Error, SpinnerContainer } from "../Requests/styles";
import { CoachList, AddCoach } from "./CoachesComponents";
import { Spinner } from "react-bootstrap";
import { SearchInput } from "../../styles";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches are shown.
 * @param props.coaches The list of coaches which need to be shown.
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.searchCoaches A function to set the filter for coaches' username.
 * @param props.gotData All data is received.
 * @param props.gettingData Waiting for data.
 * @param props.error An error message.
 * @param props.moreCoachesAvailable More unfetched coaches available.
 * @param props.searchTerm Current filter for coaches' names.
 * @param props.refreshCoaches A function which will be called when a coach is added.
 * @param props.removeCoach A function which will be called when a user is deleted as coach.
 */
export default function Coaches(props: {
    edition: string;
    coaches: User[];
    getMoreCoaches: (page: number) => void;
    searchCoaches: (word: string) => void;
    gotData: boolean;
    gettingData: boolean;
    error: string;
    moreCoachesAvailable: boolean;
    searchTerm: string;
    refreshCoaches: () => void;
    removeCoach: (user: User) => void;
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
                removeCoach={props.removeCoach}
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
            <AddCoach edition={props.edition} refreshCoaches={props.refreshCoaches} />
            {table}
        </CoachesContainer>
    );
}
