import { EditionsTable, NewEditionButton } from "../../components/EditionsPage";
import { useNavigate } from "react-router-dom";
import { PageContainer } from "../../App.styles";

/**
 * Page where users can see all editions they can access,
 * and admins can delete editions.
 */
export default function EditionsPage() {
    const navigate = useNavigate();

    return (
        <PageContainer>
            <NewEditionButton onClick={() => navigate("/editions/new")} />
            <EditionsTable />
        </PageContainer>
    );
}
