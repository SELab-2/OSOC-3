import styled from "styled-components";
import { CreateButton } from "../../../Common/Buttons";
import { FormControl } from "../../../Common/Forms";

export const AddNewSkillContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    margin-top: 5vh;
    margin-left: 0;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
    display: flex;
    height: max-content;
    justify-content: center;
`;

export const NewSkill = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    margin-top: 5vh;
    margin-left: 0;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
    align-items: center;
    height: max-content;
`;

export const NewSkillTop = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    overflow: auto;
`;

export const NewSkillBottom = styled.div``;

export const NewSkillLeft = styled.div`
    display: flex;
    align-items: center;
    max-width: 50%;
    overflow: auto;
`;
export const NewSKillRight = styled.div`
    display: flex;
    align-items: center;
    max-width: 50%;
    overflow: auto;
`;

export const StyledFormSelect = styled(FormControl)`
    background-color: var(--osoc_blue);
    color: white;
    border-color: transparent;
    min-width: 75px;
    max-width: 30%;
    padding: 0.375rem 0.75rem;
    border-radius: 0.25rem;
    height: 2.5rem;
`;

export const AmountInput = styled.input`
    margin: 5px 10px;
    padding: 0.36rem 0.75rem;
    background-color: #131329;
    color: white;
    border: none;
    border-radius: 0.25rem;
    min-width: 75px;
    max-width: 10%;
    direction: rtl;
    height: 2.5rem;
`;

export const AddNewSkillButton = styled(CreateButton)`
    margin-left: 10px;
    margin-right: 10px;
`;
