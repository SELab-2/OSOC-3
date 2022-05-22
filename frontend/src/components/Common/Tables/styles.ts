import styled from "styled-components";
import Table from "react-bootstrap/Table";

export const StyledTable = styled(Table).attrs({
    striped: true,
    bordered: true,
    variant: "dark",
    hover: false,
})``;

export const RemoveTh = styled.th`
    width: 200px;
    text-align: center;
`;

export const RemoveTd = styled.td`
    text-align: center;
    vertical-align: middle;
`;

export const DateTh = styled.th`
    text-align: center;
`;

export const DateTd = styled.td`
    text-align: center;
`;
