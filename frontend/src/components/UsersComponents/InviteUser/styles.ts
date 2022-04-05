import styled, { keyframes } from "styled-components";

export const InviteContainer = styled.div`
    clear: both;
`;

export const InviteInput = styled.input.attrs({
    name: "email",
    placeholder: "Invite user by email",
})`
    height: 30px;
    width: 200px;
    font-size: 13px;
    margin-top: 10px;
    margin-left: 10px;
    margin-right: 5px;
    text-align: center;
    border-radius: 5px;
    border-width: 0;
    float: left;
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

export const Error = styled.div`
    margin-left: 10px;
    color: var(--osoc_red);
`;

export const Message = styled.div`
    margin-left: 10px;
`;

export const InviteButton = styled.div`
    padding-top: 10px;
`;
