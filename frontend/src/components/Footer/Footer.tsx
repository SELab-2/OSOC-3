import { FooterBox, FooterTitle } from "./styles";
import FooterLinks from "./FooterLinks";

/**
 * Footer placed at the bottom of the site, containing various links related
 * to the application or our code.
 *
 * The footer is only displayed when signed in.
 */
export default function Footer() {
    return (
        <FooterBox className={"p-2"}>
            <FooterTitle className={"m-4"}>Open Summer of Code</FooterTitle>
            <FooterLinks />
        </FooterBox>
    );
}
