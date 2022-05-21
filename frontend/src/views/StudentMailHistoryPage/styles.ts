import styled from "styled-components";
import { CommonDropdownButton } from "../../components/Common/Buttons/styles";

export const TableDiv = styled.div`
    width: 100%;
    min-width: fit-content;
    margin: auto;
`;

export const BackButtonDiv = styled.div`
    margin-left: 2em;
    float: left;
`;

export const NameDiv = styled.div`
    overflow: hidden;
    width: fit-content;
    margin: auto;
`;

export const ButtonDiv = styled.div`
    width: fit-content;
    margin-bottom: 5px;
    margin-top: 10px;
`;

export const CenterDiv = styled.div`
    width: 45em;
    min-width: fit-content;
    max-width: 95%;
    margin: 2em auto;
`;

export const CustomDropdownButton = styled(CommonDropdownButton)`
    width: 11em;

    & > Button {
        width: 11em;
    }
`;

export const DateTh = styled.th`
    text-align: center;
`;

export const DateTd = styled.td`
    text-align: center;
`;
