import styled from "styled-components";
import { Button, Table } from "react-bootstrap";

export const Warning = styled.div`
    color: var(--osoc_red);
`;

export const AdminsTable = styled(Table)``;

export const ModalContentConfirm = styled.div`
    border: 3px solid var(--osoc_green);
    background-color: var(--osoc_blue);
`;

export const ModalContentWarning = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;

export const AddAdminButton = styled(Button).attrs({
    size: "sm",
})`
    float: right;
`;
