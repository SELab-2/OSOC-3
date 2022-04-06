import { StyledModal, ModalFooter, ModalHeader, Button, DeleteButton } from "./styles";

export default function ConfirmDelete({
    visible,
    handleClose,
    handleConfirm,
    name,
}: {
    visible: boolean;
    handleConfirm: () => void;
    handleClose: () => void;
    name: string;
}) {
    return (
        <StyledModal show={visible} onHide={handleClose}>
            <ModalHeader closeButton>
                <StyledModal.Title>Confirm delete</StyledModal.Title>
            </ModalHeader>

            <StyledModal.Body>Are you sure you want to delete {name}?</StyledModal.Body>

            <ModalFooter>
                <Button onClick={handleClose}>Cancel</Button>
                <DeleteButton onClick={handleConfirm}>Delete</DeleteButton>
            </ModalFooter>
        </StyledModal>
    );
}
