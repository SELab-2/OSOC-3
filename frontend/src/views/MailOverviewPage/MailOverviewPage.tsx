import React, { useState } from "react";
import { getMailOverview, setStateRequest, StudentEmail } from "../../utils/api/mail_overview";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import InfiniteScroll from "react-infinite-scroller";
import { Multiselect } from "multiselect-react-dropdown";
import { Form } from "react-bootstrap";
import {
    TableDiv,
    DropDownButtonDiv,
    SearchDiv,
    FilterDiv,
    SearchAndFilterDiv,
    CenterDiv,
    MessageDiv,
} from "./styles";
import { EmailType } from "../../data/enums";
import { useParams } from "react-router-dom";
import { Student } from "../../data/interfaces";
import LoadSpinner from "../../components/Common/LoadSpinner";
import { toast } from "react-toastify";
import { StyledTable } from "../../components/Common/Tables/styles";

interface EmailRow {
    email: StudentEmail;
    checked: boolean;
}

/**
 * Page that shows the email status of all students, with the possibility to change the status
 */
export default function MailOverviewPage() {
    const [emailRows, setEmailRows] = useState<EmailRow[]>([]);
    const [gotEmails, setGotEmails] = useState(false);
    const [loading, setLoading] = useState(false);
    const [moreEmailsAvailable, setMoreEmailsAvailable] = useState(true); // Endpoint has more emailRows available
    const [page, setPage] = useState(0);
    const [allSelected, setAllSelected] = useState(false);

    // Keep track of the set filters
    const [searchTerm, setSearchTerm] = useState("");
    const [filters, setFilters] = useState<EmailType[]>([]);

    const { editionId } = useParams();

    /**
     * update the table with new values
     */
    async function updateMailOverview() {
        if (loading) {
            return;
        }

        setLoading(true);

        const response = await toast.promise(
            getMailOverview(editionId, page, searchTerm, filters),
            { error: "Failed to receive states" }
        );
        if (response.studentEmails.length === 0) {
            setMoreEmailsAvailable(false);
        }
        if (page === 0) {
            setEmailRows(
                response.studentEmails.map(email => {
                    return {
                        email: email,
                        checked: false,
                    };
                })
            );
        } else {
            setEmailRows(
                emailRows.concat(
                    response.studentEmails.map(email => {
                        return {
                            email: email,
                            checked: false,
                        };
                    })
                )
            );
        }
        setPage(page + 1);

        setGotEmails(true);
        setLoading(false);
    }

    function refresh() {
        setPage(0);
        setGotEmails(false);
        setMoreEmailsAvailable(true);
        setEmailRows([]);
        setAllSelected(false);
    }

    function searchName(newSearchTerm: string) {
        setSearchTerm(newSearchTerm);
        refresh();
    }

    function changeFilter(newFilter: EmailType[]) {
        setFilters(newFilter);
        refresh();
    }

    /**
     * Keeps the selectedRows list up-to-date when a student is selected/unselected in the table
     */
    function selectNewStudent(student: Student, isSelect: boolean) {
        setEmailRows(
            emailRows.map(row => {
                if (row.email.student === student) {
                    row.checked = isSelect;
                }
                return row;
            })
        );
        setAllSelected(false);
    }

    function selectAll(isSelect: boolean) {
        setAllSelected(isSelect);
        setEmailRows(
            emailRows.map(row => {
                row.checked = isSelect;
                return row;
            })
        );
    }

    async function changeState(eventKey: string) {
        const selectedStudents = emailRows
            .filter(row => row.checked)
            .map(row => row.email.student.studentId);

        await toast.promise(setStateRequest(eventKey, editionId, selectedStudents), {
            error: "Failed to change state",
            pending: "Changing state",
        });
        setEmailRows(
            emailRows.map(row => {
                row.checked = false;
                return row;
            })
        );
        setAllSelected(false);
        refresh();
    }

    let table;
    if (gotEmails && emailRows.length === 0) {
        table = (
            <CenterDiv>
                <MessageDiv>No students found.</MessageDiv>
            </CenterDiv>
        );
    } else {
        table = (
            <TableDiv>
                <InfiniteScroll
                    loadMore={updateMailOverview}
                    hasMore={moreEmailsAvailable}
                    loader={<LoadSpinner show={true} />}
                    initialLoad={true}
                    useWindow={false}
                    getScrollParent={() => document.getElementById("root")}
                >
                    <StyledTable>
                        <thead>
                            <tr>
                                <th>
                                    <Form.Check
                                        type="checkbox"
                                        onChange={e => selectAll(e.target.checked)}
                                        checked={allSelected}
                                    />
                                </th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Current State</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {emailRows.map(row => (
                                <tr key={row.email.student.studentId}>
                                    <td>
                                        <Form.Check
                                            type="checkbox"
                                            onChange={e =>
                                                selectNewStudent(
                                                    row.email.student,
                                                    e.target.checked
                                                )
                                            }
                                            checked={row.checked}
                                        />
                                    </td>
                                    <td>{row.email.student.firstName}</td>
                                    <td>{row.email.student.lastName}</td>
                                    <td>
                                        {Object.values(EmailType)[row.email.emails[0].decision]}
                                    </td>
                                    <td>
                                        {new Date(String(row.email.emails[0].date)).toLocaleString(
                                            "nl-be"
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </StyledTable>
                </InfiniteScroll>
            </TableDiv>
        );
    }

    return (
        <>
            <DropDownButtonDiv>
                <DropdownButton
                    id="dropdown-setstate-button"
                    title="Set state of selected students"
                    menuVariant="dark"
                >
                    {Object.values(EmailType).map((type, index) => (
                        <Dropdown.Item
                            eventKey={index.toString()}
                            key={type}
                            onClick={() => changeState(index.toString())}
                        >
                            {type}
                        </Dropdown.Item>
                    ))}
                </DropdownButton>
            </DropDownButtonDiv>
            <SearchAndFilterDiv>
                <SearchDiv>
                    <InputGroup className="mb-3">
                        <FormControl
                            placeholder="Search a student"
                            aria-label="Username"
                            onChange={e => {
                                searchName(e.target.value);
                            }}
                        />
                    </InputGroup>
                </SearchDiv>
                <FilterDiv>
                    <Multiselect
                        placeholder="Filter on State"
                        showArrow={true}
                        isObject={false}
                        onRemove={changeFilter}
                        onSelect={changeFilter}
                        options={Object.values(EmailType)}
                    />
                </FilterDiv>
            </SearchAndFilterDiv>
            {table}
        </>
    );
}
