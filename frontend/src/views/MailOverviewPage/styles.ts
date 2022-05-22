import styled from "styled-components";
import { StyledTable } from "../../components/Common/Tables/styles";

export const DropDownButtonDiv = styled.div`
    float: right;
`;

export const SearchDiv = styled.div`
    margin-top: 20px;
    width: 14em;
    display: inline-block;
`;

export const FilterDiv = styled.div`
    width: 14em;
    max-width: 350px;
    display: inline-block;
`;

export const SearchAndChangeDiv = styled.div`
    width: 100%;
    margin-bottom: 5px;
`;

export const CenterDiv = styled.div`
    width: 100%;
    margin: auto;
`;

export const MessageDiv = styled.div`
    width: fit-content;
    margin: auto;
`;

export const MailOverviewDiv = styled.div`
    width: fit-content;
    margin: auto;
    max-width: 95%;
`;

export const ClearDiv = styled.div`
    clear: both;
`;

export const CustomStyledTable = styled(StyledTable)`
    min-width: fit-content;
    width: 60em;
    max-width: 100%;
`;
