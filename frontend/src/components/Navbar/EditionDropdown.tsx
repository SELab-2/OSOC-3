import React from "react";
import Dropdown from "react-bootstrap/esm/Dropdown";

interface Props {
    editions: string[];
    currentEdition: string;
    setCurrentEdition: (edition: string) => void;
}

export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];

    props.editions.forEach((edition: string) => {
        navItems.push(<Dropdown.Item href={"/"}>{edition}</Dropdown.Item>);
    });

    return <Dropdown title={`Edition ${props.currentEdition}`}>{navItems}</Dropdown>;
}
