from azureloggerbundle.app_insights.AzureLogWithExtraHandler import AzureLogWithExtraHandler
from loggerbundle.handler.HandlerFactoryInterface import HandlerFactoryInterface


class AppInsightsLogHandlerFactory(HandlerFactoryInterface):
    def __init__(
        self,
        instrumentation_key: str,
    ):
        self.__instrumentation_key = instrumentation_key

    def create(self):
        return AzureLogWithExtraHandler(connection_string="InstrumentationKey={}".format(self.__instrumentation_key))
