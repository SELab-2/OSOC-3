import styled from "styled-components";

export const SpinningC = styled.img.attrs(() => ({
    height: "40px",
    width: "auto",
    alt: "Loading...",
}))`
    animation: rotate-c infinite 5s linear;

    @keyframes rotate-c {
        0% {
            transform: rotate(0deg);
        }

        100% {
            transform: rotate(360deg);
        }
    }
`;
