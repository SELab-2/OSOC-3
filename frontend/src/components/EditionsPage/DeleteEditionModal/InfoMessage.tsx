import Form from "react-bootstrap/Form";
import React from "react";

interface Props {
    editionName: string;
}

export default function InfoMessage(props: Props) {
    return (
        <>
            <Form.Text>
                Deleting <i>{props.editionName}</i> has some serious consequences that{" "}
                <u>
                    <b>can never be undone</b>
                </u>
                .
            </Form.Text>
            <br />
            <br />
            <Form.Text>
                This includes, but is not limited to, removal of:
                <ul>
                    <li>the edition itself</li>
                    <li>all students linked to this edition</li>
                    <li>all projects linked to this edition</li>
                </ul>
            </Form.Text>
        </>
    );
}
