import { StyledMultiSelect } from "./styles";
import { IMultiselectProps } from "multiselect-react-dropdown/dist/multiselect/interface";

export default function CommonMultiselect(props: IMultiselectProps) {
    return <StyledMultiSelect {...props} />;
}
