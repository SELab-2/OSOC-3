import React from "react";
import {
    FilterStudentName,
    FilterStudentNameInputContainer,
    FilterStudentNameLabel,
    FilterStudentNameLabelContainer,
} from "../styles";
import { Form } from "react-bootstrap";

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
                    }}
                />
            </FilterStudentNameInputContainer>
        </FilterStudentName>
    );
}
