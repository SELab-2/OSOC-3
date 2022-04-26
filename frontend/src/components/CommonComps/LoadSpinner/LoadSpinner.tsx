import { Spinner } from "react-bootstrap";
import { SpinnerContainer } from "./styles";
/**
 *
 * @param show: whether to show the spinner or not
 * @returns a spinner to display when data is being fetched
 */
export default function LoadSpinner({ show }: { show: boolean }) {
    if (!show) return null;
    return (
        <SpinnerContainer>
            <Spinner animation="border" />
        </SpinnerContainer>
    );
}
