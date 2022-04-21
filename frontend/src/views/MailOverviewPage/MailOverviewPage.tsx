import React, { useEffect, useState } from "react";
import {
    getMailOverview,
    StudentEmails,
    handleSelect,
    handleSelectAll,
    handleSetState,
    handleFilterSelect,
    handleSetSearch,
    setFinalFilters,
} from "../../utils/api/mail_overview";
import BootstrapTable from "react-bootstrap-table-next";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";
import InfiniteScroll from "react-infinite-scroller";
import { Multiselect } from "multiselect-react-dropdown";
import {
    TableDiv,
    DropDownButtonDiv,
    SearchDiv,
    FilterDiv,
    SearchAndFilterDiv,
    ButtonDiv,
} from "./styles";
import { EmailType } from "../../data/enums";
import { useParams } from "react-router-dom";

/**
 * Page that shows the email status of all students, with the possibility to change the status
 */
export default function MailOverviewPage() {
    const init: StudentEmails = {
        studentEmails: [],
    };
    const [table, setTable] = useState(init);
    const [gotData, setGotData] = useState(false); // Received data
    const [moreEmailsAvailable, setMoreEmailsAvailable] = useState(true); // Endpoint has more emails available
    const { editionId } = useParams();

    async function updateMailOverview(page: number) {
        try {
            const studentEmails = await getMailOverview(editionId, page);
            if (studentEmails.studentEmails.length === 0) {
                setMoreEmailsAvailable(false);
            }
            if (page === 0) {
                setTable(studentEmails);
            } else {
                setTable({
                    studentEmails: table.studentEmails.concat(studentEmails.studentEmails),
                });
            }
            setGotData(true);
        } catch (exception) {
            console.log(exception);
        }
    }

    useEffect(() => {
        if (!gotData) {
            updateMailOverview(0);
        }
    });

    function handleDoSearch() {
        setFinalFilters();
        setGotData(false);
        setMoreEmailsAvailable(true);
        updateMailOverview(0);
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

    return (
        <>
            <DropDownButtonDiv>
                <DropdownButton
                    id="dropdown-setstate-button"
                    title="Set state of selected students"
                    menuVariant="dark"
                    onSelect={handleSetState}
                >
                    {Object.values(EmailType).map((type, index) => (
                        <Dropdown.Item eventKey={index.toString()} key={type}>
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
                            onChange={handleSetSearch}
                            onSubmit={handleDoSearch}
                        />
                    </InputGroup>
                </SearchDiv>
                <FilterDiv>
                    <Multiselect
                        placeholder="Filter on Email State"
                        showArrow={true}
                        isObject={false}
                        onRemove={handleFilterSelect}
                        onSelect={handleFilterSelect}
                        options={[
                            "Applied",
                            "Awaiting project",
                            "Approved",
                            "Contract confirmed",
                            "Contract declined",
                            "Rejected",
                        ]}
                    />
                </FilterDiv>
                <ButtonDiv>
                    <Button onClick={handleDoSearch}>Search</Button>
                </ButtonDiv>
            </SearchAndFilterDiv>
            <TableDiv>
                <InfiniteScroll
                    pageStart={0}
                    loadMore={updateMailOverview}
                    initialLoad={true}
                    hasMore={moreEmailsAvailable}
                >
                    <BootstrapTable
                        keyField="student.studentId"
                        data={table.studentEmails}
                        columns={columns}
                        striped
                        hover
                        bordered
                        selectRow={{
                            mode: "checkbox",
                            onSelect: handleSelect,
                            onSelectAll: handleSelectAll,
                        }}
                    />
                </InfiniteScroll>
            </TableDiv>
        </>
    );
}
