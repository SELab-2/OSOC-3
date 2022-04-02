import styled from "styled-components";
import { Table } from "react-bootstrap";

export const CoachesContainer = styled.div`
    width: 50%;
    min-width: 600px;
    margin: 10px auto auto;
`;

export const CoachesTitle = styled.div`
    padding-bottom: 3px;
    padding-left: 3px;
    width: 100px;
    font-size: 25px;
`;

export const RemoveFromEditionButton = styled.button`
    background-color: var(--osoc_red);
    margin-left: 3px;
    padding-bottom: 3px;
    padding-left: 3px;
    padding-right: 3px;
`;

export const CoachesTable = styled(Table)``;

export const PopupDiv = styled.div`
    background-color: var(--osoc_red);
    width: 200px;
    height: 100px;
    position: absolute;
    right: 0;
    top: 0;
`;

export const ModalContent = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;
