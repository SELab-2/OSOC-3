import React, { useEffect, useState } from "react";
import { FilterConfirmsDropdownContainer, FilterConfirms, ConfirmsTitle } from "../styles";
import { DropdownRole } from "../RolesFilter/RolesFilter";
import Select, { MultiValue } from "react-select";
import { setConfirmFilterStorage } from "../../../../utils/session-storage/student-filters";

/**
 * Component that filters the students list based on confirmation.
 */
export default function ConfirmFilters({
    confirmFilter,
    setConfirmFilter,
}: {
    confirmFilter: DropdownRole[];
    setConfirmFilter: (value: DropdownRole[]) => void;
}) {
    const [confirms, setConfirms] = useState<DropdownRole[]>([]);

    useEffect(() => {
        setConfirms([
            { label: "Yes", value: 1 },
            { label: "Maybe", value: 2 },
            { label: "No", value: 3 },
            { label: "Undecided", value: 0 },
        ]);
    }, []);

    function handleRolesChange(event: MultiValue<DropdownRole>): void {
        const allCheckedRoles: DropdownRole[] = [];
        event.forEach(dropdownRole => allCheckedRoles.push(dropdownRole));
        setConfirmFilter(allCheckedRoles);
        setConfirmFilterStorage(JSON.stringify(allCheckedRoles));
    }

    return (
        <FilterConfirms>
            <ConfirmsTitle>Confirmed</ConfirmsTitle>
            <FilterConfirmsDropdownContainer>
                <Select
                    className="RolesFilterDropdown"
                    options={confirms}
                    isMulti
                    isSearchable
                    placeholder="Choose roles..."
                    value={confirmFilter}
                    onChange={e => handleRolesChange(e)}
                />
            </FilterConfirmsDropdownContainer>
        </FilterConfirms>
    );
}
