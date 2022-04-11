import { EditionsTable } from "../../components/EditionsPage";
import { EditionsPageContainer } from "./styles";

/**
 * Page where users can see all editions they can access,
 * and admins can delete editions.
 */
export default function EditionsPage() {
    return (
        <EditionsPageContainer>
            <h1 className={"mx-auto mb-5"}>Editions</h1>
            <EditionsTable />
        </EditionsPageContainer>
    );
}
