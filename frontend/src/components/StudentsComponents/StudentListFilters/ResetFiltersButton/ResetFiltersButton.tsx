import React from "react";
import { FilterResetButton } from "../styles";
import { DropdownRole } from "../RolesFilter/RolesFilter";

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
        sessionStorage.removeItem("suggestedFilter");
        sessionStorage.removeItem("alumniFilter");
        sessionStorage.removeItem("nameFilter");
        sessionStorage.removeItem("studentCoachVolunteerFilter");
        sessionStorage.removeItem("rolesFilter");
    }

    return <FilterResetButton onClick={() => resetFilters()}>Reset filters</FilterResetButton>;
}
