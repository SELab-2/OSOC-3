import React, { useEffect, useState } from "react";
import { MailHistoryPage } from "./styles";
import Table from "react-bootstrap/Table";
import { getEmails, EmailHistoryList } from "../../utils/api/student_email_history";
/**
 * Page that shows the email history of a student in a table
 */
export default function StudentMailHistoryPage() {
    const init: EmailHistoryList = {
        emails: [],
    };
    const [table, setTable] = useState(init);

    useEffect(() => {
        const updateEmailList = async () => {
            try {
                const emails = await getEmails();
                setTable(emails);
            } catch (exception) {
                console.log(exception);
            }
        };
        updateEmailList();
    }, []);

    return (
        <MailHistoryPage>
            <Table bordered striped>
                <thead>
                    <tr>
                        <th>Sent</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    {table.emails.map(d => (
                        <tr key={d.email_id}>
                            <td>{d.date}</td>
                            <td>{d.type}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </MailHistoryPage>
    );
}
