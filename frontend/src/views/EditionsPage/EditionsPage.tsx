import { EditionsTable, NewEditionButton } from "../../components/EditionsPage";
import { EditionsPageContainer } from "./styles";
import { useNavigate } from "react-router-dom";

/**
 * Page where users can see all editions they can access,
 * and admins can delete editions.
 */
export default function EditionsPage() {
    const navigate = useNavigate();

    return (
        <EditionsPageContainer>
            <NewEditionButton onClick={() => navigate("/editions/new")} />
            <EditionsTable />
        </EditionsPageContainer>
    );
}
