import { StyledMultiSelect } from "./styles";
import { IMultiselectProps } from "multiselect-react-dropdown/dist/multiselect/interface";
import "./formsStyles.css";

export default function CommonMultiselect(props: IMultiselectProps) {
    return <StyledMultiSelect {...props} />;
}
