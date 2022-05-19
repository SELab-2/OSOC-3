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

export const EmailDiv = styled.div`
    overflow: auto;
`;

export const RemoveAdminBody = styled.div`
    overflow: hidden;
`;

export const AddButtonDiv = styled.div`
    float: right;
    margin-bottom: 5px;
`;
