import { BasicButton } from "./props";
import { RedButton } from "./styles";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrashCan } from "@fortawesome/free-solid-svg-icons/faTrashCan";
import { IconProp } from "@fortawesome/fontawesome-svg-core";

/**
 * Red button with a garbage can icon
 */
export default function DeleteButton({
    label = "",
    showIcon = true,
    children,
    ...props
}: BasicButton) {
    return (
        <RedButton {...props}>
            {showIcon && (
                <FontAwesomeIcon icon={faTrashCan as IconProp} className={label ? "me-2" : ""} />
            )}
            {children}
            {label}
        </RedButton>
    );
}
