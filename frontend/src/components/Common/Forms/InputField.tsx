import Form from "react-bootstrap/Form";
import { FormControlProps } from "react-bootstrap/FormControl";

/**
 * An input field that can be used in forms
 * This is just the basic React-Bootstrap input field, but it does
 * make sure that everyone uses the same one instead of their
 * own implementation of it.
 */
export default function InputField(props: FormControlProps) {
    return <Form.Control {...props} />;
}
