import { AnimatedButton } from "./props";
import { RedButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTriangleExclamation } from "@fortawesome/free-solid-svg-icons/faTriangleExclamation";
import { IconProp } from "@fortawesome/fontawesome-svg-core";

/**
 * Red button with a warning triangle icon
 */
export default function WarningButton({
    label = "",
    showIcon = true,
    animated = "false",
    children,
    ...props
}: AnimatedButton) {
    return (
        <RedButton animated={animated} {...props}>
            {showIcon && (
                <FontAwesomeIcon
                    icon={faTriangleExclamation as IconProp}
                    className={label ? "me-2" : ""}
                />
            )}
            {children}
            {label}
        </RedButton>
    );
}
