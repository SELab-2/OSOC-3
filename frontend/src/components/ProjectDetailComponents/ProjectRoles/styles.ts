import styled from "styled-components";

export const ProjectRoleContainer = styled.div`
    border: 2px solid #1a1a36;
    border-radius: 5px;
    margin: 10px 20px;
    margin-left: 0;
    padding: 20px 20px 20px 20px;
    background-color: #323252;
    box-shadow: 5px 5px 15px #131329;
`;

export const TitleDeleteContainer = styled.div`
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const Suggestions = styled.div`
    min-height: 10vh;
`;

export const NoStudents = styled.div`
    display: flex;
    align-items: center;
    border: dashed #0f0f30;
    border-radius: 20px;
    margin: 15px 0;
    padding: 20px;
    min-height: 10vh;
    max-width: 40vw;
`;

export const DescriptionAndStudentAmount = styled.div`
    margin-top: 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
`;

export const NumberOfStudents = styled.div`
    .red {
        color: var(--osoc_red);
    }
    .green {
        color: var(--osoc_green);
    }
`;

export const DescriptionContainer = styled.div`
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 2.6rem;
    max-width: 90%;
    :hover {
        overflow: auto;
    }
`;
