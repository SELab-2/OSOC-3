import React, { useEffect, useState } from "react";
import {
    FilterRoles,
    FilterRolesDropdownContainer,
    FilterRolesLabel,
    FilterRolesLabelContainer,
} from "../styles";
import Select from "react-select";
import { getSkills } from "../../../../utils/api/skills";

interface DropdownRole {
    label: string;
    value: number;
}

/**
 * Component that filters the students list based on the current roles selected.
 * @param rolesFilter
 * @param setRolesFilter
 */
export default function RolesFilter({
    setRolesFilter,
}: {
    setRolesFilter: (value: number[]) => void;
}) {
    const [roles, setRoles] = useState<DropdownRole[]>([]);

    async function fetchRoles() {
        const allRoles = await getSkills();
        const dropdownRoles = allRoles!.skills.map(role => ({
            label: role.name,
            value: role.skillId,
        }));
        setRoles(dropdownRoles);
    }

    useEffect(() => {
        fetchRoles();
    }, []);

    function handleRolesChange(): void {
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
                    onChange={handleRolesChange}
                />
            </FilterRolesDropdownContainer>
        </FilterRoles>
    );
}
