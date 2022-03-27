export default function Email({ email, setEmail }: any) {
    return (
        <div>
            <input
                type="email"
                name="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
            />
        </div>
    );
}
