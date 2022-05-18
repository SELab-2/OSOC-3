import React from "react";
import { FilterResetButton } from "../styles";
import { DropdownRole } from "../RolesFilter/RolesFilter";
import {
    setAlumniFilterStorage,
    setNameFilterStorage,
    setRolesFilterStorage,
    setStudentCoachVolunteerFilterStorage,
    setSuggestedFilterStorage,
} from "../../../../utils/session-storage/student-filters";

interface Props {
    setNameFilter: (name: string) => void;
    setRolesFilter: (roles: DropdownRole[]) => void;
    setAlumniFilter: (alumni: boolean) => void;
    setSuggestedFilter: (suggested: boolean) => void;
    setStudentCoachVolunteerFilter: (studentCoachVolunteer: boolean) => void;
}

/**
 * Component that resets all filters.
 * @param props
 */
export default function ResetFiltersButton(props: Props) {
    /**
     * Reset all filters to their default value.
     */
    function resetFilters() {
        props.setNameFilter("");
        props.setAlumniFilter(false);
        props.setStudentCoachVolunteerFilter(false);
        props.setSuggestedFilter(false);
        props.setRolesFilter([]);
        setNameFilterStorage(null);
        setAlumniFilterStorage(null);
        setStudentCoachVolunteerFilterStorage(null);
        setSuggestedFilterStorage(null);
        setRolesFilterStorage(null);
    }

    return <FilterResetButton onClick={() => resetFilters()}>Reset filters</FilterResetButton>;
}
