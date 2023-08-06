import itertools
import logging
from typing import Callable, Dict, Optional, Union

import great_expectations.exceptions as ge_exceptions
from great_expectations.core.id_dict import PartitionDefinitionSubset
from great_expectations.util import is_int

logger = logging.getLogger(__name__)


def build_partition_query(
    partition_request_dict: Optional[
        Dict[
            str,
            Optional[
                Union[
                    int,
                    list,
                    tuple,
                    slice,
                    str,
                    Union[Dict, PartitionDefinitionSubset],
                    Callable,
                ]
            ],
        ]
    ] = None
):
    if not partition_request_dict:
        return PartitionQuery(
            custom_filter_function=None,
            batch_identifiers=None,
            index=None,
            limit=None,
        )
    partition_request_keys: set = set(partition_request_dict.keys())
    if not partition_request_keys <= PartitionQuery.RECOGNIZED_KEYS:
        raise ge_exceptions.PartitionQueryError(
            f"""Unrecognized partition_request key(s):
"{str(partition_request_keys - PartitionQuery.RECOGNIZED_KEYS)}" detected.
            """
        )
    custom_filter_function: Callable = partition_request_dict.get(
        "custom_filter_function"
    )
    if custom_filter_function and not isinstance(custom_filter_function, Callable):
        raise ge_exceptions.PartitionQueryError(
            f"""The type of a custom_filter must be a function (Python "Callable").  The type given is
"{str(type(custom_filter_function))}", which is illegal.
            """
        )
    batch_identifiers: Optional[dict] = partition_request_dict.get("batch_identifiers")
    if batch_identifiers:
        if not isinstance(batch_identifiers, dict):
            raise ge_exceptions.PartitionQueryError(
                f"""The type of a batch_identifiers must be a dictionary (Python "dict").  The type given is
"{str(type(batch_identifiers))}", which is illegal.
                """
            )
        if not all([isinstance(key, str) for key in batch_identifiers.keys()]):
            raise ge_exceptions.PartitionQueryError(
                'All partition_definition keys must strings (Python "str").'
            )
    if batch_identifiers is not None:
        batch_identifiers: PartitionDefinitionSubset = PartitionDefinitionSubset(
            batch_identifiers
        )
    index: Optional[Union[int, list, tuple, slice, str]] = partition_request_dict.get(
        "index"
    )
    limit: Optional[int] = partition_request_dict.get("limit")
    if limit and (not isinstance(limit, int) or limit < 0):
        raise ge_exceptions.PartitionQueryError(
            f"""The type of a limit must be an integer (Python "int") that is greater than or equal to 0.  The
type and value given are "{str(type(limit))}" and "{limit}", respectively, which is illegal.
            """
        )
    if index is not None and limit is not None:
        raise ge_exceptions.PartitionQueryError(
            "Only one of partition_index or limit, but not both, can be specified (specifying both is illegal)."
        )
    index = _parse_index(index=index)
    return PartitionQuery(
        custom_filter_function=custom_filter_function,
        batch_identifiers=batch_identifiers,
        limit=limit,
        index=index,
    )


def _parse_index(
    index: Optional[Union[int, list, tuple, slice, str]] = None
) -> Optional[Union[int, slice]]:
    if index is None:
        return None
    elif isinstance(index, (int, slice)):
        return index
    elif isinstance(index, (list, tuple)):
        if len(index) > 3:
            raise ge_exceptions.PartitionQueryError(
                f"""The number of partition_index slice components must be between 1 and 3 (the given number is
{len(index)}).
                """
            )
        if len(index) == 1:
            return index[0]
        if len(index) == 2:
            return slice(index[0], index[1], None)
        if len(index) == 3:
            return slice(index[0], index[1], index[2])
    elif isinstance(index, str):
        if is_int(value=index):
            return _parse_index(index=int(index))
        return _parse_index(index=[int(idx_str) for idx_str in index.split(":")])
    else:
        raise ge_exceptions.PartitionQueryError(
            f"""The type of a partition_index must be an integer (Python "int"), or a list (Python "list") or a tuple
(Python "tuple"), or a Python "slice" object, or a string that has the format of a single integer or a slice argument.
The type given is "{str(type(index))}", which is illegal.
            """
        )


class PartitionQuery:
    RECOGNIZED_KEYS: set = {
        "custom_filter_function",
        "batch_identifiers",
        "index",
        "limit",
    }

    def __init__(
        self,
        custom_filter_function: Callable = None,
        batch_identifiers: Optional[PartitionDefinitionSubset] = None,
        index: Optional[Union[int, slice]] = None,
        limit: int = None,
    ):
        self._custom_filter_function = custom_filter_function
        self._batch_identifiers = batch_identifiers
        self._index = index
        self._limit = limit

    @property
    def custom_filter_function(self) -> Callable:
        return self._custom_filter_function

    @property
    def batch_identifiers(self) -> Optional[PartitionDefinitionSubset]:
        return self._batch_identifiers

    @property
    def index(self) -> Optional[Union[int, slice]]:
        return self._index

    @property
    def limit(self) -> int:
        return self._limit

    def __repr__(self) -> str:
        doc_fields_dict: dict = {
            "custom_filter_function": self._custom_filter_function,
            "batch_identifiers": self.batch_identifiers,
            "index": self.index,
            "limit": self.limit,
        }
        return str(doc_fields_dict)

    def select_from_partition_request(self, batch_definition_list=None):
        if batch_definition_list is None:
            return []
        filter_function: Callable
        if self.custom_filter_function:
            filter_function = self.custom_filter_function
        else:
            filter_function = self.best_effort_partition_matcher()
        selected_batch_definitions = list(
            filter(
                lambda batch_definition: filter_function(
                    partition_definition=batch_definition.partition_definition,
                ),
                batch_definition_list,
            )
        )
        if self.index is None:
            selected_batch_definitions = selected_batch_definitions[: self.limit]
        else:
            if isinstance(self.index, int):
                selected_batch_definitions = [selected_batch_definitions[self.index]]
            else:
                selected_batch_definitions = list(
                    itertools.chain.from_iterable(
                        [selected_batch_definitions[self.index]]
                    )
                )
        return selected_batch_definitions

    def best_effort_partition_matcher(self) -> Callable:
        def match_partition_to_query_params(partition_definition: dict) -> bool:
            if self.batch_identifiers:
                if not partition_definition:
                    return False
                partition_definition_keys: set = set(self.batch_identifiers.keys())

                if not partition_definition_keys:
                    return False
                for key in partition_definition_keys:
                    if not (
                        key in partition_definition
                        and partition_definition[key] == self.batch_identifiers[key]
                    ):
                        return False
            return True

        return match_partition_to_query_params
