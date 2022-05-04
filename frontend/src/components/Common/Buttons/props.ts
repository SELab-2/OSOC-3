import { ButtonProps } from "react-bootstrap/Button";

export interface BasicButton extends ButtonProps {
    label?: string;
    showIcon?: boolean;
}
