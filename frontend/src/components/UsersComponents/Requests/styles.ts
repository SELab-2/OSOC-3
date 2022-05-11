import styled from "styled-components";
import { Table, Button } from "react-bootstrap";
import { BiDownArrow } from "react-icons/bi";

export const RequestHeaderDiv = styled.div`
    display: inline-block;
`;

export const RequestHeaderTitle = styled.div`
    padding-bottom: 3px;
    padding-left: 3px;
    width: 100px;
    font-size: 25px;
    float: left;
`;

export const OpenArrow = styled(BiDownArrow)`
    margin-top: 13px;
    margin-left: 10px;
    offset-position: 0 30px;
`;

export const ClosedArrow = styled(BiDownArrow)`
    margin-top: 13px;
    margin-left: 10px;
    transform: rotate(-90deg);
    offset: 0 30px;
`;

export const RequestsTable = styled(Table)`
    // TODO: make all tables in site uniform
`;

export const RequestsContainer = styled.div`
    min-width: 450px;
    width: 80%;
    max-width: 700px;
    margin: 10px auto auto;
`;

export const AcceptRejectTh = styled.th`
    width: 200px;
    text-align: center;
`;

export const AcceptRejectTd = styled.td`
    text-align: center;
    vertical-align: middle;
`;

export const AcceptButton = styled(Button)`
    background-color: var(--osoc_green);
    color: black;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
    width: 65px;
`;

export const RejectButton = styled(Button)`
    background-color: var(--osoc_red);
    color: black;
    margin-left: 3px;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
    width: 65px;
`;

export const SpinnerContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px;
`;

export const Error = styled.div`
    color: var(--osoc_red);
    width: 100%;
    margin: auto;
`;

export const RequestListContainer = styled.div`
    height: 400px;
`;

export const SearchButton = styled(Button)`
    margin-left: 10px;
    color: white;
    font-size: 15px;
    height: 33px;
`;
