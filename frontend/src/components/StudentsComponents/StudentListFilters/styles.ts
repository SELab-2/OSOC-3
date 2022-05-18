import styled from "styled-components";

export const StudentListSideMenu = styled.div`
    display: flex;
    position: sticky;
    flex-direction: column;
    width: 35%;
    min-width: 35vh;
    max-width: 50vh;
    height: 100vh;
    border-right: 2px solid var(--card-color);
`;

export const StudentListLinebreak = styled.div`
    height: 1px;
    background-color: white;
    width: 90%;
    align-self: center;
`;

export const FilterStudentName = styled.div`
    width: 90%;
    display: flex;
    margin-top: 15px;
    align-self: center;
    align-items: center;
`;

export const FilterStudentNameLabelContainer = styled.div`
    display: flex;
    background-color: var(--osoc_orange);
    border: 2px solid var(--osoc_orange);
    width: 30%;
    text-align: center;
`;

export const FilterStudentNameLabel = styled.span`
    color: white;
    width: 100%;
`;

export const FilterStudentNameInputContainer = styled.div`
    width: 100%;
`;

export const FilterRoles = styled.div`
    width: 90%;
    display: flex;
    align-self: center;
    margin-top: 10px;
    margin-bottom: 10px;
    align-items: center;
`;

export const FilterRolesLabelContainer = styled.div`
    display: flex;
    background-color: var(--osoc_green);
    border: 2px solid var(--osoc_green);
    width: 30%;
    text-align: center;
`;

export const FilterRolesLabel = styled.span`
    color: white;
    width: 100%;
`;

export const FilterRolesDropdownContainer = styled.div`
    width: 100%;
`;

export const FilterResetButton = styled.button`
    width: 50%;
    align-self: center;
    border: none;
    height: 3vh;
    background-color: var(--osoc_red);
    color: white;
`;

export const FilterControls = styled.div`
    margin-top: 4%;
    flex-direction: column;
    display: flex;
    align-self: center;
    width: 80%;
`;

export const MessageDiv = styled.div`
    text-align: center;
    margin-top: 20px;
`;
