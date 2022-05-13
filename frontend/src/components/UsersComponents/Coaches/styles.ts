import styled from "styled-components";
import { Button, Table } from "react-bootstrap";

export const CoachesContainer = styled.div`
    width: 50em;
    height: fit-content;
    margin: 10px auto auto;
`;

export const CoachesTitle = styled.div`
    padding-bottom: 3px;
    padding-left: 3px;
    width: 100px;
    font-size: 25px;
`;

export const CoachesTable = styled(Table).attrs({
    striped: true,
    bordered: true,
    variant: "dark",
    hover: false,
})``;

export const ModalContent = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;

export const RemoveTh = styled.th`
    width: 200px;
    text-align: center;
`;

export const RemoveTd = styled.td`
    text-align: center;
    vertical-align: middle;
`;

export const ListDiv = styled.div`
    width: 100%;
    height: 40em;
    overflow: auto;
    margin-top: 10px;
`;

export const DialogButton = styled(Button)`
    margin-right: 4px;
    margin-bottom: 4px;
`;

export const DialogButtonContainer = styled.div`
    width: 100%;
`;

export const CancelButton = styled(Button)`
    float: right;
`;

export const EmailDiv = styled.div`
    overflow: auto;
`;

export const CredsDiv = styled.div`
    overflow: hidden;
    text-overflow: ellipsis;
`;
