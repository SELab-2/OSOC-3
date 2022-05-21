import styled from "styled-components";
import { Offcanvas } from "react-bootstrap";
import { Link } from "react-router-dom";

export const SidePanel = styled(Offcanvas)`
    background-color: #323252;
    width: 33em;
    max-width: fit-content;
    color: white;
`;

export const ListLink = styled(Link)`
    color: white;
    margin-right: 10px;
    white-space: nowrap;
`;

export const ConflictButtonDiv = styled.div`
    float: right;
`;
