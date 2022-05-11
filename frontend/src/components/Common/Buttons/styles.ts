import Button from "react-bootstrap/Button";
import styled, { css } from "styled-components";

import { HoverAnimation } from "../styles";
import { AnimatedButton } from "./props";

export const GreenButton = styled(Button)`
    ${HoverAnimation};

    background-color: var(--osoc_green);
    border-color: var(--osoc_green);
    color: var(--osoc_blue);

    &:hover {
        background-color: var(--osoc_orange);
        border-color: var(--osoc_orange);
        color: var(--osoc_blue);
    }
`;

const WarningColourAnimation = css`
    animation: button-change-colour infinite 3s ease-in-out;

    @keyframes button-change-colour {
        0% {
            background-color: var(--osoc_red);
            border-color: var(--osoc_red);

            box-shadow: none;
        }

        50% {
            background-color: #ff9089ff;
            border-color: #ff9089ff;

            box-shadow: 0 0 30px var(--osoc_red_darkened);
        }

        100% {
            background-color: var(--osoc_red);
            border-color: var(--osoc_red);

            box-shadow: none;
        }
    }
`;

export const RedButton = styled(Button)<AnimatedButton>`
    ${HoverAnimation};

    ${props => props.animated && WarningColourAnimation};

    background-color: var(--osoc_red);
    border-color: var(--osoc_red);

    &:hover {
        background-color: var(--osoc_red_darkened);
        border-color: var(--osoc_red_darkened);
    }
`;
