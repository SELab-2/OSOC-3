import styled, { css } from "styled-components";

import { HoverAnimation } from "../styles";
import { AnimatedButton } from "./props";
import { Dropdown, DropdownButton, Button } from "react-bootstrap";

export const GreenButton = styled(Button)`
    ${HoverAnimation};

    background-color: var(--osoc_green);
    border-color: var(--osoc_green);
    color: var(--osoc_blue);

    &:disabled {
        background-color: #3a6453;
        border-color: #3a6453;
        color: white;
    }

    &:hover,
    &:active,
    &:focus {
        background-color: var(--osoc_orange);
        border-color: var(--osoc_orange);
        color: var(--osoc_blue);
        box-shadow: none !important;
    }
`;

export const OrangeButton = styled(Button)`
    ${HoverAnimation};

    background-color: var(--osoc_orange);
    border-color: var(--osoc_orange);
    color: var(--osoc_blue);

    &:hover,
    &:active,
    &:focus {
        background-color: var(--osoc_orange_darkened);
        border-color: var(--osoc_orange_darkened);
        color: var(--osoc_blue);
        box-shadow: none !important;
    }
`;

export const DropdownToggle = styled(Dropdown.Toggle)`
    ${HoverAnimation};

    background-color: var(--osoc_green);
    border-color: var(--osoc_green);
    color: var(--osoc_blue);

    &:disabled {
        background-color: var(--osoc_green);
        border-color: var(--osoc_green);
        color: var(--osoc_blue);
    }

    &:hover,
    &:active,
    &:focus {
        background-color: var(--osoc_orange) !important;
        border-color: var(--osoc_orange);
        color: var(--osoc_blue);
        box-shadow: none !important;
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

    &:disabled {
        background-color: #8a4944;
        border-color: #8a4944;
    }

    &:hover,
    &:active,
    &:focus {
        background-color: var(--osoc_red_darkened);
        border-color: var(--osoc_red_darkened);
        box-shadow: none !important;
    }
`;

export const CommonDropdownButton = styled(DropdownButton).attrs({
    menuVariant: "dark",
})`
    & > Button {
        ${HoverAnimation};

        background-color: var(--osoc_green);
        border-color: var(--osoc_green);
        color: var(--osoc_blue);

        &:hover,
        &:active,
        &:focus {
            background-color: var(--osoc_orange);
            border-color: var(--osoc_orange);
            color: var(--osoc_blue);
            box-shadow: none !important;
        }
    }
`;

export const GoBack = styled.div`
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    max-width: max-content;

    :hover {
        cursor: pointer;
    }
`;
