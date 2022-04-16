import React, { useEffect, useState } from "react";
import { getMailOverview, StudentEmails } from "../../utils/api/mail_overview";
import Table from "react-bootstrap/Table";
// import BootstrapTable from "react-bootstrap-table-next";
import { EmailType } from "../../data/enums";
import { MailOverviewPageDiv } from "./styles";
// TODO: convert to react-bootstrap-table-next
// TODO: add comments to created functions and interfaces
/**
 * Page that shows the email status of all students, with the possibility to change the status
 */
export default function MailOverviewPage() {
    const init: StudentEmails = {
        studentEmails: [],
    };
    const [table, setTable] = useState(init);

    useEffect(() => {
        const updateMailOverview = async () => {
            try {
                const studentEmails = await getMailOverview();
                setTable(studentEmails);
            } catch (exception) {
                console.log(exception);
            }
        };
        updateMailOverview();
    }, []);
    return (
        <MailOverviewPageDiv>
            <Table bordered striped hover>
                <thead>
                    <tr>
                        <th>Fist name</th>
                        <th>Last name</th>
                        <th>Email ID</th>
                        <th>Last Email Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table.studentEmails.map(d => (
                        <tr key={d.student.studentId}>
                            <td>{d.student.firstName}</td>
                            <td>{d.student.lastName}</td>
                            <td>{d.emails[0].emailId}</td>
                            <td>{Object.values(EmailType)[d.emails[0].type]}</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </MailOverviewPageDiv>
    );
}
