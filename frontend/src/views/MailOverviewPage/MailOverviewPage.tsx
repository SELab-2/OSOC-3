import React, { useEffect, useState } from "react";
import { getMailOverview, setStateRequest, StudentEmail } from "../../utils/api/mail_overview";
import Dropdown from "react-bootstrap/Dropdown";
import InfiniteScroll from "react-infinite-scroller";
import { Form } from "react-bootstrap";
import {
    DropDownButtonDiv,
    SearchDiv,
    FilterDiv,
    CenterDiv,
    MessageDiv,
    MailOverviewDiv,
    SearchAndChangeDiv,
    ClearDiv,
    CustomStyledTable,
} from "./styles";
import "../../components/Common/Buttons/buttonsStyles.css";
import { EmailType } from "../../data/enums";
import { useParams } from "react-router-dom";
import { Student } from "../../data/interfaces";
import LoadSpinner from "../../components/Common/LoadSpinner";
import { toast } from "react-toastify";
import SearchBar from "../../components/Common/Forms/SearchBar";
import { CommonMultiselect } from "../../components/Common/Forms";
import { CommonDropdownButton } from "../../components/Common/Buttons/styles";
import { DateTd, DateTh } from "../../components/Common/Tables/styles";
import { isReadonlyEdition } from "../../utils/logic";
import { useAuth } from "../../contexts";

interface EmailRow {
    email: StudentEmail;
    checked: boolean;
}

/**
 * Page that shows the email status of all students, with the possibility to change the status
 */
export default function MailOverviewPage() {
    const { editionId } = useParams();
    const { editions } = useAuth();

    const [emailRows, setEmailRows] = useState<EmailRow[]>([]);
    const [loading, setLoading] = useState(false);
    const [requestedEdition, setRequestedEdition] = useState(editionId);
    const [moreEmailsAvailable, setMoreEmailsAvailable] = useState(true); // Endpoint has more emailRows available
    const [page, setPage] = useState(0);
    const [allSelected, setAllSelected] = useState(false);

    const [controller, setController] = useState<AbortController | undefined>(undefined);

    // Keep track of the set filters
    const [searchTerm, setSearchTerm] = useState("");
    const [filters, setFilters] = useState<EmailType[]>([]);
    const [filtersChanged, setFiltersChanged] = useState(0);

    /**
     * update the table with new values
     */
    async function updateMailOverview(requested: number) {
        const filterChanged = requested === -1;
        const requestedPage = requested === -1 ? 0 : page;

        if (loading && !filterChanged) {
            return;
        }

        setLoading(true);

        if (controller !== undefined) {
            controller.abort();
        }
        const newController = new AbortController();
        setController(newController);

        try {
            const response = await getMailOverview(
                editionId,
                requestedPage,
                searchTerm,
                filters,
                newController
            );
            if (response !== null) {
                if (response.studentEmails.length === 0 && !filterChanged) {
                    setMoreEmailsAvailable(false);
                } else {
                    setMoreEmailsAvailable(true);
                }
                if (requestedPage === 0) {
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
                setPage(requestedPage + 1);
            } else {
                setMoreEmailsAvailable(false);
            }
        } catch (error) {
            toast.error("Failed to retrieve states");
            setMoreEmailsAvailable(false);
        }

        setLoading(false);
    }

    useEffect(() => {
        if (editionId !== requestedEdition) {
            setRequestedEdition(editionId);
            refresh();
        } else {
            setPage(0);
            setMoreEmailsAvailable(true);
            updateMailOverview(-1);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchTerm, filtersChanged, editionId]);

    function refresh() {
        setEmailRows([]);
        setPage(0);
        setMoreEmailsAvailable(true);
        updateMailOverview(-1);
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
            success: "Successfully added state",
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
    if (emailRows.length === 0) {
        if (loading) {
            table = <LoadSpinner show={true} />;
        } else {
            table = (
                <CenterDiv>
                    <MessageDiv>No students found.</MessageDiv>
                </CenterDiv>
            );
        }
    } else {
        table = (
            <InfiniteScroll
                loadMore={updateMailOverview}
                hasMore={moreEmailsAvailable}
                loader={<LoadSpinner show={true} key="spinner" />}
                initialLoad={true}
                useWindow={false}
                getScrollParent={() => document.getElementById("root")}
            >
                <CustomStyledTable>
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
                            <DateTh>Date</DateTh>
                        </tr>
                    </thead>
                    <tbody>
                        {emailRows.map(row => (
                            <tr key={row.email.student.studentId}>
                                <td>
                                    <Form.Check
                                        type="checkbox"
                                        onChange={e =>
                                            selectNewStudent(row.email.student, e.target.checked)
                                        }
                                        checked={row.checked}
                                    />
                                </td>
                                <td>{row.email.student.firstName}</td>
                                <td>{row.email.student.lastName}</td>
                                <td>{Object.values(EmailType)[row.email.emails[0].decision]}</td>
                                <DateTd>
                                    {new Date(String(row.email.emails[0].date)).toLocaleString(
                                        "nl-be"
                                    )}
                                </DateTd>
                            </tr>
                        ))}
                    </tbody>
                </CustomStyledTable>
            </InfiniteScroll>
        );
    }

    return (
        <MailOverviewDiv>
            <SearchDiv>
                <SearchBar
                    onChange={e => {
                        setPage(0);
                        setSearchTerm(e.target.value);
                    }}
                    value={searchTerm}
                    placeholder="Search a student"
                />
            </SearchDiv>
            <SearchAndChangeDiv>
                <FilterDiv>
                    <CommonMultiselect
                        placeholder="  Filter on State"
                        showArrow={true}
                        isObject={false}
                        onRemove={e => {
                            setPage(0);
                            setFilters(e);
                            setFiltersChanged(filtersChanged + 1);
                        }}
                        onSelect={e => {
                            setPage(0);
                            setFilters(e);
                            setFiltersChanged(filtersChanged + 1);
                        }}
                        options={Object.values(EmailType)}
                    />
                </FilterDiv>
                {!isReadonlyEdition(editionId, editions) && (
                    <DropDownButtonDiv>
                        <CommonDropdownButton
                            id="dropdown-setstate-button"
                            title="Add new state to selected students"
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
                        </CommonDropdownButton>
                    </DropDownButtonDiv>
                )}
            </SearchAndChangeDiv>
            <ClearDiv />
            {table}
        </MailOverviewDiv>
    );
}
