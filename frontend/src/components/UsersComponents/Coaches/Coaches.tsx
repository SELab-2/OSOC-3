import React from "react";
import { CoachesTitle, CoachesContainer } from "./styles";
import { User } from "../../../utils/api/users/users";
import { CoachList, AddCoach } from "./CoachesComponents";
import { SearchBar } from "../../Common/Forms";
import { SearchFieldDiv, TableDiv } from "../../Common/Users/styles";
import LoadSpinner from "../../Common/LoadSpinner";

/**
 * List of coaches of the given edition.
 * This includes a searchfield and the option to remove and add coaches.
 * @param props.edition The edition of which coaches are shown.
 * @param props.coaches The list of coaches which need to be shown.
 * @param props.loading Data is being loaded
 * @param props.getMoreCoaches A function to load more coaches.
 * @param props.searchCoaches A function to set the filter for coaches' username.
 * @param props.setPage Set the next page to fetch
 * @param props.moreCoachesAvailable More unfetched coaches available.
 * @param props.searchTerm Current filter for coaches' names.
 * @param props.refreshCoaches A function which will be called when a coach is added.
 * @param props.removeCoach A function which will be called when a user is deleted as coach.
 */
export default function Coaches(props: {
    edition: string;
    coaches: User[];
    loading: boolean;
    getMoreCoaches: (page: number, reset: boolean) => void;
    searchCoaches: (word: string) => void;
    setPage: (page: number) => void;
    moreCoachesAvailable: boolean;
    searchTerm: string;
    refreshCoaches: () => void;
    removeCoach: (user: User) => void;
}) {
    let table;
    if (props.coaches.length === 0) {
        if (props.loading) {
            table = <LoadSpinner show={true} />;
        } else {
            table = <div>No coaches found</div>;
        }
    } else {
        table = (
            <CoachList
                coaches={props.coaches}
                edition={props.edition}
                removeCoach={props.removeCoach}
                getMoreCoaches={page => props.getMoreCoaches(page, false)}
                moreCoachesAvailable={props.moreCoachesAvailable}
            />
        );
    }

    return (
        <CoachesContainer>
            <CoachesTitle>Coaches</CoachesTitle>
            <SearchFieldDiv>
                <SearchBar
                    onChange={e => {
                        props.searchCoaches(e.target.value);
                        props.setPage(0);
                    }}
                    value={props.searchTerm}
                    placeholder="Search name..."
                />
            </SearchFieldDiv>
            <AddCoach edition={props.edition} refreshCoaches={props.refreshCoaches} />
            <TableDiv>{table}</TableDiv>
        </CoachesContainer>
    );
}
