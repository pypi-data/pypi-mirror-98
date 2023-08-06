from typing import List
from box import Box
from injecta.dtype.DType import DType
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias
from injecta.service.argument.PrimitiveArgument import PrimitiveArgument
from pyfonybundles.Bundle import Bundle


class AzureLoggerBundle(Bundle):
    def modify_services(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        if parameters.azureloggerbundle.enabled:
            service = Service(
                "azureloggerbundle.app_insights.AppInsightsLogHandlerFactory",
                DType("azureloggerbundle.app_insights.AppInsightsLogHandlerFactory", "AppInsightsLogHandlerFactory"),
                [PrimitiveArgument("%azureloggerbundle.app_insights.instrumentation_key%")],
                ["loghandler.factory"],
            )

            services.append(service)

        return services, aliases
