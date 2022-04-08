import { BSBrand } from "./styles";

export default function Brand() {
    return (
        <BSBrand>
            <img
                width={"60px"}
                height={"auto"}
                src={"/assets/osoc_logo_letters_dark.svg"}
                alt={"OSOC logo (light)"}
                className={"me-2"}
            />{" "}
            Open Summer Of Code
        </BSBrand>
    );
}
