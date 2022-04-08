import styled from "styled-components";

export const LoginPageContainer = styled.div`
    height: fit-content;
    text-align: center;
    display: flex;
    justify-content: center;
    flex-direction: column;
    margin: 4%;
`;

export const LoginContainer = styled.div`
    display: flex;
    margin-right: auto;
    margin-left: auto;
`;

export const EmailLoginContainer = styled.div`
    height: fit-content;
    text-align: center;
    display: flex;
    justify-content: center;
    flex-direction: column;
`;

export const VerticalDivider = styled.div`
    margin-right: 20px;
    padding-right: 20px;
    border-right: 2px solid rgba(182, 182, 182, 0.603);
`;

export const NoAccount = styled.div`
    padding-bottom: 15px;
`;

export const LoginButton = styled.button`
    width: 120px;
    height: 35px;
    cursor: pointer;
    background: var(--osoc_green);
    color: white;
    border: none;
    border-radius: 5px;
`;
