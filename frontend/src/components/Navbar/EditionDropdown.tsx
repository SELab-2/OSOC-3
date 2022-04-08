import NavDropdown from "react-bootstrap/NavDropdown";
import React, { useEffect } from "react";

interface Props {
    editions: string[];
    currentEdition: string;
    setCurrentEdition: (edition: string) => void;
}

export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];

    props.editions.forEach((edition: string) => {
        navItems.push(<NavDropdown.Item href={"/"}>{edition}</NavDropdown.Item>);
    });

    return <NavDropdown title={`Edition ${props.currentEdition}`}>{navItems}</NavDropdown>;
}
