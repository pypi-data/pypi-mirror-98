# Utility methods for dealing with DataConnector objects

import copy
import logging
import os
import re
import sre_constants
import sre_parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

import great_expectations.exceptions as ge_exceptions
from great_expectations.core.batch import BatchDefinition, BatchRequestBase
from great_expectations.core.id_dict import (
    PartitionDefinition,
    PartitionDefinitionSubset,
)
from great_expectations.data_context.util import instantiate_class_from_config
from great_expectations.datasource.data_connector.sorter import Sorter
from great_expectations.execution_engine.sqlalchemy_batch_data import (
    SqlAlchemyBatchData,
)

logger = logging.getLogger(__name__)

try:
    import pyspark
    import pyspark.sql as pyspark_sql
except ImportError:
    pyspark = None
    pyspark_sql = None
    logger.debug(
        "Unable to load pyspark and pyspark.sql; install optional spark dependency for support."
    )


DEFAULT_DATA_ASSET_NAME: str = "DEFAULT_ASSET_NAME"


def batch_definition_matches_batch_request(
    batch_definition: BatchDefinition,
    batch_request: BatchRequestBase,
) -> bool:
    assert isinstance(batch_definition, BatchDefinition)
    assert isinstance(batch_request, BatchRequestBase)

    if (
        batch_request.datasource_name
        and batch_request.datasource_name != batch_definition.datasource_name
    ):
        return False
    if (
        batch_request.data_connector_name
        and batch_request.data_connector_name != batch_definition.data_connector_name
    ):
        return False
    if (
        batch_request.data_asset_name
        and batch_request.data_asset_name != batch_definition.data_asset_name
    ):
        return False

    if batch_request.partition_request:
        batch_identifiers: Any = batch_request.partition_request.get(
            "batch_identifiers"
        )
        if batch_identifiers:
            if not isinstance(batch_identifiers, dict):
                return False
            for key in batch_identifiers.keys():
                if not (
                    key in batch_definition.partition_definition
                    and batch_definition.partition_definition[key]
                    == batch_identifiers[key]
                ):
                    return False
    return True


def map_data_reference_string_to_batch_definition_list_using_regex(
    datasource_name: str,
    data_connector_name: str,
    data_reference: str,
    regex_pattern: str,
    group_names: List[str],
    data_asset_name: Optional[str] = None,
) -> Optional[List[BatchDefinition]]:
    processed_data_reference: Optional[
        Tuple[str, PartitionDefinitionSubset]
    ] = convert_data_reference_string_to_partition_definition_using_regex(
        data_reference=data_reference,
        regex_pattern=regex_pattern,
        group_names=group_names,
    )
    if processed_data_reference is None:
        return None
    data_asset_name_from_partition_definition: str = processed_data_reference[0]
    partition_definition: PartitionDefinitionSubset = processed_data_reference[1]
    if data_asset_name is None:
        data_asset_name = data_asset_name_from_partition_definition

    return [
        BatchDefinition(
            datasource_name=datasource_name,
            data_connector_name=data_connector_name,
            data_asset_name=data_asset_name,
            partition_definition=PartitionDefinition(partition_definition),
        )
    ]


def convert_data_reference_string_to_partition_definition_using_regex(
    data_reference: str,
    regex_pattern: str,
    group_names: List[str],
) -> Optional[Tuple[str, PartitionDefinitionSubset]]:
    # noinspection PyUnresolvedReferences
    matches: Optional[re.Match] = re.match(regex_pattern, data_reference)
    if matches is None:
        return None
    groups: list = list(matches.groups())
    partition_definition: PartitionDefinitionSubset = PartitionDefinitionSubset(
        dict(zip(group_names, groups))
    )

    # TODO: <Alex>Accommodating "data_asset_name" inside partition_definition (e.g., via "group_names") is problematic; we need a better mechanism.</Alex>
    # TODO: <Alex>Update: Approach -- we can differentiate "def map_data_reference_string_to_batch_definition_list_using_regex(()" methods between ConfiguredAssetFilesystemDataConnector and InferredAssetFilesystemDataConnector so that PartitionDefinition never needs to include data_asset_name. (ref: https://superconductivedata.slack.com/archives/C01C0BVPL5Q/p1603843413329400?thread_ts=1603842470.326800&cid=C01C0BVPL5Q)</Alex>
    data_asset_name: str = DEFAULT_DATA_ASSET_NAME
    if "data_asset_name" in partition_definition:
        data_asset_name = partition_definition.pop("data_asset_name")
    return data_asset_name, partition_definition


