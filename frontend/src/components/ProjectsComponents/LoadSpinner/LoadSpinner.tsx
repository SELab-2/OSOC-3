import { Spinner } from "react-bootstrap";
import { SpinnerContainer } from "./styles";

export default function LoadSpinner({ show }: { show: boolean }) {
    if (!show) return null;
    return (
        <SpinnerContainer>
            <Spinner animation="border" />
        </SpinnerContainer>
    );
}
