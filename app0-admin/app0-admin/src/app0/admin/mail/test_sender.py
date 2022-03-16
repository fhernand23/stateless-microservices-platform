"""
test_sender modules
"""
from typing import List, Union
from io import BytesIO

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3  # type: ignore

REGION_NAME = "us-east-2"
CHARSET = "UTF-8"
FROM_MAIL = "devmaster@claimsattendant.com"


def send_test_plain_email():
    """
    Send plain mail example
    """
    ses_client = boto3.client("ses", region_name=REGION_NAME)

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "devmaster@claimsattendant.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": "Hello! This is a plain mail from Claims Platform.",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Plain mail from Claims Attendant",
            },
        },
        Source=FROM_MAIL,
    )
    print(response)


def send_test_html_email():
    """
    Send html example
    """
    ses_client = boto3.client("ses", region_name=REGION_NAME)
    html_email_content = """
        <html>
            <head></head>
            <h1 style='text-align:center'>Hello! This is the heading</h1>
            <p>This is an html mail from Claims Platform.</p>
            </body>
        </html>
    """

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "devmaster@claimsattendant.com",
            ],
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": html_email_content,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Html mail from Claims Attendant",
            },
        },
        Source=FROM_MAIL,
    )
    print(response)


async def send_test_multipart_email(to: List[str], subject: str, content: str,
                                    attachments: dict[str, Union[BytesIO, bytes]]):
    """
    Send multipart mail example
    """
    for t in to:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = FROM_MAIL
        msg["To"] = t

        body = MIMEText(content, "html")
        msg.attach(body)

        for filenamename, attach in attachments.items():
            part = MIMEApplication(attach.getvalue() if isinstance(attach, BytesIO) else attach)
            part.add_header("Content-Disposition", "attachment", filename=filenamename)
            msg.attach(part)

        # Convert message to string and send
        ses_client = boto3.client("ses", region_name=REGION_NAME)
        response = ses_client.send_raw_email(
            Source=FROM_MAIL,
            Destinations=[t],
            RawMessage={"Data": msg.as_string()}
        )
        print(response)
