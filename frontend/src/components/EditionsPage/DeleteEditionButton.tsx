import { Edition } from "../../data/interfaces";
import { DeleteButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons/faTriangleExclamation";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";
import React, { useState } from "react";
import DeleteEditionModal from "./DeleteEditionModal/DeleteEditionModal";

interface Props {
    edition: Edition;
}

export default function DeleteEditionButton(props: Props) {
    const { role } = useAuth();
    const [showModal, setShowModal] = useState(false);

    // Only admins can see this button
    if (role !== Role.ADMIN) {
        return null;
    }

    function handleClick() {
        setShowModal(true);
    }

    return (
        <DeleteButton onClick={handleClick}>
            <FontAwesomeIcon icon={faTriangleExclamation as IconProp} /> Delete this edition
            <DeleteEditionModal edition={props.edition} show={showModal} setShow={setShowModal} />
        </DeleteButton>
    );
}
