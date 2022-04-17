import React, { useEffect, useState } from "react";
import {
    getMailOverview,
    StudentEmails,
    handleSelect,
    handleSelectAll,
    handleSetState,
} from "../../utils/api/mail_overview";
import BootstrapTable from "react-bootstrap-table-next";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import { TableDiv, DropDownButtonDiv, SearchDiv, FilterDiv, SearchAndFilterDiv } from "./styles";
import { EmailType } from "../../data/enums";

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
            dataField: "emails[0].type",
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
                    <Dropdown.Item eventKey="0">Applied</Dropdown.Item>
                    <Dropdown.Item eventKey="1">Awaiting project</Dropdown.Item>
                    <Dropdown.Item eventKey="2">Approved</Dropdown.Item>
                    <Dropdown.Item eventKey="3">Contract confirmed</Dropdown.Item>
                    <Dropdown.Item eventKey="4">Contract declined</Dropdown.Item>
                    <Dropdown.Item eventKey="5">Rejected</Dropdown.Item>
                </DropdownButton>
            </DropDownButtonDiv>
            <SearchAndFilterDiv>
                <SearchDiv>
                    <InputGroup className="mb-3">
                        <FormControl placeholder="Search a student" aria-label="Username" />
                    </InputGroup>
                </SearchDiv>
                <FilterDiv>
                    <DropdownButton
                        id="dropdown-filterstate-button"
                        title="Filter on Email State"
                        menuVariant="dark"
                        autoClose="outside"
                    >
                        <Dropdown.Item eventKey="0">Applied</Dropdown.Item>
                        <Dropdown.Item eventKey="1">Awaiting project</Dropdown.Item>
                        <Dropdown.Item eventKey="2">Approved</Dropdown.Item>
                        <Dropdown.Item eventKey="3">Contract confirmed</Dropdown.Item>
                        <Dropdown.Item eventKey="4">Contract declined</Dropdown.Item>
                        <Dropdown.Item eventKey="5">Rejected</Dropdown.Item>
                    </DropdownButton>
                </FilterDiv>
            </SearchAndFilterDiv>
            <TableDiv>
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
            </TableDiv>
        </>
    );
}
