import styled from "styled-components";
import { Table } from "react-bootstrap";

export const Warning = styled.div`
    color: var(--osoc_red);
`;

export const AdminsTable = styled(Table).attrs({
    striped: true,
    bordered: true,
    variant: "dark",
    hover: false,
})`
    width: 45em;
    max-width: 100%;
    margin-top: 10px;
`;

export const AdminsTableDiv = styled.div`
    overflow: auto;
`;

export const ModalContentConfirm = styled.div`
    border: 3px solid var(--osoc_green);
    background-color: var(--osoc_blue);
`;

export const ModalContentWarning = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;

export const EmailDiv = styled.div`
    overflow: auto;
`;

export const RemoveAdminBody = styled.div`
    overflow: hidden;
`;

export const AddCoachButtonDiv = styled.div`
    float: right;
    margin-bottom: 5px;
`;
