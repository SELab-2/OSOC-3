import React from "react";
import {
    FilterStudentName,
    FilterStudentNameInputContainer,
    FilterStudentNameLabel,
    FilterStudentNameLabelContainer,
} from "../styles";
import { Form } from "react-bootstrap";
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
            <FilterStudentNameLabelContainer>
                <FilterStudentNameLabel>Search: </FilterStudentNameLabel>
            </FilterStudentNameLabelContainer>
            <FilterStudentNameInputContainer>
                <Form.Control
                    type="text"
                    name="nameFilter"
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
