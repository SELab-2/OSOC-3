import React, { useEffect, useState } from "react";
import { LoadingSpinner, StyledTable } from "./styles";
import { getEditions, patchEdition } from "../../utils/api/editions";
import EditionRow from "./EditionRow";
import EmptyEditionsTableMessage from "./EmptyEditionsTableMessage";
import { Edition } from "../../data/interfaces";
import { toast } from "react-toastify";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";

/**
 * Table on the [[EditionsPage]] that renders a list of all editions
 * that the user has access to.
 *
 * If the user is an admin, this will also render a delete button.
 */
export default function EditionsTable() {
    const { role } = useAuth();
    const [loading, setLoading] = useState(true);
    const [rows, setRows] = useState<React.ReactNode[]>([]);

    async function handleClick(edition: Edition) {
        if (role !== Role.ADMIN) return;

        await toast.promise(async () => await patchEdition(edition.name, !edition.readonly), {
            pending: "Changing edition status",
            error: "Error changing status",
            success: `Successfully changed status to ${
                edition.readonly ? '"editable"' : '"read-only"'
            }.`,
        });

        await loadEditions();
    }

    async function loadEditions() {
        const response = await getEditions();

        const newRows: React.ReactNode[] = response.editions.map(edition => (
            <EditionRow edition={edition} key={edition.name} handleClick={handleClick} />
        ));

        setRows(newRows);
        setLoading(false);
    }

    useEffect(() => {
        loadEditions();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Still loading: display a spinner instead
    if (loading) {
        return <LoadingSpinner />;
    }

    if (rows.length === 0) {
        return <EmptyEditionsTableMessage />;
    }

    return (
        <StyledTable>
            <tbody>{rows}</tbody>
        </StyledTable>
    );
}