def map_batch_definition_to_data_reference_string_using_regex(
    batch_definition: BatchDefinition,
    regex_pattern: str,
    group_names: List[str],
) -> str:
    if not isinstance(batch_definition, BatchDefinition):
        raise TypeError(
            "batch_definition is not of an instance of type BatchDefinition"
        )

    data_asset_name: str = batch_definition.data_asset_name
    partition_definition: PartitionDefinition = batch_definition.partition_definition
    data_reference: str = (
        convert_partition_definition_to_data_reference_string_using_regex(
            data_asset_name=data_asset_name,
            partition_definition=partition_definition,
            regex_pattern=regex_pattern,
            group_names=group_names,
        )
    )
    return data_reference


# TODO: <Alex>How are we able to recover the full file path, including the file extension?  Relying on file extension being part of the regex_pattern does not work when multiple file extensions are specified as part of the regex_pattern.</Alex>
def convert_partition_definition_to_data_reference_string_using_regex(
    partition_definition: PartitionDefinition,
    regex_pattern: str,
    group_names: List[str],
    data_asset_name: Optional[str] = None,
) -> str:
    if not isinstance(
        partition_definition, (PartitionDefinitionSubset, PartitionDefinition)
    ):
        raise TypeError(
            "partition_definition is not "
            "an instance of type PartitionDefinitionSubset or PartitionDefinition"
        )

    template_arguments: dict = copy.deepcopy(partition_definition)
    # TODO: <Alex>How does "data_asset_name" factor in the computation of "converted_string"?  Does it have any effect?</Alex>
    if data_asset_name is not None:
        template_arguments["data_asset_name"] = data_asset_name

    filepath_template: str = _invert_regex_to_data_reference_template(
        regex_pattern=regex_pattern,
        group_names=group_names,
    )
    converted_string = filepath_template.format(**template_arguments)

    return converted_string


# noinspection PyUnresolvedReferences
def _invert_regex_to_data_reference_template(
    regex_pattern: str,
    group_names: List[str],
) -> str:
    """Create a string template based on a regex and corresponding list of group names.

    For example:

        filepath_template = _invert_regex_to_data_reference_template(
            regex_pattern=r"^(.+)_(\d+)_(\d+)\.csv$",
            group_names=["name", "timestamp", "price"],
        )
        filepath_template
        >> "{name}_{timestamp}_{price}.csv"

    Such templates are useful because they can be populated using string substitution:

        filepath_template.format(**{
            "name": "user_logs",
            "timestamp": "20200101",
            "price": "250",
        })
        >> "user_logs_20200101_250.csv"


    NOTE Abe 20201017: This method is almost certainly still brittle. I haven't exhaustively mapped the OPCODES in sre_constants
    """
    data_reference_template: str = ""
    group_name_index: int = 0

    num_groups = len(group_names)

    # print("-"*80)
    parsed_sre = sre_parse.parse(regex_pattern)
    for token, value in parsed_sre:
        if token == sre_constants.LITERAL:
            # Transcribe the character directly into the template
            data_reference_template += chr(value)

        elif token == sre_constants.SUBPATTERN:
            if not (group_name_index < num_groups):
                break
            # Replace the captured group with "{next_group_name}" in the template
            data_reference_template += "{" + group_names[group_name_index] + "}"
            group_name_index += 1

        elif token in [
            sre_constants.MAX_REPEAT,
            sre_constants.IN,
            sre_constants.BRANCH,
            sre_constants.ANY,
        ]:
            # Replace the uncaptured group a wildcard in the template
            data_reference_template += "*"

        elif token in [
            sre_constants.AT,
            sre_constants.ASSERT_NOT,
            sre_constants.ASSERT,
        ]:
            pass
        else:
            raise ValueError(
                f"Unrecognized regex token {token} in regex pattern {regex_pattern}."
            )

    # Collapse adjacent wildcards into a single wildcard
    data_reference_template: str = re.sub("\\*+", "*", data_reference_template)
    return data_reference_template


def normalize_directory_path(
    dir_path: str, root_directory_path: Optional[str] = None
) -> str:
    # If directory is a relative path, interpret it as relative to the root directory.
    if Path(dir_path).is_absolute() or root_directory_path is None:
        return dir_path
    else:
        return str(Path(root_directory_path).joinpath(dir_path))


