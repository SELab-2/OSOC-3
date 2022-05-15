import React, { useEffect, useState } from "react";
import { MailHistoryPage } from "./styles";
import Table from "react-bootstrap/Table";
import { getEmails } from "../../utils/api/student_email_history";
import { EmailHistoryList } from "../../data/interfaces";
import { EmailType } from "../../data/enums";
import { useParams } from "react-router-dom";
import { CenterDiv, MessageDiv } from "../MailOverviewPage/styles";

/**
 * Page that shows the email history of a student in a table
 */
export default function StudentMailHistoryPage() {
    const init: EmailHistoryList = {
        emails: [],
    };
    const [table, setTable] = useState(init);
    const [gotEmails, setGotEmails] = useState(false);
    const { editionId, id } = useParams();
    useEffect(() => {
        const updateEmailList = async () => {
            try {
                setGotEmails(false);
                const emails = await getEmails(editionId, id);
                setTable(emails);
                setGotEmails(true);
            } catch (exception) {
                console.log(exception);
            }
        };
        updateEmailList();
    }, [editionId, id]);

    let emailtable;
    if (gotEmails && table.emails.length === 0) {
        emailtable = (
            <CenterDiv>
                <MessageDiv>No states found.</MessageDiv>
            </CenterDiv>
        );
    } else {
        emailtable = (
            <Table bordered striped>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>State</th>
                    </tr>
                </thead>
                <tbody>
                    {table.emails.map(d => (
                        <tr key={d.emailId}>
                            <td>{new Date(String(d.date)).toLocaleString("nl-be")}</td>
                            <td>{Object.values(EmailType)[d.decision]}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        );
    }

    return <MailHistoryPage>{emailtable}</MailHistoryPage>;
}
