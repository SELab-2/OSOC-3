import { Edition } from "../../data/interfaces";
import DeleteEditionButton from "./DeleteEditionButton";
import { RowContainer } from "./styles";

interface Props {
    edition: Edition;
}

/**
 * A row in the [[EditionsTable]]
 */
export default function EditionRow(props: Props) {
    return (
        <tr>
            <RowContainer>
                <div className={"ms-0 me-auto"}>
                    <h4>{props.edition.name}</h4>
                    {props.edition.year}
                </div>
                <DeleteEditionButton edition={props.edition} />
            </RowContainer>
        </tr>
    );
}
