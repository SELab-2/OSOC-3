import { CreateButton } from "../../Common/Buttons";
import { StyledModal, ModalHeader, ModalFooter, Button } from "./styles";

export default function AddStudentModal({
    visible,
    handleClose,
    handleConfirm,
    name,
}: {
    visible: boolean;
    handleClose: () => void;
    handleConfirm: () => void;
    name: string;
}) {
    return (
        <StyledModal show={visible} onHide={handleClose}>
            <ModalHeader closeButton>
                <StyledModal.Title>Suggest student for project</StyledModal.Title>
            </ModalHeader>

            <StyledModal.Body>Please motivate your decision</StyledModal.Body>

            <ModalFooter>
                <Button onClick={handleClose}>Cancel</Button>
                <CreateButton label="Suggest student" onClick={handleConfirm}/>
            </ModalFooter>
        </StyledModal>
    );
}
