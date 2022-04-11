import React, { useEffect, useState } from "react";
import { StyledTable, LoadingSpinner } from "./styles";
import { getEditions } from "../../utils/api/editions";
import EditionRow from "./EditionRow";

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

    return (
        <StyledTable>
            <tbody>{rows}</tbody>
        </StyledTable>
    );
}
