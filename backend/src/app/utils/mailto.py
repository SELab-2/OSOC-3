from urllib.parse import quote


def generate_mailto_string(recipient: str, subject: str, body: str, cc: str = "", bcc: str = "") -> str:
    """Create a mailto string for the given arguments"""
    res = f"mailto:{recipient}?subject={quote(subject)}&body={quote(body)}"

    # Append optional fields
    if cc:
        res += f"&cc={cc}"
    if bcc:
        res += f"&bcc={bcc}"

    return res
