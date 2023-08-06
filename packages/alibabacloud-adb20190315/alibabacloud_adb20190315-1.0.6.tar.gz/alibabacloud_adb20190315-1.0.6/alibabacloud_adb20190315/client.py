# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_adb20190315 import models as adb_20190315_models
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
        self._endpoint_map = {
            'cn-qingdao': 'adb.aliyuncs.com',
            'cn-beijing': 'adb.aliyuncs.com',
            'cn-hangzhou': 'adb.aliyuncs.com',
            'cn-shanghai': 'adb.aliyuncs.com',
            'cn-shenzhen': 'adb.aliyuncs.com',
            'cn-hongkong': 'adb.aliyuncs.com',
            'ap-southeast-1': 'adb.aliyuncs.com',
            'us-west-1': 'adb.aliyuncs.com',
            'us-east-1': 'adb.aliyuncs.com',
            'cn-hangzhou-finance': 'adb.aliyuncs.com',
            'cn-north-2-gov-1': 'adb.aliyuncs.com',
            'ap-northeast-2-pop': 'adb.ap-northeast-1.aliyuncs.com',
            'cn-beijing-finance-1': 'adb.aliyuncs.com',
            'cn-beijing-finance-pop': 'adb.aliyuncs.com',
            'cn-beijing-gov-1': 'adb.aliyuncs.com',
            'cn-beijing-nu16-b01': 'adb.aliyuncs.com',
            'cn-edge-1': 'adb.aliyuncs.com',
            'cn-fujian': 'adb.aliyuncs.com',
            'cn-haidian-cm12-c01': 'adb.aliyuncs.com',
            'cn-hangzhou-bj-b01': 'adb.aliyuncs.com',
            'cn-hangzhou-internal-prod-1': 'adb.aliyuncs.com',
            'cn-hangzhou-internal-test-1': 'adb.aliyuncs.com',
            'cn-hangzhou-internal-test-2': 'adb.aliyuncs.com',
            'cn-hangzhou-internal-test-3': 'adb.aliyuncs.com',
            'cn-hangzhou-test-306': 'adb.aliyuncs.com',
            'cn-hongkong-finance-pop': 'adb.aliyuncs.com',
            'cn-qingdao-nebula': 'adb.aliyuncs.com',
            'cn-shanghai-et15-b01': 'adb.aliyuncs.com',
            'cn-shanghai-et2-b01': 'adb.aliyuncs.com',
            'cn-shanghai-finance-1': 'adb.aliyuncs.com',
            'cn-shanghai-inner': 'adb.aliyuncs.com',
            'cn-shanghai-internal-test-1': 'adb.aliyuncs.com',
            'cn-shenzhen-finance-1': 'adb.aliyuncs.com',
            'cn-shenzhen-inner': 'adb.aliyuncs.com',
            'cn-shenzhen-st4-d01': 'adb.aliyuncs.com',
            'cn-shenzhen-su18-b01': 'adb.aliyuncs.com',
            'cn-wuhan': 'adb.aliyuncs.com',
            'cn-yushanfang': 'adb.aliyuncs.com',
            'cn-zhangbei-na61-b01': 'adb.aliyuncs.com',
            'cn-zhangjiakou-na62-a01': 'adb.aliyuncs.com',
            'cn-zhengzhou-nebula-1': 'adb.aliyuncs.com',
            'eu-west-1-oxs': 'adb.ap-northeast-1.aliyuncs.com',
            'me-east-1': 'adb.ap-northeast-1.aliyuncs.com',
            'rus-west-1-pop': 'adb.ap-northeast-1.aliyuncs.com'
        }
        self.check_config(config)
        self._endpoint = self.get_endpoint('adb', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

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

    def modify_cluster_connection_string_with_options(
        self,
        request: adb_20190315_models.ModifyClusterConnectionStringRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyClusterConnectionStringResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyClusterConnectionStringResponse().from_map(
            self.do_rpcrequest('ModifyClusterConnectionString', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_cluster_connection_string_with_options_async(
        self,
        request: adb_20190315_models.ModifyClusterConnectionStringRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyClusterConnectionStringResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyClusterConnectionStringResponse().from_map(
            await self.do_rpcrequest_async('ModifyClusterConnectionString', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_cluster_connection_string(
        self,
        request: adb_20190315_models.ModifyClusterConnectionStringRequest,
    ) -> adb_20190315_models.ModifyClusterConnectionStringResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_cluster_connection_string_with_options(request, runtime)

    async def modify_cluster_connection_string_async(
        self,
        request: adb_20190315_models.ModifyClusterConnectionStringRequest,
    ) -> adb_20190315_models.ModifyClusterConnectionStringResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_cluster_connection_string_with_options_async(request, runtime)

    def untag_resources_with_options(
        self,
        request: adb_20190315_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.UntagResourcesResponse().from_map(
            self.do_rpcrequest('UntagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def untag_resources_with_options_async(
        self,
        request: adb_20190315_models.UntagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.UntagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.UntagResourcesResponse().from_map(
            await self.do_rpcrequest_async('UntagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def untag_resources(
        self,
        request: adb_20190315_models.UntagResourcesRequest,
    ) -> adb_20190315_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.untag_resources_with_options(request, runtime)

    async def untag_resources_async(
        self,
        request: adb_20190315_models.UntagResourcesRequest,
    ) -> adb_20190315_models.UntagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.untag_resources_with_options_async(request, runtime)

    def modify_account_description_with_options(
        self,
        request: adb_20190315_models.ModifyAccountDescriptionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAccountDescriptionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAccountDescriptionResponse().from_map(
            self.do_rpcrequest('ModifyAccountDescription', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_account_description_with_options_async(
        self,
        request: adb_20190315_models.ModifyAccountDescriptionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAccountDescriptionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAccountDescriptionResponse().from_map(
            await self.do_rpcrequest_async('ModifyAccountDescription', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_account_description(
        self,
        request: adb_20190315_models.ModifyAccountDescriptionRequest,
    ) -> adb_20190315_models.ModifyAccountDescriptionResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_account_description_with_options(request, runtime)

    async def modify_account_description_async(
        self,
        request: adb_20190315_models.ModifyAccountDescriptionRequest,
    ) -> adb_20190315_models.ModifyAccountDescriptionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_account_description_with_options_async(request, runtime)

    def describe_elastic_daily_plan_with_options(
        self,
        request: adb_20190315_models.DescribeElasticDailyPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeElasticDailyPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeElasticDailyPlanResponse().from_map(
            self.do_rpcrequest('DescribeElasticDailyPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_elastic_daily_plan_with_options_async(
        self,
        request: adb_20190315_models.DescribeElasticDailyPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeElasticDailyPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeElasticDailyPlanResponse().from_map(
            await self.do_rpcrequest_async('DescribeElasticDailyPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_elastic_daily_plan(
        self,
        request: adb_20190315_models.DescribeElasticDailyPlanRequest,
    ) -> adb_20190315_models.DescribeElasticDailyPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_elastic_daily_plan_with_options(request, runtime)

    async def describe_elastic_daily_plan_async(
        self,
        request: adb_20190315_models.DescribeElasticDailyPlanRequest,
    ) -> adb_20190315_models.DescribeElasticDailyPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_elastic_daily_plan_with_options_async(request, runtime)

    def modify_auto_renew_attribute_with_options(
        self,
        request: adb_20190315_models.ModifyAutoRenewAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAutoRenewAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAutoRenewAttributeResponse().from_map(
            self.do_rpcrequest('ModifyAutoRenewAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_auto_renew_attribute_with_options_async(
        self,
        request: adb_20190315_models.ModifyAutoRenewAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAutoRenewAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAutoRenewAttributeResponse().from_map(
            await self.do_rpcrequest_async('ModifyAutoRenewAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_auto_renew_attribute(
        self,
        request: adb_20190315_models.ModifyAutoRenewAttributeRequest,
    ) -> adb_20190315_models.ModifyAutoRenewAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_auto_renew_attribute_with_options(request, runtime)

    async def modify_auto_renew_attribute_async(
        self,
        request: adb_20190315_models.ModifyAutoRenewAttributeRequest,
    ) -> adb_20190315_models.ModifyAutoRenewAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_auto_renew_attribute_with_options_async(request, runtime)

    def delete_dbcluster_with_options(
        self,
        request: adb_20190315_models.DeleteDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteDBClusterResponse().from_map(
            self.do_rpcrequest('DeleteDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_dbcluster_with_options_async(
        self,
        request: adb_20190315_models.DeleteDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteDBClusterResponse().from_map(
            await self.do_rpcrequest_async('DeleteDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_dbcluster(
        self,
        request: adb_20190315_models.DeleteDBClusterRequest,
    ) -> adb_20190315_models.DeleteDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_dbcluster_with_options(request, runtime)

    async def delete_dbcluster_async(
        self,
        request: adb_20190315_models.DeleteDBClusterRequest,
    ) -> adb_20190315_models.DeleteDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_dbcluster_with_options_async(request, runtime)

    def describe_sqlplan_with_options(
        self,
        request: adb_20190315_models.DescribeSQLPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSQLPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSQLPlanResponse().from_map(
            self.do_rpcrequest('DescribeSQLPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_sqlplan_with_options_async(
        self,
        request: adb_20190315_models.DescribeSQLPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSQLPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSQLPlanResponse().from_map(
            await self.do_rpcrequest_async('DescribeSQLPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_sqlplan(
        self,
        request: adb_20190315_models.DescribeSQLPlanRequest,
    ) -> adb_20190315_models.DescribeSQLPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_sqlplan_with_options(request, runtime)

    async def describe_sqlplan_async(
        self,
        request: adb_20190315_models.DescribeSQLPlanRequest,
    ) -> adb_20190315_models.DescribeSQLPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_sqlplan_with_options_async(request, runtime)

    def create_account_with_options(
        self,
        request: adb_20190315_models.CreateAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateAccountResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateAccountResponse().from_map(
            self.do_rpcrequest('CreateAccount', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_account_with_options_async(
        self,
        request: adb_20190315_models.CreateAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateAccountResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateAccountResponse().from_map(
            await self.do_rpcrequest_async('CreateAccount', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_account(
        self,
        request: adb_20190315_models.CreateAccountRequest,
    ) -> adb_20190315_models.CreateAccountResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_account_with_options(request, runtime)

    async def create_account_async(
        self,
        request: adb_20190315_models.CreateAccountRequest,
    ) -> adb_20190315_models.CreateAccountResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_account_with_options_async(request, runtime)

    def describe_operator_permission_with_options(
        self,
        request: adb_20190315_models.DescribeOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeOperatorPermissionResponse().from_map(
            self.do_rpcrequest('DescribeOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_operator_permission_with_options_async(
        self,
        request: adb_20190315_models.DescribeOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeOperatorPermissionResponse().from_map(
            await self.do_rpcrequest_async('DescribeOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_operator_permission(
        self,
        request: adb_20190315_models.DescribeOperatorPermissionRequest,
    ) -> adb_20190315_models.DescribeOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_operator_permission_with_options(request, runtime)

    async def describe_operator_permission_async(
        self,
        request: adb_20190315_models.DescribeOperatorPermissionRequest,
    ) -> adb_20190315_models.DescribeOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_operator_permission_with_options_async(request, runtime)

    def describe_process_list_with_options(
        self,
        request: adb_20190315_models.DescribeProcessListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeProcessListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeProcessListResponse().from_map(
            self.do_rpcrequest('DescribeProcessList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_process_list_with_options_async(
        self,
        request: adb_20190315_models.DescribeProcessListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeProcessListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeProcessListResponse().from_map(
            await self.do_rpcrequest_async('DescribeProcessList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_process_list(
        self,
        request: adb_20190315_models.DescribeProcessListRequest,
    ) -> adb_20190315_models.DescribeProcessListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_process_list_with_options(request, runtime)

    async def describe_process_list_async(
        self,
        request: adb_20190315_models.DescribeProcessListRequest,
    ) -> adb_20190315_models.DescribeProcessListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_process_list_with_options_async(request, runtime)

    def describe_table_statistics_with_options(
        self,
        request: adb_20190315_models.DescribeTableStatisticsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTableStatisticsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTableStatisticsResponse().from_map(
            self.do_rpcrequest('DescribeTableStatistics', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_table_statistics_with_options_async(
        self,
        request: adb_20190315_models.DescribeTableStatisticsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTableStatisticsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTableStatisticsResponse().from_map(
            await self.do_rpcrequest_async('DescribeTableStatistics', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_table_statistics(
        self,
        request: adb_20190315_models.DescribeTableStatisticsRequest,
    ) -> adb_20190315_models.DescribeTableStatisticsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_table_statistics_with_options(request, runtime)

    async def describe_table_statistics_async(
        self,
        request: adb_20190315_models.DescribeTableStatisticsRequest,
    ) -> adb_20190315_models.DescribeTableStatisticsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_table_statistics_with_options_async(request, runtime)

    def delete_elastic_plan_with_options(
        self,
        request: adb_20190315_models.DeleteElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteElasticPlanResponse().from_map(
            self.do_rpcrequest('DeleteElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_elastic_plan_with_options_async(
        self,
        request: adb_20190315_models.DeleteElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteElasticPlanResponse().from_map(
            await self.do_rpcrequest_async('DeleteElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_elastic_plan(
        self,
        request: adb_20190315_models.DeleteElasticPlanRequest,
    ) -> adb_20190315_models.DeleteElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_elastic_plan_with_options(request, runtime)

    async def delete_elastic_plan_async(
        self,
        request: adb_20190315_models.DeleteElasticPlanRequest,
    ) -> adb_20190315_models.DeleteElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_elastic_plan_with_options_async(request, runtime)

    def unbind_dbresource_pool_with_user_with_options(
        self,
        request: adb_20190315_models.UnbindDBResourcePoolWithUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.UnbindDBResourcePoolWithUserResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.UnbindDBResourcePoolWithUserResponse().from_map(
            self.do_rpcrequest('UnbindDBResourcePoolWithUser', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def unbind_dbresource_pool_with_user_with_options_async(
        self,
        request: adb_20190315_models.UnbindDBResourcePoolWithUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.UnbindDBResourcePoolWithUserResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.UnbindDBResourcePoolWithUserResponse().from_map(
            await self.do_rpcrequest_async('UnbindDBResourcePoolWithUser', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def unbind_dbresource_pool_with_user(
        self,
        request: adb_20190315_models.UnbindDBResourcePoolWithUserRequest,
    ) -> adb_20190315_models.UnbindDBResourcePoolWithUserResponse:
        runtime = util_models.RuntimeOptions()
        return self.unbind_dbresource_pool_with_user_with_options(request, runtime)

    async def unbind_dbresource_pool_with_user_async(
        self,
        request: adb_20190315_models.UnbindDBResourcePoolWithUserRequest,
    ) -> adb_20190315_models.UnbindDBResourcePoolWithUserResponse:
        runtime = util_models.RuntimeOptions()
        return await self.unbind_dbresource_pool_with_user_with_options_async(request, runtime)

    def describe_sqlplan_task_with_options(
        self,
        request: adb_20190315_models.DescribeSQLPlanTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSQLPlanTaskResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSQLPlanTaskResponse().from_map(
            self.do_rpcrequest('DescribeSQLPlanTask', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_sqlplan_task_with_options_async(
        self,
        request: adb_20190315_models.DescribeSQLPlanTaskRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSQLPlanTaskResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSQLPlanTaskResponse().from_map(
            await self.do_rpcrequest_async('DescribeSQLPlanTask', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_sqlplan_task(
        self,
        request: adb_20190315_models.DescribeSQLPlanTaskRequest,
    ) -> adb_20190315_models.DescribeSQLPlanTaskResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_sqlplan_task_with_options(request, runtime)

    async def describe_sqlplan_task_async(
        self,
        request: adb_20190315_models.DescribeSQLPlanTaskRequest,
    ) -> adb_20190315_models.DescribeSQLPlanTaskResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_sqlplan_task_with_options_async(request, runtime)

    def modify_backup_policy_with_options(
        self,
        request: adb_20190315_models.ModifyBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyBackupPolicyResponse().from_map(
            self.do_rpcrequest('ModifyBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_backup_policy_with_options_async(
        self,
        request: adb_20190315_models.ModifyBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyBackupPolicyResponse().from_map(
            await self.do_rpcrequest_async('ModifyBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_backup_policy(
        self,
        request: adb_20190315_models.ModifyBackupPolicyRequest,
    ) -> adb_20190315_models.ModifyBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_backup_policy_with_options(request, runtime)

    async def modify_backup_policy_async(
        self,
        request: adb_20190315_models.ModifyBackupPolicyRequest,
    ) -> adb_20190315_models.ModifyBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_backup_policy_with_options_async(request, runtime)

    def describe_audit_log_records_with_options(
        self,
        request: adb_20190315_models.DescribeAuditLogRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAuditLogRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAuditLogRecordsResponse().from_map(
            self.do_rpcrequest('DescribeAuditLogRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_audit_log_records_with_options_async(
        self,
        request: adb_20190315_models.DescribeAuditLogRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAuditLogRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAuditLogRecordsResponse().from_map(
            await self.do_rpcrequest_async('DescribeAuditLogRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_audit_log_records(
        self,
        request: adb_20190315_models.DescribeAuditLogRecordsRequest,
    ) -> adb_20190315_models.DescribeAuditLogRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_audit_log_records_with_options(request, runtime)

    async def describe_audit_log_records_async(
        self,
        request: adb_20190315_models.DescribeAuditLogRecordsRequest,
    ) -> adb_20190315_models.DescribeAuditLogRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_audit_log_records_with_options_async(request, runtime)

    def create_dbcluster_with_options(
        self,
        request: adb_20190315_models.CreateDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateDBClusterResponse().from_map(
            self.do_rpcrequest('CreateDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_dbcluster_with_options_async(
        self,
        request: adb_20190315_models.CreateDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateDBClusterResponse().from_map(
            await self.do_rpcrequest_async('CreateDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_dbcluster(
        self,
        request: adb_20190315_models.CreateDBClusterRequest,
    ) -> adb_20190315_models.CreateDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_dbcluster_with_options(request, runtime)

    async def create_dbcluster_async(
        self,
        request: adb_20190315_models.CreateDBClusterRequest,
    ) -> adb_20190315_models.CreateDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_dbcluster_with_options_async(request, runtime)

    def modify_dbcluster_resource_group_with_options(
        self,
        request: adb_20190315_models.ModifyDBClusterResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterResourceGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterResourceGroupResponse().from_map(
            self.do_rpcrequest('ModifyDBClusterResourceGroup', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbcluster_resource_group_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBClusterResourceGroupRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterResourceGroupResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterResourceGroupResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBClusterResourceGroup', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbcluster_resource_group(
        self,
        request: adb_20190315_models.ModifyDBClusterResourceGroupRequest,
    ) -> adb_20190315_models.ModifyDBClusterResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbcluster_resource_group_with_options(request, runtime)

    async def modify_dbcluster_resource_group_async(
        self,
        request: adb_20190315_models.ModifyDBClusterResourceGroupRequest,
    ) -> adb_20190315_models.ModifyDBClusterResourceGroupResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbcluster_resource_group_with_options_async(request, runtime)

    def bind_dbresource_pool_with_user_with_options(
        self,
        request: adb_20190315_models.BindDBResourcePoolWithUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.BindDBResourcePoolWithUserResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.BindDBResourcePoolWithUserResponse().from_map(
            self.do_rpcrequest('BindDBResourcePoolWithUser', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def bind_dbresource_pool_with_user_with_options_async(
        self,
        request: adb_20190315_models.BindDBResourcePoolWithUserRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.BindDBResourcePoolWithUserResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.BindDBResourcePoolWithUserResponse().from_map(
            await self.do_rpcrequest_async('BindDBResourcePoolWithUser', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def bind_dbresource_pool_with_user(
        self,
        request: adb_20190315_models.BindDBResourcePoolWithUserRequest,
    ) -> adb_20190315_models.BindDBResourcePoolWithUserResponse:
        runtime = util_models.RuntimeOptions()
        return self.bind_dbresource_pool_with_user_with_options(request, runtime)

    async def bind_dbresource_pool_with_user_async(
        self,
        request: adb_20190315_models.BindDBResourcePoolWithUserRequest,
    ) -> adb_20190315_models.BindDBResourcePoolWithUserResponse:
        runtime = util_models.RuntimeOptions()
        return await self.bind_dbresource_pool_with_user_with_options_async(request, runtime)

    def describe_schemas_with_options(
        self,
        request: adb_20190315_models.DescribeSchemasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSchemasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSchemasResponse().from_map(
            self.do_rpcrequest('DescribeSchemas', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_schemas_with_options_async(
        self,
        request: adb_20190315_models.DescribeSchemasRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSchemasResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSchemasResponse().from_map(
            await self.do_rpcrequest_async('DescribeSchemas', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_schemas(
        self,
        request: adb_20190315_models.DescribeSchemasRequest,
    ) -> adb_20190315_models.DescribeSchemasResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_schemas_with_options(request, runtime)

    async def describe_schemas_async(
        self,
        request: adb_20190315_models.DescribeSchemasRequest,
    ) -> adb_20190315_models.DescribeSchemasResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_schemas_with_options_async(request, runtime)

    def modify_dbcluster_maintain_time_with_options(
        self,
        request: adb_20190315_models.ModifyDBClusterMaintainTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterMaintainTimeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterMaintainTimeResponse().from_map(
            self.do_rpcrequest('ModifyDBClusterMaintainTime', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbcluster_maintain_time_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBClusterMaintainTimeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterMaintainTimeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterMaintainTimeResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBClusterMaintainTime', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbcluster_maintain_time(
        self,
        request: adb_20190315_models.ModifyDBClusterMaintainTimeRequest,
    ) -> adb_20190315_models.ModifyDBClusterMaintainTimeResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbcluster_maintain_time_with_options(request, runtime)

    async def modify_dbcluster_maintain_time_async(
        self,
        request: adb_20190315_models.ModifyDBClusterMaintainTimeRequest,
    ) -> adb_20190315_models.ModifyDBClusterMaintainTimeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbcluster_maintain_time_with_options_async(request, runtime)

    def describe_connection_count_records_with_options(
        self,
        request: adb_20190315_models.DescribeConnectionCountRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeConnectionCountRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeConnectionCountRecordsResponse().from_map(
            self.do_rpcrequest('DescribeConnectionCountRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_connection_count_records_with_options_async(
        self,
        request: adb_20190315_models.DescribeConnectionCountRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeConnectionCountRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeConnectionCountRecordsResponse().from_map(
            await self.do_rpcrequest_async('DescribeConnectionCountRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_connection_count_records(
        self,
        request: adb_20190315_models.DescribeConnectionCountRecordsRequest,
    ) -> adb_20190315_models.DescribeConnectionCountRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_connection_count_records_with_options(request, runtime)

    async def describe_connection_count_records_async(
        self,
        request: adb_20190315_models.DescribeConnectionCountRecordsRequest,
    ) -> adb_20190315_models.DescribeConnectionCountRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_connection_count_records_with_options_async(request, runtime)

    def describe_backups_with_options(
        self,
        request: adb_20190315_models.DescribeBackupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeBackupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeBackupsResponse().from_map(
            self.do_rpcrequest('DescribeBackups', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_backups_with_options_async(
        self,
        request: adb_20190315_models.DescribeBackupsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeBackupsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeBackupsResponse().from_map(
            await self.do_rpcrequest_async('DescribeBackups', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_backups(
        self,
        request: adb_20190315_models.DescribeBackupsRequest,
    ) -> adb_20190315_models.DescribeBackupsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_backups_with_options(request, runtime)

    async def describe_backups_async(
        self,
        request: adb_20190315_models.DescribeBackupsRequest,
    ) -> adb_20190315_models.DescribeBackupsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_backups_with_options_async(request, runtime)

    def modify_dbcluster_description_with_options(
        self,
        request: adb_20190315_models.ModifyDBClusterDescriptionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterDescriptionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterDescriptionResponse().from_map(
            self.do_rpcrequest('ModifyDBClusterDescription', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbcluster_description_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBClusterDescriptionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterDescriptionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterDescriptionResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBClusterDescription', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbcluster_description(
        self,
        request: adb_20190315_models.ModifyDBClusterDescriptionRequest,
    ) -> adb_20190315_models.ModifyDBClusterDescriptionResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbcluster_description_with_options(request, runtime)

    async def modify_dbcluster_description_async(
        self,
        request: adb_20190315_models.ModifyDBClusterDescriptionRequest,
    ) -> adb_20190315_models.ModifyDBClusterDescriptionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbcluster_description_with_options_async(request, runtime)

    def describe_columns_with_options(
        self,
        request: adb_20190315_models.DescribeColumnsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeColumnsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeColumnsResponse().from_map(
            self.do_rpcrequest('DescribeColumns', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_columns_with_options_async(
        self,
        request: adb_20190315_models.DescribeColumnsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeColumnsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeColumnsResponse().from_map(
            await self.do_rpcrequest_async('DescribeColumns', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_columns(
        self,
        request: adb_20190315_models.DescribeColumnsRequest,
    ) -> adb_20190315_models.DescribeColumnsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_columns_with_options(request, runtime)

    async def describe_columns_async(
        self,
        request: adb_20190315_models.DescribeColumnsRequest,
    ) -> adb_20190315_models.DescribeColumnsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_columns_with_options_async(request, runtime)

    def revoke_operator_permission_with_options(
        self,
        request: adb_20190315_models.RevokeOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.RevokeOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.RevokeOperatorPermissionResponse().from_map(
            self.do_rpcrequest('RevokeOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def revoke_operator_permission_with_options_async(
        self,
        request: adb_20190315_models.RevokeOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.RevokeOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.RevokeOperatorPermissionResponse().from_map(
            await self.do_rpcrequest_async('RevokeOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def revoke_operator_permission(
        self,
        request: adb_20190315_models.RevokeOperatorPermissionRequest,
    ) -> adb_20190315_models.RevokeOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.revoke_operator_permission_with_options(request, runtime)

    async def revoke_operator_permission_async(
        self,
        request: adb_20190315_models.RevokeOperatorPermissionRequest,
    ) -> adb_20190315_models.RevokeOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.revoke_operator_permission_with_options_async(request, runtime)

    def create_dbresource_pool_with_options(
        self,
        request: adb_20190315_models.CreateDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateDBResourcePoolResponse().from_map(
            self.do_rpcrequest('CreateDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_dbresource_pool_with_options_async(
        self,
        request: adb_20190315_models.CreateDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateDBResourcePoolResponse().from_map(
            await self.do_rpcrequest_async('CreateDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_dbresource_pool(
        self,
        request: adb_20190315_models.CreateDBResourcePoolRequest,
    ) -> adb_20190315_models.CreateDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_dbresource_pool_with_options(request, runtime)

    async def create_dbresource_pool_async(
        self,
        request: adb_20190315_models.CreateDBResourcePoolRequest,
    ) -> adb_20190315_models.CreateDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_dbresource_pool_with_options_async(request, runtime)

    def describe_all_accounts_with_options(
        self,
        request: adb_20190315_models.DescribeAllAccountsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAllAccountsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAllAccountsResponse().from_map(
            self.do_rpcrequest('DescribeAllAccounts', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_all_accounts_with_options_async(
        self,
        request: adb_20190315_models.DescribeAllAccountsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAllAccountsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAllAccountsResponse().from_map(
            await self.do_rpcrequest_async('DescribeAllAccounts', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_all_accounts(
        self,
        request: adb_20190315_models.DescribeAllAccountsRequest,
    ) -> adb_20190315_models.DescribeAllAccountsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_all_accounts_with_options(request, runtime)

    async def describe_all_accounts_async(
        self,
        request: adb_20190315_models.DescribeAllAccountsRequest,
    ) -> adb_20190315_models.DescribeAllAccountsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_all_accounts_with_options_async(request, runtime)

    def modify_audit_log_config_with_options(
        self,
        request: adb_20190315_models.ModifyAuditLogConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAuditLogConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAuditLogConfigResponse().from_map(
            self.do_rpcrequest('ModifyAuditLogConfig', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_audit_log_config_with_options_async(
        self,
        request: adb_20190315_models.ModifyAuditLogConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyAuditLogConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyAuditLogConfigResponse().from_map(
            await self.do_rpcrequest_async('ModifyAuditLogConfig', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_audit_log_config(
        self,
        request: adb_20190315_models.ModifyAuditLogConfigRequest,
    ) -> adb_20190315_models.ModifyAuditLogConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_audit_log_config_with_options(request, runtime)

    async def modify_audit_log_config_async(
        self,
        request: adb_20190315_models.ModifyAuditLogConfigRequest,
    ) -> adb_20190315_models.ModifyAuditLogConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_audit_log_config_with_options_async(request, runtime)

    def delete_dbresource_pool_with_options(
        self,
        request: adb_20190315_models.DeleteDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteDBResourcePoolResponse().from_map(
            self.do_rpcrequest('DeleteDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_dbresource_pool_with_options_async(
        self,
        request: adb_20190315_models.DeleteDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteDBResourcePoolResponse().from_map(
            await self.do_rpcrequest_async('DeleteDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_dbresource_pool(
        self,
        request: adb_20190315_models.DeleteDBResourcePoolRequest,
    ) -> adb_20190315_models.DeleteDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_dbresource_pool_with_options(request, runtime)

    async def delete_dbresource_pool_async(
        self,
        request: adb_20190315_models.DeleteDBResourcePoolRequest,
    ) -> adb_20190315_models.DeleteDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_dbresource_pool_with_options_async(request, runtime)

    def tag_resources_with_options(
        self,
        request: adb_20190315_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.TagResourcesResponse().from_map(
            self.do_rpcrequest('TagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def tag_resources_with_options_async(
        self,
        request: adb_20190315_models.TagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.TagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.TagResourcesResponse().from_map(
            await self.do_rpcrequest_async('TagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def tag_resources(
        self,
        request: adb_20190315_models.TagResourcesRequest,
    ) -> adb_20190315_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.tag_resources_with_options(request, runtime)

    async def tag_resources_async(
        self,
        request: adb_20190315_models.TagResourcesRequest,
    ) -> adb_20190315_models.TagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.tag_resources_with_options_async(request, runtime)

    def grant_operator_permission_with_options(
        self,
        request: adb_20190315_models.GrantOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.GrantOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.GrantOperatorPermissionResponse().from_map(
            self.do_rpcrequest('GrantOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def grant_operator_permission_with_options_async(
        self,
        request: adb_20190315_models.GrantOperatorPermissionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.GrantOperatorPermissionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.GrantOperatorPermissionResponse().from_map(
            await self.do_rpcrequest_async('GrantOperatorPermission', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def grant_operator_permission(
        self,
        request: adb_20190315_models.GrantOperatorPermissionRequest,
    ) -> adb_20190315_models.GrantOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return self.grant_operator_permission_with_options(request, runtime)

    async def grant_operator_permission_async(
        self,
        request: adb_20190315_models.GrantOperatorPermissionRequest,
    ) -> adb_20190315_models.GrantOperatorPermissionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.grant_operator_permission_with_options_async(request, runtime)

    def describe_all_data_source_with_options(
        self,
        request: adb_20190315_models.DescribeAllDataSourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAllDataSourceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAllDataSourceResponse().from_map(
            self.do_rpcrequest('DescribeAllDataSource', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_all_data_source_with_options_async(
        self,
        request: adb_20190315_models.DescribeAllDataSourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAllDataSourceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAllDataSourceResponse().from_map(
            await self.do_rpcrequest_async('DescribeAllDataSource', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_all_data_source(
        self,
        request: adb_20190315_models.DescribeAllDataSourceRequest,
    ) -> adb_20190315_models.DescribeAllDataSourceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_all_data_source_with_options(request, runtime)

    async def describe_all_data_source_async(
        self,
        request: adb_20190315_models.DescribeAllDataSourceRequest,
    ) -> adb_20190315_models.DescribeAllDataSourceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_all_data_source_with_options_async(request, runtime)

    def modify_dbcluster_with_options(
        self,
        request: adb_20190315_models.ModifyDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterResponse().from_map(
            self.do_rpcrequest('ModifyDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbcluster_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBClusterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBCluster', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbcluster(
        self,
        request: adb_20190315_models.ModifyDBClusterRequest,
    ) -> adb_20190315_models.ModifyDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbcluster_with_options(request, runtime)

    async def modify_dbcluster_async(
        self,
        request: adb_20190315_models.ModifyDBClusterRequest,
    ) -> adb_20190315_models.ModifyDBClusterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbcluster_with_options_async(request, runtime)

    def describe_table_partition_diagnose_with_options(
        self,
        request: adb_20190315_models.DescribeTablePartitionDiagnoseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTablePartitionDiagnoseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTablePartitionDiagnoseResponse().from_map(
            self.do_rpcrequest('DescribeTablePartitionDiagnose', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_table_partition_diagnose_with_options_async(
        self,
        request: adb_20190315_models.DescribeTablePartitionDiagnoseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTablePartitionDiagnoseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTablePartitionDiagnoseResponse().from_map(
            await self.do_rpcrequest_async('DescribeTablePartitionDiagnose', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_table_partition_diagnose(
        self,
        request: adb_20190315_models.DescribeTablePartitionDiagnoseRequest,
    ) -> adb_20190315_models.DescribeTablePartitionDiagnoseResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_table_partition_diagnose_with_options(request, runtime)

    async def describe_table_partition_diagnose_async(
        self,
        request: adb_20190315_models.DescribeTablePartitionDiagnoseRequest,
    ) -> adb_20190315_models.DescribeTablePartitionDiagnoseResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_table_partition_diagnose_with_options_async(request, runtime)

    def describe_dbresource_pool_with_options(
        self,
        request: adb_20190315_models.DescribeDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBResourcePoolResponse().from_map(
            self.do_rpcrequest('DescribeDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbresource_pool_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBResourcePoolResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbresource_pool(
        self,
        request: adb_20190315_models.DescribeDBResourcePoolRequest,
    ) -> adb_20190315_models.DescribeDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbresource_pool_with_options(request, runtime)

    async def describe_dbresource_pool_async(
        self,
        request: adb_20190315_models.DescribeDBResourcePoolRequest,
    ) -> adb_20190315_models.DescribeDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbresource_pool_with_options_async(request, runtime)

    def list_tag_resources_with_options(
        self,
        request: adb_20190315_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ListTagResourcesResponse().from_map(
            self.do_rpcrequest('ListTagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def list_tag_resources_with_options_async(
        self,
        request: adb_20190315_models.ListTagResourcesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ListTagResourcesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ListTagResourcesResponse().from_map(
            await self.do_rpcrequest_async('ListTagResources', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def list_tag_resources(
        self,
        request: adb_20190315_models.ListTagResourcesRequest,
    ) -> adb_20190315_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return self.list_tag_resources_with_options(request, runtime)

    async def list_tag_resources_async(
        self,
        request: adb_20190315_models.ListTagResourcesRequest,
    ) -> adb_20190315_models.ListTagResourcesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.list_tag_resources_with_options_async(request, runtime)

    def describe_dbcluster_performance_with_options(
        self,
        request: adb_20190315_models.DescribeDBClusterPerformanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterPerformanceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterPerformanceResponse().from_map(
            self.do_rpcrequest('DescribeDBClusterPerformance', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbcluster_performance_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClusterPerformanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterPerformanceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterPerformanceResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusterPerformance', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbcluster_performance(
        self,
        request: adb_20190315_models.DescribeDBClusterPerformanceRequest,
    ) -> adb_20190315_models.DescribeDBClusterPerformanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbcluster_performance_with_options(request, runtime)

    async def describe_dbcluster_performance_async(
        self,
        request: adb_20190315_models.DescribeDBClusterPerformanceRequest,
    ) -> adb_20190315_models.DescribeDBClusterPerformanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbcluster_performance_with_options_async(request, runtime)

    def modify_elastic_plan_with_options(
        self,
        request: adb_20190315_models.ModifyElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyElasticPlanResponse().from_map(
            self.do_rpcrequest('ModifyElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_elastic_plan_with_options_async(
        self,
        request: adb_20190315_models.ModifyElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyElasticPlanResponse().from_map(
            await self.do_rpcrequest_async('ModifyElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_elastic_plan(
        self,
        request: adb_20190315_models.ModifyElasticPlanRequest,
    ) -> adb_20190315_models.ModifyElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_elastic_plan_with_options(request, runtime)

    async def modify_elastic_plan_async(
        self,
        request: adb_20190315_models.ModifyElasticPlanRequest,
    ) -> adb_20190315_models.ModifyElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_elastic_plan_with_options_async(request, runtime)

    def modify_log_backup_policy_with_options(
        self,
        request: adb_20190315_models.ModifyLogBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyLogBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyLogBackupPolicyResponse().from_map(
            self.do_rpcrequest('ModifyLogBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_log_backup_policy_with_options_async(
        self,
        request: adb_20190315_models.ModifyLogBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyLogBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyLogBackupPolicyResponse().from_map(
            await self.do_rpcrequest_async('ModifyLogBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_log_backup_policy(
        self,
        request: adb_20190315_models.ModifyLogBackupPolicyRequest,
    ) -> adb_20190315_models.ModifyLogBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_log_backup_policy_with_options(request, runtime)

    async def modify_log_backup_policy_async(
        self,
        request: adb_20190315_models.ModifyLogBackupPolicyRequest,
    ) -> adb_20190315_models.ModifyLogBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_log_backup_policy_with_options_async(request, runtime)

    def describe_slow_log_trend_with_options(
        self,
        request: adb_20190315_models.DescribeSlowLogTrendRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSlowLogTrendResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSlowLogTrendResponse().from_map(
            self.do_rpcrequest('DescribeSlowLogTrend', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_slow_log_trend_with_options_async(
        self,
        request: adb_20190315_models.DescribeSlowLogTrendRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSlowLogTrendResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSlowLogTrendResponse().from_map(
            await self.do_rpcrequest_async('DescribeSlowLogTrend', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_slow_log_trend(
        self,
        request: adb_20190315_models.DescribeSlowLogTrendRequest,
    ) -> adb_20190315_models.DescribeSlowLogTrendResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_slow_log_trend_with_options(request, runtime)

    async def describe_slow_log_trend_async(
        self,
        request: adb_20190315_models.DescribeSlowLogTrendRequest,
    ) -> adb_20190315_models.DescribeSlowLogTrendResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_slow_log_trend_with_options_async(request, runtime)

    def describe_available_resource_with_options(
        self,
        request: adb_20190315_models.DescribeAvailableResourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAvailableResourceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAvailableResourceResponse().from_map(
            self.do_rpcrequest('DescribeAvailableResource', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_available_resource_with_options_async(
        self,
        request: adb_20190315_models.DescribeAvailableResourceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAvailableResourceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAvailableResourceResponse().from_map(
            await self.do_rpcrequest_async('DescribeAvailableResource', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_available_resource(
        self,
        request: adb_20190315_models.DescribeAvailableResourceRequest,
    ) -> adb_20190315_models.DescribeAvailableResourceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_available_resource_with_options(request, runtime)

    async def describe_available_resource_async(
        self,
        request: adb_20190315_models.DescribeAvailableResourceRequest,
    ) -> adb_20190315_models.DescribeAvailableResourceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_available_resource_with_options_async(request, runtime)

    def create_elastic_plan_with_options(
        self,
        request: adb_20190315_models.CreateElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateElasticPlanResponse().from_map(
            self.do_rpcrequest('CreateElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def create_elastic_plan_with_options_async(
        self,
        request: adb_20190315_models.CreateElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.CreateElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.CreateElasticPlanResponse().from_map(
            await self.do_rpcrequest_async('CreateElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def create_elastic_plan(
        self,
        request: adb_20190315_models.CreateElasticPlanRequest,
    ) -> adb_20190315_models.CreateElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.create_elastic_plan_with_options(request, runtime)

    async def create_elastic_plan_async(
        self,
        request: adb_20190315_models.CreateElasticPlanRequest,
    ) -> adb_20190315_models.CreateElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.create_elastic_plan_with_options_async(request, runtime)

    def release_cluster_public_connection_with_options(
        self,
        request: adb_20190315_models.ReleaseClusterPublicConnectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ReleaseClusterPublicConnectionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ReleaseClusterPublicConnectionResponse().from_map(
            self.do_rpcrequest('ReleaseClusterPublicConnection', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def release_cluster_public_connection_with_options_async(
        self,
        request: adb_20190315_models.ReleaseClusterPublicConnectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ReleaseClusterPublicConnectionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ReleaseClusterPublicConnectionResponse().from_map(
            await self.do_rpcrequest_async('ReleaseClusterPublicConnection', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def release_cluster_public_connection(
        self,
        request: adb_20190315_models.ReleaseClusterPublicConnectionRequest,
    ) -> adb_20190315_models.ReleaseClusterPublicConnectionResponse:
        runtime = util_models.RuntimeOptions()
        return self.release_cluster_public_connection_with_options(request, runtime)

    async def release_cluster_public_connection_async(
        self,
        request: adb_20190315_models.ReleaseClusterPublicConnectionRequest,
    ) -> adb_20190315_models.ReleaseClusterPublicConnectionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.release_cluster_public_connection_with_options_async(request, runtime)

    def describe_audit_log_config_with_options(
        self,
        request: adb_20190315_models.DescribeAuditLogConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAuditLogConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAuditLogConfigResponse().from_map(
            self.do_rpcrequest('DescribeAuditLogConfig', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_audit_log_config_with_options_async(
        self,
        request: adb_20190315_models.DescribeAuditLogConfigRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAuditLogConfigResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAuditLogConfigResponse().from_map(
            await self.do_rpcrequest_async('DescribeAuditLogConfig', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_audit_log_config(
        self,
        request: adb_20190315_models.DescribeAuditLogConfigRequest,
    ) -> adb_20190315_models.DescribeAuditLogConfigResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_audit_log_config_with_options(request, runtime)

    async def describe_audit_log_config_async(
        self,
        request: adb_20190315_models.DescribeAuditLogConfigRequest,
    ) -> adb_20190315_models.DescribeAuditLogConfigResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_audit_log_config_with_options_async(request, runtime)

    def describe_tables_with_options(
        self,
        request: adb_20190315_models.DescribeTablesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTablesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTablesResponse().from_map(
            self.do_rpcrequest('DescribeTables', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_tables_with_options_async(
        self,
        request: adb_20190315_models.DescribeTablesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTablesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTablesResponse().from_map(
            await self.do_rpcrequest_async('DescribeTables', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_tables(
        self,
        request: adb_20190315_models.DescribeTablesRequest,
    ) -> adb_20190315_models.DescribeTablesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_tables_with_options(request, runtime)

    async def describe_tables_async(
        self,
        request: adb_20190315_models.DescribeTablesRequest,
    ) -> adb_20190315_models.DescribeTablesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_tables_with_options_async(request, runtime)

    def describe_dbcluster_net_info_with_options(
        self,
        request: adb_20190315_models.DescribeDBClusterNetInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterNetInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterNetInfoResponse().from_map(
            self.do_rpcrequest('DescribeDBClusterNetInfo', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbcluster_net_info_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClusterNetInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterNetInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterNetInfoResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusterNetInfo', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbcluster_net_info(
        self,
        request: adb_20190315_models.DescribeDBClusterNetInfoRequest,
    ) -> adb_20190315_models.DescribeDBClusterNetInfoResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbcluster_net_info_with_options(request, runtime)

    async def describe_dbcluster_net_info_async(
        self,
        request: adb_20190315_models.DescribeDBClusterNetInfoRequest,
    ) -> adb_20190315_models.DescribeDBClusterNetInfoResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbcluster_net_info_with_options_async(request, runtime)

    def describe_inclined_tables_with_options(
        self,
        request: adb_20190315_models.DescribeInclinedTablesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeInclinedTablesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeInclinedTablesResponse().from_map(
            self.do_rpcrequest('DescribeInclinedTables', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_inclined_tables_with_options_async(
        self,
        request: adb_20190315_models.DescribeInclinedTablesRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeInclinedTablesResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeInclinedTablesResponse().from_map(
            await self.do_rpcrequest_async('DescribeInclinedTables', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_inclined_tables(
        self,
        request: adb_20190315_models.DescribeInclinedTablesRequest,
    ) -> adb_20190315_models.DescribeInclinedTablesResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_inclined_tables_with_options(request, runtime)

    async def describe_inclined_tables_async(
        self,
        request: adb_20190315_models.DescribeInclinedTablesRequest,
    ) -> adb_20190315_models.DescribeInclinedTablesResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_inclined_tables_with_options_async(request, runtime)

    def describe_dbcluster_attribute_with_options(
        self,
        request: adb_20190315_models.DescribeDBClusterAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterAttributeResponse().from_map(
            self.do_rpcrequest('DescribeDBClusterAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbcluster_attribute_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClusterAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterAttributeResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusterAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbcluster_attribute(
        self,
        request: adb_20190315_models.DescribeDBClusterAttributeRequest,
    ) -> adb_20190315_models.DescribeDBClusterAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbcluster_attribute_with_options(request, runtime)

    async def describe_dbcluster_attribute_async(
        self,
        request: adb_20190315_models.DescribeDBClusterAttributeRequest,
    ) -> adb_20190315_models.DescribeDBClusterAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbcluster_attribute_with_options_async(request, runtime)

    def describe_dbclusters_with_options(
        self,
        request: adb_20190315_models.DescribeDBClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClustersResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClustersResponse().from_map(
            self.do_rpcrequest('DescribeDBClusters', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbclusters_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClustersRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClustersResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClustersResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusters', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbclusters(
        self,
        request: adb_20190315_models.DescribeDBClustersRequest,
    ) -> adb_20190315_models.DescribeDBClustersResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbclusters_with_options(request, runtime)

    async def describe_dbclusters_async(
        self,
        request: adb_20190315_models.DescribeDBClustersRequest,
    ) -> adb_20190315_models.DescribeDBClustersResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbclusters_with_options_async(request, runtime)

    def kill_process_with_options(
        self,
        request: adb_20190315_models.KillProcessRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.KillProcessResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.KillProcessResponse().from_map(
            self.do_rpcrequest('KillProcess', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def kill_process_with_options_async(
        self,
        request: adb_20190315_models.KillProcessRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.KillProcessResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.KillProcessResponse().from_map(
            await self.do_rpcrequest_async('KillProcess', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def kill_process(
        self,
        request: adb_20190315_models.KillProcessRequest,
    ) -> adb_20190315_models.KillProcessResponse:
        runtime = util_models.RuntimeOptions()
        return self.kill_process_with_options(request, runtime)

    async def kill_process_async(
        self,
        request: adb_20190315_models.KillProcessRequest,
    ) -> adb_20190315_models.KillProcessResponse:
        runtime = util_models.RuntimeOptions()
        return await self.kill_process_with_options_async(request, runtime)

    def describe_auto_renew_attribute_with_options(
        self,
        request: adb_20190315_models.DescribeAutoRenewAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAutoRenewAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAutoRenewAttributeResponse().from_map(
            self.do_rpcrequest('DescribeAutoRenewAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_auto_renew_attribute_with_options_async(
        self,
        request: adb_20190315_models.DescribeAutoRenewAttributeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAutoRenewAttributeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAutoRenewAttributeResponse().from_map(
            await self.do_rpcrequest_async('DescribeAutoRenewAttribute', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_auto_renew_attribute(
        self,
        request: adb_20190315_models.DescribeAutoRenewAttributeRequest,
    ) -> adb_20190315_models.DescribeAutoRenewAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_auto_renew_attribute_with_options(request, runtime)

    async def describe_auto_renew_attribute_async(
        self,
        request: adb_20190315_models.DescribeAutoRenewAttributeRequest,
    ) -> adb_20190315_models.DescribeAutoRenewAttributeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_auto_renew_attribute_with_options_async(request, runtime)

    def describe_dbcluster_access_white_list_with_options(
        self,
        request: adb_20190315_models.DescribeDBClusterAccessWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterAccessWhiteListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterAccessWhiteListResponse().from_map(
            self.do_rpcrequest('DescribeDBClusterAccessWhiteList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbcluster_access_white_list_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClusterAccessWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterAccessWhiteListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterAccessWhiteListResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusterAccessWhiteList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbcluster_access_white_list(
        self,
        request: adb_20190315_models.DescribeDBClusterAccessWhiteListRequest,
    ) -> adb_20190315_models.DescribeDBClusterAccessWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbcluster_access_white_list_with_options(request, runtime)

    async def describe_dbcluster_access_white_list_async(
        self,
        request: adb_20190315_models.DescribeDBClusterAccessWhiteListRequest,
    ) -> adb_20190315_models.DescribeDBClusterAccessWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbcluster_access_white_list_with_options_async(request, runtime)

    def describe_task_info_with_options(
        self,
        request: adb_20190315_models.DescribeTaskInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTaskInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTaskInfoResponse().from_map(
            self.do_rpcrequest('DescribeTaskInfo', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_task_info_with_options_async(
        self,
        request: adb_20190315_models.DescribeTaskInfoRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTaskInfoResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTaskInfoResponse().from_map(
            await self.do_rpcrequest_async('DescribeTaskInfo', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_task_info(
        self,
        request: adb_20190315_models.DescribeTaskInfoRequest,
    ) -> adb_20190315_models.DescribeTaskInfoResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_task_info_with_options(request, runtime)

    async def describe_task_info_async(
        self,
        request: adb_20190315_models.DescribeTaskInfoRequest,
    ) -> adb_20190315_models.DescribeTaskInfoResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_task_info_with_options_async(request, runtime)

    def describe_regions_with_options(
        self,
        request: adb_20190315_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeRegionsResponse().from_map(
            self.do_rpcrequest('DescribeRegions', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_regions_with_options_async(
        self,
        request: adb_20190315_models.DescribeRegionsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeRegionsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeRegionsResponse().from_map(
            await self.do_rpcrequest_async('DescribeRegions', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_regions(
        self,
        request: adb_20190315_models.DescribeRegionsRequest,
    ) -> adb_20190315_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_regions_with_options(request, runtime)

    async def describe_regions_async(
        self,
        request: adb_20190315_models.DescribeRegionsRequest,
    ) -> adb_20190315_models.DescribeRegionsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_regions_with_options_async(request, runtime)

    def modify_dbresource_pool_with_options(
        self,
        request: adb_20190315_models.ModifyDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBResourcePoolResponse().from_map(
            self.do_rpcrequest('ModifyDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbresource_pool_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBResourcePoolRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBResourcePoolResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBResourcePoolResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBResourcePool', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbresource_pool(
        self,
        request: adb_20190315_models.ModifyDBResourcePoolRequest,
    ) -> adb_20190315_models.ModifyDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbresource_pool_with_options(request, runtime)

    async def modify_dbresource_pool_async(
        self,
        request: adb_20190315_models.ModifyDBResourcePoolRequest,
    ) -> adb_20190315_models.ModifyDBResourcePoolResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbresource_pool_with_options_async(request, runtime)

    def delete_account_with_options(
        self,
        request: adb_20190315_models.DeleteAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteAccountResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteAccountResponse().from_map(
            self.do_rpcrequest('DeleteAccount', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def delete_account_with_options_async(
        self,
        request: adb_20190315_models.DeleteAccountRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DeleteAccountResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DeleteAccountResponse().from_map(
            await self.do_rpcrequest_async('DeleteAccount', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def delete_account(
        self,
        request: adb_20190315_models.DeleteAccountRequest,
    ) -> adb_20190315_models.DeleteAccountResponse:
        runtime = util_models.RuntimeOptions()
        return self.delete_account_with_options(request, runtime)

    async def delete_account_async(
        self,
        request: adb_20190315_models.DeleteAccountRequest,
    ) -> adb_20190315_models.DeleteAccountResponse:
        runtime = util_models.RuntimeOptions()
        return await self.delete_account_with_options_async(request, runtime)

    def describe_slow_log_records_with_options(
        self,
        request: adb_20190315_models.DescribeSlowLogRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSlowLogRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSlowLogRecordsResponse().from_map(
            self.do_rpcrequest('DescribeSlowLogRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_slow_log_records_with_options_async(
        self,
        request: adb_20190315_models.DescribeSlowLogRecordsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeSlowLogRecordsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeSlowLogRecordsResponse().from_map(
            await self.do_rpcrequest_async('DescribeSlowLogRecords', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_slow_log_records(
        self,
        request: adb_20190315_models.DescribeSlowLogRecordsRequest,
    ) -> adb_20190315_models.DescribeSlowLogRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_slow_log_records_with_options(request, runtime)

    async def describe_slow_log_records_async(
        self,
        request: adb_20190315_models.DescribeSlowLogRecordsRequest,
    ) -> adb_20190315_models.DescribeSlowLogRecordsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_slow_log_records_with_options_async(request, runtime)

    def describe_dbcluster_resource_pool_performance_with_options(
        self,
        request: adb_20190315_models.DescribeDBClusterResourcePoolPerformanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse().from_map(
            self.do_rpcrequest('DescribeDBClusterResourcePoolPerformance', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_dbcluster_resource_pool_performance_with_options_async(
        self,
        request: adb_20190315_models.DescribeDBClusterResourcePoolPerformanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse().from_map(
            await self.do_rpcrequest_async('DescribeDBClusterResourcePoolPerformance', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_dbcluster_resource_pool_performance(
        self,
        request: adb_20190315_models.DescribeDBClusterResourcePoolPerformanceRequest,
    ) -> adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_dbcluster_resource_pool_performance_with_options(request, runtime)

    async def describe_dbcluster_resource_pool_performance_async(
        self,
        request: adb_20190315_models.DescribeDBClusterResourcePoolPerformanceRequest,
    ) -> adb_20190315_models.DescribeDBClusterResourcePoolPerformanceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_dbcluster_resource_pool_performance_with_options_async(request, runtime)

    def reset_account_password_with_options(
        self,
        request: adb_20190315_models.ResetAccountPasswordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ResetAccountPasswordResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ResetAccountPasswordResponse().from_map(
            self.do_rpcrequest('ResetAccountPassword', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def reset_account_password_with_options_async(
        self,
        request: adb_20190315_models.ResetAccountPasswordRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ResetAccountPasswordResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ResetAccountPasswordResponse().from_map(
            await self.do_rpcrequest_async('ResetAccountPassword', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def reset_account_password(
        self,
        request: adb_20190315_models.ResetAccountPasswordRequest,
    ) -> adb_20190315_models.ResetAccountPasswordResponse:
        runtime = util_models.RuntimeOptions()
        return self.reset_account_password_with_options(request, runtime)

    async def reset_account_password_async(
        self,
        request: adb_20190315_models.ResetAccountPasswordRequest,
    ) -> adb_20190315_models.ResetAccountPasswordResponse:
        runtime = util_models.RuntimeOptions()
        return await self.reset_account_password_with_options_async(request, runtime)

    def describe_accounts_with_options(
        self,
        request: adb_20190315_models.DescribeAccountsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAccountsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAccountsResponse().from_map(
            self.do_rpcrequest('DescribeAccounts', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_accounts_with_options_async(
        self,
        request: adb_20190315_models.DescribeAccountsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeAccountsResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeAccountsResponse().from_map(
            await self.do_rpcrequest_async('DescribeAccounts', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_accounts(
        self,
        request: adb_20190315_models.DescribeAccountsRequest,
    ) -> adb_20190315_models.DescribeAccountsResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_accounts_with_options(request, runtime)

    async def describe_accounts_async(
        self,
        request: adb_20190315_models.DescribeAccountsRequest,
    ) -> adb_20190315_models.DescribeAccountsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_accounts_with_options_async(request, runtime)

    def describe_elastic_plan_with_options(
        self,
        request: adb_20190315_models.DescribeElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeElasticPlanResponse().from_map(
            self.do_rpcrequest('DescribeElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_elastic_plan_with_options_async(
        self,
        request: adb_20190315_models.DescribeElasticPlanRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeElasticPlanResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeElasticPlanResponse().from_map(
            await self.do_rpcrequest_async('DescribeElasticPlan', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_elastic_plan(
        self,
        request: adb_20190315_models.DescribeElasticPlanRequest,
    ) -> adb_20190315_models.DescribeElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_elastic_plan_with_options(request, runtime)

    async def describe_elastic_plan_async(
        self,
        request: adb_20190315_models.DescribeElasticPlanRequest,
    ) -> adb_20190315_models.DescribeElasticPlanResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_elastic_plan_with_options_async(request, runtime)

    def describe_table_detail_with_options(
        self,
        request: adb_20190315_models.DescribeTableDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTableDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTableDetailResponse().from_map(
            self.do_rpcrequest('DescribeTableDetail', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_table_detail_with_options_async(
        self,
        request: adb_20190315_models.DescribeTableDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeTableDetailResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeTableDetailResponse().from_map(
            await self.do_rpcrequest_async('DescribeTableDetail', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_table_detail(
        self,
        request: adb_20190315_models.DescribeTableDetailRequest,
    ) -> adb_20190315_models.DescribeTableDetailResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_table_detail_with_options(request, runtime)

    async def describe_table_detail_async(
        self,
        request: adb_20190315_models.DescribeTableDetailRequest,
    ) -> adb_20190315_models.DescribeTableDetailResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_table_detail_with_options_async(request, runtime)

    def allocate_cluster_public_connection_with_options(
        self,
        request: adb_20190315_models.AllocateClusterPublicConnectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.AllocateClusterPublicConnectionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.AllocateClusterPublicConnectionResponse().from_map(
            self.do_rpcrequest('AllocateClusterPublicConnection', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def allocate_cluster_public_connection_with_options_async(
        self,
        request: adb_20190315_models.AllocateClusterPublicConnectionRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.AllocateClusterPublicConnectionResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.AllocateClusterPublicConnectionResponse().from_map(
            await self.do_rpcrequest_async('AllocateClusterPublicConnection', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def allocate_cluster_public_connection(
        self,
        request: adb_20190315_models.AllocateClusterPublicConnectionRequest,
    ) -> adb_20190315_models.AllocateClusterPublicConnectionResponse:
        runtime = util_models.RuntimeOptions()
        return self.allocate_cluster_public_connection_with_options(request, runtime)

    async def allocate_cluster_public_connection_async(
        self,
        request: adb_20190315_models.AllocateClusterPublicConnectionRequest,
    ) -> adb_20190315_models.AllocateClusterPublicConnectionResponse:
        runtime = util_models.RuntimeOptions()
        return await self.allocate_cluster_public_connection_with_options_async(request, runtime)

    def describe_backup_policy_with_options(
        self,
        request: adb_20190315_models.DescribeBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeBackupPolicyResponse().from_map(
            self.do_rpcrequest('DescribeBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def describe_backup_policy_with_options_async(
        self,
        request: adb_20190315_models.DescribeBackupPolicyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.DescribeBackupPolicyResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.DescribeBackupPolicyResponse().from_map(
            await self.do_rpcrequest_async('DescribeBackupPolicy', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def describe_backup_policy(
        self,
        request: adb_20190315_models.DescribeBackupPolicyRequest,
    ) -> adb_20190315_models.DescribeBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_backup_policy_with_options(request, runtime)

    async def describe_backup_policy_async(
        self,
        request: adb_20190315_models.DescribeBackupPolicyRequest,
    ) -> adb_20190315_models.DescribeBackupPolicyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_backup_policy_with_options_async(request, runtime)

    def modify_dbcluster_access_white_list_with_options(
        self,
        request: adb_20190315_models.ModifyDBClusterAccessWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterAccessWhiteListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterAccessWhiteListResponse().from_map(
            self.do_rpcrequest('ModifyDBClusterAccessWhiteList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def modify_dbcluster_access_white_list_with_options_async(
        self,
        request: adb_20190315_models.ModifyDBClusterAccessWhiteListRequest,
        runtime: util_models.RuntimeOptions,
    ) -> adb_20190315_models.ModifyDBClusterAccessWhiteListResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return adb_20190315_models.ModifyDBClusterAccessWhiteListResponse().from_map(
            await self.do_rpcrequest_async('ModifyDBClusterAccessWhiteList', '2019-03-15', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def modify_dbcluster_access_white_list(
        self,
        request: adb_20190315_models.ModifyDBClusterAccessWhiteListRequest,
    ) -> adb_20190315_models.ModifyDBClusterAccessWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return self.modify_dbcluster_access_white_list_with_options(request, runtime)

    async def modify_dbcluster_access_white_list_async(
        self,
        request: adb_20190315_models.ModifyDBClusterAccessWhiteListRequest,
    ) -> adb_20190315_models.ModifyDBClusterAccessWhiteListResponse:
        runtime = util_models.RuntimeOptions()
        return await self.modify_dbcluster_access_white_list_with_options_async(request, runtime)
