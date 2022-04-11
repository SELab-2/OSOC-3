import { StyledNewEditionButton } from "./styles";

interface Props {
    onClick: () => void;
}

/**
 * Button to create a new edition, redirects to the [[CreateEditionPage]].
 */
export default function NewEditionButton({ onClick }: Props) {
    return <StyledNewEditionButton onClick={onClick}>Create new edition</StyledNewEditionButton>;
}
