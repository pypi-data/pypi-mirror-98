# -*- coding: utf-8 -*-
"""Google Cloud Asset Inventory API."""

from bits.google.services.base import Base
from google.cloud import asset_v1
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession


class CloudAssetInventory(Base):
    """CloudAssetInventory class."""

    def __init__(self, credentials):
        """Initialize a class instance."""
        self.asset = build('cloudasset', 'v1', credentials=credentials, cache_discovery=False)
        self.asset_v1 = asset_v1
        self.credentials = credentials
        self.requests = AuthorizedSession(self.credentials)

    def export_assets(self, parent, body):
        """Export new asset inventory."""
        v1 = self.asset.v1()
        return v1.exportAssets(parent=parent, body=body).execute()

    def export_assets_to_bigquery(
        self,
        parent,
        asset_types=None,
        content_type=None,
        read_time=None,
        dataset=None,
        table=None,
        force=False,
        separate_tables_per_asset_type=False,
        partition_spec=None,
    ):
        """Export Assets to BigQuery."""
        body = {
            'assetTypes': asset_types,
            'contentType': content_type,
            'outputConfig': {
                'bigqueryDestination': {
                    'dataset': dataset,
                    'table': table,
                    'force': force,
                    'separateTablesPerAssetType': separate_tables_per_asset_type,
                    'partitionSpec': partition_spec,
                },
            },
            'readTime': read_time,
        }
        return self.export_assets(parent, body)

    def export_assets_to_gcs(
        self,
        parent,
        asset_types=None,
        content_type=None,
        read_time=None,
        uri=None,
        uri_prefix=None,
    ):
        """Export Assets to GCS."""
        if uri:
            output_config = {'gcsDestination': {'uri': uri}}
        else:
            output_config = {'gcsDestination': {'uriPrefix': uri_prefix}}
        body = {
            'assetTypes': asset_types,
            'contentType': content_type,
            'outputConfig': output_config,
            'readTime': read_time,
        }
        return self.export_assets(parent, body)

    def get_operation(self, name):
        """Get the status of an asset inventory export operation."""
        operations = self.asset.operations()
        return operations.get(name=name).execute()

    def search_all_iam_policies(
        self,
        scope,
        asset_types=[],
        query=None,
        page_size=1000
    ):
        """Search all iam policies in asset inventory for a given scope."""
        assets = self.asset.v1()
        request = assets.searchAllIamPolicies(
            scope=scope,
            pageSize=page_size,
            query=query,
        )
        items = []
        while request is not None:
            response = request.execute()
            items += response.get("results", [])
            request = assets.searchAllIamPolicies_next(request, response)
        return items

    def search_all_resources(
        self,
        scope,
        asset_types=[],
        query=None,
        page_size=1000
    ):
        """Search all resources in asset inventory for a given scope."""
        assets = self.asset.v1()
        request = assets.searchAllResources(
            scope=scope,
            assetTypes=asset_types,
            pageSize=page_size,
            query=query,
        )
        items = []
        while request is not None:
            response = request.execute()
            items += response.get("results", [])
            request = assets.searchAllResources_next(request, response)
        return items
