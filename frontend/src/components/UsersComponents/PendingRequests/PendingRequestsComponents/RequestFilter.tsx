import { SearchInput } from "../styles";
import React from "react";

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
