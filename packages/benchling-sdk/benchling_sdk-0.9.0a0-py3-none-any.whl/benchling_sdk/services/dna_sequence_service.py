from typing import Any, Dict, Iterable, List, Optional

from benchling_api_client.api.dna_sequences import (
    archive_dna_sequences,
    autofill_dna_sequence_parts,
    autofill_dna_sequence_translations,
    bulk_create_dna_sequences,
    bulk_get_dna_sequences,
    bulk_update_dna_sequences,
    create_dna_sequence,
    get_dna_sequence,
    list_dna_sequences,
    unarchive_dna_sequences,
    update_dna_sequence,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param, schema_fields_query_param
from benchling_sdk.models import (
    AsyncTaskLink,
    AutofillSequences,
    DnaSequence,
    DnaSequenceBulkCreate,
    DnaSequenceBulkUpdate,
    DnaSequenceCreate,
    DnaSequencesArchivalChange,
    DnaSequencesArchive,
    DnaSequencesArchiveReason,
    DnaSequencesBulkCreateRequest,
    DnaSequencesBulkUpdateRequest,
    DnaSequencesPaginatedList,
    DnaSequencesUnarchive,
    DnaSequenceUpdate,
    ListDNASequencesSort,
)
from benchling_sdk.services.base_service import BaseService


class DnaSequenceService(BaseService):
    @api_method
    def get_by_id(self, dna_sequence_id: str) -> DnaSequence:
        response = get_dna_sequence.sync_detailed(client=self.client, dna_sequence_id=dna_sequence_id)
        return model_from_detailed(response)

    @api_method
    def dna_sequences_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[ListDNASequencesSort] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        next_token: NextToken = None,
    ) -> Response[DnaSequencesPaginatedList]:
        return list_dna_sequences.sync_detailed(  # type: ignore
            client=self.client,
            modified_at=modified_at,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            mentions=mentions,
            sort=sort,
            ids=optional_array_query_param(ids),
            schema_fields=schema_fields_query_param(schema_fields),
            page_size=page_size,
            next_token=next_token,
        )

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[ListDNASequencesSort] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[DnaSequence]:
        def api_call(next_token: NextToken) -> Response[DnaSequencesPaginatedList]:
            return self.dna_sequences_page(
                modified_at=modified_at,
                name=name,
                bases=bases,
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

        def results_extractor(body: DnaSequencesPaginatedList) -> Optional[List[DnaSequence]]:
            return body.dna_sequences

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, dna_sequence: DnaSequenceCreate) -> DnaSequence:
        response = create_dna_sequence.sync_detailed(client=self.client, json_body=dna_sequence)
        return model_from_detailed(response)

    @api_method
    def update(self, dna_sequence_id: str, dna_sequence: DnaSequenceUpdate) -> DnaSequence:
        response = update_dna_sequence.sync_detailed(
            client=self.client, dna_sequence_id=dna_sequence_id, json_body=dna_sequence
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, dna_sequence_ids: Iterable[str], reason: DnaSequencesArchiveReason
    ) -> DnaSequencesArchivalChange:
        archive_request = DnaSequencesArchive(reason=reason, dna_sequence_ids=list(dna_sequence_ids))
        response = archive_dna_sequences.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, dna_sequence_ids: Iterable[str]) -> DnaSequencesArchivalChange:
        unarchive_request = DnaSequencesUnarchive(dna_sequence_ids=list(dna_sequence_ids))
        response = unarchive_dna_sequences.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(self, dna_sequence_ids: Iterable[str]) -> Optional[List[DnaSequence]]:
        dna_sequence_id_string = ",".join(dna_sequence_ids)
        response = bulk_get_dna_sequences.sync_detailed(
            client=self.client, dna_sequence_ids=dna_sequence_id_string
        )
        dna_sequences_results = model_from_detailed(response)
        return dna_sequences_results.dna_sequences

    @api_method
    def bulk_create(self, dna_sequences: Iterable[DnaSequenceBulkCreate]) -> AsyncTaskLink:
        body = DnaSequencesBulkCreateRequest(list(dna_sequences))
        response = bulk_create_dna_sequences.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def bulk_update(self, dna_sequences: Iterable[DnaSequenceBulkUpdate]) -> AsyncTaskLink:
        body = DnaSequencesBulkUpdateRequest(list(dna_sequences))
        response = bulk_update_dna_sequences.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def autofill_parts(self, dna_sequence_ids: Iterable[str]) -> AsyncTaskLink:
        body = AutofillSequences(dna_sequence_ids=list(dna_sequence_ids))
        response = autofill_dna_sequence_parts.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)

    @api_method
    def autofill_translations(self, dna_sequence_ids: Iterable[str]) -> AsyncTaskLink:
        body = AutofillSequences(dna_sequence_ids=list(dna_sequence_ids))
        response = autofill_dna_sequence_translations.sync_detailed(client=self.client, json_body=body)
        return model_from_detailed(response)
