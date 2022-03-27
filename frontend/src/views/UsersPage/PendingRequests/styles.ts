import styled from "styled-components";
import { Table } from "react-bootstrap";

export const RequestHeader = styled.div`
    background-color: var(--osoc_red);
    padding-bottom: 3px;
    padding-left: 3px;
`;

export const RequestsTable = styled(Table)``;

export const PendingRequestsContainer = styled.div`
    width: 50%;
    min-width: 600px;
    margin: 10px auto auto;
`;

export const AcceptButton = styled.button`
    background-color: var(--osoc_green);
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
`;

export const RejectButton = styled.button`
    background-color: var(--osoc_red);
    margin-left: 3px;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
`;
