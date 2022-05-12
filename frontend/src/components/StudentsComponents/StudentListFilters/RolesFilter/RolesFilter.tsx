import React from "react";
import {
    FilterRoles,
    FilterRolesDropdownContainer,
    FilterRolesLabel,
    FilterRolesLabelContainer,
} from "../styles";
import Select from "react-select";

/**
 * Component that filters the students list based on the current roles selected.
 * @param rolesFilter
 * @param setRolesFilter
 */
export default function RolesFilter({
    rolesFilter,
    setRolesFilter,
}: {
    rolesFilter: number[];
    setRolesFilter: (value: number[]) => void;
}) {
    const roles = [
        { value: 0, label: "Frontend" },
        { value: 1, label: "Backend" },
        { value: 2, label: "Communication" },
    ];

    function handleRolesChange(
        clickedRoles: () => IterableIterator<{ value: number; label: string }>
    ): void {
        const newRoles: number[] = [];
        for (const role of roles) {
            newRoles.push(role.value);
        }
        setRolesFilter(newRoles);
    }

    return (
        <FilterRoles>
            <FilterRolesLabelContainer>
                <FilterRolesLabel>Roles: </FilterRolesLabel>
            </FilterRolesLabelContainer>
            <FilterRolesDropdownContainer>
                <Select
                    options={roles}
                    isMulti
                    isSearchable
                    placeholder="Choose roles..."
                    onChange={e => handleRolesChange(e.values)}
                />
            </FilterRolesDropdownContainer>
        </FilterRoles>
    );
}
