import { Form, Spinner } from "react-bootstrap";
import { SyntheticEvent, useState } from "react";
import { createEdition, getSortedEditions } from "../../utils/api/editions";
import { useNavigate } from "react-router-dom";
import { CreateEditionDiv, FormGroup, ButtonDiv, CancelButton } from "./styles";
import { useAuth } from "../../contexts";
import { setCurrentEdition } from "../../utils/session-storage";
import { toast } from "react-toastify";
import { BiArrowBack } from "react-icons/bi";
import { CreateButton } from "../../components/Common/Buttons";
import { FormControl } from "../../components/Common/Forms";

/**
 * Page to create a new edition.
 */
export default function CreateEditionPage() {
    const navigate = useNavigate();
    const { setEditions } = useAuth();

    const currentYear = new Date().getFullYear();

    const [name, setName] = useState("");
    const [year, setYear] = useState<string>(currentYear.toString());
    const [nameError, setNameError] = useState<boolean>(false);
    const [yearError, setYearError] = useState<boolean>(false);
    const [loading, setLoading] = useState(false);

    async function sendEdition(name: string, year: number): Promise<boolean> {
        const response = await toast.promise(
            createEdition(name, year),
            {
                pending: "Creating new edition",
                error: "Connection issue",
            },
            { toastId: "createEdition" }
        );
        if (response.status === 201) {
            const allEditions = await getSortedEditions();
            setEditions(allEditions);
            setCurrentEdition(response.data.name);
            toast.success("Successfully made new edition", { toastId: "createEditionSuccess" });
            return true;
        } else if (response.status === 409) {
            setNameError(true);
            toast.error("Edition name already exists", { toastId: "createEditionNameExists" });
        } else if (response.status === 422) {
            setNameError(true);
            toast.error("Invalid edition name", { toastId: "createEditionBadName" });
        } else {
            toast.error("Something went wrong", { toastId: "createEditionError" });
        }
        return false;
    }

    async function handleSubmit(event: SyntheticEvent<HTMLFormElement>) {
        event.stopPropagation();
        event.preventDefault();
        let correct = true;

        // Edition name can't contain spaces and must be at least 5 long.
        if (!/^([^ ]{5,})$/.test(name)) {
            if (name.includes(" ")) {
                setNameError(true);
                toast.error("Edition name can't contain spaces.", {
                    toastId: "createEditionNoSpaces",
                });
            } else if (name.length < 5) {
                setNameError(true);
                toast.error("Edition name must be longer than 4 characters.", {
                    toastId: "createEditionBadName",
                });
            } else {
                setNameError(true);
                toast.error("Invalid edition name", { toastId: "createEditionBadName" });
            }
            correct = false;
        }

        const yearNumber = Number(year);
        if (isNaN(yearNumber)) {
            correct = false;
            setYearError(true);
            toast.error("Invalid year.", { toastId: "createEditionYearNoNumber" });
        } else {
            if (yearNumber < currentYear) {
                correct = false;
                setYearError(true);
                toast.error("New editions can't be in the past.", {
                    toastId: "createEditionPastYear",
                });
            } else if (yearNumber > 3000) {
                correct = false;
                setYearError(true);
                toast.error("Invalid year.", { toastId: "createEditionYearName" });
            }
        }

        let success = false;
        if (correct) {
            setLoading(true);
            try {
                success = await sendEdition(name, yearNumber);
                setLoading(false);
            } catch (error) {
                setLoading(false);
            }
        }

        if (success) {
            // navigate must be at the end of the function
            navigate("/editions/");
        }
    }

    let submitButton;
    if (loading) {
        submitButton = <Spinner animation="border" />;
    } else {
        submitButton = <CreateButton label="Submit" type="submit" />;
    }

    return (
        <CreateEditionDiv>
            <Form noValidate onSubmit={handleSubmit}>
                <FormGroup>
                    <Form.Label>Edition name</Form.Label>
                    <FormControl
                        type="text"
                        value={name}
                        placeholder="Edition name"
                        isInvalid={nameError}
                        onChange={e => {
                            setName(e.target.value);
                            setNameError(false);
                        }}
                    />
                </FormGroup>

                <FormGroup>
                    <Form.Label>Edition year</Form.Label>
                    <FormControl
                        type="number"
                        value={year}
                        placeholder="Edition year"
                        isInvalid={yearError}
                        onChange={e => {
                            setYear(e.target.value);
                            setYearError(false);
                        }}
                    />
                </FormGroup>
                <ButtonDiv>
                    <CancelButton onClick={() => navigate("/editions")}>
                        <BiArrowBack />
                        Cancel
                    </CancelButton>
                    {submitButton}
                </ButtonDiv>
            </Form>
        </CreateEditionDiv>
    );
}
