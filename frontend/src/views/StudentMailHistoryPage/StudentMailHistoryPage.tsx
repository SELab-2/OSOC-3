import React, { useEffect, useState } from "react";
import {
    BackButtonDiv,
    ButtonDiv,
    CenterDiv,
    CustomDropdownButton,
    NameDiv,
    TableDiv,
} from "./styles";
import { getEmails } from "../../utils/api/student_email_history";
import { Email, Student } from "../../data/interfaces";
import { EmailType } from "../../data/enums";
import { useNavigate, useParams } from "react-router-dom";
import { MessageDiv } from "../MailOverviewPage/styles";
import { DateTd, DateTh, StyledTable } from "../../components/Common/Tables/styles";
import { LoadSpinner } from "../../components/Common";
import BackButton from "../../components/Common/Buttons/BackButton";
import Dropdown from "react-bootstrap/Dropdown";
import { toast } from "react-toastify";
import { setStateRequest } from "../../utils/api/mail_overview";
import { isReadonlyEdition } from "../../utils/logic";
import { useAuth } from "../../contexts";

/**
 * Page that shows the email history of a student in a table
 */
export default function StudentMailHistoryPage() {
    const [emails, setEmails] = useState<Email[]>([]);
    const [gotEmails, setGotEmails] = useState(false);
    const [student, setStudent] = useState<Student | undefined>();

    const { editionId, id } = useParams();
    const { editions } = useAuth();
    const navigate = useNavigate();

    async function getData() {
        setEmails([]);
        setGotEmails(false);
        try {
            const response = await getEmails(editionId, id);
            setEmails(response.emails);
            setStudent(response.student);
            setGotEmails(true);
        } catch (exception) {
            console.log(exception);
        }
    }

    useEffect(() => {
        getData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [editionId, id]);

    async function changeState(eventKey: string) {
        await toast.promise(setStateRequest(eventKey, editionId, [student!.studentId]), {
            error: "Failed to change state",
            pending: "Changing state",
            success: "Successfully added state",
        });
        await getData();
    }

    if (!gotEmails) {
        return <LoadSpinner show={true} />;
    }

    let emailtable;
    if (emails.length === 0) {
        emailtable = <MessageDiv>No states found.</MessageDiv>;
    } else {
        emailtable = (
            <TableDiv>
                <StyledTable>
                    <thead>
                        <tr>
                            <th>State</th>
                            <DateTh>Date</DateTh>
                        </tr>
                    </thead>
                    <tbody>
                        {emails.map(d => (
                            <tr key={d.emailId}>
                                <td>{Object.values(EmailType)[d.decision]}</td>
                                <DateTd>{new Date(String(d.date)).toLocaleString("nl-be")}</DateTd>
                            </tr>
                        ))}
                    </tbody>
                </StyledTable>
            </TableDiv>
        );
    }

    return (
        <div>
            <BackButtonDiv>
                <BackButton
                    onClick={() => navigate("/editions/" + editionId + "/students/" + id)}
                    label="  Student details"
                />
            </BackButtonDiv>
            <CenterDiv>
                <NameDiv>
                    <h4>{student?.firstName + " " + student?.lastName}</h4>
                </NameDiv>
                {!isReadonlyEdition(editionId, editions) && (
                    <ButtonDiv>
                        <CustomDropdownButton id="dropdown-setstate-button" title="Add new state">
                            {Object.values(EmailType).map((type, index) => (
                                <Dropdown.Item
                                    eventKey={index.toString()}
                                    key={type}
                                    onClick={() => changeState(index.toString())}
                                >
                                    {type}
                                </Dropdown.Item>
                            ))}
                        </CustomDropdownButton>
                    </ButtonDiv>
                )}
                {emailtable}
            </CenterDiv>
        </div>
    );
}
