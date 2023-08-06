from opencensus.ext.azure.log_exporter import AzureLogHandler, Envelope, Message
from loggerbundle.extra.ExtraKeysResolver import ExtraKeysResolver


class AzureLogWithExtraHandler(AzureLogHandler):
    def log_record_to_envelope(self, record):
        envelope = super().log_record_to_envelope(record)  # type: Envelope

        message = envelope.data.base_data  # type: Message

        record_dict = record.__dict__
        extra_keys = ExtraKeysResolver.get_extra_keys(record)

        message.properties["loggerName"] = record.name

        for k in extra_keys:
            if k != "message":
                message.properties["extra_{}".format(k)] = str(record_dict[k])

        return envelope
