import { css } from "styled-components";

// Css for a component that does an animation on hover
export const HoverAnimation = css`
    transition: 200ms ease-out;

    &:hover {
        transition: 200ms ease-in;
    }
`;
