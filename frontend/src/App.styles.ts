import styled from "styled-components";

export const Container = styled.div`
    min-height: 100vh;
    display: flex;
    flex-direction: column;
`;

export const ContentWrapper = styled.div`
    flex: 1;
`;

export const PageContainer = styled.div.attrs(() => ({
    className: "mt-2",
}))`
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: auto;
`;

export const CenterText = styled.div`
    text-align: center;
`;
