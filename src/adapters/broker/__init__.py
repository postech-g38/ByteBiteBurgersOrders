from src.adapters.broker.settings import AwsSQS
from src.settings import get_settings


def aws_sqs_facade() -> AwsSQS:
    return AwsSQS(url=get_settings().queue_settings.queue_url)
