import React from "react";
import { FilterResetButton } from "../styles";

interface Props {
    setNameFilter: (name: string) => void;
    setAlumniFilter: (alumni: boolean) => void;
    setStudentCoachVolunteerFilter: (studentCoachVolunteer: boolean) => void;
}

export default function ResetFiltersButton(props: Props) {
    function resetFilters() {
        props.setNameFilter("");
        props.setAlumniFilter(false);
        props.setStudentCoachVolunteerFilter(false);
    }

    return <FilterResetButton onClick={() => resetFilters()}>Reset filters</FilterResetButton>;
}
