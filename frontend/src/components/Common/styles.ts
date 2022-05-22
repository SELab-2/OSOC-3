import styled, { css } from "styled-components";

// Css for a component that does an animation on hover
export const HoverAnimation = css`
    transition: 200ms ease-out;

    &:hover {
        transition: 200ms ease-in;
    }
`;

export const ModalContentConfirm = styled.div`
    border: 3px solid var(--osoc_green);
    background-color: var(--osoc_blue);
`;

export const ModalContentWarning = styled.div`
    border: 3px solid var(--osoc_red);
    background-color: var(--osoc_blue);
`;
