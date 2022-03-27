import styled, { keyframes } from "styled-components";

export const InviteContainer = styled.div`
    overflow: hidden;
`;

export const InviteInput = styled.input.attrs({
    name: "email",
    placeholder: "Invite user by email",
})`
    height: 35px;
    width: 250px;
    font-size: 15px;
    margin-top: 10px;
    margin-left: 10px;
    text-align: center;
    border-radius: 5px;
    border-width: 0;
    float: left;
`;

export const InviteButton = styled.button`
    width: 90px;
    height: 35px;
    cursor: pointer;
    background: var(--osoc_green);
    color: white;
    border: none;
    border-radius: 5px;
    margin-left: 7px;
    margin-top: 10px;
`;

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
`;

export const Loader = styled.div`
    border: 8px solid var(--osoc_green);
    border-top: 8px solid var(--osoc_blue);
    border-radius: 50%;
    width: 35px;
    height: 35px;
    animation: ${rotate} 2s linear infinite;
    margin-left: 37px;
    margin-top: 10px;
    float: left;
`;

export const Link = styled.div`
    margin-left: 10px;
`;

export const Error = styled.div`
    margin-left: 10px;
    color: var(--osoc_red);
`;
