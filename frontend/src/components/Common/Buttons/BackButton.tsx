import { GoBack } from "./styles";
import { BiArrowBack } from "react-icons/bi";

export default function BackButton(props: { label: string; onClick: () => void }) {
    return (
        <GoBack onClick={props.onClick}>
            <BiArrowBack />
            {props.label}
        </GoBack>
    );
}
