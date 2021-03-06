import { getUsersExcludeEdition, User } from "../../../../utils/api/users/users";
import { useState, createRef, useEffect } from "react";
import { addCoachToEdition } from "../../../../utils/api/users/coaches";
import { Button, Modal, Spinner } from "react-bootstrap";
import { AddButtonDiv } from "../../../AdminsComponents/styles";
import Typeahead from "react-bootstrap-typeahead/types/core/Typeahead";
import UserMenuItem from "../../../Common/Users/MenuItem";
import { StyledMenuItem } from "../../../Common/Users/styles";
import { EmailAndAuth } from "../../../Common/Users";
import { EmailDiv } from "../styles";
import CreateButton from "../../../Common/Buttons/CreateButton";
import { ModalContentConfirm } from "../../../Common/styles";
import { StyledInput } from "../../../Common/Forms/styles";
import { AsyncTypeahead, Menu } from "react-bootstrap-typeahead";
import { toast } from "react-toastify";

/**
 * A button and popup to add a new coach to the given edition.
 * The popup consists of a field to search for a user.
 * @param props.edition The edition to which users need to be added.
 * @param props.coachAdded A function which will be called when a user is added as coach.
 */
export default function AddCoach(props: { edition: string; refreshCoaches: () => void }) {
    const [show, setShow] = useState(false);
    const [selected, setSelected] = useState<User | undefined>(undefined);
    const [loading, setLoading] = useState(false);
    const [gettingData, setGettingData] = useState(false); // Waiting for data
    const [users, setUsers] = useState<User[]>([]); // All users which are not a coach
    const [searchTerm, setSearchTerm] = useState(""); // The word set in filter
    const [clearRef, setClearRef] = useState(false); // The ref must be cleared

    const typeaheadRef = createRef<Typeahead>();

    useEffect(() => {
        // For some obscure reason the ref can only be cleared in here & not somewhere else
        if (clearRef) {
            // This triggers itself, but only once, so it doesn't really matter
            setClearRef(false);
            typeaheadRef.current?.clear();
        }
    }, [clearRef, typeaheadRef]);

    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingData(true);
        const response = await toast.promise(getUsersExcludeEdition(props.edition, filter, page), {
            error: "Failed to retrieve users",
        });
        if (page === 0) {
            setUsers(response.users);
        } else {
            setUsers(users.concat(response.users));
        }

        setGettingData(false);
    }

    function filterData(searchTerm: string) {
        setSearchTerm(searchTerm);
        setUsers([]);
        getData(0, searchTerm);
    }

    const handleClose = () => {
        setSelected(undefined);
        props.refreshCoaches();
        setShow(false);
    };
    const handleShow = () => {
        setShow(true);
    };

    async function addCoach(user: User) {
        setLoading(true);
        await toast.promise(addCoachToEdition(user.userId, props.edition), {
            error: "Failed to add coach",
            pending: "Adding coach",
            success: "Coach successfully added",
        });

        setLoading(false);
        setSelected(undefined);
        setClearRef(true);
    }

    let addButton;
    if (loading) {
        addButton = <Spinner animation="border" />;
    } else {
        addButton = (
            <CreateButton
                showIcon={false}
                onClick={() => {
                    if (selected !== undefined) {
                        addCoach(selected);
                    }
                }}
                disabled={selected === undefined}
            >
                Add coach
            </CreateButton>
        );
    }

    return (
        <>
            <AddButtonDiv>
                <CreateButton showIcon={false} onClick={handleShow}>
                    Add coach to current edition
                </CreateButton>
            </AddButtonDiv>

            <Modal show={show} onHide={handleClose}>
                <ModalContentConfirm>
                    <Modal.Header closeButton>
                        <Modal.Title>Add Coach</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <AsyncTypeahead
                            filterBy={["name"]}
                            id="non-coach-users"
                            isLoading={gettingData}
                            labelKey="name"
                            minLength={1}
                            onSearch={filterData}
                            options={users}
                            ref={typeaheadRef}
                            placeholder={"Username"}
                            onChange={selected => {
                                setSelected(selected[0] as User);
                            }}
                            renderInput={({ inputRef, referenceElementRef, ...inputProps }) => (
                                <StyledInput
                                    {...inputProps}
                                    ref={input => {
                                        inputRef(input);
                                        referenceElementRef(input);
                                    }}
                                />
                            )}
                            renderMenu={(results, menuProps) => {
                                const {
                                    newSelectionPrefix,
                                    paginationText,
                                    renderMenuItemChildren,
                                    ...props
                                } = menuProps;
                                return (
                                    <Menu {...props}>
                                        {results.map((result, index) => {
                                            const user = result as User;
                                            return (
                                                <StyledMenuItem
                                                    option={result}
                                                    position={index}
                                                    key={user.userId}
                                                >
                                                    <UserMenuItem user={user} />
                                                    <br />
                                                </StyledMenuItem>
                                            );
                                        })}
                                    </Menu>
                                );
                            }}
                        />
                        <EmailDiv>
                            <EmailAndAuth user={selected} />
                        </EmailDiv>
                    </Modal.Body>
                    <Modal.Footer>
                        {addButton}
                        <Button variant="secondary" onClick={handleClose}>
                            Cancel
                        </Button>
                    </Modal.Footer>
                </ModalContentConfirm>
            </Modal>
        </>
    );
}
