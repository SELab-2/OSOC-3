import React from "react";
import { CoachesTitle, CoachesContainer, SearchFieldDiv, TableDiv } from "./styles";
import { User } from "../../../utils/api/users/users";
import { Error } from "../Requests/styles";
import { CoachList, AddCoach } from "./CoachesComponents";
import { SearchBar } from "../../Common/Forms";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches are shown.
 * @param props.coaches The list of coaches which need to be shown.
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.searchCoaches A function to set the filter for coaches' username.
 * @param props.gotData All data is received.
 * @param props.error An error message.
 * @param props.moreCoachesAvailable More unfetched coaches available.
 * @param props.searchTerm Current filter for coaches' names.
 * @param props.refreshCoaches A function which will be called when a coach is added.
 * @param props.removeCoach A function which will be called when a user is deleted as coach.
 */
export default function Coaches(props: {
    edition: string;
    coaches: User[];
    getMoreCoaches: () => void;
    searchCoaches: (word: string) => void;
    gotData: boolean;
    error: string;
    moreCoachesAvailable: boolean;
    searchTerm: string;
    refreshCoaches: () => void;
    removeCoach: (user: User) => void;
}) {
    let table;
    if (props.error) {
        table = <Error> {props.error} </Error>;
    } else if (props.gotData && props.coaches.length === 0) {
        table = <div>No coaches found</div>;
    } else {
        table = (
            <CoachList
                coaches={props.coaches}
                edition={props.edition}
                removeCoach={props.removeCoach}
                getMoreCoaches={props.getMoreCoaches}
                moreCoachesAvailable={props.moreCoachesAvailable}
            />
        );
    }

    return (
        <CoachesContainer>
            <CoachesTitle>Coaches</CoachesTitle>
            <SearchFieldDiv>
                <SearchBar
                    onChange={e => props.searchCoaches(e.target.value)}
                    value={props.searchTerm}
                    placeholder="Search name..."
                />
            </SearchFieldDiv>
            <AddCoach edition={props.edition} refreshCoaches={props.refreshCoaches} />
            <TableDiv>{table}</TableDiv>
        </CoachesContainer>
    );
}
