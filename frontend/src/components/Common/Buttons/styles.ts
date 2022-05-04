import Button from "react-bootstrap/Button";
import styled from "styled-components";

import { HoverAnimation } from "../styles";

export const GreenButton = styled(Button)`
    ${HoverAnimation};

    background-color: var(--osoc_green);
    border-color: var(--osoc_green);

    &:hover {
        background-color: var(--osoc_green_darkened);
        border-color: var(--osoc_green_darkened);
    }
`;

export const RedButton = styled(Button)`
    ${HoverAnimation};

    background-color: var(--osoc_red);
    border-color: var(--osoc_red);

    &:hover {
        background-color: var(--osoc_red_darkened);
        border-color: var(--osoc_red_darkened);
    }
`;
