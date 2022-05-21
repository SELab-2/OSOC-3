import styled from "styled-components";
import { Table } from "react-bootstrap";
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
    margin-right: 15px;
`;

export const OpenArrow = styled(BiDownArrow)`
    margin-top: 13px;
    margin-left: 10px;
`;

export const ClosedArrow = styled(BiDownArrow)`
    margin-top: 13px;
    margin-left: 10px;
    transform: rotate(-90deg);
`;

export const RequestsTable = styled(Table).attrs({
    striped: true,
    bordered: true,
    variant: "dark",
    hover: false,
})``;

export const RequestsContainer = styled.div`
    width: 50em;
    height: fit-content;
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

export const Spacing = styled.div`
    display: inline-block;
    width: 5px;
`;

export const RequestListContainer = styled.div`
    height: fit-content;
    width: 100%;
    clear: left;
`;
