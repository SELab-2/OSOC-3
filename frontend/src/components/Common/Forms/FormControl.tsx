import { FormControlProps } from "react-bootstrap/FormControl";
import { StyledFormControl } from "./styles";

/**
 * An styled version of Bootstrap's Form.Control
 */
export default function FormControl(props: FormControlProps) {
    return <StyledFormControl {...props} />;
}
