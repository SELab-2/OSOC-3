import { FooterBox, FooterTitle } from "./styles";
import FooterLinks from "./FooterLinks";

export default function Footer() {
    return (
        <FooterBox className={"p-2"}>
            <FooterTitle className={"m-4"}>Open Summer of Code</FooterTitle>
            <FooterLinks />
        </FooterBox>
    );
}
