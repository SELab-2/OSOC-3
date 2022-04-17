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
                min="0"
                value={numberOfStudents}
                onChange={e => {
                    setNumberOfStudents(e.target.valueAsNumber);
                }}
                placeholder="Number of students"
            />
        </div>
    );
}
