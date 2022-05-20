import React, { useEffect, useState } from "react";
import { FilterRoles, FilterRolesDropdownContainer, RolesTitle } from "../styles";
import Select, { MultiValue } from "react-select";
import { getSkills } from "../../../../utils/api/skills";
import "../Dropdown.css";
import { setRolesFilterStorage } from "../../../../utils/session-storage/student-filters";

export interface DropdownRole {
    label: string;
    value: number;
}

/**
 * Component that filters the students list based on the current roles selected.
 * @param rolesFilter
 * @param setRolesFilter
 * @param setPage Function to set the page to fetch next
 */
export default function RolesFilter({
    rolesFilter,
    setRolesFilter,
    setPage,
}: {
    rolesFilter: DropdownRole[];
    setRolesFilter: (value: DropdownRole[]) => void;
    setPage: (page: number) => void;
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
        const allCheckedRoles: DropdownRole[] = [];
        event.forEach(dropdownRole => allCheckedRoles.push(dropdownRole));
        setRolesFilter(allCheckedRoles);
        setRolesFilterStorage(JSON.stringify(allCheckedRoles));
    }

    return (
        <FilterRoles>
            <RolesTitle>Roles</RolesTitle>
            <FilterRolesDropdownContainer>
                <Select
                    className="RolesFilterDropdown"
                    options={roles}
                    isMulti
                    isSearchable
                    placeholder="Choose roles..."
                    value={rolesFilter}
                    onChange={e => {
                        handleRolesChange(e);
                        setPage(0);
                    }}
                />
            </FilterRolesDropdownContainer>
        </FilterRoles>
    );
}
