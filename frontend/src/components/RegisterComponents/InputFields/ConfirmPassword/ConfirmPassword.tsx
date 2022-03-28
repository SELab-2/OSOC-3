import { Input } from "../styles";

export default function ConfirmPassword({
    confirmPassword,
    setConfirmPassword,
}: {
    confirmPassword: string;
    setConfirmPassword: (value: string) => void;
}) {
    return (
        <div>
            <Input
                type="password"
                name="password"
                placeholder="Password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
            />
        </div>
    );
}
