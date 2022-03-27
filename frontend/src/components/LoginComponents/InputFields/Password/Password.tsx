export default function Password({password, setPassword }: any) {
    return (
        <div>
            <input
                type="password"
                name="password"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
        </div>
    );
}
