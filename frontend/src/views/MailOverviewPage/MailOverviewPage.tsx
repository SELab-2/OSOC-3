import React, { useEffect, useState } from "react";
import {
    getMailOverview,
    StudentEmails,
    handleSelect,
    handleSelectAll,
    handleSetState,
    handleFilterSelect,
    handleSetSearch,
    handleDoSearch,
} from "../../utils/api/mail_overview";
import BootstrapTable from "react-bootstrap-table-next";
import DropdownButton from "react-bootstrap/DropdownButton";
import Dropdown from "react-bootstrap/Dropdown";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";
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
