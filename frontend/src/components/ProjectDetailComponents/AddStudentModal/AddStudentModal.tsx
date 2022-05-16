import { CreateButton } from "../../Common/Buttons";
import { FormControl } from "../../Common/Forms";
import { StyledModal, ModalHeader, ModalFooter, Button } from "./styles";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import { useState } from "react";
import { DropResult } from "react-beautiful-dnd";

export default function AddStudentModal({
    visible,
    handleClose,
    handleConfirm,
    result,
}: {
    visible: boolean;
    handleClose: () => void;
    handleConfirm: (motivation: string, result: DropResult) => void;
    result: DropResult;
}) {
    const [motivation, setMotivation] = useState("");
    return (
        <StyledModal show={visible} onHide={handleClose}>
            <ModalHeader closeButton>
                <StyledModal.Title>Suggest student for project</StyledModal.Title>
            </ModalHeader>

            <StyledModal.Body>
                Please motivate your decision
                <FloatingLabel label={"Motivation"} className={"mb-1"}>
                    <FormControl
                        placeholder={"Good fit!"}
                        value={motivation}
                        onChange={e => {
                            setMotivation(e.target.value);
                        }}
                    />
                </FloatingLabel>
            </StyledModal.Body>

            <ModalFooter>
                <Button
                    onClick={() => {
                        handleClose();
                        setMotivation("");
                    }}
                >
                    Cancel
                </Button>
                <CreateButton
                    label="Suggest"
                    onClick={() => {
                        handleConfirm(motivation, result);
                        setMotivation("");
                    }}
                />
            </ModalFooter>
        </StyledModal>
    );
}
