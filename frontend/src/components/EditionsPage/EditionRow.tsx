import { Edition } from "../../data/interfaces";
import DeleteEditionButton from "./DeleteEditionButton";
import { RowContainer } from "./styles";
import MarkReadonlyButton from "./MarkReadonlyButton";
import React from "react";
import Col from "react-bootstrap/Col";

interface Props {
    edition: Edition;
    handleClick: (edition: Edition) => Promise<void>;
}

/**
 * A row in the [[EditionsTable]]
 */
export default function EditionRow(props: Props) {
    return (
        <tr>
            <RowContainer>
                <Col sm={"4"}>
                    <div className={"ms-0"}>
                        <h4>{props.edition.name}</h4>
                        {props.edition.year}
                    </div>
                </Col>
                <Col sm={"4"} className={"my-auto text-center"}>
                    <MarkReadonlyButton
                        edition={props.edition}
                        handleClick={async () => await props.handleClick(props.edition)}
                    />
                </Col>
                <Col sm={"4"} className={"my-auto"}>
                    <DeleteEditionButton edition={props.edition} />
                </Col>
            </RowContainer>
        </tr>
    );
}
