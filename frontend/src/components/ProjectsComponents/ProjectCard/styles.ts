import { Modal } from "react-bootstrap";
import styled from "styled-components";
import { BsArrowUpRightSquare } from "react-icons/bs";
import { HoverAnimation } from "../../Common/styles";

export const CardContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
`;

export const TitleContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const Title = styled.h2`
    ${HoverAnimation}
    max-height: 3.7em;
    overflow: hidden;
    display: flex;
    align-items: center;
    margin-right: 10px;

    &:hover {
        overflow: hidden;
        cursor: pointer;
        color: var(--osoc_green);
    }
`;

export const OpenIcon = styled(BsArrowUpRightSquare)`
    margin-left: 5px;
    margin-top: 2px;
    height: 20px;
`;

export const ClientContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: lightgray;
`;

export const Clients = styled.div`
    display: flex;
    overflow: hidden;
    max-height: 3rem;
    :hover {
        overflow: hidden;
    }
`;

export const Client = styled.h5`
    margin-right: 10px;
`;

export const NumberOfStudents = styled.div`
    margin-left: 10px;
    display: flex;
    align-items: center;
    margin-bottom: 4px;
`;

export const CoachesContainer = styled.div`
    display: flex;
    align-items: center;
    margin-top: 20px;
    overflow-x: hidden;
    padding-bottom: 15px;
    :hover {
        overflow: auto;
    }
`;

export const CoachContainer = styled.div`
    background-color: #1a1a36;
    border-radius: 5px;
    margin-right: 10px;
    text-align: center;
    padding: 7.5px 15px;
    width: fit-content;
    max-width: 20vw;
    display: flex;
`;

export const CoachText = styled.div`
    overflow: hidden;
    white-space: nowrap;
    :hover {
        overflow: auto;
    }
`;

export const PopUp = styled(Modal)``;
