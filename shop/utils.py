from ippanel import Client
import os
from uuid import uuid4
def create_random_code(count):
    import random
    return random.randint(10 ** (count - 1), 10 ** count - 1)

def send_sms(mobile_number, message):
    # you api key that generated from panel
    api_key = "wLunDPzEF4xP5u8ORdjy0oE0nzEbn9bQ3hGMjXdfBTs="
    # create client instance
    sms = Client(api_key)
    sms.send(
        "+9810004223",  # originator
        [mobile_number, ],  # recipients
        message,  # message
        "summery"  # is logged
    )

class FileUpload:
    def __init__(self,dir , prefix):
        self.dir = dir
        self.prefix = prefix

    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"