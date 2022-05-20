import { BasicButton } from "./props";
import { OrangeButton as StyledOrangeButton } from "./styles";

/**
 * Orange button
 */
export default function OrangeButton({
    label = "",
    showIcon = false,
    children,
    ...props
}: BasicButton) {
    return (
        <StyledOrangeButton {...props}>
            {children}
            {label}
        </StyledOrangeButton>
    );
}
