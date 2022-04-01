import { Input } from "../styles";

export default function ConfirmPassword({
    confirmPassword,
    setConfirmPassword,
    callRegister,
}: {
    confirmPassword: string;
    setConfirmPassword: (value: string) => void;
    callRegister: () => void;
}) {
    return (
        <div>
            <Input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                onKeyPress={e => {
                    if (e.key === "Enter") {
                        callRegister();
                    }
                }}
            />
        </div>
    );
}
