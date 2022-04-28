import styled from "styled-components";

export const FooterBox = styled.div`
    background-color: var(--osoc_blue);
    width: 100%;
`;

export const FooterTitle = styled.h3`
    font-weight: bold;
`;

export const FooterLink = styled.a`
    color: white;
    transition: 200ms ease-out;
    text-decoration: none;

    &:hover {
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }
`;
