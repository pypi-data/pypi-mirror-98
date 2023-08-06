import logging
import traceback
import uuid
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Union

import numpy as np

import great_expectations.exceptions as ge_exceptions
from great_expectations.core import ExpectationConfiguration
from great_expectations.core.util import convert_to_json_serializable
from great_expectations.exceptions.metric_exceptions import MetricProviderError
from great_expectations.execution_engine import ExecutionEngine, PandasExecutionEngine
from great_expectations.execution_engine.execution_engine import (
    MetricDomainTypes,
    MetricFunctionTypes,
    MetricPartialFunctionTypes,
)
from great_expectations.execution_engine.sparkdf_execution_engine import (
    F,
    SparkDFExecutionEngine,
)
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    OperationalError,
    SqlAlchemyExecutionEngine,
    sa,
)
from great_expectations.expectations.metrics.metric_provider import (
    MetricProvider,
    metric_partial,
)
from great_expectations.expectations.registry import (
    get_metric_provider,
    register_metric,
)
from great_expectations.validator.validation_graph import MetricConfiguration

logger = logging.getLogger(__name__)


def column_function_partial(
    engine: Type[ExecutionEngine], partial_fn_type: str = None, **kwargs
):
    """Provides engine-specific support for authing a metric_fn with a simplified signature.

    A metric function that is decorated as a column_function_partial will be called with the engine-specific column type
    and any value_kwargs associated with the Metric for which the provider function is being declared.

    Args:
        engine:
        **kwargs:

    Returns:
        An annotated metric_function which will be called with a simplified signature.

    """
    domain_type = MetricDomainTypes.COLUMN
    if issubclass(engine, PandasExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_SERIES
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type != MetricPartialFunctionTypes.MAP_SERIES:
            raise ValueError(
                "PandasExecutionEngine only supports map_series for column_function_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "PandasExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
                )

                (
                    df,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    domain_kwargs=metric_domain_kwargs, domain_type=domain_type
                )

                column_name = accessor_domain_kwargs["column"]
                try:
                    if filter_column_isnull:
                        df = df[df[column_name].notnull()]

                    values = metric_fn(
                        cls,
                        df[column_name],
                        **metric_value_kwargs,
                        _metrics=metrics,
                    )
                    return values, compute_domain_kwargs, accessor_domain_kwargs
                except KeyError:
                    raise ge_exceptions.ExecutionEngineError(
                        message=f'Error: The column "{column_name}" in BatchData does not exist.'
                    )

            return inner_func

        return wrapper

    elif issubclass(engine, SqlAlchemyExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_FN
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type not in [MetricPartialFunctionTypes.MAP_FN]:
            raise ValueError(
                "SqlAlchemyExecutionEngine only supports map_fn for column_function_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "SqlAlchemyExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
                )
                if filter_column_isnull:
                    compute_domain_kwargs = execution_engine.add_column_row_condition(
                        metric_domain_kwargs
                    )
                else:
                    # We do not copy here because if compute domain is different, it will be copied by get_compute_domain
                    compute_domain_kwargs = metric_domain_kwargs
                (
                    selectable,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    domain_kwargs=compute_domain_kwargs, domain_type=domain_type
                )
                column_name = accessor_domain_kwargs["column"]
                dialect = execution_engine.dialect_module
                column_function = metric_fn(
                    cls,
                    sa.column(column_name),
                    **metric_value_kwargs,
                    _dialect=dialect,
                    _table=selectable,
                    _metrics=metrics,
                )
                return column_function, compute_domain_kwargs, accessor_domain_kwargs

            return inner_func

        return wrapper

    elif issubclass(engine, SparkDFExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_FN
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type not in [
            MetricPartialFunctionTypes.MAP_FN,
            MetricPartialFunctionTypes.WINDOW_FN,
        ]:
            raise ValueError(
                "SparkDFExecutionEngine only supports map_fn and window_fn for column_function_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "SparkDFExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
                )

                if filter_column_isnull:
                    compute_domain_kwargs = execution_engine.add_column_row_condition(
                        metric_domain_kwargs
                    )
                else:
                    # We do not copy here because if compute domain is different, it will be copied by get_compute_domain
                    compute_domain_kwargs = metric_domain_kwargs

                (
                    data,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    domain_kwargs=compute_domain_kwargs, domain_type=domain_type
                )

                column_name = accessor_domain_kwargs["column"]
                if column_name not in data.columns:
                    raise ge_exceptions.ExecutionEngineError(
                        message=f'Error: The column "{column_name}" in BatchData does not exist.'
                    )

                column = data[column_name]
                column_function = metric_fn(
                    cls,
                    column=column,
                    **metric_value_kwargs,
                    _metrics=metrics,
                    _compute_domain_kwargs=compute_domain_kwargs,
                )
                return column_function, compute_domain_kwargs, accessor_domain_kwargs

            return inner_func

        return wrapper

    else:
        raise ValueError("Unsupported engine for column_function_partial")


def column_condition_partial(
    engine: Type[ExecutionEngine],
    partial_fn_type: Optional[Union[str, MetricPartialFunctionTypes]] = None,
    **kwargs,
):
    """Provides engine-specific support for authing a metric_fn with a simplified signature. A column_condition_partial
    must provide a map function that evalues to a boolean value; it will be used to provide supplemental metrics, such
    as the unexpected_value count, unexpected_values, and unexpected_rows.

    A metric function that is decorated as a column_condition_partial will be called with the engine-specific column type
    and any value_kwargs associated with the Metric for which the provider function is being declared.



    Args:
        engine:
        **kwargs:

    Returns:
        An annotated metric_function which will be called with a simplified signature.

    """
    domain_type = MetricDomainTypes.COLUMN
    if issubclass(engine, PandasExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_CONDITION_SERIES
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type not in [MetricPartialFunctionTypes.MAP_CONDITION_SERIES]:
            raise ValueError(
                "PandasExecutionEngine only supports map_condition_series for column_condition_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "PandasExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", True)
                )

                (
                    df,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    domain_kwargs=metric_domain_kwargs, domain_type=domain_type
                )

                column_name = accessor_domain_kwargs["column"]
                try:
                    if filter_column_isnull:
                        df = df[df[column_name].notnull()]

                    meets_expectation_series = metric_fn(
                        cls,
                        df[column_name],
                        **metric_value_kwargs,
                        _metrics=metrics,
                    )
                    return (
                        ~meets_expectation_series,
                        compute_domain_kwargs,
                        accessor_domain_kwargs,
                    )
                except KeyError:
                    raise ge_exceptions.ExecutionEngineError(
                        message=f'Error: The column "{column_name}" in BatchData does not exist.'
                    )

            return inner_func

        return wrapper

    elif issubclass(engine, SqlAlchemyExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_CONDITION_FN
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type not in [
            MetricPartialFunctionTypes.MAP_CONDITION_FN,
            MetricPartialFunctionTypes.WINDOW_CONDITION_FN,
        ]:
            raise ValueError(
                "SqlAlchemyExecutionEngine only supports map_condition_fn for column_condition_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "SqlAlchemyExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", True)
                )

                (
                    selectable,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    metric_domain_kwargs, domain_type=domain_type
                )

                column_name = accessor_domain_kwargs["column"]
                dialect = execution_engine.dialect_module
                sqlalchemy_engine = execution_engine.engine

                expected_condition = metric_fn(
                    cls,
                    sa.column(column_name),
                    **metric_value_kwargs,
                    _dialect=dialect,
                    _table=selectable,
                    _sqlalchemy_engine=sqlalchemy_engine,
                    _metrics=metrics,
                )
                if filter_column_isnull:
                    # If we "filter" (ignore) nulls then we allow null as part of our new expected condition
                    unexpected_condition = sa.and_(
                        sa.not_(sa.column(column_name).is_(None)),
                        sa.not_(expected_condition),
                    )
                else:
                    unexpected_condition = sa.not_(expected_condition)
                return (
                    unexpected_condition,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                )

            return inner_func

        return wrapper

    elif issubclass(engine, SparkDFExecutionEngine):
        if partial_fn_type is None:
            partial_fn_type = MetricPartialFunctionTypes.MAP_CONDITION_FN
        partial_fn_type = MetricPartialFunctionTypes(partial_fn_type)
        if partial_fn_type not in [
            MetricPartialFunctionTypes.MAP_CONDITION_FN,
            MetricPartialFunctionTypes.WINDOW_CONDITION_FN,
        ]:
            raise ValueError(
                "SparkDFExecutionEngine only supports map_condition_fn and window_condition_fn for column_condition_partial partial_fn_type"
            )

        def wrapper(metric_fn: Callable):
            @metric_partial(
                engine=engine,
                partial_fn_type=partial_fn_type,
                domain_type=domain_type,
                **kwargs,
            )
            @wraps(metric_fn)
            def inner_func(
                cls,
                execution_engine: "SparkDFExecutionEngine",
                metric_domain_kwargs: Dict,
                metric_value_kwargs: Dict,
                metrics: Dict[str, Any],
                runtime_configuration: Dict,
            ):
                filter_column_isnull = kwargs.get(
                    "filter_column_isnull", getattr(cls, "filter_column_isnull", True)
                )

                (
                    data,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                ) = execution_engine.get_compute_domain(
                    domain_kwargs=metric_domain_kwargs, domain_type=domain_type
                )

                column_name = accessor_domain_kwargs["column"]
                if column_name not in data.columns:
                    raise ge_exceptions.ExecutionEngineError(
                        message=f'Error: The column "{column_name}" in BatchData does not exist.'
                    )

                column = data[column_name]
                expected_condition = metric_fn(
                    cls,
                    column,
                    **metric_value_kwargs,
                    _table=data,
                    _metrics=metrics,
                    _compute_domain_kwargs=compute_domain_kwargs,
                    _accessor_domain_kwargs=accessor_domain_kwargs,
                )
                if partial_fn_type == MetricPartialFunctionTypes.WINDOW_CONDITION_FN:
                    if filter_column_isnull:
                        compute_domain_kwargs = (
                            execution_engine.add_column_row_condition(
                                compute_domain_kwargs, column_name=column_name
                            )
                        )
                    unexpected_condition = ~expected_condition
                else:
                    if filter_column_isnull:
                        unexpected_condition = column.isNotNull() & ~expected_condition
                    else:
                        unexpected_condition = ~expected_condition
                return (
                    unexpected_condition,
                    compute_domain_kwargs,
                    accessor_domain_kwargs,
                )

            return inner_func

        return wrapper
    else:
        raise ValueError("Unsupported engine for column_condition_partial")


def _pandas_map_condition_unexpected_count(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Returns unexpected count for MapExpectations"""
    return np.count_nonzero(metrics["unexpected_condition"][0])


def _pandas_column_map_condition_values(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Return values from the specified domain that match the map-style metric in the metrics dictionary."""
    (
        boolean_map_unexpected_values,
        compute_domain_kwargs,
        accessor_domain_kwargs,
    ) = metrics["unexpected_condition"]
    df, _, _ = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )

    ###
    # NOTE: 20201111 - JPC - in the map_series / map_condition_series world (pandas), we
    # currently handle filter_column_isnull differently than other map_fn / map_condition
    # cases.
    ###
    filter_column_isnull = kwargs.get(
        "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
    )

    column_name = accessor_domain_kwargs["column"]
    try:
        if filter_column_isnull:
            df = df[df[column_name].notnull()]

        if "column" in accessor_domain_kwargs:
            domain_values = df[column_name]
        else:
            raise ValueError(
                "_pandas_column_map_condition_values requires a column in accessor_domain_kwargs"
            )
    except KeyError:
        raise ge_exceptions.ExecutionEngineError(
            message=f'Error: The column "{column_name}" in BatchData does not exist.'
        )

    result_format = metric_value_kwargs["result_format"]
    if result_format["result_format"] == "COMPLETE":
        return list(domain_values[boolean_map_unexpected_values == True])
    else:
        return list(
            domain_values[boolean_map_unexpected_values == True][
                : result_format["partial_unexpected_count"]
            ]
        )


def _pandas_column_map_series_and_domain_values(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Return values from the specified domain that match the map-style metric in the metrics dictionary."""
    (
        boolean_map_unexpected_values,
        compute_domain_kwargs,
        accessor_domain_kwargs,
    ) = metrics["unexpected_condition"]
    (
        map_series,
        compute_domain_kwargs_2,
        accessor_domain_kwargs_2,
    ) = metrics["metric_partial_fn"]
    assert (
        compute_domain_kwargs == compute_domain_kwargs_2
    ), "map_series and condition must have the same compute domain"
    assert (
        accessor_domain_kwargs == accessor_domain_kwargs_2
    ), "map_series and condition must have the same accessor kwargs"
    df, _, _ = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )

    ###
    # NOTE: 20201111 - JPC - in the map_series / map_condition_series world (pandas), we
    # currently handle filter_column_isnull differently than other map_fn / map_condition
    # cases.
    ###
    filter_column_isnull = kwargs.get(
        "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
    )

    column_name = accessor_domain_kwargs["column"]
    try:
        if filter_column_isnull:
            df = df[df[column_name].notnull()]

        if "column" in accessor_domain_kwargs:
            domain_values = df[column_name]
        else:
            raise ValueError(
                "_pandas_column_map_series_and_domain_values requires a column in accessor_domain_kwargs"
            )
    except KeyError:
        raise ge_exceptions.ExecutionEngineError(
            message=f'Error: The column "{column_name}" in BatchData does not exist.'
        )

    result_format = metric_value_kwargs["result_format"]
    if result_format["result_format"] == "COMPLETE":
        return (
            list(domain_values[boolean_map_unexpected_values == True]),
            list(map_series[boolean_map_unexpected_values == True]),
        )
    else:
        return (
            list(
                domain_values[boolean_map_unexpected_values == True][
                    : result_format["partial_unexpected_count"]
                ]
            ),
            list(
                map_series[boolean_map_unexpected_values == True][
                    : result_format["partial_unexpected_count"]
                ]
            ),
        )


def _pandas_map_condition_index(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    (
        boolean_mapped_unexpected_values,
        compute_domain_kwargs,
        accessor_domain_kwargs,
    ) = metrics.get("unexpected_condition")

    df, _, _ = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )

    ###
    # NOTE: 20201111 - JPC - in the map_series / map_condition_series world (pandas), we
    # currently handle filter_column_isnull differently than other map_fn / map_condition
    # cases.
    ###
    filter_column_isnull = kwargs.get(
        "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
    )

    column_name = accessor_domain_kwargs["column"]
    try:
        if filter_column_isnull:
            df = df[df[column_name].notnull()]
    except KeyError:
        raise ge_exceptions.ExecutionEngineError(
            message=f'Error: The column "{column_name}" in BatchData does not exist.'
        )

    result_format = metric_value_kwargs["result_format"]
    if result_format["result_format"] == "COMPLETE":
        return list(df[boolean_mapped_unexpected_values].index)
    else:
        return list(
            df[boolean_mapped_unexpected_values].index[
                : result_format["partial_unexpected_count"]
            ]
        )


def _pandas_column_map_condition_value_counts(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Returns respective value counts for distinct column values"""
    (
        boolean_mapped_unexpected_values,
        compute_domain_kwargs,
        accessor_domain_kwargs,
    ) = metrics.get("unexpected_condition")

    df, _, _ = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )

    ###
    # NOTE: 20201111 - JPC - in the map_series / map_condition_series world (pandas), we
    # currently handle filter_column_isnull differently than other map_fn / map_condition
    # cases.
    ###
    filter_column_isnull = kwargs.get(
        "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
    )

    column_name = accessor_domain_kwargs["column"]
    try:
        if filter_column_isnull:
            df = df[df[column_name].notnull()]
        if "column" in accessor_domain_kwargs:
            domain_values = df[column_name]
        else:
            raise ValueError(
                "_pandas_column_map_condition_value_counts requires a column in accessor_domain_kwargs"
            )
    except KeyError:
        raise ge_exceptions.ExecutionEngineError(
            message=f'Error: The column "{column_name}" in BatchData does not exist.'
        )

    result_format = metric_value_kwargs["result_format"]
    value_counts = None
    try:
        value_counts = domain_values[boolean_mapped_unexpected_values].value_counts()
    except ValueError:
        try:
            value_counts = (
                domain_values[boolean_mapped_unexpected_values]
                .apply(tuple)
                .value_counts()
            )
        except ValueError:
            pass

    if not value_counts:
        raise ge_exceptions.MetricError("Unable to compute value counts")

    if result_format["result_format"] == "COMPLETE":
        return value_counts
    else:
        return value_counts[result_format["partial_unexpected_count"]]


def _pandas_map_condition_rows(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Return values from the specified domain (ignoring the column constraint) that match the map-style metric in the metrics dictionary."""
    (
        boolean_mapped_unexpected_values,
        compute_domain_kwargs,
        accessor_domain_kwargs,
    ) = metrics.get("unexpected_condition")

    df, _, _ = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )

    ###
    # NOTE: 20201111 - JPC - in the map_series / map_condition_series world (pandas), we
    # currently handle filter_column_isnull differently than other map_fn / map_condition
    # cases.
    ###
    filter_column_isnull = kwargs.get(
        "filter_column_isnull", getattr(cls, "filter_column_isnull", False)
    )

    column_name = accessor_domain_kwargs["column"]
    try:
        if filter_column_isnull:
            df = df[df[column_name].notnull()]
    except KeyError:
        raise ge_exceptions.ExecutionEngineError(
            message=f'Error: The column "{column_name}" in BatchData does not exist.'
        )

    result_format = metric_value_kwargs["result_format"]
    if result_format["result_format"] == "COMPLETE":
        return df[boolean_mapped_unexpected_values]
    else:
        return df[boolean_mapped_unexpected_values][
            result_format["partial_unexpected_count"]
        ]


def _sqlalchemy_map_condition_unexpected_count_aggregate_fn(
    cls,
    execution_engine: "SqlAlchemyExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Returns unexpected count for MapExpectations"""
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    return (
        sa.func.sum(
            sa.case(
                [(unexpected_condition, 1)],
                else_=0,
            )
        ),
        compute_domain_kwargs,
        accessor_domain_kwargs,
    )


def _sqlalchemy_map_condition_unexpected_count_value(
    cls,
    execution_engine: "SqlAlchemyExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """Returns unexpected count for MapExpectations. This is a *value* metric, which is useful for
    when the unexpected_condition is a window function.
    """
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (selectable, _, _,) = execution_engine.get_compute_domain(
        compute_domain_kwargs, domain_type="identity"
    )
    temp_table_name: str = f"ge_tmp_{str(uuid.uuid4())[:8]}"
    if execution_engine.dialect == "mssql":
        # mssql expects all temporary table names to have a prefix '#'
        temp_table_name = f"#{temp_table_name}"

    try:
        with execution_engine.engine.begin():
            metadata: sa.MetaData = sa.MetaData(execution_engine.engine)
            temp_table_obj: sa.Table = sa.Table(
                temp_table_name,
                metadata,
                sa.Column("condition", sa.Integer, primary_key=False, nullable=False),
            )
            temp_table_obj.create(execution_engine.engine, checkfirst=True)

            count_case_statement: List[sa.sql.elements.Label] = [
                sa.case(
                    [
                        (
                            unexpected_condition,
                            1,
                        )
                    ],
                    else_=0,
                ).label("condition")
            ]
            inner_case_query: sa.sql.dml.Insert = temp_table_obj.insert().from_select(
                count_case_statement,
                sa.select(count_case_statement).select_from(selectable),
            )
            execution_engine.engine.execute(inner_case_query)

        unexpected_count_query: sa.Select = (
            sa.select(
                [
                    sa.func.sum(sa.column("condition")).label("unexpected_count"),
                ]
            )
            .select_from(temp_table_obj)
            .alias("UnexpectedCountSubquery")
        )

        unexpected_count = execution_engine.engine.execute(
            sa.select(
                [
                    unexpected_count_query.c.unexpected_count,
                ]
            )
        ).scalar()
    except OperationalError as oe:
        exception_message: str = "An SQL execution Exception occurred.  "
        exception_traceback: str = traceback.format_exc()
        exception_message += (
            f'{type(oe).__name__}: "{str(oe)}".  Traceback: "{exception_traceback}".'
        )
        logger.error(exception_message)
        raise ge_exceptions.ExecutionEngineError(message=exception_message)

    return convert_to_json_serializable(unexpected_count)


def _sqlalchemy_column_map_condition_values(
    cls,
    execution_engine: "SqlAlchemyExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """
    Particularly for the purpose of finding unexpected values, returns all the metric values which do not meet an
    expected Expectation condition for ColumnMapExpectation Expectations.
    """
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (selectable, _, _,) = execution_engine.get_compute_domain(
        compute_domain_kwargs, domain_type="identity"
    )

    result_format = metric_value_kwargs["result_format"]
    if "column" not in accessor_domain_kwargs:
        raise ValueError(
            "_sqlalchemy_column_map_condition_values requires a column in accessor_domain_kwargs"
        )

    query = (
        sa.select(
            [sa.column(accessor_domain_kwargs.get("column")).label("unexpected_values")]
        )
        .select_from(selectable)
        .where(unexpected_condition)
    )
    if result_format["result_format"] != "COMPLETE":
        query = query.limit(result_format["partial_unexpected_count"])
    try:
        return [
            val.unexpected_values
            for val in execution_engine.engine.execute(query).fetchall()
        ]
    except OperationalError as oe:
        exception_message: str = "An SQL execution Exception occurred.  "
        exception_traceback: str = traceback.format_exc()
        exception_message += (
            f'{type(oe).__name__}: "{str(oe)}".  Traceback: "{exception_traceback}".'
        )
        logger.error(exception_message)
        raise ge_exceptions.ExecutionEngineError(message=exception_message)


def _sqlalchemy_column_map_condition_value_counts(
    cls,
    execution_engine: "SqlAlchemyExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """
    Returns value counts for all the metric values which do not meet an expected Expectation condition for instances
    of ColumnMapExpectation.
    """
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (selectable, _, _,) = execution_engine.get_compute_domain(
        compute_domain_kwargs, domain_type="identity"
    )
    if "column" not in accessor_domain_kwargs:
        raise ValueError(
            "_sqlalchemy_column_map_condition_value_counts requires a column in accessor_domain_kwargs"
        )
    column = sa.column(accessor_domain_kwargs["column"])
    try:
        return execution_engine.engine.execute(
            sa.select([column, sa.func.count(column)])
            .select_from(selectable)
            .where(unexpected_condition)
            .group_by(column)
        ).fetchall()
    except OperationalError as oe:
        exception_message: str = "An SQL execution Exception occurred.  "
        exception_traceback: str = traceback.format_exc()
        exception_message += (
            f'{type(oe).__name__}: "{str(oe)}".  Traceback: "{exception_traceback}".'
        )
        logger.error(exception_message)
        raise ge_exceptions.ExecutionEngineError(message=exception_message)


def _sqlalchemy_map_condition_rows(
    cls,
    execution_engine: "SqlAlchemyExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    """
    Returns all rows of the metric values which do not meet an expected Expectation condition for instances
    of ColumnMapExpectation.
    """
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (selectable, _, _,) = execution_engine.get_compute_domain(
        compute_domain_kwargs, domain_type="identity"
    )

    result_format = metric_value_kwargs["result_format"]
    query = (
        sa.select([sa.text("*")]).select_from(selectable).where(unexpected_condition)
    )
    if result_format["result_format"] != "COMPLETE":
        query = query.limit(result_format["partial_unexpected_count"])
    try:
        return execution_engine.engine.execute(query).fetchall()
    except OperationalError as oe:
        exception_message: str = "An SQL execution Exception occurred.  "
        exception_traceback: str = traceback.format_exc()
        exception_message += (
            f'{type(oe).__name__}: "{str(oe)}".  Traceback: "{exception_traceback}".'
        )
        logger.error(exception_message)
        raise ge_exceptions.ExecutionEngineError(message=exception_message)


def _spark_map_condition_unexpected_count_aggregate_fn(
    cls,
    execution_engine: "SparkDFExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    return (
        F.sum(F.when(unexpected_condition, 1).otherwise(0)),
        compute_domain_kwargs,
        accessor_domain_kwargs,
    )


def _spark_map_condition_unexpected_count_value(
    cls,
    execution_engine: "SparkDFExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    # fn_domain_kwargs maybe updated to reflect null filtering
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (df, _, _) = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )
    data = df.withColumn("__unexpected", unexpected_condition)
    filtered = data.filter(F.col("__unexpected") == True).drop(F.col("__unexpected"))
    return filtered.count()


def spark_column_map_condition_values(
    cls,
    execution_engine: "SparkDFExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (df, _, _) = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )
    data = df.withColumn("__unexpected", unexpected_condition)

    if "column" not in accessor_domain_kwargs:
        raise ValueError(
            "spark_column_map_condition_values requires a column in accessor_domain_kwargs"
        )
    column_name = accessor_domain_kwargs["column"]

    result_format = metric_value_kwargs["result_format"]
    filtered = data.filter(F.col("__unexpected") == True).drop(F.col("__unexpected"))
    if result_format["result_format"] == "COMPLETE":
        rows = filtered.select(F.col(column_name)).collect()
    else:
        rows = (
            filtered.select(F.col(column_name))
            .limit(result_format["partial_unexpected_count"])
            .collect()
        )
    return [row[column_name] for row in rows]


def _spark_column_map_condition_value_counts(
    cls,
    execution_engine: "SparkDFExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (df, _, _) = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )
    data = df.withColumn("__unexpected", unexpected_condition)

    if "column" not in accessor_domain_kwargs:
        raise ValueError(
            "spark_column_map_condition_values requires a column in accessor_domain_kwargs"
        )
    column_name = accessor_domain_kwargs["column"]

    result_format = metric_value_kwargs["result_format"]

    filtered = data.filter(F.col("__unexpected") == True).drop(F.col("__unexpected"))
    value_counts = filtered.groupBy(F.col(column_name)).count()
    if result_format["result_format"] == "COMPLETE":
        rows = value_counts.collect()
    else:
        rows = value_counts.collect()[: result_format["partial_unexpected_count"]]
    return rows


def _spark_map_condition_rows(
    cls,
    execution_engine: "PandasExecutionEngine",
    metric_domain_kwargs: Dict,
    metric_value_kwargs: Dict,
    metrics: Dict[str, Any],
    **kwargs,
):
    unexpected_condition, compute_domain_kwargs, accessor_domain_kwargs = metrics.get(
        "unexpected_condition"
    )
    (df, _, _) = execution_engine.get_compute_domain(
        domain_kwargs=compute_domain_kwargs, domain_type="identity"
    )
    data = df.withColumn("__unexpected", unexpected_condition)

    result_format = metric_value_kwargs["result_format"]

    filtered = data.filter(F.col("__unexpected") == True).drop(F.col("__unexpected"))
    if result_format["result_format"] == "COMPLETE":
        return filtered.collect()
    else:
        return filtered.limit(result_format["partial_unexpected_count"]).collect()


class MapMetricProvider(MetricProvider):
    condition_domain_keys = (
        "batch_id",
        "table",
        "row_condition",
        "condition_parser",
    )
    function_domain_keys = (
        "batch_id",
        "table",
        "row_condition",
        "condition_parser",
    )
    condition_value_keys = tuple()
    function_value_keys = tuple()
    filter_column_isnull = True

    @classmethod
    def _register_metric_functions(cls):
        if not hasattr(cls, "function_metric_name") and not hasattr(
            cls, "condition_metric_name"
        ):
            return

        for attr, candidate_metric_fn in cls.__dict__.items():
            if not hasattr(candidate_metric_fn, "metric_engine"):
                # This is not a metric
                continue
            metric_fn_type = getattr(candidate_metric_fn, "metric_fn_type")
            engine = candidate_metric_fn.metric_engine
            if not issubclass(engine, ExecutionEngine):
                raise ValueError(
                    "metric functions must be defined with an Execution Engine"
                )

            if metric_fn_type in [
                MetricPartialFunctionTypes.MAP_CONDITION_SERIES,
                MetricPartialFunctionTypes.MAP_CONDITION_FN,
                MetricPartialFunctionTypes.WINDOW_CONDITION_FN,
            ]:
                if not hasattr(cls, "condition_metric_name"):
                    raise ValueError(
                        "A MapMetricProvider must have a metric_condition_name to have a decorated column_condition_partial method."
                    )

                condition_provider = candidate_metric_fn
                metric_name = cls.condition_metric_name
                metric_domain_keys = cls.condition_domain_keys
                metric_value_keys = cls.condition_value_keys
                metric_definition_kwargs = getattr(
                    condition_provider, "metric_definition_kwargs", dict()
                )
                domain_type = getattr(
                    condition_provider,
                    "domain_type",
                    metric_definition_kwargs.get(
                        "domain_type", MetricDomainTypes.TABLE
                    ),
                )
                if issubclass(engine, PandasExecutionEngine):
                    register_metric(
                        metric_name=metric_name + ".condition",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=metric_value_keys,
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=condition_provider,
                        metric_fn_type=metric_fn_type,
                    )
                    register_metric(
                        metric_name=metric_name + ".unexpected_count",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=metric_value_keys,
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=_pandas_map_condition_unexpected_count,
                        metric_fn_type=MetricFunctionTypes.VALUE,
                    )
                    register_metric(
                        metric_name=metric_name + ".unexpected_index_list",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=(*metric_value_keys, "result_format"),
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=_pandas_map_condition_index,
                        metric_fn_type=MetricFunctionTypes.VALUE,
                    )
                    register_metric(
                        metric_name=metric_name + ".unexpected_rows",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=(*metric_value_keys, "result_format"),
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=_pandas_map_condition_rows,
                        metric_fn_type=MetricFunctionTypes.VALUE,
                    )
                    if domain_type == MetricDomainTypes.COLUMN:
                        register_metric(
                            metric_name=metric_name + ".unexpected_values",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_pandas_column_map_condition_values,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                        register_metric(
                            metric_name=metric_name + ".unexpected_value_counts",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_pandas_column_map_condition_value_counts,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )

                elif issubclass(engine, SqlAlchemyExecutionEngine):
                    register_metric(
                        metric_name=metric_name + ".condition",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=metric_value_keys,
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=condition_provider,
                        metric_fn_type=metric_fn_type,
                    )
                    if metric_fn_type == MetricPartialFunctionTypes.MAP_CONDITION_FN:
                        register_metric(
                            metric_name=metric_name + ".unexpected_count.aggregate_fn",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_sqlalchemy_map_condition_unexpected_count_aggregate_fn,
                            metric_fn_type=MetricPartialFunctionTypes.AGGREGATE_FN,
                        )
                        register_metric(
                            metric_name=metric_name + ".unexpected_count",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=None,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                    elif (
                        metric_fn_type == MetricPartialFunctionTypes.WINDOW_CONDITION_FN
                    ):
                        register_metric(
                            metric_name=metric_name + ".unexpected_count",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_sqlalchemy_map_condition_unexpected_count_value,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                    register_metric(
                        metric_name=metric_name + ".unexpected_rows",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=(*metric_value_keys, "result_format"),
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=_sqlalchemy_map_condition_rows,
                        metric_fn_type=MetricFunctionTypes.VALUE,
                    )
                    if domain_type == MetricDomainTypes.COLUMN:
                        register_metric(
                            metric_name=metric_name + ".unexpected_values",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_sqlalchemy_column_map_condition_values,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                        register_metric(
                            metric_name=metric_name + ".unexpected_value_counts",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_sqlalchemy_column_map_condition_value_counts,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                elif issubclass(engine, SparkDFExecutionEngine):
                    register_metric(
                        metric_name=metric_name + ".condition",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=metric_value_keys,
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=condition_provider,
                        metric_fn_type=metric_fn_type,
                    )
                    if metric_fn_type == MetricPartialFunctionTypes.MAP_CONDITION_FN:
                        register_metric(
                            metric_name=metric_name + ".unexpected_count.aggregate_fn",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_spark_map_condition_unexpected_count_aggregate_fn,
                            metric_fn_type=MetricPartialFunctionTypes.AGGREGATE_FN,
                        )
                        register_metric(
                            metric_name=metric_name + ".unexpected_count",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=None,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                    elif (
                        metric_fn_type == MetricPartialFunctionTypes.WINDOW_CONDITION_FN
                    ):
                        register_metric(
                            metric_name=metric_name + ".unexpected_count",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=metric_value_keys,
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_spark_map_condition_unexpected_count_value,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                    register_metric(
                        metric_name=metric_name + ".unexpected_rows",
                        metric_domain_keys=metric_domain_keys,
                        metric_value_keys=(*metric_value_keys, "result_format"),
                        execution_engine=engine,
                        metric_class=cls,
                        metric_provider=_spark_map_condition_rows,
                        metric_fn_type=MetricFunctionTypes.VALUE,
                    )
                    if domain_type == MetricDomainTypes.COLUMN:
                        register_metric(
                            metric_name=metric_name + ".unexpected_values",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=spark_column_map_condition_values,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )
                        register_metric(
                            metric_name=metric_name + ".unexpected_value_counts",
                            metric_domain_keys=metric_domain_keys,
                            metric_value_keys=(*metric_value_keys, "result_format"),
                            execution_engine=engine,
                            metric_class=cls,
                            metric_provider=_spark_column_map_condition_value_counts,
                            metric_fn_type=MetricFunctionTypes.VALUE,
                        )

            elif metric_fn_type in [
                MetricPartialFunctionTypes.MAP_SERIES,
                MetricPartialFunctionTypes.MAP_FN,
                MetricPartialFunctionTypes.WINDOW_FN,
            ]:
                if not hasattr(cls, "function_metric_name"):
                    raise ValueError(
                        "A MapMetricProvider must have a function_metric_name to have a decorated column_function_partial method."
                    )
                map_function_provider = candidate_metric_fn
                metric_name = cls.function_metric_name
                metric_domain_keys = cls.function_domain_keys
                metric_value_keys = cls.function_value_keys
                register_metric(
                    metric_name=metric_name + ".map",
                    metric_domain_keys=metric_domain_keys,
                    metric_value_keys=metric_value_keys,
                    execution_engine=engine,
                    metric_class=cls,
                    metric_provider=map_function_provider,
                    metric_fn_type=metric_fn_type,
                )

    @classmethod
    def _get_evaluation_dependencies(
        cls,
        metric: MetricConfiguration,
        configuration: Optional[ExpectationConfiguration] = None,
        execution_engine: Optional[ExecutionEngine] = None,
        runtime_configuration: Optional[dict] = None,
    ):
        metric_name = metric.metric_name
        base_metric_value_kwargs = {
            k: v for k, v in metric.metric_value_kwargs.items() if k != "result_format"
        }
        dependencies = dict()

        metric_suffix = ".unexpected_count"
        if metric_name.endswith(metric_suffix):
            try:
                _ = get_metric_provider(metric_name + ".aggregate_fn", execution_engine)
                has_aggregate_fn = True
            except MetricProviderError:
                has_aggregate_fn = False
            if has_aggregate_fn:
                dependencies["metric_partial_fn"] = MetricConfiguration(
                    metric_name + ".aggregate_fn",
                    metric.metric_domain_kwargs,
                    base_metric_value_kwargs,
                )
            else:
                dependencies["unexpected_condition"] = MetricConfiguration(
                    metric_name[: -len(metric_suffix)] + ".condition",
                    metric.metric_domain_kwargs,
                    base_metric_value_kwargs,
                )

        # MapMetric uses the condition to build unexpected_count.aggregate_fn as well
        metric_suffix = ".unexpected_count.aggregate_fn"
        if metric_name.endswith(metric_suffix):
            dependencies["unexpected_condition"] = MetricConfiguration(
                metric_name[: -len(metric_suffix)] + ".condition",
                metric.metric_domain_kwargs,
                base_metric_value_kwargs,
            )

        for metric_suffix in [
            ".unexpected_values",
            ".unexpected_value_counts",
            ".unexpected_index_list",
            ".unexpected_rows",
        ]:
            if metric_name.endswith(metric_suffix):
                dependencies["unexpected_condition"] = MetricConfiguration(
                    metric_name[: -len(metric_suffix)] + ".condition",
                    metric.metric_domain_kwargs,
                    base_metric_value_kwargs,
                )

        try:
            _ = get_metric_provider(metric_name + ".map", execution_engine)
            dependencies["metric_map_fn"] = MetricConfiguration(
                metric_name + ".map",
                metric.metric_domain_kwargs,
                metric.metric_value_kwargs,
            )
        except MetricProviderError:
            pass

        return dependencies


class ColumnMapMetricProvider(MapMetricProvider):
    condition_domain_keys = (
        "batch_id",
        "table",
        "column",
        "row_condition",
        "condition_parser",
    )
    function_domain_keys = (
        "batch_id",
        "table",
        "column",
        "row_condition",
        "condition_parser",
    )
    condition_value_keys = tuple()
    function_value_keys = tuple()
