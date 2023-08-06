from typing import Any, Dict, Iterable, List, Optional

from benchling_api_client.api.locations import (
    archive_locations,
    bulk_get_locations,
    create_location,
    get_location,
    list_locations,
    unarchive_locations,
    update_location,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param, schema_fields_query_param
from benchling_sdk.models import (
    ListLocationsSort,
    Location,
    LocationCreate,
    LocationsArchivalChange,
    LocationsArchive,
    LocationsArchiveReason,
    LocationsPaginatedList,
    LocationsUnarchive,
    LocationUpdate,
)
from benchling_sdk.services.base_service import BaseService


class LocationService(BaseService):
    @api_method
    def get_by_id(self, location_id: str) -> Location:
        response = get_location.sync_detailed(client=self.client, location_id=location_id)
        return model_from_detailed(response)

    @api_method
    def locations_page(
        self,
        *,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListLocationsSort] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        ids: Optional[str] = None,
        barcodes: Optional[str] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
    ) -> Response[LocationsPaginatedList]:
        return list_locations.sync_detailed(  # type: ignore
            client=self.client,
            sort=sort,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            ancestor_storage_id=ancestor_storage_id,
            archive_reason=archive_reason,
            ids=ids,
            barcodes=barcodes,
            schema_fields=schema_fields_query_param(schema_fields),
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        *,
        sort: Optional[ListLocationsSort] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        ids: Optional[str] = None,
        barcodes: Optional[str] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[Location]:
        def api_call(next_token: NextToken) -> Response[LocationsPaginatedList]:
            return self.locations_page(
                sort=sort,
                schema_id=schema_id,
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                ancestor_storage_id=ancestor_storage_id,
                archive_reason=archive_reason,
                ids=ids,
                barcodes=barcodes,
                schema_fields=schema_fields,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: LocationsPaginatedList) -> Optional[List[Location]]:
            return body.locations

        return PageIterator(api_call, results_extractor)

    @api_method
    def bulk_get(
        self, *, location_ids: Optional[Iterable[str]] = None, barcodes: Optional[Iterable[str]] = None
    ) -> Optional[List[Location]]:
        location_id_string = optional_array_query_param(location_ids)
        barcode_string = optional_array_query_param(barcodes)
        response = bulk_get_locations.sync_detailed(
            client=self.client, location_ids=location_id_string, barcodes=barcode_string
        )
        locations_list = model_from_detailed(response)
        return locations_list.locations

    @api_method
    def create(self, location: LocationCreate) -> Location:
        response = create_location.sync_detailed(client=self.client, json_body=location)
        return model_from_detailed(response)

    @api_method
    def update(self, location_id: str, location: LocationUpdate) -> Location:
        response = update_location.sync_detailed(
            client=self.client, location_id=location_id, json_body=location
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, location_ids: Iterable[str], reason: LocationsArchiveReason, should_remove_barcodes: bool
    ) -> LocationsArchivalChange:
        archive_request = LocationsArchive(
            location_ids=list(location_ids), reason=reason, should_remove_barcodes=should_remove_barcodes
        )
        response = archive_locations.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, location_ids: Iterable[str]) -> LocationsArchivalChange:
        unarchive_request = LocationsUnarchive(location_ids=list(location_ids))
        response = unarchive_locations.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
