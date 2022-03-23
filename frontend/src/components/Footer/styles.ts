import styled from "styled-components";

export const FooterBox = styled.div`
    background-color: var(--osoc_blue);
    position: absolute;
    bottom: 0;
    width: 100%;
`;

export const FooterTitle = styled.h3`
    font-weight: bold;
`;

export const FooterLink = styled.a`
    color: white;

    &:hover {
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }
`;
