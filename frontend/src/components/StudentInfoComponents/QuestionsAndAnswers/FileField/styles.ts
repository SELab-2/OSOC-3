import styled from "styled-components";

export const FileLink = styled.a`
    width: fit-content;
    color: var(--osoc_orange);
    &:hover {
        cursor: pointer;
        color: var(--osoc_green);
        transition: 200ms ease-out;
    }
`;
