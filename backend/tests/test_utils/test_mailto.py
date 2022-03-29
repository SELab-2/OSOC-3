from src.app.utils.mailto import generate_mailto_string


def test_mailto():
    """Test generating mailto links"""
    # Basic
    assert generate_mailto_string(recipient="me",
                                  subject="subject",
                                  body="body") == "mailto:me?subject=subject&body=body"

    # Add spaces and newlines
    assert generate_mailto_string(recipient="me",
                                  subject="Subject with spaces",
                                  body="Body with spaces \nand newlines"
                                  ) == "mailto:me?subject=Subject%20with%20spaces&body=Body%20with%20spaces%20%0Aand" \
                                       "%20newlines"

    # Add optional fields
    assert generate_mailto_string(recipient="a", subject="b",
                                  body="c", cc="cchere",
                                  bcc="bcchere") == "mailto:a?subject=b&body=c&cc=cchere&bcc=bcchere"
