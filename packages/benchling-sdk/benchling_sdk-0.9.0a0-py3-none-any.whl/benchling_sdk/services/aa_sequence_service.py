from typing import Any, Dict, Iterable, List, Optional

from benchling_api_client.api.aa_sequences import (
    archive_aa_sequences,
    bulk_create_aa_sequences,
    bulk_get_aa_sequences,
    create_aa_sequence,
    get_aa_sequence,
    list_aa_sequences,
    unarchive_aa_sequences,
    update_aa_sequence,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param, schema_fields_query_param
from benchling_sdk.models import (
    AaSequence,
    AaSequenceBulkCreate,
    AaSequenceCreate,
    AaSequencesArchivalChange,
    AaSequencesArchive,
    AaSequencesArchiveReason,
    AaSequencesBulkCreateRequest,
    AaSequencesPaginatedList,
    AaSequencesUnarchive,
    AaSequenceUpdate,
    AsyncTaskLink,
    ListAASequencesSort,
)
from benchling_sdk.services.base_service import BaseService


class AaSequenceService(BaseService):
    @api_method
    def get_by_id(self, aa_sequence_id: str) -> AaSequence:
        response = get_aa_sequence.sync_detailed(client=self.client, aa_sequence_id=aa_sequence_id)
        return model_from_detailed(response)

    @api_method
    def aa_sequences_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        amino_acids: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[ListAASequencesSort] = None,
        page_size: Optional[int] = None,
        next_token: NextToken = None,
    ) -> Response[AaSequencesPaginatedList]:
        return list_aa_sequences.sync_detailed(  # type: ignore
            client=self.client,
            modified_at=modified_at,
            name=name,
            amino_acids=amino_acids,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            mentions=mentions,
            ids=optional_array_query_param(ids),
            schema_fields=schema_fields_query_param(schema_fields),
            sort=sort,
            page_size=page_size,
            next_token=next_token,
        )

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        amino_acids: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[ListAASequencesSort] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[AaSequence]:
        def api_call(next_token: NextToken) -> Response[AaSequencesPaginatedList]:
            return self.aa_sequences_page(
                modified_at=modified_at,
                name=name,
                amino_acids=amino_acids,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                schema_id=schema_id,
                archive_reason=archive_reason,
                mentions=mentions,
                ids=ids,
                schema_fields=schema_fields,
                sort=sort,
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: AaSequencesPaginatedList) -> Optional[List[AaSequence]]:
            return body.aa_sequences

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, aa_sequence: AaSequenceCreate) -> AaSequence:
        response = create_aa_sequence.sync_detailed(client=self.client, json_body=aa_sequence)
        return model_from_detailed(response)

    @api_method
    def update(self, aa_sequence_id: str, aa_sequence: AaSequenceUpdate) -> AaSequence:
        response = update_aa_sequence.sync_detailed(
            client=self.client, aa_sequence_id=aa_sequence_id, json_body=aa_sequence
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, aa_sequence_ids: Iterable[str], reason: AaSequencesArchiveReason
    ) -> AaSequencesArchivalChange:
        archive_request = AaSequencesArchive(reason=reason, aa_sequence_ids=list(aa_sequence_ids))
        response = archive_aa_sequences.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, aa_sequence_ids: Iterable[str]) -> AaSequencesArchivalChange:
        unarchive_request = AaSequencesUnarchive(aa_sequence_ids=list(aa_sequence_ids))
        response = unarchive_aa_sequences.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(self, aa_sequence_ids: Iterable[str]) -> Optional[List[AaSequence]]:
        aa_sequence_id_string = ",".join(aa_sequence_ids)
        response = bulk_get_aa_sequences.sync_detailed(
            client=self.client, aa_sequence_ids=aa_sequence_id_string
        )
        aa_sequences_results = model_from_detailed(response)
        return aa_sequences_results.aa_sequences

    @api_method
    def bulk_create(self, aa_sequences: Iterable[AaSequenceBulkCreate]) -> AsyncTaskLink:
        body = AaSequencesBulkCreateRequest(list(aa_sequences))
        response = bulk_create_aa_sequences.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)
