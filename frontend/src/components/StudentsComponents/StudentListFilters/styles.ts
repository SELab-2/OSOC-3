import styled from "styled-components";

export const StudentListSideMenu = styled.div`
    display: flex;
    position: sticky;
    flex-direction: column;
    width: 35%;
    min-width: 35vh;
    max-width: 50vh;
    height: 100vh;
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

export const FilterStudentNameInputContainer = styled.div`
    width: 100%;
`;

export const RolesTitle = styled.p`
    margin-top: 2%;
    margin-right: 2%;
    font-size: 1.7vh;
`;

export const ConfirmsTitle = styled.p`
    margin-top: 2%;
    margin-right: 2%;
    font-size: 1.7vh;
`;

export const FilterRoles = styled.div`
    width: 90%;
    display: flex;
    align-self: center;
    margin-top: 2%;
    margin-bottom: 2%;
    align-items: center;
`;

export const FilterConfirms = styled.div`
    width: 90%;
    display: flex;
    align-self: center;
    margin-top: 2%;
    margin-bottom: 2%;
    align-items: center;
`;

export const FilterRolesDropdownContainer = styled.div`
    width: 100%;
`;

export const FilterConfirmsDropdownContainer = styled.div`
    width: 100%;
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

export const ConfirmButtonsContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-self: center;
    width: 90%;
    margin-bottom: 2%;
`;
