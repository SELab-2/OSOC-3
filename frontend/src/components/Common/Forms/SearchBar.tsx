import { FormControlProps } from "react-bootstrap/FormControl";
import { StyledSearchBar } from "./styles";

export default function SearchBar(props: FormControlProps) {
    return <StyledSearchBar {...props} />;
}
