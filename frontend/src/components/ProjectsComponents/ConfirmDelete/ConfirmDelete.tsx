import { StyledModal, ModalFooter, ModalHeader, Button, DeleteButton } from "./styles";

/**
 *
 * @param visible whether to display the confirm screen.
 * @param handleClose what to do when the user closes the confirm screen.
 * @param handleConfirm what to do when the user confirms the delete action.
 * @param name the name of the project that is going to be deleted.
 * @returns the modal the confirm the deletion of a project.
 */
export default function ConfirmDelete({
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
