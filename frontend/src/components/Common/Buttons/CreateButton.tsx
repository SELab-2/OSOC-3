import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons/faPlus";
import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { BasicButton } from "./props";
import { GreenButton } from "./styles";

/**
 * Green button with a "+"-icon
 */
export default function CreateButton({ label = "", showIcon = true, ...props }: BasicButton) {
    return (
        <GreenButton {...props}>
            {showIcon && (
                <FontAwesomeIcon icon={faPlus as IconProp} className={label ? "me-2" : ""} />
            )}
            {label}
        </GreenButton>
    );
}
