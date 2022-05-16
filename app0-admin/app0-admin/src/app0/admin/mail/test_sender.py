"""
test_sender modules
"""
from typing import List, Union
from io import BytesIO


def send_test_plain_email():
    """
    Send plain mail example
    """
    print("TODO Send plain mail example")


def send_test_html_email():
    """
    Send html example
    """
    print("TODO Send html example")


async def send_test_multipart_email(to: List[str], subject: str, content: str,
                                    attachments: dict[str, Union[BytesIO, bytes]]):
    """
    Send multipart mail example
    """
    print("TODO Send multipart mail example")
