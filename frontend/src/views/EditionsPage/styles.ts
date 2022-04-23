import styled from "styled-components";
import Container from "react-bootstrap/Container";

export const EditionsPageContainer = styled(Container).attrs(() => ({
    className: "mt-2",
}))`
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: auto;
`;
