import { Input } from "../../styles";

export default function NumberOfStudents({
    numberOfStudents,
    setNumberOfStudents,
}: {
    numberOfStudents: number;
    setNumberOfStudents: (numberOfStudents: number) => void;
}) {
    return (
        <div>
            <Input
                type="number"
                min="1"
                value={numberOfStudents.toString()}
                onChange={e => {
                    if (e.target.valueAsNumber > 0 || isNaN(e.target.valueAsNumber))
                        setNumberOfStudents(e.target.valueAsNumber);
                }}
                placeholder="Number of students"
            />
        </div>
    );
}
