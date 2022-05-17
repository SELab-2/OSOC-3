import { ConflictButtonDiv, SidePanel } from "./styles";
import { useEffect, useState } from "react";
import { Offcanvas } from "react-bootstrap";
import { getConflicts } from "../../../utils/api/conflicts";
import { Conflict } from "../../../data/interfaces";
import ConflictDiv from "./Conflict";
import LoadSpinner from "../../Common/LoadSpinner";
import CreateButton from "../../Common/Buttons/CreateButton";
import WarningButton from "../../Common/Buttons/WarningButton";

/**
 * A button which opens a side-panel to show all students who are assigned to multiple projects.
 */
export default function ConflictsButton(props: { editionId: string }) {
    const [conflicts, setConflicts] = useState<Conflict[] | undefined>(undefined);
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    useEffect(() => {
        const fetchConflicts = async () => {
            const conflicts = await getConflicts(props.editionId);
            setConflicts(conflicts.conflictStudents);
        };

        fetchConflicts().catch(console.error);
    }, [props.editionId]);

    if (conflicts === undefined) {
        return <LoadSpinner show={true} />;
    }
    if (show) {
        return (
            <SidePanel variant="dark" show={show} onHide={handleClose} placement="end">
                <Offcanvas.Header closeButton closeVariant="white">
                    <Offcanvas.Title>
                        <h2>Resolve Conflicts</h2>
                    </Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    <b>The student may be a better fit for a specific team, if they:</b>
                    <ul>
                        <li>are an alumni and the team doesn't have any yet</li>
                        <li>are an alumni on a team with a half-time coach</li>
                        <li>are an alumni and provide skills the coach does not have</li>
                        <li>have pre-existing history with the project in question</li>
                        <li>enrich the team's diversity</li>
                        <li>
                            have a skillset that is tough to find in other applicants,
                            <br />
                            and matches exceptionally well with the project
                        </li>
                    </ul>
                    <h3>Conflicts</h3>
                    <ul>
                        {conflicts.map(conflict => (
                            <ConflictDiv
                                key={conflict.studentId}
                                conflict={conflict}
                                editionId={props.editionId}
                            />
                        ))}
                    </ul>
                </Offcanvas.Body>
            </SidePanel>
        );
    }

    if (conflicts.length === 0) {
        return (
            <ConflictButtonDiv>
                <CreateButton disabled={true} showIcon={false}>
                    No conflicts
                </CreateButton>
            </ConflictButtonDiv>
        );
    }
    return (
        <ConflictButtonDiv>
            <WarningButton
                onClick={handleShow}
                animated={true}
            >{`Conflicts (${conflicts.length})`}</WarningButton>
        </ConflictButtonDiv>
    );
}