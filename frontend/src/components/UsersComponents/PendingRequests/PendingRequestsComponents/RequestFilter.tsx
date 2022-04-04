import { SearchInput } from "../styles";
import React from "react";

/**
 * Input field to filter the [[RequestList]].
 * @param props.searchTerm The word in the input filed.
 * @param props.filter A function to change the search term.
 * @param props.show Boolean to reflect if the component needs to be shown.
 */
export default function RequestFilter(props: {
    searchTerm: string;
    filter: (key: string) => void;
    show: boolean;
}) {
    if (props.show) {
        return (
            <SearchInput value={props.searchTerm} onChange={e => props.filter(e.target.value)} />
        );
    } else {
        return null;
    }
}
