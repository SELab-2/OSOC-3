import styled from "styled-components";
import Modal from "react-bootstrap/Modal";

export const StyledModal = styled(Modal)`
    color: white;
    background-color: #00000060;
    margin-top: 5%;
    .modal-content {
        background-color: #272741;
        border-radius: 5px;
        border-color: #f14a3b;
    }
`;

export const ModalHeader = styled(Modal.Header)`
    border-bottom: 1px solid #131329;
`;
export const ModalFooter = styled(Modal.Footer)`
    border-top: 1px solid #131329;
`;

export const Button = styled.button`
    border-radius: 5px;
    border: none;
    padding: 5px 10px;
    background-color: #131329;
    color: white;
`;

export const DeleteButton = styled(Button)`
    background-color: #f14a3b;
`;