def get_filesystem_one_level_directory_glob_path_list(
    base_directory_path: str, glob_directive: str
) -> List[str]:
    """
    List file names, relative to base_directory_path one level deep, with expansion specified by glob_directive.
    :param base_directory_path -- base directory path, relative to which file paths will be collected
    :param glob_directive -- glob expansion directive
    :returns -- list of relative file paths
    """
    globbed_paths = Path(base_directory_path).glob(glob_directive)
    path_list: List[str] = [
        os.path.relpath(str(posix_path), base_directory_path)
        for posix_path in globbed_paths
    ]
    return path_list


def list_s3_keys(
    s3, query_options: dict, iterator_dict: dict, recursive: bool = False
) -> str:
    """
    For InferredAssetS3DataConnector, we take bucket and prefix and search for files using RegEx at and below the level
    specified by that bucket and prefix.  However, for ConfiguredAssetS3DataConnector, we take bucket and prefix and
    search for files using RegEx only at the level specified by that bucket and prefix.  This restriction for the
    ConfiguredAssetS3DataConnector is needed, because paths on S3 are comprised not only the leaf file name but the
    full path that includes both the prefix and the file name.  Otherwise, in the situations where multiple data assets
    share levels of a directory tree, matching files to data assets will not be possible, due to the path ambiguity.
    :param s3: s3 client connection
    :param query_options: s3 query attributes ("Bucket", "Prefix", "Delimiter", "MaxKeys")
    :param iterator_dict: dictionary to manage "NextContinuationToken" (if "IsTruncated" is returned from S3)
    :param recursive: True for InferredAssetS3DataConnector and False for ConfiguredAssetS3DataConnector (see above)
    :return: string valued key representing file path on S3 (full prefix and leaf file name)
    """
    if iterator_dict is None:
        iterator_dict = {}

    if "continuation_token" in iterator_dict:
        query_options.update({"ContinuationToken": iterator_dict["continuation_token"]})

    logger.debug(f"Fetching objects from S3 with query options: {query_options}")

    s3_objects_info: dict = s3.list_objects_v2(**query_options)

    if not any(key in s3_objects_info for key in ["Contents", "CommonPrefixes"]):
        raise ValueError("S3 query may not have been configured correctly.")

    if "Contents" in s3_objects_info:
        keys: List[str] = [
            item["Key"] for item in s3_objects_info["Contents"] if item["Size"] > 0
        ]
        yield from keys
    if recursive and "CommonPrefixes" in s3_objects_info:
        common_prefixes: List[Dict[str, Any]] = s3_objects_info["CommonPrefixes"]
        for prefix_info in common_prefixes:
            query_options_tmp: dict = copy.deepcopy(query_options)
            query_options_tmp.update({"Prefix": prefix_info["Prefix"]})
            # Recursively fetch from updated prefix
            yield from list_s3_keys(
                s3=s3,
                query_options=query_options_tmp,
                iterator_dict={},
                recursive=recursive,
            )
    if s3_objects_info["IsTruncated"]:
        iterator_dict["continuation_token"] = s3_objects_info["NextContinuationToken"]
        # Recursively fetch more
        yield from list_s3_keys(
            s3=s3,
            query_options=query_options,
            iterator_dict=iterator_dict,
            recursive=recursive,
        )

    if "continuation_token" in iterator_dict:
        # Make sure we clear the token once we've gotten fully through
        del iterator_dict["continuation_token"]


# TODO: <Alex>We need to move sorters and _validate_sorters_configuration() to DataConnector</Alex>
# As a rule, this method should not be in "util", but in the specific high-level "DataConnector" class, where it is
# called (and declared as private in that class).  Currently, this is "FilePathDataConnector".  However, since this
# method is also used in tests, it can remain in the present "util" module (as an exception to the above stated rule).
def build_sorters_from_config(config_list: List[Dict[str, Any]]) -> Optional[dict]:
    sorter_dict: Dict[str, Sorter] = {}
    if config_list is not None:
        for sorter_config in config_list:
            # if sorters were not configured
            if sorter_config is None:
                return None
            if "name" not in sorter_config:
                raise ValueError("Sorter config should have a name")
            sorter_name: str = sorter_config["name"]
            new_sorter: Sorter = _build_sorter_from_config(sorter_config=sorter_config)
            sorter_dict[sorter_name] = new_sorter
    return sorter_dict


def _build_sorter_from_config(sorter_config: Dict[str, Any]) -> Sorter:
    """Build a Sorter using the provided configuration and return the newly-built Sorter."""
    runtime_environment: dict = {"name": sorter_config["name"]}
    sorter: Sorter = instantiate_class_from_config(
        config=sorter_config,
        runtime_environment=runtime_environment,
        config_defaults={
            "module_name": "great_expectations.datasource.data_connector.sorter"
        },
    )
    return sorter
