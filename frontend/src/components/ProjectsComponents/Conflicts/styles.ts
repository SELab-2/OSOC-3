import styled from "styled-components";
import { Button, Offcanvas, Spinner } from "react-bootstrap";
import { Link } from "react-router-dom";

export const ConButton = styled(Button)`
    float: right;
    margin: 20px;
`;

export const SidePanel = styled(Offcanvas)`
    background-color: #323252;
    width: fit-content;
    color: white;
`;

export const Loader = styled(Spinner)`
    float: right;
    margin: 20px;
`;

export const ListLink = styled(Link)`
    color: white;
`;
