import React from "react";
import { DropdownRole } from "../RolesFilter/RolesFilter";
import { DeleteButton } from "../../../Common/Buttons";
import {
    setAlumniFilterStorage,
    setConfirmFilterStorage,
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
    setConfirmFilter: (confirm: DropdownRole[]) => void;
    setPage: (page: number) => void;
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
        props.setConfirmFilter([]);
        props.setPage(0);
        setNameFilterStorage(null);
        setAlumniFilterStorage(null);
        setStudentCoachVolunteerFilterStorage(null);
        setSuggestedFilterStorage(null);
        setRolesFilterStorage(null);
        setConfirmFilterStorage(null);
    }

    return (
        <>
            <DeleteButton onClick={() => resetFilters()}>Reset filters</DeleteButton>
        </>
    );
}
