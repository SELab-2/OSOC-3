import { BSBrand } from "./styles";

/**
 * React component that shows the OSOC logo & title in the [[Navbar]]
 */
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
            Open Summer of Code
        </BSBrand>
    );
}
