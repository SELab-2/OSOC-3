import React from "react";
import { MailHistoryPage } from "./styles";
import Table from "react-bootstrap/Table";

/**
 * Page that shows the email history of a student in a table
 */
export default function StudentMailHistoryPage() {
    const data = [
        { date: "Tuesday, 12-Apr-22 13:52:31", type: "Practical Information" },
        { date: "Monday, 11-Apr-22 12:52:31", type: "Accepted" },
        { date: "Sunday, 10-Apr-22 12:51:01", type: "Maybe" },
    ];
    const tableItems = data.map(d => (
        <tr>
            <td>{d.date}</td>
            <td>{d.type}</td>
        </tr>
    ));
    return (
        <MailHistoryPage>
            <Table bordered striped>
                <thead>
                    <tr>
                        <th>Sent</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>{tableItems}</tbody>
            </Table>
        </MailHistoryPage>
    );
}
