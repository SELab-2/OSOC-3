import React, { useEffect, useState } from "react";
import {
    FilterRoles,
    FilterRolesDropdownContainer,
    FilterRolesLabel,
    FilterRolesLabelContainer,
} from "../styles";
import Select, { MultiValue } from "react-select";
import { getSkills } from "../../../../utils/api/skills";
import "./RolesFilter.css";

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

    function handleRolesChange(event: MultiValue<DropdownRole>): void {
        const newRoles: number[] = [];
        for (const role of event) {
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
                    className="RolesFilterDropdown"
                    options={roles}
                    isMulti
                    isSearchable
                    placeholder="Choose roles..."
                    onChange={e => handleRolesChange(e)}
                />
            </FilterRolesDropdownContainer>
        </FilterRoles>
    );
}
