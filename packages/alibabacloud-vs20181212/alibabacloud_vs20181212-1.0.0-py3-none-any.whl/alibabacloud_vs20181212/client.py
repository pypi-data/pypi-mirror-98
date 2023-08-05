# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_vs20181212 import models as vs_20181212_models
from alibabacloud_tea_util import models as util_models


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('vs', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def add_vs_pull_stream_info_config_with_options(
        self,
        request: vs_20181212_models.AddVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.AddVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.AddVsPullStreamInfoConfigResponse().from_map(
            self.do_rpcrequest('AddVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def add_vs_pull_stream_info_config_with_options_async(
        self,
        request: vs_20181212_models.AddVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.AddVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.AddVsPullStreamInfoConfigResponse().from_map(
            await self.do_rpcrequest_async('AddVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def add_vs_pull_stream_info_config(
        self,
        request: vs_20181212_models.AddVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.AddVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.add_vs_pull_stream_info_config_with_options(request, runtime)

    async def add_vs_pull_stream_info_config_async(
        self,
        request: vs_20181212_models.AddVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.AddVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.add_vs_pull_stream_info_config_with_options_async(request, runtime)

    def batch_bind_directories_with_options(
        self,
        request: vs_20181212_models.BatchBindDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindDirectoriesResponse().from_map(
            self.do_rpcrequest('BatchBindDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_bind_directories_with_options_async(
        self,
        request: vs_20181212_models.BatchBindDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindDirectoriesResponse().from_map(
            await self.do_rpcrequest_async('BatchBindDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_bind_directories(
        self,
        request: vs_20181212_models.BatchBindDirectoriesRequest,
    ) -> vs_20181212_models.BatchBindDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_bind_directories_with_options(request, runtime)

    async def batch_bind_directories_async(
        self,
        request: vs_20181212_models.BatchBindDirectoriesRequest,
    ) -> vs_20181212_models.BatchBindDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_bind_directories_with_options_async(request, runtime)

    def batch_bind_parent_platform_devices_with_options(
        self,
        request: vs_20181212_models.BatchBindParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindParentPlatformDevicesResponse().from_map(
            self.do_rpcrequest('BatchBindParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_bind_parent_platform_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchBindParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindParentPlatformDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchBindParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_bind_parent_platform_devices(
        self,
        request: vs_20181212_models.BatchBindParentPlatformDevicesRequest,
    ) -> vs_20181212_models.BatchBindParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_bind_parent_platform_devices_with_options(request, runtime)

    async def batch_bind_parent_platform_devices_async(
        self,
        request: vs_20181212_models.BatchBindParentPlatformDevicesRequest,
    ) -> vs_20181212_models.BatchBindParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_bind_parent_platform_devices_with_options_async(request, runtime)

    def batch_bind_purchased_devices_with_options(
        self,
        request: vs_20181212_models.BatchBindPurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindPurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindPurchasedDevicesResponse().from_map(
            self.do_rpcrequest('BatchBindPurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_bind_purchased_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchBindPurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindPurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindPurchasedDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchBindPurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_bind_purchased_devices(
        self,
        request: vs_20181212_models.BatchBindPurchasedDevicesRequest,
    ) -> vs_20181212_models.BatchBindPurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_bind_purchased_devices_with_options(request, runtime)

    async def batch_bind_purchased_devices_async(
        self,
        request: vs_20181212_models.BatchBindPurchasedDevicesRequest,
    ) -> vs_20181212_models.BatchBindPurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_bind_purchased_devices_with_options_async(request, runtime)

    def batch_bind_template_with_options(
        self,
        request: vs_20181212_models.BatchBindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindTemplateResponse().from_map(
            self.do_rpcrequest('BatchBindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_bind_template_with_options_async(
        self,
        request: vs_20181212_models.BatchBindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindTemplateResponse().from_map(
            await self.do_rpcrequest_async('BatchBindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_bind_template(
        self,
        request: vs_20181212_models.BatchBindTemplateRequest,
    ) -> vs_20181212_models.BatchBindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_bind_template_with_options(request, runtime)

    async def batch_bind_template_async(
        self,
        request: vs_20181212_models.BatchBindTemplateRequest,
    ) -> vs_20181212_models.BatchBindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_bind_template_with_options_async(request, runtime)

    def batch_bind_templates_with_options(
        self,
        request: vs_20181212_models.BatchBindTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindTemplatesResponse().from_map(
            self.do_rpcrequest('BatchBindTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_bind_templates_with_options_async(
        self,
        request: vs_20181212_models.BatchBindTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchBindTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchBindTemplatesResponse().from_map(
            await self.do_rpcrequest_async('BatchBindTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_bind_templates(
        self,
        request: vs_20181212_models.BatchBindTemplatesRequest,
    ) -> vs_20181212_models.BatchBindTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_bind_templates_with_options(request, runtime)

    async def batch_bind_templates_async(
        self,
        request: vs_20181212_models.BatchBindTemplatesRequest,
    ) -> vs_20181212_models.BatchBindTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_bind_templates_with_options_async(request, runtime)

    def batch_delete_devices_with_options(
        self,
        request: vs_20181212_models.BatchDeleteDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchDeleteDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchDeleteDevicesResponse().from_map(
            self.do_rpcrequest('BatchDeleteDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_delete_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchDeleteDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchDeleteDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchDeleteDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchDeleteDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_delete_devices(
        self,
        request: vs_20181212_models.BatchDeleteDevicesRequest,
    ) -> vs_20181212_models.BatchDeleteDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_delete_devices_with_options(request, runtime)

    async def batch_delete_devices_async(
        self,
        request: vs_20181212_models.BatchDeleteDevicesRequest,
    ) -> vs_20181212_models.BatchDeleteDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_delete_devices_with_options_async(request, runtime)

    def batch_delete_vs_domain_configs_with_options(
        self,
        request: vs_20181212_models.BatchDeleteVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchDeleteVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchDeleteVsDomainConfigsResponse().from_map(
            self.do_rpcrequest('BatchDeleteVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_delete_vs_domain_configs_with_options_async(
        self,
        request: vs_20181212_models.BatchDeleteVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchDeleteVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchDeleteVsDomainConfigsResponse().from_map(
            await self.do_rpcrequest_async('BatchDeleteVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_delete_vs_domain_configs(
        self,
        request: vs_20181212_models.BatchDeleteVsDomainConfigsRequest,
    ) -> vs_20181212_models.BatchDeleteVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_delete_vs_domain_configs_with_options(request, runtime)

    async def batch_delete_vs_domain_configs_async(
        self,
        request: vs_20181212_models.BatchDeleteVsDomainConfigsRequest,
    ) -> vs_20181212_models.BatchDeleteVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_delete_vs_domain_configs_with_options_async(request, runtime)

    def batch_forbid_vs_stream_with_options(
        self,
        request: vs_20181212_models.BatchForbidVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchForbidVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchForbidVsStreamResponse().from_map(
            self.do_rpcrequest('BatchForbidVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_forbid_vs_stream_with_options_async(
        self,
        request: vs_20181212_models.BatchForbidVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchForbidVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchForbidVsStreamResponse().from_map(
            await self.do_rpcrequest_async('BatchForbidVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_forbid_vs_stream(
        self,
        request: vs_20181212_models.BatchForbidVsStreamRequest,
    ) -> vs_20181212_models.BatchForbidVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_forbid_vs_stream_with_options(request, runtime)

    async def batch_forbid_vs_stream_async(
        self,
        request: vs_20181212_models.BatchForbidVsStreamRequest,
    ) -> vs_20181212_models.BatchForbidVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_forbid_vs_stream_with_options_async(request, runtime)

    def batch_resume_vs_stream_with_options(
        self,
        request: vs_20181212_models.BatchResumeVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchResumeVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchResumeVsStreamResponse().from_map(
            self.do_rpcrequest('BatchResumeVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_resume_vs_stream_with_options_async(
        self,
        request: vs_20181212_models.BatchResumeVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchResumeVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchResumeVsStreamResponse().from_map(
            await self.do_rpcrequest_async('BatchResumeVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_resume_vs_stream(
        self,
        request: vs_20181212_models.BatchResumeVsStreamRequest,
    ) -> vs_20181212_models.BatchResumeVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_resume_vs_stream_with_options(request, runtime)

    async def batch_resume_vs_stream_async(
        self,
        request: vs_20181212_models.BatchResumeVsStreamRequest,
    ) -> vs_20181212_models.BatchResumeVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_resume_vs_stream_with_options_async(request, runtime)

    def batch_set_vs_domain_configs_with_options(
        self,
        request: vs_20181212_models.BatchSetVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchSetVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchSetVsDomainConfigsResponse().from_map(
            self.do_rpcrequest('BatchSetVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_set_vs_domain_configs_with_options_async(
        self,
        request: vs_20181212_models.BatchSetVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchSetVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchSetVsDomainConfigsResponse().from_map(
            await self.do_rpcrequest_async('BatchSetVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_set_vs_domain_configs(
        self,
        request: vs_20181212_models.BatchSetVsDomainConfigsRequest,
    ) -> vs_20181212_models.BatchSetVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_set_vs_domain_configs_with_options(request, runtime)

    async def batch_set_vs_domain_configs_async(
        self,
        request: vs_20181212_models.BatchSetVsDomainConfigsRequest,
    ) -> vs_20181212_models.BatchSetVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_set_vs_domain_configs_with_options_async(request, runtime)

    def batch_start_devices_with_options(
        self,
        request: vs_20181212_models.BatchStartDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStartDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStartDevicesResponse().from_map(
            self.do_rpcrequest('BatchStartDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_start_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchStartDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStartDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStartDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchStartDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_start_devices(
        self,
        request: vs_20181212_models.BatchStartDevicesRequest,
    ) -> vs_20181212_models.BatchStartDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_start_devices_with_options(request, runtime)

    async def batch_start_devices_async(
        self,
        request: vs_20181212_models.BatchStartDevicesRequest,
    ) -> vs_20181212_models.BatchStartDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_start_devices_with_options_async(request, runtime)

    def batch_start_streams_with_options(
        self,
        request: vs_20181212_models.BatchStartStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStartStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStartStreamsResponse().from_map(
            self.do_rpcrequest('BatchStartStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_start_streams_with_options_async(
        self,
        request: vs_20181212_models.BatchStartStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStartStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStartStreamsResponse().from_map(
            await self.do_rpcrequest_async('BatchStartStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_start_streams(
        self,
        request: vs_20181212_models.BatchStartStreamsRequest,
    ) -> vs_20181212_models.BatchStartStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_start_streams_with_options(request, runtime)

    async def batch_start_streams_async(
        self,
        request: vs_20181212_models.BatchStartStreamsRequest,
    ) -> vs_20181212_models.BatchStartStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_start_streams_with_options_async(request, runtime)

    def batch_stop_devices_with_options(
        self,
        request: vs_20181212_models.BatchStopDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStopDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStopDevicesResponse().from_map(
            self.do_rpcrequest('BatchStopDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_stop_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchStopDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStopDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStopDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchStopDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_stop_devices(
        self,
        request: vs_20181212_models.BatchStopDevicesRequest,
    ) -> vs_20181212_models.BatchStopDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_stop_devices_with_options(request, runtime)

    async def batch_stop_devices_async(
        self,
        request: vs_20181212_models.BatchStopDevicesRequest,
    ) -> vs_20181212_models.BatchStopDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_stop_devices_with_options_async(request, runtime)

    def batch_stop_streams_with_options(
        self,
        request: vs_20181212_models.BatchStopStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStopStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStopStreamsResponse().from_map(
            self.do_rpcrequest('BatchStopStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_stop_streams_with_options_async(
        self,
        request: vs_20181212_models.BatchStopStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchStopStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchStopStreamsResponse().from_map(
            await self.do_rpcrequest_async('BatchStopStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_stop_streams(
        self,
        request: vs_20181212_models.BatchStopStreamsRequest,
    ) -> vs_20181212_models.BatchStopStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_stop_streams_with_options(request, runtime)

    async def batch_stop_streams_async(
        self,
        request: vs_20181212_models.BatchStopStreamsRequest,
    ) -> vs_20181212_models.BatchStopStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_stop_streams_with_options_async(request, runtime)

    def batch_unbind_directories_with_options(
        self,
        request: vs_20181212_models.BatchUnbindDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindDirectoriesResponse().from_map(
            self.do_rpcrequest('BatchUnbindDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_unbind_directories_with_options_async(
        self,
        request: vs_20181212_models.BatchUnbindDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindDirectoriesResponse().from_map(
            await self.do_rpcrequest_async('BatchUnbindDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_unbind_directories(
        self,
        request: vs_20181212_models.BatchUnbindDirectoriesRequest,
    ) -> vs_20181212_models.BatchUnbindDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_unbind_directories_with_options(request, runtime)

    async def batch_unbind_directories_async(
        self,
        request: vs_20181212_models.BatchUnbindDirectoriesRequest,
    ) -> vs_20181212_models.BatchUnbindDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_unbind_directories_with_options_async(request, runtime)

    def batch_unbind_parent_platform_devices_with_options(
        self,
        request: vs_20181212_models.BatchUnbindParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindParentPlatformDevicesResponse().from_map(
            self.do_rpcrequest('BatchUnbindParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_unbind_parent_platform_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchUnbindParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindParentPlatformDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchUnbindParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_unbind_parent_platform_devices(
        self,
        request: vs_20181212_models.BatchUnbindParentPlatformDevicesRequest,
    ) -> vs_20181212_models.BatchUnbindParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_unbind_parent_platform_devices_with_options(request, runtime)

    async def batch_unbind_parent_platform_devices_async(
        self,
        request: vs_20181212_models.BatchUnbindParentPlatformDevicesRequest,
    ) -> vs_20181212_models.BatchUnbindParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_unbind_parent_platform_devices_with_options_async(request, runtime)

    def batch_unbind_purchased_devices_with_options(
        self,
        request: vs_20181212_models.BatchUnbindPurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindPurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindPurchasedDevicesResponse().from_map(
            self.do_rpcrequest('BatchUnbindPurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_unbind_purchased_devices_with_options_async(
        self,
        request: vs_20181212_models.BatchUnbindPurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindPurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindPurchasedDevicesResponse().from_map(
            await self.do_rpcrequest_async('BatchUnbindPurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_unbind_purchased_devices(
        self,
        request: vs_20181212_models.BatchUnbindPurchasedDevicesRequest,
    ) -> vs_20181212_models.BatchUnbindPurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_unbind_purchased_devices_with_options(request, runtime)

    async def batch_unbind_purchased_devices_async(
        self,
        request: vs_20181212_models.BatchUnbindPurchasedDevicesRequest,
    ) -> vs_20181212_models.BatchUnbindPurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_unbind_purchased_devices_with_options_async(request, runtime)

    def batch_unbind_template_with_options(
        self,
        request: vs_20181212_models.BatchUnbindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindTemplateResponse().from_map(
            self.do_rpcrequest('BatchUnbindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_unbind_template_with_options_async(
        self,
        request: vs_20181212_models.BatchUnbindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindTemplateResponse().from_map(
            await self.do_rpcrequest_async('BatchUnbindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_unbind_template(
        self,
        request: vs_20181212_models.BatchUnbindTemplateRequest,
    ) -> vs_20181212_models.BatchUnbindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_unbind_template_with_options(request, runtime)

    async def batch_unbind_template_async(
        self,
        request: vs_20181212_models.BatchUnbindTemplateRequest,
    ) -> vs_20181212_models.BatchUnbindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_unbind_template_with_options_async(request, runtime)

    def batch_unbind_templates_with_options(
        self,
        request: vs_20181212_models.BatchUnbindTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindTemplatesResponse().from_map(
            self.do_rpcrequest('BatchUnbindTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def batch_unbind_templates_with_options_async(
        self,
        request: vs_20181212_models.BatchUnbindTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BatchUnbindTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BatchUnbindTemplatesResponse().from_map(
            await self.do_rpcrequest_async('BatchUnbindTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def batch_unbind_templates(
        self,
        request: vs_20181212_models.BatchUnbindTemplatesRequest,
    ) -> vs_20181212_models.BatchUnbindTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return self.batch_unbind_templates_with_options(request, runtime)

    async def batch_unbind_templates_async(
        self,
        request: vs_20181212_models.BatchUnbindTemplatesRequest,
    ) -> vs_20181212_models.BatchUnbindTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.batch_unbind_templates_with_options_async(request, runtime)

    def bind_directory_with_options(
        self,
        request: vs_20181212_models.BindDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindDirectoryResponse().from_map(
            self.do_rpcrequest('BindDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bind_directory_with_options_async(
        self,
        request: vs_20181212_models.BindDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindDirectoryResponse().from_map(
            await self.do_rpcrequest_async('BindDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bind_directory(
        self,
        request: vs_20181212_models.BindDirectoryRequest,
    ) -> vs_20181212_models.BindDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.bind_directory_with_options(request, runtime)

    async def bind_directory_async(
        self,
        request: vs_20181212_models.BindDirectoryRequest,
    ) -> vs_20181212_models.BindDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bind_directory_with_options_async(request, runtime)

    def bind_parent_platform_device_with_options(
        self,
        request: vs_20181212_models.BindParentPlatformDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindParentPlatformDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindParentPlatformDeviceResponse().from_map(
            self.do_rpcrequest('BindParentPlatformDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bind_parent_platform_device_with_options_async(
        self,
        request: vs_20181212_models.BindParentPlatformDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindParentPlatformDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindParentPlatformDeviceResponse().from_map(
            await self.do_rpcrequest_async('BindParentPlatformDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bind_parent_platform_device(
        self,
        request: vs_20181212_models.BindParentPlatformDeviceRequest,
    ) -> vs_20181212_models.BindParentPlatformDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.bind_parent_platform_device_with_options(request, runtime)

    async def bind_parent_platform_device_async(
        self,
        request: vs_20181212_models.BindParentPlatformDeviceRequest,
    ) -> vs_20181212_models.BindParentPlatformDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bind_parent_platform_device_with_options_async(request, runtime)

    def bind_purchased_device_with_options(
        self,
        request: vs_20181212_models.BindPurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindPurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindPurchasedDeviceResponse().from_map(
            self.do_rpcrequest('BindPurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bind_purchased_device_with_options_async(
        self,
        request: vs_20181212_models.BindPurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindPurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindPurchasedDeviceResponse().from_map(
            await self.do_rpcrequest_async('BindPurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bind_purchased_device(
        self,
        request: vs_20181212_models.BindPurchasedDeviceRequest,
    ) -> vs_20181212_models.BindPurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.bind_purchased_device_with_options(request, runtime)

    async def bind_purchased_device_async(
        self,
        request: vs_20181212_models.BindPurchasedDeviceRequest,
    ) -> vs_20181212_models.BindPurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bind_purchased_device_with_options_async(request, runtime)

    def bind_template_with_options(
        self,
        request: vs_20181212_models.BindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindTemplateResponse().from_map(
            self.do_rpcrequest('BindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bind_template_with_options_async(
        self,
        request: vs_20181212_models.BindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.BindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.BindTemplateResponse().from_map(
            await self.do_rpcrequest_async('BindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bind_template(
        self,
        request: vs_20181212_models.BindTemplateRequest,
    ) -> vs_20181212_models.BindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.bind_template_with_options(request, runtime)

    async def bind_template_async(
        self,
        request: vs_20181212_models.BindTemplateRequest,
    ) -> vs_20181212_models.BindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bind_template_with_options_async(request, runtime)

    def continuous_adjust_with_options(
        self,
        request: vs_20181212_models.ContinuousAdjustRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ContinuousAdjustResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ContinuousAdjustResponse().from_map(
            self.do_rpcrequest('ContinuousAdjust', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def continuous_adjust_with_options_async(
        self,
        request: vs_20181212_models.ContinuousAdjustRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ContinuousAdjustResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ContinuousAdjustResponse().from_map(
            await self.do_rpcrequest_async('ContinuousAdjust', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def continuous_adjust(
        self,
        request: vs_20181212_models.ContinuousAdjustRequest,
    ) -> vs_20181212_models.ContinuousAdjustResponse:
        runtime = util_models.RuntimeOptions()
        return self.continuous_adjust_with_options(request, runtime)

    async def continuous_adjust_async(
        self,
        request: vs_20181212_models.ContinuousAdjustRequest,
    ) -> vs_20181212_models.ContinuousAdjustResponse:
        runtime = util_models.RuntimeOptions()
        return await self.continuous_adjust_with_options_async(request, runtime)

    def continuous_move_with_options(
        self,
        request: vs_20181212_models.ContinuousMoveRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ContinuousMoveResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ContinuousMoveResponse().from_map(
            self.do_rpcrequest('ContinuousMove', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def continuous_move_with_options_async(
        self,
        request: vs_20181212_models.ContinuousMoveRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ContinuousMoveResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ContinuousMoveResponse().from_map(
            await self.do_rpcrequest_async('ContinuousMove', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def continuous_move(
        self,
        request: vs_20181212_models.ContinuousMoveRequest,
    ) -> vs_20181212_models.ContinuousMoveResponse:
        runtime = util_models.RuntimeOptions()
        return self.continuous_move_with_options(request, runtime)

    async def continuous_move_async(
        self,
        request: vs_20181212_models.ContinuousMoveRequest,
    ) -> vs_20181212_models.ContinuousMoveResponse:
        runtime = util_models.RuntimeOptions()
        return await self.continuous_move_with_options_async(request, runtime)

    def create_device_with_options(
        self,
        request: vs_20181212_models.CreateDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDeviceResponse().from_map(
            self.do_rpcrequest('CreateDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_device_with_options_async(
        self,
        request: vs_20181212_models.CreateDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDeviceResponse().from_map(
            await self.do_rpcrequest_async('CreateDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_device(
        self,
        request: vs_20181212_models.CreateDeviceRequest,
    ) -> vs_20181212_models.CreateDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_device_with_options(request, runtime)

    async def create_device_async(
        self,
        request: vs_20181212_models.CreateDeviceRequest,
    ) -> vs_20181212_models.CreateDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_device_with_options_async(request, runtime)

    def create_device_alarm_with_options(
        self,
        request: vs_20181212_models.CreateDeviceAlarmRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDeviceAlarmResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDeviceAlarmResponse().from_map(
            self.do_rpcrequest('CreateDeviceAlarm', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_device_alarm_with_options_async(
        self,
        request: vs_20181212_models.CreateDeviceAlarmRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDeviceAlarmResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDeviceAlarmResponse().from_map(
            await self.do_rpcrequest_async('CreateDeviceAlarm', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_device_alarm(
        self,
        request: vs_20181212_models.CreateDeviceAlarmRequest,
    ) -> vs_20181212_models.CreateDeviceAlarmResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_device_alarm_with_options(request, runtime)

    async def create_device_alarm_async(
        self,
        request: vs_20181212_models.CreateDeviceAlarmRequest,
    ) -> vs_20181212_models.CreateDeviceAlarmResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_device_alarm_with_options_async(request, runtime)

    def create_directory_with_options(
        self,
        request: vs_20181212_models.CreateDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDirectoryResponse().from_map(
            self.do_rpcrequest('CreateDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_directory_with_options_async(
        self,
        request: vs_20181212_models.CreateDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateDirectoryResponse().from_map(
            await self.do_rpcrequest_async('CreateDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_directory(
        self,
        request: vs_20181212_models.CreateDirectoryRequest,
    ) -> vs_20181212_models.CreateDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_directory_with_options(request, runtime)

    async def create_directory_async(
        self,
        request: vs_20181212_models.CreateDirectoryRequest,
    ) -> vs_20181212_models.CreateDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_directory_with_options_async(request, runtime)

    def create_group_with_options(
        self,
        request: vs_20181212_models.CreateGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateGroupResponse().from_map(
            self.do_rpcrequest('CreateGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_group_with_options_async(
        self,
        request: vs_20181212_models.CreateGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateGroupResponse().from_map(
            await self.do_rpcrequest_async('CreateGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_group(
        self,
        request: vs_20181212_models.CreateGroupRequest,
    ) -> vs_20181212_models.CreateGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_group_with_options(request, runtime)

    async def create_group_async(
        self,
        request: vs_20181212_models.CreateGroupRequest,
    ) -> vs_20181212_models.CreateGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_group_with_options_async(request, runtime)

    def create_parent_platform_with_options(
        self,
        request: vs_20181212_models.CreateParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateParentPlatformResponse().from_map(
            self.do_rpcrequest('CreateParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_parent_platform_with_options_async(
        self,
        request: vs_20181212_models.CreateParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateParentPlatformResponse().from_map(
            await self.do_rpcrequest_async('CreateParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_parent_platform(
        self,
        request: vs_20181212_models.CreateParentPlatformRequest,
    ) -> vs_20181212_models.CreateParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_parent_platform_with_options(request, runtime)

    async def create_parent_platform_async(
        self,
        request: vs_20181212_models.CreateParentPlatformRequest,
    ) -> vs_20181212_models.CreateParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_parent_platform_with_options_async(request, runtime)

    def create_stream_snapshot_with_options(
        self,
        request: vs_20181212_models.CreateStreamSnapshotRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateStreamSnapshotResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateStreamSnapshotResponse().from_map(
            self.do_rpcrequest('CreateStreamSnapshot', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_stream_snapshot_with_options_async(
        self,
        request: vs_20181212_models.CreateStreamSnapshotRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateStreamSnapshotResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateStreamSnapshotResponse().from_map(
            await self.do_rpcrequest_async('CreateStreamSnapshot', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_stream_snapshot(
        self,
        request: vs_20181212_models.CreateStreamSnapshotRequest,
    ) -> vs_20181212_models.CreateStreamSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_stream_snapshot_with_options(request, runtime)

    async def create_stream_snapshot_async(
        self,
        request: vs_20181212_models.CreateStreamSnapshotRequest,
    ) -> vs_20181212_models.CreateStreamSnapshotResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_stream_snapshot_with_options_async(request, runtime)

    def create_template_with_options(
        self,
        request: vs_20181212_models.CreateTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateTemplateResponse().from_map(
            self.do_rpcrequest('CreateTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_template_with_options_async(
        self,
        request: vs_20181212_models.CreateTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.CreateTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.CreateTemplateResponse().from_map(
            await self.do_rpcrequest_async('CreateTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_template(
        self,
        request: vs_20181212_models.CreateTemplateRequest,
    ) -> vs_20181212_models.CreateTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_template_with_options(request, runtime)

    async def create_template_async(
        self,
        request: vs_20181212_models.CreateTemplateRequest,
    ) -> vs_20181212_models.CreateTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_template_with_options_async(request, runtime)

    def delete_device_with_options(
        self,
        request: vs_20181212_models.DeleteDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteDeviceResponse().from_map(
            self.do_rpcrequest('DeleteDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_device_with_options_async(
        self,
        request: vs_20181212_models.DeleteDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteDeviceResponse().from_map(
            await self.do_rpcrequest_async('DeleteDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_device(
        self,
        request: vs_20181212_models.DeleteDeviceRequest,
    ) -> vs_20181212_models.DeleteDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_device_with_options(request, runtime)

    async def delete_device_async(
        self,
        request: vs_20181212_models.DeleteDeviceRequest,
    ) -> vs_20181212_models.DeleteDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_device_with_options_async(request, runtime)

    def delete_directory_with_options(
        self,
        request: vs_20181212_models.DeleteDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteDirectoryResponse().from_map(
            self.do_rpcrequest('DeleteDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_directory_with_options_async(
        self,
        request: vs_20181212_models.DeleteDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteDirectoryResponse().from_map(
            await self.do_rpcrequest_async('DeleteDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_directory(
        self,
        request: vs_20181212_models.DeleteDirectoryRequest,
    ) -> vs_20181212_models.DeleteDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_directory_with_options(request, runtime)

    async def delete_directory_async(
        self,
        request: vs_20181212_models.DeleteDirectoryRequest,
    ) -> vs_20181212_models.DeleteDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_directory_with_options_async(request, runtime)

    def delete_group_with_options(
        self,
        request: vs_20181212_models.DeleteGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteGroupResponse().from_map(
            self.do_rpcrequest('DeleteGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_group_with_options_async(
        self,
        request: vs_20181212_models.DeleteGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteGroupResponse().from_map(
            await self.do_rpcrequest_async('DeleteGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_group(
        self,
        request: vs_20181212_models.DeleteGroupRequest,
    ) -> vs_20181212_models.DeleteGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_group_with_options(request, runtime)

    async def delete_group_async(
        self,
        request: vs_20181212_models.DeleteGroupRequest,
    ) -> vs_20181212_models.DeleteGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_group_with_options_async(request, runtime)

    def delete_parent_platform_with_options(
        self,
        request: vs_20181212_models.DeleteParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteParentPlatformResponse().from_map(
            self.do_rpcrequest('DeleteParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_parent_platform_with_options_async(
        self,
        request: vs_20181212_models.DeleteParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteParentPlatformResponse().from_map(
            await self.do_rpcrequest_async('DeleteParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_parent_platform(
        self,
        request: vs_20181212_models.DeleteParentPlatformRequest,
    ) -> vs_20181212_models.DeleteParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_parent_platform_with_options(request, runtime)

    async def delete_parent_platform_async(
        self,
        request: vs_20181212_models.DeleteParentPlatformRequest,
    ) -> vs_20181212_models.DeleteParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_parent_platform_with_options_async(request, runtime)

    def delete_preset_with_options(
        self,
        request: vs_20181212_models.DeletePresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeletePresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeletePresetResponse().from_map(
            self.do_rpcrequest('DeletePreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_preset_with_options_async(
        self,
        request: vs_20181212_models.DeletePresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeletePresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeletePresetResponse().from_map(
            await self.do_rpcrequest_async('DeletePreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_preset(
        self,
        request: vs_20181212_models.DeletePresetRequest,
    ) -> vs_20181212_models.DeletePresetResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_preset_with_options(request, runtime)

    async def delete_preset_async(
        self,
        request: vs_20181212_models.DeletePresetRequest,
    ) -> vs_20181212_models.DeletePresetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_preset_with_options_async(request, runtime)

    def delete_template_with_options(
        self,
        request: vs_20181212_models.DeleteTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteTemplateResponse().from_map(
            self.do_rpcrequest('DeleteTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_template_with_options_async(
        self,
        request: vs_20181212_models.DeleteTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteTemplateResponse().from_map(
            await self.do_rpcrequest_async('DeleteTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_template(
        self,
        request: vs_20181212_models.DeleteTemplateRequest,
    ) -> vs_20181212_models.DeleteTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_template_with_options(request, runtime)

    async def delete_template_async(
        self,
        request: vs_20181212_models.DeleteTemplateRequest,
    ) -> vs_20181212_models.DeleteTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_template_with_options_async(request, runtime)

    def delete_vs_pull_stream_info_config_with_options(
        self,
        request: vs_20181212_models.DeleteVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteVsPullStreamInfoConfigResponse().from_map(
            self.do_rpcrequest('DeleteVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_vs_pull_stream_info_config_with_options_async(
        self,
        request: vs_20181212_models.DeleteVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteVsPullStreamInfoConfigResponse().from_map(
            await self.do_rpcrequest_async('DeleteVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_vs_pull_stream_info_config(
        self,
        request: vs_20181212_models.DeleteVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.DeleteVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_vs_pull_stream_info_config_with_options(request, runtime)

    async def delete_vs_pull_stream_info_config_async(
        self,
        request: vs_20181212_models.DeleteVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.DeleteVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_vs_pull_stream_info_config_with_options_async(request, runtime)

    def delete_vs_streams_notify_url_config_with_options(
        self,
        request: vs_20181212_models.DeleteVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse().from_map(
            self.do_rpcrequest('DeleteVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_vs_streams_notify_url_config_with_options_async(
        self,
        request: vs_20181212_models.DeleteVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse().from_map(
            await self.do_rpcrequest_async('DeleteVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_vs_streams_notify_url_config(
        self,
        request: vs_20181212_models.DeleteVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_vs_streams_notify_url_config_with_options(request, runtime)

    async def delete_vs_streams_notify_url_config_async(
        self,
        request: vs_20181212_models.DeleteVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.DeleteVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_vs_streams_notify_url_config_with_options_async(request, runtime)

    def describe_account_stat_with_options(
        self,
        request: vs_20181212_models.DescribeAccountStatRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeAccountStatResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeAccountStatResponse().from_map(
            self.do_rpcrequest('DescribeAccountStat', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_account_stat_with_options_async(
        self,
        request: vs_20181212_models.DescribeAccountStatRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeAccountStatResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeAccountStatResponse().from_map(
            await self.do_rpcrequest_async('DescribeAccountStat', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_account_stat(
        self,
        request: vs_20181212_models.DescribeAccountStatRequest,
    ) -> vs_20181212_models.DescribeAccountStatResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_account_stat_with_options(request, runtime)

    async def describe_account_stat_async(
        self,
        request: vs_20181212_models.DescribeAccountStatRequest,
    ) -> vs_20181212_models.DescribeAccountStatResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_account_stat_with_options_async(request, runtime)

    def describe_device_with_options(
        self,
        request: vs_20181212_models.DescribeDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceResponse().from_map(
            self.do_rpcrequest('DescribeDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_device_with_options_async(
        self,
        request: vs_20181212_models.DescribeDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceResponse().from_map(
            await self.do_rpcrequest_async('DescribeDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_device(
        self,
        request: vs_20181212_models.DescribeDeviceRequest,
    ) -> vs_20181212_models.DescribeDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_device_with_options(request, runtime)

    async def describe_device_async(
        self,
        request: vs_20181212_models.DescribeDeviceRequest,
    ) -> vs_20181212_models.DescribeDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_device_with_options_async(request, runtime)

    def describe_device_channels_with_options(
        self,
        request: vs_20181212_models.DescribeDeviceChannelsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceChannelsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceChannelsResponse().from_map(
            self.do_rpcrequest('DescribeDeviceChannels', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_device_channels_with_options_async(
        self,
        request: vs_20181212_models.DescribeDeviceChannelsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceChannelsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceChannelsResponse().from_map(
            await self.do_rpcrequest_async('DescribeDeviceChannels', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_device_channels(
        self,
        request: vs_20181212_models.DescribeDeviceChannelsRequest,
    ) -> vs_20181212_models.DescribeDeviceChannelsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_device_channels_with_options(request, runtime)

    async def describe_device_channels_async(
        self,
        request: vs_20181212_models.DescribeDeviceChannelsRequest,
    ) -> vs_20181212_models.DescribeDeviceChannelsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_device_channels_with_options_async(request, runtime)

    def describe_device_gateway_with_options(
        self,
        request: vs_20181212_models.DescribeDeviceGatewayRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceGatewayResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceGatewayResponse().from_map(
            self.do_rpcrequest('DescribeDeviceGateway', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_device_gateway_with_options_async(
        self,
        request: vs_20181212_models.DescribeDeviceGatewayRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceGatewayResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceGatewayResponse().from_map(
            await self.do_rpcrequest_async('DescribeDeviceGateway', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_device_gateway(
        self,
        request: vs_20181212_models.DescribeDeviceGatewayRequest,
    ) -> vs_20181212_models.DescribeDeviceGatewayResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_device_gateway_with_options(request, runtime)

    async def describe_device_gateway_async(
        self,
        request: vs_20181212_models.DescribeDeviceGatewayRequest,
    ) -> vs_20181212_models.DescribeDeviceGatewayResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_device_gateway_with_options_async(request, runtime)

    def describe_devices_with_options(
        self,
        request: vs_20181212_models.DescribeDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDevicesResponse().from_map(
            self.do_rpcrequest('DescribeDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_devices_with_options_async(
        self,
        request: vs_20181212_models.DescribeDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDevicesResponse().from_map(
            await self.do_rpcrequest_async('DescribeDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_devices(
        self,
        request: vs_20181212_models.DescribeDevicesRequest,
    ) -> vs_20181212_models.DescribeDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_devices_with_options(request, runtime)

    async def describe_devices_async(
        self,
        request: vs_20181212_models.DescribeDevicesRequest,
    ) -> vs_20181212_models.DescribeDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_devices_with_options_async(request, runtime)

    def describe_device_urlwith_options(
        self,
        request: vs_20181212_models.DescribeDeviceURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceURLResponse().from_map(
            self.do_rpcrequest('DescribeDeviceURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_device_urlwith_options_async(
        self,
        request: vs_20181212_models.DescribeDeviceURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDeviceURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDeviceURLResponse().from_map(
            await self.do_rpcrequest_async('DescribeDeviceURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_device_url(
        self,
        request: vs_20181212_models.DescribeDeviceURLRequest,
    ) -> vs_20181212_models.DescribeDeviceURLResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_device_urlwith_options(request, runtime)

    async def describe_device_url_async(
        self,
        request: vs_20181212_models.DescribeDeviceURLRequest,
    ) -> vs_20181212_models.DescribeDeviceURLResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_device_urlwith_options_async(request, runtime)

    def describe_directories_with_options(
        self,
        request: vs_20181212_models.DescribeDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDirectoriesResponse().from_map(
            self.do_rpcrequest('DescribeDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_directories_with_options_async(
        self,
        request: vs_20181212_models.DescribeDirectoriesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDirectoriesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDirectoriesResponse().from_map(
            await self.do_rpcrequest_async('DescribeDirectories', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_directories(
        self,
        request: vs_20181212_models.DescribeDirectoriesRequest,
    ) -> vs_20181212_models.DescribeDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_directories_with_options(request, runtime)

    async def describe_directories_async(
        self,
        request: vs_20181212_models.DescribeDirectoriesRequest,
    ) -> vs_20181212_models.DescribeDirectoriesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_directories_with_options_async(request, runtime)

    def describe_directory_with_options(
        self,
        request: vs_20181212_models.DescribeDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDirectoryResponse().from_map(
            self.do_rpcrequest('DescribeDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_directory_with_options_async(
        self,
        request: vs_20181212_models.DescribeDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeDirectoryResponse().from_map(
            await self.do_rpcrequest_async('DescribeDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_directory(
        self,
        request: vs_20181212_models.DescribeDirectoryRequest,
    ) -> vs_20181212_models.DescribeDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_directory_with_options(request, runtime)

    async def describe_directory_async(
        self,
        request: vs_20181212_models.DescribeDirectoryRequest,
    ) -> vs_20181212_models.DescribeDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_directory_with_options_async(request, runtime)

    def describe_group_with_options(
        self,
        request: vs_20181212_models.DescribeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeGroupResponse().from_map(
            self.do_rpcrequest('DescribeGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_group_with_options_async(
        self,
        request: vs_20181212_models.DescribeGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeGroupResponse().from_map(
            await self.do_rpcrequest_async('DescribeGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_group(
        self,
        request: vs_20181212_models.DescribeGroupRequest,
    ) -> vs_20181212_models.DescribeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_group_with_options(request, runtime)

    async def describe_group_async(
        self,
        request: vs_20181212_models.DescribeGroupRequest,
    ) -> vs_20181212_models.DescribeGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_group_with_options_async(request, runtime)

    def describe_groups_with_options(
        self,
        request: vs_20181212_models.DescribeGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeGroupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeGroupsResponse().from_map(
            self.do_rpcrequest('DescribeGroups', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_groups_with_options_async(
        self,
        request: vs_20181212_models.DescribeGroupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeGroupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeGroupsResponse().from_map(
            await self.do_rpcrequest_async('DescribeGroups', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_groups(
        self,
        request: vs_20181212_models.DescribeGroupsRequest,
    ) -> vs_20181212_models.DescribeGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_groups_with_options(request, runtime)

    async def describe_groups_async(
        self,
        request: vs_20181212_models.DescribeGroupsRequest,
    ) -> vs_20181212_models.DescribeGroupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_groups_with_options_async(request, runtime)

    def describe_parent_platform_with_options(
        self,
        request: vs_20181212_models.DescribeParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformResponse().from_map(
            self.do_rpcrequest('DescribeParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_parent_platform_with_options_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformResponse().from_map(
            await self.do_rpcrequest_async('DescribeParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_parent_platform(
        self,
        request: vs_20181212_models.DescribeParentPlatformRequest,
    ) -> vs_20181212_models.DescribeParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_parent_platform_with_options(request, runtime)

    async def describe_parent_platform_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformRequest,
    ) -> vs_20181212_models.DescribeParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_parent_platform_with_options_async(request, runtime)

    def describe_parent_platform_devices_with_options(
        self,
        request: vs_20181212_models.DescribeParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformDevicesResponse().from_map(
            self.do_rpcrequest('DescribeParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_parent_platform_devices_with_options_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformDevicesResponse().from_map(
            await self.do_rpcrequest_async('DescribeParentPlatformDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_parent_platform_devices(
        self,
        request: vs_20181212_models.DescribeParentPlatformDevicesRequest,
    ) -> vs_20181212_models.DescribeParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_parent_platform_devices_with_options(request, runtime)

    async def describe_parent_platform_devices_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformDevicesRequest,
    ) -> vs_20181212_models.DescribeParentPlatformDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_parent_platform_devices_with_options_async(request, runtime)

    def describe_parent_platforms_with_options(
        self,
        request: vs_20181212_models.DescribeParentPlatformsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformsResponse().from_map(
            self.do_rpcrequest('DescribeParentPlatforms', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_parent_platforms_with_options_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeParentPlatformsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeParentPlatformsResponse().from_map(
            await self.do_rpcrequest_async('DescribeParentPlatforms', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_parent_platforms(
        self,
        request: vs_20181212_models.DescribeParentPlatformsRequest,
    ) -> vs_20181212_models.DescribeParentPlatformsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_parent_platforms_with_options(request, runtime)

    async def describe_parent_platforms_async(
        self,
        request: vs_20181212_models.DescribeParentPlatformsRequest,
    ) -> vs_20181212_models.DescribeParentPlatformsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_parent_platforms_with_options_async(request, runtime)

    def describe_presets_with_options(
        self,
        request: vs_20181212_models.DescribePresetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePresetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePresetsResponse().from_map(
            self.do_rpcrequest('DescribePresets', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_presets_with_options_async(
        self,
        request: vs_20181212_models.DescribePresetsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePresetsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePresetsResponse().from_map(
            await self.do_rpcrequest_async('DescribePresets', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_presets(
        self,
        request: vs_20181212_models.DescribePresetsRequest,
    ) -> vs_20181212_models.DescribePresetsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_presets_with_options(request, runtime)

    async def describe_presets_async(
        self,
        request: vs_20181212_models.DescribePresetsRequest,
    ) -> vs_20181212_models.DescribePresetsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_presets_with_options_async(request, runtime)

    def describe_purchased_device_with_options(
        self,
        request: vs_20181212_models.DescribePurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePurchasedDeviceResponse().from_map(
            self.do_rpcrequest('DescribePurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_purchased_device_with_options_async(
        self,
        request: vs_20181212_models.DescribePurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePurchasedDeviceResponse().from_map(
            await self.do_rpcrequest_async('DescribePurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_purchased_device(
        self,
        request: vs_20181212_models.DescribePurchasedDeviceRequest,
    ) -> vs_20181212_models.DescribePurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_purchased_device_with_options(request, runtime)

    async def describe_purchased_device_async(
        self,
        request: vs_20181212_models.DescribePurchasedDeviceRequest,
    ) -> vs_20181212_models.DescribePurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_purchased_device_with_options_async(request, runtime)

    def describe_purchased_devices_with_options(
        self,
        request: vs_20181212_models.DescribePurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePurchasedDevicesResponse().from_map(
            self.do_rpcrequest('DescribePurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_purchased_devices_with_options_async(
        self,
        request: vs_20181212_models.DescribePurchasedDevicesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribePurchasedDevicesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribePurchasedDevicesResponse().from_map(
            await self.do_rpcrequest_async('DescribePurchasedDevices', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_purchased_devices(
        self,
        request: vs_20181212_models.DescribePurchasedDevicesRequest,
    ) -> vs_20181212_models.DescribePurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_purchased_devices_with_options(request, runtime)

    async def describe_purchased_devices_async(
        self,
        request: vs_20181212_models.DescribePurchasedDevicesRequest,
    ) -> vs_20181212_models.DescribePurchasedDevicesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_purchased_devices_with_options_async(request, runtime)

    def describe_records_with_options(
        self,
        request: vs_20181212_models.DescribeRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeRecordsResponse().from_map(
            self.do_rpcrequest('DescribeRecords', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_records_with_options_async(
        self,
        request: vs_20181212_models.DescribeRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeRecordsResponse().from_map(
            await self.do_rpcrequest_async('DescribeRecords', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_records(
        self,
        request: vs_20181212_models.DescribeRecordsRequest,
    ) -> vs_20181212_models.DescribeRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_records_with_options(request, runtime)

    async def describe_records_async(
        self,
        request: vs_20181212_models.DescribeRecordsRequest,
    ) -> vs_20181212_models.DescribeRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_records_with_options_async(request, runtime)

    def describe_stream_with_options(
        self,
        request: vs_20181212_models.DescribeStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamResponse().from_map(
            self.do_rpcrequest('DescribeStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_stream_with_options_async(
        self,
        request: vs_20181212_models.DescribeStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamResponse().from_map(
            await self.do_rpcrequest_async('DescribeStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_stream(
        self,
        request: vs_20181212_models.DescribeStreamRequest,
    ) -> vs_20181212_models.DescribeStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_stream_with_options(request, runtime)

    async def describe_stream_async(
        self,
        request: vs_20181212_models.DescribeStreamRequest,
    ) -> vs_20181212_models.DescribeStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_stream_with_options_async(request, runtime)

    def describe_streams_with_options(
        self,
        request: vs_20181212_models.DescribeStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamsResponse().from_map(
            self.do_rpcrequest('DescribeStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_streams_with_options_async(
        self,
        request: vs_20181212_models.DescribeStreamsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamsResponse().from_map(
            await self.do_rpcrequest_async('DescribeStreams', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_streams(
        self,
        request: vs_20181212_models.DescribeStreamsRequest,
    ) -> vs_20181212_models.DescribeStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_streams_with_options(request, runtime)

    async def describe_streams_async(
        self,
        request: vs_20181212_models.DescribeStreamsRequest,
    ) -> vs_20181212_models.DescribeStreamsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_streams_with_options_async(request, runtime)

    def describe_stream_urlwith_options(
        self,
        request: vs_20181212_models.DescribeStreamURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamURLResponse().from_map(
            self.do_rpcrequest('DescribeStreamURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_stream_urlwith_options_async(
        self,
        request: vs_20181212_models.DescribeStreamURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamURLResponse().from_map(
            await self.do_rpcrequest_async('DescribeStreamURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_stream_url(
        self,
        request: vs_20181212_models.DescribeStreamURLRequest,
    ) -> vs_20181212_models.DescribeStreamURLResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_stream_urlwith_options(request, runtime)

    async def describe_stream_url_async(
        self,
        request: vs_20181212_models.DescribeStreamURLRequest,
    ) -> vs_20181212_models.DescribeStreamURLResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_stream_urlwith_options_async(request, runtime)

    def describe_stream_vod_list_with_options(
        self,
        request: vs_20181212_models.DescribeStreamVodListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamVodListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamVodListResponse().from_map(
            self.do_rpcrequest('DescribeStreamVodList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_stream_vod_list_with_options_async(
        self,
        request: vs_20181212_models.DescribeStreamVodListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeStreamVodListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeStreamVodListResponse().from_map(
            await self.do_rpcrequest_async('DescribeStreamVodList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_stream_vod_list(
        self,
        request: vs_20181212_models.DescribeStreamVodListRequest,
    ) -> vs_20181212_models.DescribeStreamVodListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_stream_vod_list_with_options(request, runtime)

    async def describe_stream_vod_list_async(
        self,
        request: vs_20181212_models.DescribeStreamVodListRequest,
    ) -> vs_20181212_models.DescribeStreamVodListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_stream_vod_list_with_options_async(request, runtime)

    def describe_template_with_options(
        self,
        request: vs_20181212_models.DescribeTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeTemplateResponse().from_map(
            self.do_rpcrequest('DescribeTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_template_with_options_async(
        self,
        request: vs_20181212_models.DescribeTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeTemplateResponse().from_map(
            await self.do_rpcrequest_async('DescribeTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_template(
        self,
        request: vs_20181212_models.DescribeTemplateRequest,
    ) -> vs_20181212_models.DescribeTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_template_with_options(request, runtime)

    async def describe_template_async(
        self,
        request: vs_20181212_models.DescribeTemplateRequest,
    ) -> vs_20181212_models.DescribeTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_template_with_options_async(request, runtime)

    def describe_templates_with_options(
        self,
        request: vs_20181212_models.DescribeTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeTemplatesResponse().from_map(
            self.do_rpcrequest('DescribeTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_templates_with_options_async(
        self,
        request: vs_20181212_models.DescribeTemplatesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeTemplatesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeTemplatesResponse().from_map(
            await self.do_rpcrequest_async('DescribeTemplates', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_templates(
        self,
        request: vs_20181212_models.DescribeTemplatesRequest,
    ) -> vs_20181212_models.DescribeTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_templates_with_options(request, runtime)

    async def describe_templates_async(
        self,
        request: vs_20181212_models.DescribeTemplatesRequest,
    ) -> vs_20181212_models.DescribeTemplatesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_templates_with_options_async(request, runtime)

    def describe_vod_stream_urlwith_options(
        self,
        request: vs_20181212_models.DescribeVodStreamURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVodStreamURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVodStreamURLResponse().from_map(
            self.do_rpcrequest('DescribeVodStreamURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vod_stream_urlwith_options_async(
        self,
        request: vs_20181212_models.DescribeVodStreamURLRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVodStreamURLResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVodStreamURLResponse().from_map(
            await self.do_rpcrequest_async('DescribeVodStreamURL', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vod_stream_url(
        self,
        request: vs_20181212_models.DescribeVodStreamURLRequest,
    ) -> vs_20181212_models.DescribeVodStreamURLResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vod_stream_urlwith_options(request, runtime)

    async def describe_vod_stream_url_async(
        self,
        request: vs_20181212_models.DescribeVodStreamURLRequest,
    ) -> vs_20181212_models.DescribeVodStreamURLResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vod_stream_urlwith_options_async(request, runtime)

    def describe_vs_certificate_detail_with_options(
        self,
        request: vs_20181212_models.DescribeVsCertificateDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsCertificateDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsCertificateDetailResponse().from_map(
            self.do_rpcrequest('DescribeVsCertificateDetail', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_certificate_detail_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsCertificateDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsCertificateDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsCertificateDetailResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsCertificateDetail', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_certificate_detail(
        self,
        request: vs_20181212_models.DescribeVsCertificateDetailRequest,
    ) -> vs_20181212_models.DescribeVsCertificateDetailResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_certificate_detail_with_options(request, runtime)

    async def describe_vs_certificate_detail_async(
        self,
        request: vs_20181212_models.DescribeVsCertificateDetailRequest,
    ) -> vs_20181212_models.DescribeVsCertificateDetailResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_certificate_detail_with_options_async(request, runtime)

    def describe_vs_certificate_list_with_options(
        self,
        request: vs_20181212_models.DescribeVsCertificateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsCertificateListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsCertificateListResponse().from_map(
            self.do_rpcrequest('DescribeVsCertificateList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_certificate_list_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsCertificateListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsCertificateListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsCertificateListResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsCertificateList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_certificate_list(
        self,
        request: vs_20181212_models.DescribeVsCertificateListRequest,
    ) -> vs_20181212_models.DescribeVsCertificateListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_certificate_list_with_options(request, runtime)

    async def describe_vs_certificate_list_async(
        self,
        request: vs_20181212_models.DescribeVsCertificateListRequest,
    ) -> vs_20181212_models.DescribeVsCertificateListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_certificate_list_with_options_async(request, runtime)

    def describe_vs_domain_bps_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainBpsDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainBpsDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainBpsDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainBpsData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_bps_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainBpsDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainBpsDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainBpsDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainBpsData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_bps_data(
        self,
        request: vs_20181212_models.DescribeVsDomainBpsDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainBpsDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_bps_data_with_options(request, runtime)

    async def describe_vs_domain_bps_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainBpsDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainBpsDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_bps_data_with_options_async(request, runtime)

    def describe_vs_domain_certificate_info_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainCertificateInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainCertificateInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainCertificateInfoResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainCertificateInfo', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_certificate_info_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainCertificateInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainCertificateInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainCertificateInfoResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainCertificateInfo', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_certificate_info(
        self,
        request: vs_20181212_models.DescribeVsDomainCertificateInfoRequest,
    ) -> vs_20181212_models.DescribeVsDomainCertificateInfoResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_certificate_info_with_options(request, runtime)

    async def describe_vs_domain_certificate_info_async(
        self,
        request: vs_20181212_models.DescribeVsDomainCertificateInfoRequest,
    ) -> vs_20181212_models.DescribeVsDomainCertificateInfoResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_certificate_info_with_options_async(request, runtime)

    def describe_vs_domain_configs_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainConfigsResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_configs_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainConfigsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainConfigsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainConfigsResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainConfigs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_configs(
        self,
        request: vs_20181212_models.DescribeVsDomainConfigsRequest,
    ) -> vs_20181212_models.DescribeVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_configs_with_options(request, runtime)

    async def describe_vs_domain_configs_async(
        self,
        request: vs_20181212_models.DescribeVsDomainConfigsRequest,
    ) -> vs_20181212_models.DescribeVsDomainConfigsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_configs_with_options_async(request, runtime)

    def describe_vs_domain_detail_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainDetailResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainDetail', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_detail_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainDetailResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainDetail', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_detail(
        self,
        request: vs_20181212_models.DescribeVsDomainDetailRequest,
    ) -> vs_20181212_models.DescribeVsDomainDetailResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_detail_with_options(request, runtime)

    async def describe_vs_domain_detail_async(
        self,
        request: vs_20181212_models.DescribeVsDomainDetailRequest,
    ) -> vs_20181212_models.DescribeVsDomainDetailResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_detail_with_options_async(request, runtime)

    def describe_vs_domain_pv_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainPvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainPvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainPvDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainPvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_pv_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainPvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainPvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainPvDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainPvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_pv_data(
        self,
        request: vs_20181212_models.DescribeVsDomainPvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainPvDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_pv_data_with_options(request, runtime)

    async def describe_vs_domain_pv_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainPvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainPvDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_pv_data_with_options_async(request, runtime)

    def describe_vs_domain_pv_uv_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainPvUvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainPvUvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainPvUvDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainPvUvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_pv_uv_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainPvUvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainPvUvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainPvUvDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainPvUvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_pv_uv_data(
        self,
        request: vs_20181212_models.DescribeVsDomainPvUvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainPvUvDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_pv_uv_data_with_options(request, runtime)

    async def describe_vs_domain_pv_uv_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainPvUvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainPvUvDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_pv_uv_data_with_options_async(request, runtime)

    def describe_vs_domain_record_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainRecordDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainRecordDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainRecordDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainRecordData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_record_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainRecordDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainRecordDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainRecordDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainRecordData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_record_data(
        self,
        request: vs_20181212_models.DescribeVsDomainRecordDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainRecordDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_record_data_with_options(request, runtime)

    async def describe_vs_domain_record_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainRecordDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainRecordDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_record_data_with_options_async(request, runtime)

    def describe_vs_domain_region_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainRegionDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainRegionDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainRegionDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainRegionData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_region_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainRegionDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainRegionDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainRegionDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainRegionData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_region_data(
        self,
        request: vs_20181212_models.DescribeVsDomainRegionDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainRegionDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_region_data_with_options(request, runtime)

    async def describe_vs_domain_region_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainRegionDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainRegionDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_region_data_with_options_async(request, runtime)

    def describe_vs_domain_req_bps_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainReqBpsDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainReqBpsDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainReqBpsDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainReqBpsData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_req_bps_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainReqBpsDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainReqBpsDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainReqBpsDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainReqBpsData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_req_bps_data(
        self,
        request: vs_20181212_models.DescribeVsDomainReqBpsDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainReqBpsDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_req_bps_data_with_options(request, runtime)

    async def describe_vs_domain_req_bps_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainReqBpsDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainReqBpsDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_req_bps_data_with_options_async(request, runtime)

    def describe_vs_domain_req_traffic_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainReqTrafficDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainReqTrafficDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainReqTrafficDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainReqTrafficData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_req_traffic_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainReqTrafficDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainReqTrafficDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainReqTrafficDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainReqTrafficData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_req_traffic_data(
        self,
        request: vs_20181212_models.DescribeVsDomainReqTrafficDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainReqTrafficDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_req_traffic_data_with_options(request, runtime)

    async def describe_vs_domain_req_traffic_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainReqTrafficDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainReqTrafficDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_req_traffic_data_with_options_async(request, runtime)

    def describe_vs_domain_snapshot_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainSnapshotDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainSnapshotDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainSnapshotDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainSnapshotData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_snapshot_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainSnapshotDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainSnapshotDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainSnapshotDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainSnapshotData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_snapshot_data(
        self,
        request: vs_20181212_models.DescribeVsDomainSnapshotDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainSnapshotDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_snapshot_data_with_options(request, runtime)

    async def describe_vs_domain_snapshot_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainSnapshotDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainSnapshotDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_snapshot_data_with_options_async(request, runtime)

    def describe_vs_domain_traffic_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainTrafficDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainTrafficDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainTrafficDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainTrafficData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_traffic_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainTrafficDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainTrafficDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainTrafficDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainTrafficData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_traffic_data(
        self,
        request: vs_20181212_models.DescribeVsDomainTrafficDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainTrafficDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_traffic_data_with_options(request, runtime)

    async def describe_vs_domain_traffic_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainTrafficDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainTrafficDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_traffic_data_with_options_async(request, runtime)

    def describe_vs_domain_uv_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsDomainUvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainUvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainUvDataResponse().from_map(
            self.do_rpcrequest('DescribeVsDomainUvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_domain_uv_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsDomainUvDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsDomainUvDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsDomainUvDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsDomainUvData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_domain_uv_data(
        self,
        request: vs_20181212_models.DescribeVsDomainUvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainUvDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_domain_uv_data_with_options(request, runtime)

    async def describe_vs_domain_uv_data_async(
        self,
        request: vs_20181212_models.DescribeVsDomainUvDataRequest,
    ) -> vs_20181212_models.DescribeVsDomainUvDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_domain_uv_data_with_options_async(request, runtime)

    def describe_vs_pull_stream_info_config_with_options(
        self,
        request: vs_20181212_models.DescribeVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsPullStreamInfoConfigResponse().from_map(
            self.do_rpcrequest('DescribeVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_pull_stream_info_config_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsPullStreamInfoConfigResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_pull_stream_info_config(
        self,
        request: vs_20181212_models.DescribeVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.DescribeVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_pull_stream_info_config_with_options(request, runtime)

    async def describe_vs_pull_stream_info_config_async(
        self,
        request: vs_20181212_models.DescribeVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.DescribeVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_pull_stream_info_config_with_options_async(request, runtime)

    def describe_vs_streams_notify_url_config_with_options(
        self,
        request: vs_20181212_models.DescribeVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse().from_map(
            self.do_rpcrequest('DescribeVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_streams_notify_url_config_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_streams_notify_url_config(
        self,
        request: vs_20181212_models.DescribeVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_streams_notify_url_config_with_options(request, runtime)

    async def describe_vs_streams_notify_url_config_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.DescribeVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_streams_notify_url_config_with_options_async(request, runtime)

    def describe_vs_streams_online_list_with_options(
        self,
        request: vs_20181212_models.DescribeVsStreamsOnlineListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsOnlineListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsOnlineListResponse().from_map(
            self.do_rpcrequest('DescribeVsStreamsOnlineList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_streams_online_list_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsOnlineListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsOnlineListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsOnlineListResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsStreamsOnlineList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_streams_online_list(
        self,
        request: vs_20181212_models.DescribeVsStreamsOnlineListRequest,
    ) -> vs_20181212_models.DescribeVsStreamsOnlineListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_streams_online_list_with_options(request, runtime)

    async def describe_vs_streams_online_list_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsOnlineListRequest,
    ) -> vs_20181212_models.DescribeVsStreamsOnlineListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_streams_online_list_with_options_async(request, runtime)

    def describe_vs_streams_publish_list_with_options(
        self,
        request: vs_20181212_models.DescribeVsStreamsPublishListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsPublishListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsPublishListResponse().from_map(
            self.do_rpcrequest('DescribeVsStreamsPublishList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_streams_publish_list_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsPublishListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsStreamsPublishListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsStreamsPublishListResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsStreamsPublishList', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_streams_publish_list(
        self,
        request: vs_20181212_models.DescribeVsStreamsPublishListRequest,
    ) -> vs_20181212_models.DescribeVsStreamsPublishListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_streams_publish_list_with_options(request, runtime)

    async def describe_vs_streams_publish_list_async(
        self,
        request: vs_20181212_models.DescribeVsStreamsPublishListRequest,
    ) -> vs_20181212_models.DescribeVsStreamsPublishListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_streams_publish_list_with_options_async(request, runtime)

    def describe_vs_top_domains_by_flow_with_options(
        self,
        request: vs_20181212_models.DescribeVsTopDomainsByFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsTopDomainsByFlowResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsTopDomainsByFlowResponse().from_map(
            self.do_rpcrequest('DescribeVsTopDomainsByFlow', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_top_domains_by_flow_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsTopDomainsByFlowRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsTopDomainsByFlowResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsTopDomainsByFlowResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsTopDomainsByFlow', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_top_domains_by_flow(
        self,
        request: vs_20181212_models.DescribeVsTopDomainsByFlowRequest,
    ) -> vs_20181212_models.DescribeVsTopDomainsByFlowResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_top_domains_by_flow_with_options(request, runtime)

    async def describe_vs_top_domains_by_flow_async(
        self,
        request: vs_20181212_models.DescribeVsTopDomainsByFlowRequest,
    ) -> vs_20181212_models.DescribeVsTopDomainsByFlowResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_top_domains_by_flow_with_options_async(request, runtime)

    def describe_vs_up_peak_publish_stream_data_with_options(
        self,
        request: vs_20181212_models.DescribeVsUpPeakPublishStreamDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse().from_map(
            self.do_rpcrequest('DescribeVsUpPeakPublishStreamData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_up_peak_publish_stream_data_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsUpPeakPublishStreamDataRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsUpPeakPublishStreamData', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_up_peak_publish_stream_data(
        self,
        request: vs_20181212_models.DescribeVsUpPeakPublishStreamDataRequest,
    ) -> vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_up_peak_publish_stream_data_with_options(request, runtime)

    async def describe_vs_up_peak_publish_stream_data_async(
        self,
        request: vs_20181212_models.DescribeVsUpPeakPublishStreamDataRequest,
    ) -> vs_20181212_models.DescribeVsUpPeakPublishStreamDataResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_up_peak_publish_stream_data_with_options_async(request, runtime)

    def describe_vs_user_resource_package_with_options(
        self,
        request: vs_20181212_models.DescribeVsUserResourcePackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsUserResourcePackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsUserResourcePackageResponse().from_map(
            self.do_rpcrequest('DescribeVsUserResourcePackage', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_vs_user_resource_package_with_options_async(
        self,
        request: vs_20181212_models.DescribeVsUserResourcePackageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.DescribeVsUserResourcePackageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.DescribeVsUserResourcePackageResponse().from_map(
            await self.do_rpcrequest_async('DescribeVsUserResourcePackage', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_vs_user_resource_package(
        self,
        request: vs_20181212_models.DescribeVsUserResourcePackageRequest,
    ) -> vs_20181212_models.DescribeVsUserResourcePackageResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_vs_user_resource_package_with_options(request, runtime)

    async def describe_vs_user_resource_package_async(
        self,
        request: vs_20181212_models.DescribeVsUserResourcePackageRequest,
    ) -> vs_20181212_models.DescribeVsUserResourcePackageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_vs_user_resource_package_with_options_async(request, runtime)

    def forbid_vs_stream_with_options(
        self,
        request: vs_20181212_models.ForbidVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ForbidVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ForbidVsStreamResponse().from_map(
            self.do_rpcrequest('ForbidVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def forbid_vs_stream_with_options_async(
        self,
        request: vs_20181212_models.ForbidVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ForbidVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ForbidVsStreamResponse().from_map(
            await self.do_rpcrequest_async('ForbidVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def forbid_vs_stream(
        self,
        request: vs_20181212_models.ForbidVsStreamRequest,
    ) -> vs_20181212_models.ForbidVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.forbid_vs_stream_with_options(request, runtime)

    async def forbid_vs_stream_async(
        self,
        request: vs_20181212_models.ForbidVsStreamRequest,
    ) -> vs_20181212_models.ForbidVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.forbid_vs_stream_with_options_async(request, runtime)

    def goto_preset_with_options(
        self,
        request: vs_20181212_models.GotoPresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.GotoPresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.GotoPresetResponse().from_map(
            self.do_rpcrequest('GotoPreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def goto_preset_with_options_async(
        self,
        request: vs_20181212_models.GotoPresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.GotoPresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.GotoPresetResponse().from_map(
            await self.do_rpcrequest_async('GotoPreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def goto_preset(
        self,
        request: vs_20181212_models.GotoPresetRequest,
    ) -> vs_20181212_models.GotoPresetResponse:
        runtime = util_models.RuntimeOptions()
        return self.goto_preset_with_options(request, runtime)

    async def goto_preset_async(
        self,
        request: vs_20181212_models.GotoPresetRequest,
    ) -> vs_20181212_models.GotoPresetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.goto_preset_with_options_async(request, runtime)

    def modify_device_with_options(
        self,
        request: vs_20181212_models.ModifyDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceResponse().from_map(
            self.do_rpcrequest('ModifyDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_device_with_options_async(
        self,
        request: vs_20181212_models.ModifyDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceResponse().from_map(
            await self.do_rpcrequest_async('ModifyDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_device(
        self,
        request: vs_20181212_models.ModifyDeviceRequest,
    ) -> vs_20181212_models.ModifyDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_device_with_options(request, runtime)

    async def modify_device_async(
        self,
        request: vs_20181212_models.ModifyDeviceRequest,
    ) -> vs_20181212_models.ModifyDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_device_with_options_async(request, runtime)

    def modify_device_alarm_with_options(
        self,
        request: vs_20181212_models.ModifyDeviceAlarmRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceAlarmResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceAlarmResponse().from_map(
            self.do_rpcrequest('ModifyDeviceAlarm', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_device_alarm_with_options_async(
        self,
        request: vs_20181212_models.ModifyDeviceAlarmRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceAlarmResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceAlarmResponse().from_map(
            await self.do_rpcrequest_async('ModifyDeviceAlarm', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_device_alarm(
        self,
        request: vs_20181212_models.ModifyDeviceAlarmRequest,
    ) -> vs_20181212_models.ModifyDeviceAlarmResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_device_alarm_with_options(request, runtime)

    async def modify_device_alarm_async(
        self,
        request: vs_20181212_models.ModifyDeviceAlarmRequest,
    ) -> vs_20181212_models.ModifyDeviceAlarmResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_device_alarm_with_options_async(request, runtime)

    def modify_device_capture_with_options(
        self,
        request: vs_20181212_models.ModifyDeviceCaptureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceCaptureResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceCaptureResponse().from_map(
            self.do_rpcrequest('ModifyDeviceCapture', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_device_capture_with_options_async(
        self,
        request: vs_20181212_models.ModifyDeviceCaptureRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceCaptureResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceCaptureResponse().from_map(
            await self.do_rpcrequest_async('ModifyDeviceCapture', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_device_capture(
        self,
        request: vs_20181212_models.ModifyDeviceCaptureRequest,
    ) -> vs_20181212_models.ModifyDeviceCaptureResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_device_capture_with_options(request, runtime)

    async def modify_device_capture_async(
        self,
        request: vs_20181212_models.ModifyDeviceCaptureRequest,
    ) -> vs_20181212_models.ModifyDeviceCaptureResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_device_capture_with_options_async(request, runtime)

    def modify_device_channels_with_options(
        self,
        request: vs_20181212_models.ModifyDeviceChannelsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceChannelsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceChannelsResponse().from_map(
            self.do_rpcrequest('ModifyDeviceChannels', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_device_channels_with_options_async(
        self,
        request: vs_20181212_models.ModifyDeviceChannelsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDeviceChannelsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDeviceChannelsResponse().from_map(
            await self.do_rpcrequest_async('ModifyDeviceChannels', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_device_channels(
        self,
        request: vs_20181212_models.ModifyDeviceChannelsRequest,
    ) -> vs_20181212_models.ModifyDeviceChannelsResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_device_channels_with_options(request, runtime)

    async def modify_device_channels_async(
        self,
        request: vs_20181212_models.ModifyDeviceChannelsRequest,
    ) -> vs_20181212_models.ModifyDeviceChannelsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_device_channels_with_options_async(request, runtime)

    def modify_directory_with_options(
        self,
        request: vs_20181212_models.ModifyDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDirectoryResponse().from_map(
            self.do_rpcrequest('ModifyDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_directory_with_options_async(
        self,
        request: vs_20181212_models.ModifyDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyDirectoryResponse().from_map(
            await self.do_rpcrequest_async('ModifyDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_directory(
        self,
        request: vs_20181212_models.ModifyDirectoryRequest,
    ) -> vs_20181212_models.ModifyDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_directory_with_options(request, runtime)

    async def modify_directory_async(
        self,
        request: vs_20181212_models.ModifyDirectoryRequest,
    ) -> vs_20181212_models.ModifyDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_directory_with_options_async(request, runtime)

    def modify_group_with_options(
        self,
        request: vs_20181212_models.ModifyGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyGroupResponse().from_map(
            self.do_rpcrequest('ModifyGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_group_with_options_async(
        self,
        request: vs_20181212_models.ModifyGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyGroupResponse().from_map(
            await self.do_rpcrequest_async('ModifyGroup', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_group(
        self,
        request: vs_20181212_models.ModifyGroupRequest,
    ) -> vs_20181212_models.ModifyGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_group_with_options(request, runtime)

    async def modify_group_async(
        self,
        request: vs_20181212_models.ModifyGroupRequest,
    ) -> vs_20181212_models.ModifyGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_group_with_options_async(request, runtime)

    def modify_parent_platform_with_options(
        self,
        request: vs_20181212_models.ModifyParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyParentPlatformResponse().from_map(
            self.do_rpcrequest('ModifyParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_parent_platform_with_options_async(
        self,
        request: vs_20181212_models.ModifyParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyParentPlatformResponse().from_map(
            await self.do_rpcrequest_async('ModifyParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_parent_platform(
        self,
        request: vs_20181212_models.ModifyParentPlatformRequest,
    ) -> vs_20181212_models.ModifyParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_parent_platform_with_options(request, runtime)

    async def modify_parent_platform_async(
        self,
        request: vs_20181212_models.ModifyParentPlatformRequest,
    ) -> vs_20181212_models.ModifyParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_parent_platform_with_options_async(request, runtime)

    def modify_template_with_options(
        self,
        request: vs_20181212_models.ModifyTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyTemplateResponse().from_map(
            self.do_rpcrequest('ModifyTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_template_with_options_async(
        self,
        request: vs_20181212_models.ModifyTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ModifyTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ModifyTemplateResponse().from_map(
            await self.do_rpcrequest_async('ModifyTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_template(
        self,
        request: vs_20181212_models.ModifyTemplateRequest,
    ) -> vs_20181212_models.ModifyTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_template_with_options(request, runtime)

    async def modify_template_async(
        self,
        request: vs_20181212_models.ModifyTemplateRequest,
    ) -> vs_20181212_models.ModifyTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_template_with_options_async(request, runtime)

    def open_vs_service_with_options(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.OpenVsServiceResponse:
        req = open_api_models.OpenApiRequest()
        return vs_20181212_models.OpenVsServiceResponse().from_map(
            self.do_rpcrequest('OpenVsService', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def open_vs_service_with_options_async(
        self,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.OpenVsServiceResponse:
        req = open_api_models.OpenApiRequest()
        return vs_20181212_models.OpenVsServiceResponse().from_map(
            await self.do_rpcrequest_async('OpenVsService', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def open_vs_service(self) -> vs_20181212_models.OpenVsServiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.open_vs_service_with_options(runtime)

    async def open_vs_service_async(self) -> vs_20181212_models.OpenVsServiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.open_vs_service_with_options_async(runtime)

    def resume_vs_stream_with_options(
        self,
        request: vs_20181212_models.ResumeVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ResumeVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ResumeVsStreamResponse().from_map(
            self.do_rpcrequest('ResumeVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def resume_vs_stream_with_options_async(
        self,
        request: vs_20181212_models.ResumeVsStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.ResumeVsStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.ResumeVsStreamResponse().from_map(
            await self.do_rpcrequest_async('ResumeVsStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def resume_vs_stream(
        self,
        request: vs_20181212_models.ResumeVsStreamRequest,
    ) -> vs_20181212_models.ResumeVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.resume_vs_stream_with_options(request, runtime)

    async def resume_vs_stream_async(
        self,
        request: vs_20181212_models.ResumeVsStreamRequest,
    ) -> vs_20181212_models.ResumeVsStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.resume_vs_stream_with_options_async(request, runtime)

    def set_preset_with_options(
        self,
        request: vs_20181212_models.SetPresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetPresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetPresetResponse().from_map(
            self.do_rpcrequest('SetPreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def set_preset_with_options_async(
        self,
        request: vs_20181212_models.SetPresetRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetPresetResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetPresetResponse().from_map(
            await self.do_rpcrequest_async('SetPreset', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def set_preset(
        self,
        request: vs_20181212_models.SetPresetRequest,
    ) -> vs_20181212_models.SetPresetResponse:
        runtime = util_models.RuntimeOptions()
        return self.set_preset_with_options(request, runtime)

    async def set_preset_async(
        self,
        request: vs_20181212_models.SetPresetRequest,
    ) -> vs_20181212_models.SetPresetResponse:
        runtime = util_models.RuntimeOptions()
        return await self.set_preset_with_options_async(request, runtime)

    def set_vs_domain_certificate_with_options(
        self,
        request: vs_20181212_models.SetVsDomainCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetVsDomainCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetVsDomainCertificateResponse().from_map(
            self.do_rpcrequest('SetVsDomainCertificate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def set_vs_domain_certificate_with_options_async(
        self,
        request: vs_20181212_models.SetVsDomainCertificateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetVsDomainCertificateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetVsDomainCertificateResponse().from_map(
            await self.do_rpcrequest_async('SetVsDomainCertificate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def set_vs_domain_certificate(
        self,
        request: vs_20181212_models.SetVsDomainCertificateRequest,
    ) -> vs_20181212_models.SetVsDomainCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return self.set_vs_domain_certificate_with_options(request, runtime)

    async def set_vs_domain_certificate_async(
        self,
        request: vs_20181212_models.SetVsDomainCertificateRequest,
    ) -> vs_20181212_models.SetVsDomainCertificateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.set_vs_domain_certificate_with_options_async(request, runtime)

    def set_vs_streams_notify_url_config_with_options(
        self,
        request: vs_20181212_models.SetVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse().from_map(
            self.do_rpcrequest('SetVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def set_vs_streams_notify_url_config_with_options_async(
        self,
        request: vs_20181212_models.SetVsStreamsNotifyUrlConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse().from_map(
            await self.do_rpcrequest_async('SetVsStreamsNotifyUrlConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def set_vs_streams_notify_url_config(
        self,
        request: vs_20181212_models.SetVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.set_vs_streams_notify_url_config_with_options(request, runtime)

    async def set_vs_streams_notify_url_config_async(
        self,
        request: vs_20181212_models.SetVsStreamsNotifyUrlConfigRequest,
    ) -> vs_20181212_models.SetVsStreamsNotifyUrlConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.set_vs_streams_notify_url_config_with_options_async(request, runtime)

    def start_device_with_options(
        self,
        request: vs_20181212_models.StartDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartDeviceResponse().from_map(
            self.do_rpcrequest('StartDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def start_device_with_options_async(
        self,
        request: vs_20181212_models.StartDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartDeviceResponse().from_map(
            await self.do_rpcrequest_async('StartDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def start_device(
        self,
        request: vs_20181212_models.StartDeviceRequest,
    ) -> vs_20181212_models.StartDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_device_with_options(request, runtime)

    async def start_device_async(
        self,
        request: vs_20181212_models.StartDeviceRequest,
    ) -> vs_20181212_models.StartDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_device_with_options_async(request, runtime)

    def start_parent_platform_with_options(
        self,
        request: vs_20181212_models.StartParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartParentPlatformResponse().from_map(
            self.do_rpcrequest('StartParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def start_parent_platform_with_options_async(
        self,
        request: vs_20181212_models.StartParentPlatformRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartParentPlatformResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartParentPlatformResponse().from_map(
            await self.do_rpcrequest_async('StartParentPlatform', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def start_parent_platform(
        self,
        request: vs_20181212_models.StartParentPlatformRequest,
    ) -> vs_20181212_models.StartParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_parent_platform_with_options(request, runtime)

    async def start_parent_platform_async(
        self,
        request: vs_20181212_models.StartParentPlatformRequest,
    ) -> vs_20181212_models.StartParentPlatformResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_parent_platform_with_options_async(request, runtime)

    def start_record_stream_with_options(
        self,
        request: vs_20181212_models.StartRecordStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartRecordStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartRecordStreamResponse().from_map(
            self.do_rpcrequest('StartRecordStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def start_record_stream_with_options_async(
        self,
        request: vs_20181212_models.StartRecordStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartRecordStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartRecordStreamResponse().from_map(
            await self.do_rpcrequest_async('StartRecordStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def start_record_stream(
        self,
        request: vs_20181212_models.StartRecordStreamRequest,
    ) -> vs_20181212_models.StartRecordStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_record_stream_with_options(request, runtime)

    async def start_record_stream_async(
        self,
        request: vs_20181212_models.StartRecordStreamRequest,
    ) -> vs_20181212_models.StartRecordStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_record_stream_with_options_async(request, runtime)

    def start_stream_with_options(
        self,
        request: vs_20181212_models.StartStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartStreamResponse().from_map(
            self.do_rpcrequest('StartStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def start_stream_with_options_async(
        self,
        request: vs_20181212_models.StartStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartStreamResponse().from_map(
            await self.do_rpcrequest_async('StartStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def start_stream(
        self,
        request: vs_20181212_models.StartStreamRequest,
    ) -> vs_20181212_models.StartStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_stream_with_options(request, runtime)

    async def start_stream_async(
        self,
        request: vs_20181212_models.StartStreamRequest,
    ) -> vs_20181212_models.StartStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_stream_with_options_async(request, runtime)

    def start_transfer_stream_with_options(
        self,
        request: vs_20181212_models.StartTransferStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartTransferStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartTransferStreamResponse().from_map(
            self.do_rpcrequest('StartTransferStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def start_transfer_stream_with_options_async(
        self,
        request: vs_20181212_models.StartTransferStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StartTransferStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StartTransferStreamResponse().from_map(
            await self.do_rpcrequest_async('StartTransferStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def start_transfer_stream(
        self,
        request: vs_20181212_models.StartTransferStreamRequest,
    ) -> vs_20181212_models.StartTransferStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.start_transfer_stream_with_options(request, runtime)

    async def start_transfer_stream_async(
        self,
        request: vs_20181212_models.StartTransferStreamRequest,
    ) -> vs_20181212_models.StartTransferStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.start_transfer_stream_with_options_async(request, runtime)

    def stop_adjust_with_options(
        self,
        request: vs_20181212_models.StopAdjustRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopAdjustResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopAdjustResponse().from_map(
            self.do_rpcrequest('StopAdjust', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_adjust_with_options_async(
        self,
        request: vs_20181212_models.StopAdjustRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopAdjustResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopAdjustResponse().from_map(
            await self.do_rpcrequest_async('StopAdjust', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_adjust(
        self,
        request: vs_20181212_models.StopAdjustRequest,
    ) -> vs_20181212_models.StopAdjustResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_adjust_with_options(request, runtime)

    async def stop_adjust_async(
        self,
        request: vs_20181212_models.StopAdjustRequest,
    ) -> vs_20181212_models.StopAdjustResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_adjust_with_options_async(request, runtime)

    def stop_device_with_options(
        self,
        request: vs_20181212_models.StopDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopDeviceResponse().from_map(
            self.do_rpcrequest('StopDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_device_with_options_async(
        self,
        request: vs_20181212_models.StopDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopDeviceResponse().from_map(
            await self.do_rpcrequest_async('StopDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_device(
        self,
        request: vs_20181212_models.StopDeviceRequest,
    ) -> vs_20181212_models.StopDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_device_with_options(request, runtime)

    async def stop_device_async(
        self,
        request: vs_20181212_models.StopDeviceRequest,
    ) -> vs_20181212_models.StopDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_device_with_options_async(request, runtime)

    def stop_move_with_options(
        self,
        request: vs_20181212_models.StopMoveRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopMoveResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopMoveResponse().from_map(
            self.do_rpcrequest('StopMove', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_move_with_options_async(
        self,
        request: vs_20181212_models.StopMoveRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopMoveResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopMoveResponse().from_map(
            await self.do_rpcrequest_async('StopMove', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_move(
        self,
        request: vs_20181212_models.StopMoveRequest,
    ) -> vs_20181212_models.StopMoveResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_move_with_options(request, runtime)

    async def stop_move_async(
        self,
        request: vs_20181212_models.StopMoveRequest,
    ) -> vs_20181212_models.StopMoveResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_move_with_options_async(request, runtime)

    def stop_record_stream_with_options(
        self,
        request: vs_20181212_models.StopRecordStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopRecordStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopRecordStreamResponse().from_map(
            self.do_rpcrequest('StopRecordStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_record_stream_with_options_async(
        self,
        request: vs_20181212_models.StopRecordStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopRecordStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopRecordStreamResponse().from_map(
            await self.do_rpcrequest_async('StopRecordStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_record_stream(
        self,
        request: vs_20181212_models.StopRecordStreamRequest,
    ) -> vs_20181212_models.StopRecordStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_record_stream_with_options(request, runtime)

    async def stop_record_stream_async(
        self,
        request: vs_20181212_models.StopRecordStreamRequest,
    ) -> vs_20181212_models.StopRecordStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_record_stream_with_options_async(request, runtime)

    def stop_stream_with_options(
        self,
        request: vs_20181212_models.StopStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopStreamResponse().from_map(
            self.do_rpcrequest('StopStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_stream_with_options_async(
        self,
        request: vs_20181212_models.StopStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopStreamResponse().from_map(
            await self.do_rpcrequest_async('StopStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_stream(
        self,
        request: vs_20181212_models.StopStreamRequest,
    ) -> vs_20181212_models.StopStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_stream_with_options(request, runtime)

    async def stop_stream_async(
        self,
        request: vs_20181212_models.StopStreamRequest,
    ) -> vs_20181212_models.StopStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_stream_with_options_async(request, runtime)

    def stop_transfer_stream_with_options(
        self,
        request: vs_20181212_models.StopTransferStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopTransferStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopTransferStreamResponse().from_map(
            self.do_rpcrequest('StopTransferStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def stop_transfer_stream_with_options_async(
        self,
        request: vs_20181212_models.StopTransferStreamRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.StopTransferStreamResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.StopTransferStreamResponse().from_map(
            await self.do_rpcrequest_async('StopTransferStream', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def stop_transfer_stream(
        self,
        request: vs_20181212_models.StopTransferStreamRequest,
    ) -> vs_20181212_models.StopTransferStreamResponse:
        runtime = util_models.RuntimeOptions()
        return self.stop_transfer_stream_with_options(request, runtime)

    async def stop_transfer_stream_async(
        self,
        request: vs_20181212_models.StopTransferStreamRequest,
    ) -> vs_20181212_models.StopTransferStreamResponse:
        runtime = util_models.RuntimeOptions()
        return await self.stop_transfer_stream_with_options_async(request, runtime)

    def sync_catalogs_with_options(
        self,
        request: vs_20181212_models.SyncCatalogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SyncCatalogsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SyncCatalogsResponse().from_map(
            self.do_rpcrequest('SyncCatalogs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def sync_catalogs_with_options_async(
        self,
        request: vs_20181212_models.SyncCatalogsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.SyncCatalogsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.SyncCatalogsResponse().from_map(
            await self.do_rpcrequest_async('SyncCatalogs', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def sync_catalogs(
        self,
        request: vs_20181212_models.SyncCatalogsRequest,
    ) -> vs_20181212_models.SyncCatalogsResponse:
        runtime = util_models.RuntimeOptions()
        return self.sync_catalogs_with_options(request, runtime)

    async def sync_catalogs_async(
        self,
        request: vs_20181212_models.SyncCatalogsRequest,
    ) -> vs_20181212_models.SyncCatalogsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.sync_catalogs_with_options_async(request, runtime)

    def unbind_directory_with_options(
        self,
        request: vs_20181212_models.UnbindDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindDirectoryResponse().from_map(
            self.do_rpcrequest('UnbindDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unbind_directory_with_options_async(
        self,
        request: vs_20181212_models.UnbindDirectoryRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindDirectoryResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindDirectoryResponse().from_map(
            await self.do_rpcrequest_async('UnbindDirectory', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unbind_directory(
        self,
        request: vs_20181212_models.UnbindDirectoryRequest,
    ) -> vs_20181212_models.UnbindDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return self.unbind_directory_with_options(request, runtime)

    async def unbind_directory_async(
        self,
        request: vs_20181212_models.UnbindDirectoryRequest,
    ) -> vs_20181212_models.UnbindDirectoryResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unbind_directory_with_options_async(request, runtime)

    def unbind_parent_platform_device_with_options(
        self,
        request: vs_20181212_models.UnbindParentPlatformDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindParentPlatformDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindParentPlatformDeviceResponse().from_map(
            self.do_rpcrequest('UnbindParentPlatformDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unbind_parent_platform_device_with_options_async(
        self,
        request: vs_20181212_models.UnbindParentPlatformDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindParentPlatformDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindParentPlatformDeviceResponse().from_map(
            await self.do_rpcrequest_async('UnbindParentPlatformDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unbind_parent_platform_device(
        self,
        request: vs_20181212_models.UnbindParentPlatformDeviceRequest,
    ) -> vs_20181212_models.UnbindParentPlatformDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.unbind_parent_platform_device_with_options(request, runtime)

    async def unbind_parent_platform_device_async(
        self,
        request: vs_20181212_models.UnbindParentPlatformDeviceRequest,
    ) -> vs_20181212_models.UnbindParentPlatformDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unbind_parent_platform_device_with_options_async(request, runtime)

    def unbind_purchased_device_with_options(
        self,
        request: vs_20181212_models.UnbindPurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindPurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindPurchasedDeviceResponse().from_map(
            self.do_rpcrequest('UnbindPurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unbind_purchased_device_with_options_async(
        self,
        request: vs_20181212_models.UnbindPurchasedDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindPurchasedDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindPurchasedDeviceResponse().from_map(
            await self.do_rpcrequest_async('UnbindPurchasedDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unbind_purchased_device(
        self,
        request: vs_20181212_models.UnbindPurchasedDeviceRequest,
    ) -> vs_20181212_models.UnbindPurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.unbind_purchased_device_with_options(request, runtime)

    async def unbind_purchased_device_async(
        self,
        request: vs_20181212_models.UnbindPurchasedDeviceRequest,
    ) -> vs_20181212_models.UnbindPurchasedDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unbind_purchased_device_with_options_async(request, runtime)

    def unbind_template_with_options(
        self,
        request: vs_20181212_models.UnbindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindTemplateResponse().from_map(
            self.do_rpcrequest('UnbindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unbind_template_with_options_async(
        self,
        request: vs_20181212_models.UnbindTemplateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnbindTemplateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnbindTemplateResponse().from_map(
            await self.do_rpcrequest_async('UnbindTemplate', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unbind_template(
        self,
        request: vs_20181212_models.UnbindTemplateRequest,
    ) -> vs_20181212_models.UnbindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return self.unbind_template_with_options(request, runtime)

    async def unbind_template_async(
        self,
        request: vs_20181212_models.UnbindTemplateRequest,
    ) -> vs_20181212_models.UnbindTemplateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unbind_template_with_options_async(request, runtime)

    def unlock_device_with_options(
        self,
        request: vs_20181212_models.UnlockDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnlockDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnlockDeviceResponse().from_map(
            self.do_rpcrequest('UnlockDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unlock_device_with_options_async(
        self,
        request: vs_20181212_models.UnlockDeviceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UnlockDeviceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UnlockDeviceResponse().from_map(
            await self.do_rpcrequest_async('UnlockDevice', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unlock_device(
        self,
        request: vs_20181212_models.UnlockDeviceRequest,
    ) -> vs_20181212_models.UnlockDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return self.unlock_device_with_options(request, runtime)

    async def unlock_device_async(
        self,
        request: vs_20181212_models.UnlockDeviceRequest,
    ) -> vs_20181212_models.UnlockDeviceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unlock_device_with_options_async(request, runtime)

    def update_vs_pull_stream_info_config_with_options(
        self,
        request: vs_20181212_models.UpdateVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UpdateVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UpdateVsPullStreamInfoConfigResponse().from_map(
            self.do_rpcrequest('UpdateVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def update_vs_pull_stream_info_config_with_options_async(
        self,
        request: vs_20181212_models.UpdateVsPullStreamInfoConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> vs_20181212_models.UpdateVsPullStreamInfoConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return vs_20181212_models.UpdateVsPullStreamInfoConfigResponse().from_map(
            await self.do_rpcrequest_async('UpdateVsPullStreamInfoConfig', '2018-12-12', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def update_vs_pull_stream_info_config(
        self,
        request: vs_20181212_models.UpdateVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.UpdateVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.update_vs_pull_stream_info_config_with_options(request, runtime)

    async def update_vs_pull_stream_info_config_async(
        self,
        request: vs_20181212_models.UpdateVsPullStreamInfoConfigRequest,
    ) -> vs_20181212_models.UpdateVsPullStreamInfoConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.update_vs_pull_stream_info_config_with_options_async(request, runtime)
