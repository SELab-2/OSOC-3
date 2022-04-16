import styled from "styled-components";
import Spinner from "react-bootstrap/Spinner";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";

export const StyledTable = styled(Table).attrs(() => ({
    striped: true,
    bordered: true,
    hover: true,
    variant: "dark",
    className: "mx-0 mt-0 mb-5",
}))``;

export const LoadingSpinner = styled(Spinner).attrs(() => ({
    animation: "border",
    role: "status",
    className: "mx-auto",
}))``;

export const DeleteButton = styled(Button).attrs(() => ({
    variant: "danger",
    className: "me-0 ms-auto my-auto",
}))``;

export const RowContainer = styled.td.attrs(() => ({
    className: "p-3 d-flex",
}))``;

export const StyledNewEditionButton = styled(Button).attrs(() => ({
    className: "ms-auto my-3",
}))`
    background-color: var(--osoc_green);
    border-color: var(--osoc_green);

    &:hover {
        background-color: var(--osoc_orange);
        border-color: var(--osoc_orange);
    }
`;
