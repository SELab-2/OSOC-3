import React, { useEffect, useState } from "react";
import { MailHistoryPage } from "./styles";
import Table from "react-bootstrap/Table";
import { getEmails } from "../../utils/api/student_email_history";
import { EmailHistoryList } from "../../data/interfaces";
import { EmailType } from "../../data/enums";
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
                        <tr key={d.emailId}>
                            <td>{new Date(String(d.date)).toLocaleString("nl-be")}</td>
                            <td>{Object.values(EmailType)[d.type]}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </MailHistoryPage>
    );
}
