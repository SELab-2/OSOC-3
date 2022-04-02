import styled from "styled-components";
import { Button, Table } from "react-bootstrap";

export const AdminsContainer = styled.div`
    width: 50%;
    min-width: 600px;
    margin: 10px auto auto;
`;

export const AdminsTable = styled(Table)``;

export const ModalContentGreen = styled.div`
    border: 3px solid var(--osoc_green);
    background-color: var(--osoc_blue);
`;

export const ModalContentRed = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;

export const AddAdminButton = styled(Button).attrs({
    size: "sm",
})`
    float: right;
`;

export const Warning = styled.div`
    color: var(--osoc_red);
`;
