import React from "react";
import { FilterStudentName, FilterStudentNameInputContainer } from "../styles";
import { FormControl } from "../../../Common/Forms";
import { setNameFilterStorage } from "../../../../utils/session-storage/student-filters";
/**
 * Component that filters the students list based on the name inserted in the input field.
 * @param nameFilter
 * @param setNameFilter
 */
export default function NameFilter({
    nameFilter,
    setNameFilter,
}: {
    nameFilter: string;
    setNameFilter: (value: string) => void;
}) {
    return (
        <FilterStudentName>
            <FilterStudentNameInputContainer>
                <FormControl
                    type="text"
                    placeholder="Search student..."
                    value={nameFilter}
                    onChange={e => {
                        setNameFilter(e.target.value);
                        setNameFilterStorage(e.target.value);
                    }}
                />
            </FilterStudentNameInputContainer>
        </FilterStudentName>
    );
}
