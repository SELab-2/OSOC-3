import styled from "styled-components";
import { Table, Button } from "react-bootstrap";

export const RequestHeaderTitle = styled.div`
    padding-bottom: 3px;
    padding-left: 3px;
    width: 100px;
    font-size: 25px;
`;

export const SearchInput = styled.input.attrs({
    placeholder: "Search",
})`
    margin: 3px;
    height: 20px;
    width: 150px;
    font-size: 15px;
    border-radius: 5px;
    border-width: 0;
`;

export const RequestsTable = styled(Table)``;

export const PendingRequestsContainer = styled.div`
    width: 50%;
    min-width: 600px;
    margin: 10px auto auto;
`;

export const AcceptButton = styled(Button)`
    background-color: var(--osoc_green);
    color: black;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
`;

export const RejectButton = styled(Button)`
    background-color: var(--osoc_red);
    color: black;
    margin-left: 3px;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
`;

export const SpinnerContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px;
`;
