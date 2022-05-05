import React, { useState } from "react";
import { getMailOverview, setStateRequest, StudentEmail } from "../../utils/api/mail_overview";
import BootstrapTable from "react-bootstrap-table-next";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import InfiniteScroll from "react-infinite-scroller";
import { Multiselect } from "multiselect-react-dropdown";
import { TableDiv, DropDownButtonDiv, SearchDiv, FilterDiv, SearchAndFilterDiv } from "./styles";
import { EmailType } from "../../data/enums";
import { SpinnerContainer, Error } from "../../components/UsersComponents/Requests/styles";
import { useParams } from "react-router-dom";
import { Spinner } from "react-bootstrap";

/**
 * Page that shows the email status of all students, with the possibility to change the status
 */
export default function MailOverviewPage() {
    const [emails, setEmails] = useState<StudentEmail[]>([]);
    const [gotEmails, setGotEmails] = useState(false);
    const [loading, setLoading] = useState(false);
    const [moreEmailsAvailable, setMoreEmailsAvailable] = useState(true); // Endpoint has more emails available
    const [error, setError] = useState<string | undefined>(undefined);
    const [page, setPage] = useState(0);

    // Keep track of the set filters
    const [searhTerm, setSearchTerm] = useState("");
    const [filters, setFilters] = useState<EmailType[]>([]);

    const [selectedRows, setSelectedRows] = useState<number[]>([]);

    const { editionId } = useParams();

    /**
     * update the table with new values
     * @param page
     */
    async function updateMailOverview() {
        if (loading) {
            return;
        }

        setLoading(true);

        try {
            const response = await getMailOverview(editionId, page, searhTerm, filters);

            if (response.studentEmails.length === 0) {
                setMoreEmailsAvailable(false);
            }
            if (page === 0) {
                setEmails(response.studentEmails);
            } else {
                setEmails(emails.concat(response.studentEmails));
            }

            setPage(page + 1);
            setGotEmails(true);
        } catch (exception) {
            setError("Oops, something went wrong...");
        }
        setLoading(false);
    }

    function searchName(newSearchTerm: string) {
        setPage(0);
        setGotEmails(false);
        setMoreEmailsAvailable(true);
        setSearchTerm(newSearchTerm);
        setEmails([]);
    }

    function changeFilter(newFilter: EmailType[]) {
        setPage(0);
        setGotEmails(false);
        setMoreEmailsAvailable(true);
        setFilters(newFilter);
        setEmails([]);
    }

    /**
     * Keeps the selectedRows list up-to-date when a student is selected/unselected in the table
     * @param row
     * @param isSelect
     */
    function selectNewRow(row: StudentEmail, isSelect: boolean) {
        if (isSelect) {
            setSelectedRows(selectedRows.concat(row.student.studentId));
        } else {
            setSelectedRows(selectedRows.filter(item => item !== row.student.studentId));
        }
    }

    function selectAll(isSelect: boolean, rows: StudentEmail[]) {
        for (const row of rows) {
            selectNewRow(row, isSelect);
        }
    }

    const columns = [
        {
            dataField: "student.firstName",
            text: "First Name",
        },
        {
            dataField: "student.lastName",
            text: "Last Name",
        },
        {
            dataField: "emails[0].decision",
            text: "Current Email State",
            formatter: (cellContent: number) => {
                return Object.values(EmailType)[cellContent];
            },
        },
        {
            dataField: "emails[0].date",
            text: "Date Of Last Email",
            formatter: (cellContent: number) => {
                return new Date(String(cellContent)).toLocaleString("nl-be");
            },
        },
    ];

    let table;
    if (error) {
        table = <Error>{error}</Error>;
    } else if (gotEmails && emails.length === 0) {
        table = <div>No emails found.</div>;
    } else {
        table = (
            <TableDiv>
                <InfiniteScroll
                    loadMore={updateMailOverview}
                    hasMore={moreEmailsAvailable}
                    loader={
                        <SpinnerContainer key={"spinner"}>
                            <Spinner animation="border" />
                        </SpinnerContainer>
                    }
                    initialLoad={true}
                    useWindow={false}
                    getScrollParent={() => document.getElementById("root")}
                >
                    <BootstrapTable
                        keyField="student.studentId"
                        data={emails}
                        columns={columns}
                        striped
                        hover
                        bordered
                        selectRow={{
                            mode: "checkbox",
                            onSelect: selectNewRow,
                            onSelectAll: selectAll,
                        }}
                    />
                </InfiniteScroll>
            </TableDiv>
        );
    }

    // TODO: Change state

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
                            onClick={() =>
                                setStateRequest(index.toString(), editionId, selectedRows)
                            }
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
                        placeholder="Filter on Email State"
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
