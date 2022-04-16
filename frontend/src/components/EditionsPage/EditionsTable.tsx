import React, { useEffect, useState } from "react";
import { StyledTable, LoadingSpinner } from "./styles";
import { getEditions } from "../../utils/api/editions";
import EditionRow from "./EditionRow";

/**
 * Table on the [[EditionsPage]] that renders a list of all editions
 * that the user has access to.
 *
 * If the user is an admin, this will also render a delete button.
 */
export default function EditionsTable() {
    const [loading, setLoading] = useState(true);
    const [rows, setRows] = useState<React.ReactNode[]>([]);

    async function loadEditions() {
        const response = await getEditions();

        const newRows: React.ReactNode[] = response.editions.map(edition => (
            <EditionRow edition={edition} key={edition.name} />
        ));

        setRows(newRows);
        setLoading(false);
    }

    useEffect(() => {
        loadEditions();
    }, []);

    // Still loading: display a spinner instead
    if (loading) {
        return <LoadingSpinner />;
    }

    if (rows.length === 0) {
        return (
            <div className={"mx-auto text-center"}>
                It looks like you're not a part of any editions so far.
                <br />
                Contact an admin to receive an invite.
            </div>
        );
    }

    return (
        <StyledTable>
            <tbody>{rows}</tbody>
        </StyledTable>
    );
}