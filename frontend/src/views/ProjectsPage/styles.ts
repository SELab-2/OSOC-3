import styled from "styled-components";

export const CardsGrid = styled.div`
    display: grid;
    grid-gap: 5px;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-flow: dense;
`;
