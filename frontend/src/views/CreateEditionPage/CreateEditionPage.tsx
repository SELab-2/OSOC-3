import { Form, Spinner } from "react-bootstrap";
import { SyntheticEvent, useState } from "react";
import { createEdition, getSortedEditions } from "../../utils/api/editions";
import { useNavigate } from "react-router-dom";
import { CreateEditionDiv, Error, FormGroup, ButtonDiv, CancelButton } from "./styles";
import { useAuth } from "../../contexts";
import { setCurrentEdition } from "../../utils/session-storage";
import { toast } from "react-toastify";
import { BiArrowBack } from "react-icons/bi";
import { CreateButton } from "../../components/Common/Buttons";

/**
 * Page to create a new edition.
 */
export default function CreateEditionPage() {
    const navigate = useNavigate();
    const { setEditions } = useAuth();

    const currentYear = new Date().getFullYear();

    const [name, setName] = useState("");
    const [year, setYear] = useState<string>(currentYear.toString());
    const [nameError, setNameError] = useState<string | undefined>(undefined);
    const [yearError, setYearError] = useState<string | undefined>(undefined);
    const [error, setError] = useState<string | undefined>(undefined);
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
            setNameError("Edition name already exists.");
            toast.warning("Edition name already exists", { toastId: "createEditionNameExists" });
        } else if (response.status === 422) {
            setNameError("Invalid edition name.");
            toast.warning("Invalid edition name", { toastId: "createEditionBadName" });
        } else {
            setError("Something went wrong.");
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
                setNameError("Edition name can't contain spaces.");
            } else if (name.length < 5) {
                setNameError("Edition name must be longer than 4 characters.");
            } else {
                setNameError("Invalid edition name.");
            }
            correct = false;
        }

        const yearNumber = Number(year);
        if (isNaN(yearNumber)) {
            correct = false;
            setYearError("Invalid year.");
        } else {
            if (yearNumber < currentYear) {
                correct = false;
                setYearError("New editions can't be in the past.");
            } else if (yearNumber > 3000) {
                correct = false;
                setYearError("Invalid year.");
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
                    <Form.Control
                        type="text"
                        value={name}
                        required
                        placeholder="Edition name"
                        isInvalid={nameError !== undefined}
                        onChange={e => {
                            setName(e.target.value);
                            setNameError(undefined);
                            setError(undefined);
                        }}
                    />
                    <Form.Control.Feedback type="invalid">{nameError}</Form.Control.Feedback>
                </FormGroup>

                <FormGroup>
                    <Form.Label>Edition year</Form.Label>
                    <Form.Control
                        type="number"
                        value={year}
                        required
                        placeholder="Edition year"
                        isInvalid={yearError !== undefined}
                        onChange={e => {
                            setYear(e.target.value);
                            setYearError(undefined);
                            setError(undefined);
                        }}
                    />
                    <Form.Control.Feedback type="invalid">{yearError}</Form.Control.Feedback>
                </FormGroup>
                <ButtonDiv>
                    <CancelButton onClick={() => navigate("/editions")}>
                        <BiArrowBack />
                        Cancel
                    </CancelButton>
                    {submitButton}
                </ButtonDiv>
                <Error>{error}</Error>
            </Form>
        </CreateEditionDiv>
    );
}
