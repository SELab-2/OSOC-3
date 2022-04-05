import { Input } from "../styles";

/**
 * Input field for passwords (confirmation), submits when pressing the Enter key.
 * @param confirmPassword getter for the state of the password
 * @param setConfirmPassword setter for the state of the password
 * @param callRegister callback that tries to register the user
 */
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
