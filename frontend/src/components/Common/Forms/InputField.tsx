import Form from "react-bootstrap/Form";
import { FormControlProps } from "react-bootstrap/FormControl";

/**
 * An input field that can be used in forms
 */
export default function InputField(props: FormControlProps) {
    return <Form.Control {...props} />;
}
