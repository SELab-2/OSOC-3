import { StyledModal, Button, ModalFooter, ModalHeader, DeleteButton } from "./styles";

export default function Modal({
    show,
    handleClose,
    name,
}: {
    show: boolean;
    handleClose: () => void;
    name: string;
}) {
    return (
        <StyledModal show={show} onHide={handleClose}>
            <ModalHeader closeButton>
                <StyledModal.Title>Confirm delete</StyledModal.Title>
            </ModalHeader>

            <StyledModal.Body>Are you sure you want to delete {name}?</StyledModal.Body>

            <ModalFooter>
                <Button onClick={handleClose}>Cancel</Button>
                <DeleteButton onClick={handleClose}>Delete</DeleteButton>
            </ModalFooter>
        </StyledModal>
    );
}
