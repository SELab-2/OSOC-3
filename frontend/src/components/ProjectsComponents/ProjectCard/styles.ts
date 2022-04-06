import { Modal } from "react-bootstrap";
import styled from "styled-components";

export const CardContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 20px;
    margin: 10px 20px;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
`;

export const TitleContainer = styled.div`
    display: flex;
    align-items: baseline;
    justify-content: space-between;
`;

export const Title = styled.h2`
    text-overflow: ellipsis;
    overflow: hidden;
`;

export const ClientContainer = styled.div`
    display: flex;
    align-items: top;
    justify-content: space-between;
    color: lightgray;
`;

export const Client = styled.h5`
    text-overflow: ellipsis;
    overflow: hidden;
`;

export const NumberOfStudents = styled.div`
    margin-left: 2.5%;
    display: flex;
    align-items: center;
    margin-bottom: 4px;
`;

export const CoachesContainer = styled.div`
    display: flex;
    margin-top: 20px;
    overflow-x: scroll;
`;

export const CoachContainer = styled.div`
    background-color: #1a1a36;
    border-radius: 10px;
    margin-right: 10px;
    text-align: center;
    padding: 10px 20px;
    width: fit-content;
    max-width: 20vw;
`;

export const CoachText = styled.div`
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

export const Delete = styled.button`
    background-color: #f14a3b;
    padding: 5px 5px;
    border: 0;
    border-radius: 5px;
    max-height: 30px;
    margin-left: 5%;
    display: flex;
    align-items: center;
`;

export const PopUp = styled(Modal)`

`
