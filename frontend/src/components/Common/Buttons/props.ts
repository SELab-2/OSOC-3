import { ButtonProps } from "react-bootstrap/Button";
import React from "react";

export interface BasicButton extends ButtonProps {
    label?: string;
    showIcon?: boolean;
    children?: React.ReactNode;
}

export interface AnimatedButton extends BasicButton {
    animated?: string;
}
