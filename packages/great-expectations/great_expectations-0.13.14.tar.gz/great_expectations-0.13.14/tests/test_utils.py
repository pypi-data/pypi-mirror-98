import copy
import locale
import logging
import os
import random
import string
import threading
import uuid
from functools import wraps
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pytest
from dateutil.parser import parse

from great_expectations.core import (
    ExpectationConfigurationSchema,
    ExpectationSuite,
    ExpectationSuiteSchema,
    ExpectationSuiteValidationResultSchema,
    ExpectationValidationResultSchema,
)
from great_expectations.core.batch import Batch
from great_expectations.core.util import get_or_create_spark_application
from great_expectations.data_context.store import CheckpointStore, StoreBackend
from great_expectations.data_context.store.util import (
    build_checkpoint_store_using_store_backend,
    delete_checkpoint_config_from_store_backend,
    delete_config_from_store_backend,
    load_checkpoint_config_from_store_backend,
    load_config_from_store_backend,
    save_checkpoint_config_to_store_backend,
    save_config_to_store_backend,
)
from great_expectations.data_context.types.base import BaseYamlConfig, CheckpointConfig
from great_expectations.data_context.util import build_store_from_config
from great_expectations.dataset import PandasDataset, SparkDFDataset, SqlAlchemyDataset
from great_expectations.dataset.util import (
    get_sql_dialect_floating_point_infinity_value,
)
from great_expectations.execution_engine import (
    PandasExecutionEngine,
    SparkDFExecutionEngine,
)
from great_expectations.execution_engine.sparkdf_batch_data import SparkDFBatchData
from great_expectations.execution_engine.sqlalchemy_batch_data import (
    SqlAlchemyBatchData,
)
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    SqlAlchemyExecutionEngine,
)
from great_expectations.profile import ColumnsExistProfiler
from great_expectations.validator.validator import Validator

expectationValidationResultSchema = ExpectationValidationResultSchema()
expectationSuiteValidationResultSchema = ExpectationSuiteValidationResultSchema()
expectationConfigurationSchema = ExpectationConfigurationSchema()
expectationSuiteSchema = ExpectationSuiteSchema()

logger = logging.getLogger(__name__)

try:
    from sqlalchemy import create_engine
except ImportError:
    create_engine = None

try:
    from pyspark.sql import DataFrame as SparkDataFrame
except ImportError:
    SparkDataFrame = type(None)

try:
    import sqlalchemy.dialects.sqlite as sqlitetypes

    SQLITE_TYPES = {
        "VARCHAR": sqlitetypes.VARCHAR,
        "CHAR": sqlitetypes.CHAR,
        "INTEGER": sqlitetypes.INTEGER,
        "SMALLINT": sqlitetypes.SMALLINT,
        "DATETIME": sqlitetypes.DATETIME(truncate_microseconds=True),
        "DATE": sqlitetypes.DATE,
        "FLOAT": sqlitetypes.FLOAT,
        "BOOLEAN": sqlitetypes.BOOLEAN,
        "TIMESTAMP": sqlitetypes.TIMESTAMP,
    }
except ImportError:
    sqlitetypes = None
    SQLITE_TYPES = {}

try:
    import sqlalchemy.dialects.postgresql as postgresqltypes

    POSTGRESQL_TYPES = {
        "TEXT": postgresqltypes.TEXT,
        "CHAR": postgresqltypes.CHAR,
        "INTEGER": postgresqltypes.INTEGER,
        "SMALLINT": postgresqltypes.SMALLINT,
        "BIGINT": postgresqltypes.BIGINT,
        "TIMESTAMP": postgresqltypes.TIMESTAMP,
        "DATE": postgresqltypes.DATE,
        "DOUBLE_PRECISION": postgresqltypes.DOUBLE_PRECISION,
        "BOOLEAN": postgresqltypes.BOOLEAN,
        "NUMERIC": postgresqltypes.NUMERIC,
    }
except ImportError:
    postgresqltypes = None
    POSTGRESQL_TYPES = {}

try:
    import sqlalchemy.dialects.mysql as mysqltypes

    MYSQL_TYPES = {
        "TEXT": mysqltypes.TEXT,
        "CHAR": mysqltypes.CHAR,
        "INTEGER": mysqltypes.INTEGER,
        "SMALLINT": mysqltypes.SMALLINT,
        "BIGINT": mysqltypes.BIGINT,
        "DATETIME": mysqltypes.DATETIME,
        "TIMESTAMP": mysqltypes.TIMESTAMP,
        "DATE": mysqltypes.DATE,
        "FLOAT": mysqltypes.FLOAT,
        "DOUBLE": mysqltypes.DOUBLE,
        "BOOLEAN": mysqltypes.BOOLEAN,
        "TINYINT": mysqltypes.TINYINT,
    }
except ImportError:
    mysqltypes = None
    MYSQL_TYPES = {}

try:
    import sqlalchemy.dialects.mssql as mssqltypes

    MSSQL_TYPES = {
        "BIGINT": mssqltypes.BIGINT,
        "BINARY": mssqltypes.BINARY,
        "BIT": mssqltypes.BIT,
        "CHAR": mssqltypes.CHAR,
        "DATE": mssqltypes.DATE,
        "DATETIME": mssqltypes.DATETIME,
        "DATETIME2": mssqltypes.DATETIME2,
        "DATETIMEOFFSET": mssqltypes.DATETIMEOFFSET,
        "DECIMAL": mssqltypes.DECIMAL,
        "FLOAT": mssqltypes.FLOAT,
        "IMAGE": mssqltypes.IMAGE,
        "INTEGER": mssqltypes.INTEGER,
        "MONEY": mssqltypes.MONEY,
        "NCHAR": mssqltypes.NCHAR,
        "NTEXT": mssqltypes.NTEXT,
        "NUMERIC": mssqltypes.NUMERIC,
        "NVARCHAR": mssqltypes.NVARCHAR,
        "REAL": mssqltypes.REAL,
        "SMALLDATETIME": mssqltypes.SMALLDATETIME,
        "SMALLINT": mssqltypes.SMALLINT,
        "SMALLMONEY": mssqltypes.SMALLMONEY,
        "SQL_VARIANT": mssqltypes.SQL_VARIANT,
        "TEXT": mssqltypes.TEXT,
        "TIME": mssqltypes.TIME,
        "TIMESTAMP": mssqltypes.TIMESTAMP,
        "TINYINT": mssqltypes.TINYINT,
        "UNIQUEIDENTIFIER": mssqltypes.UNIQUEIDENTIFIER,
        "VARBINARY": mssqltypes.VARBINARY,
        "VARCHAR": mssqltypes.VARCHAR,
    }
except ImportError:
    mssqltypes = None
    MSSQL_TYPES = {}


class SqlAlchemyConnectionManager:
    def __init__(self):
        self.lock = threading.Lock()
        self._connections = dict()

    def get_engine(self, connection_string):
        import sqlalchemy as sa

        with self.lock:
            if connection_string not in self._connections:
                try:
                    engine = create_engine(connection_string)
                    conn = engine.connect()
                    self._connections[connection_string] = conn

                except (ImportError, sa.exc.SQLAlchemyError):
                    print(f"Unable to establish connection with {connection_string}")
                    raise

            return self._connections[connection_string]


connection_manager = SqlAlchemyConnectionManager()


def modify_locale(func):
    @wraps(func)
    def locale_wrapper(*args, **kwargs):
        old_locale = locale.setlocale(locale.LC_TIME, None)
        print(old_locale)
        # old_locale = locale.getlocale(locale.LC_TIME) Why not getlocale? not sure
        try:
            new_locale = locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
            assert new_locale == "en_US.UTF-8"
            func(*args, **kwargs)
        except Exception:
            raise
        finally:
            locale.setlocale(locale.LC_TIME, old_locale)

    return locale_wrapper


# Taken from the following stackoverflow:
# https://stackoverflow.com/questions/23549419/assert-that-two-dictionaries-are-almost-equal
def assertDeepAlmostEqual(expected, actual, *args, **kwargs):
    """
    Assert that two complex structures have almost equal contents.

    Compares lists, dicts and tuples recursively. Checks numeric values
    using pyteset.approx and checks all other values with an assertion equality statement
    Accepts additional positional and keyword arguments and pass those
    intact to pytest.approx() (that's how you specify comparison
    precision).

    """
    is_root = "__trace" not in kwargs
    trace = kwargs.pop("__trace", "ROOT")
    try:
        # if isinstance(expected, (int, float, long, complex)):
        if isinstance(expected, (int, float, complex)):
            assert expected == pytest.approx(actual, *args, **kwargs)
        elif isinstance(expected, (list, tuple, np.ndarray)):
            assert len(expected) == len(actual)
            for index in range(len(expected)):
                v1, v2 = expected[index], actual[index]
                assertDeepAlmostEqual(v1, v2, __trace=repr(index), *args, **kwargs)
        elif isinstance(expected, dict):
            assert set(expected) == set(actual)
            for key in expected:
                assertDeepAlmostEqual(
                    expected[key], actual[key], __trace=repr(key), *args, **kwargs
                )
        else:
            assert expected == actual
    except AssertionError as exc:
        exc.__dict__.setdefault("traces", []).append(trace)
        if is_root:
            trace = " -> ".join(reversed(exc.traces))
            exc = AssertionError("{}\nTRACE: {}".format(str(exc), trace))
        raise exc


def get_dataset(
    dataset_type,
    data,
    schemas=None,
    profiler=ColumnsExistProfiler,
    caching=True,
    table_name=None,
    sqlite_db_path=None,
):
    """Utility to create datasets for json-formatted tests."""
    df = pd.DataFrame(data)
    if dataset_type == "PandasDataset":
        if schemas and "pandas" in schemas:
            schema = schemas["pandas"]
            pandas_schema = {}
            for (key, value) in schema.items():
                # Note, these are just names used in our internal schemas to build datasets *for internal tests*
                # Further, some changes in pandas internal about how datetimes are created means to support pandas
                # pre- 0.25, we need to explicitly specify when we want timezone.

                # We will use timestamp for timezone-aware (UTC only) dates in our tests
                if value.lower() in ["timestamp", "datetime64[ns, tz]"]:
                    df[key] = pd.to_datetime(df[key], utc=True)
                    continue
                elif value.lower() in ["datetime", "datetime64", "datetime64[ns]"]:
                    df[key] = pd.to_datetime(df[key])
                    continue
                try:
                    type_ = np.dtype(value)
                except TypeError:
                    type_ = getattr(pd.core.dtypes.dtypes, value)
                    # If this raises AttributeError it's okay: it means someone built a bad test
                pandas_schema[key] = type_
            # pandas_schema = {key: np.dtype(value) for (key, value) in schemas["pandas"].items()}
            df = df.astype(pandas_schema)
        return PandasDataset(df, profiler=profiler, caching=caching)

    elif dataset_type == "sqlite":
        if not create_engine:
            return None

        if sqlite_db_path is not None:
            # Create a new database
            engine = create_engine(f"sqlite:////{sqlite_db_path}")
        else:
            engine = create_engine("sqlite://")
        # Add the data to the database as a new table

        sql_dtypes = {}
        if (
            schemas
            and "sqlite" in schemas
            and isinstance(engine.dialect, sqlitetypes.dialect)
        ):
            schema = schemas["sqlite"]
            sql_dtypes = {col: SQLITE_TYPES[dtype] for (col, dtype) in schema.items()}
            for col in schema:
                type_ = schema[col]
                if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                    df[col] = pd.to_numeric(df[col], downcast="signed")
                elif type_ in ["FLOAT", "DOUBLE", "DOUBLE_PRECISION"]:
                    df[col] = pd.to_numeric(df[col])
                    min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=True
                    )
                    max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=False
                    )
                    for api_schema_type in ["api_np", "api_cast"]:
                        min_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=True
                        )
                        max_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=False
                        )
                        df.replace(
                            to_replace=[min_value_api, max_value_api],
                            value=[min_value_dbms, max_value_dbms],
                            inplace=True,
                        )
                elif type_ in ["DATETIME", "TIMESTAMP"]:
                    df[col] = pd.to_datetime(df[col])

        if table_name is None:
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )
        df.to_sql(
            name=table_name,
            con=engine,
            index=False,
            dtype=sql_dtypes,
            if_exists="replace",
        )

        # Build a SqlAlchemyDataset using that database
        return SqlAlchemyDataset(
            table_name, engine=engine, profiler=profiler, caching=caching
        )

    elif dataset_type == "postgresql":
        if not create_engine:
            return None

        # Create a new database
        db_hostname = os.getenv("GE_TEST_LOCAL_DB_HOSTNAME", "localhost")
        engine = connection_manager.get_engine(
            f"postgresql://postgres@{db_hostname}/test_ci"
        )
        sql_dtypes = {}
        if (
            schemas
            and "postgresql" in schemas
            and isinstance(engine.dialect, postgresqltypes.dialect)
        ):
            schema = schemas["postgresql"]
            sql_dtypes = {
                col: POSTGRESQL_TYPES[dtype] for (col, dtype) in schema.items()
            }
            for col in schema:
                type_ = schema[col]
                if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                    df[col] = pd.to_numeric(df[col], downcast="signed")
                elif type_ in ["FLOAT", "DOUBLE", "DOUBLE_PRECISION"]:
                    df[col] = pd.to_numeric(df[col])
                    min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=True
                    )
                    max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=False
                    )
                    for api_schema_type in ["api_np", "api_cast"]:
                        min_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=True
                        )
                        max_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=False
                        )
                        df.replace(
                            to_replace=[min_value_api, max_value_api],
                            value=[min_value_dbms, max_value_dbms],
                            inplace=True,
                        )
                elif type_ in ["DATETIME", "TIMESTAMP"]:
                    df[col] = pd.to_datetime(df[col])

        if table_name is None:
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )
        df.to_sql(
            name=table_name,
            con=engine,
            index=False,
            dtype=sql_dtypes,
            if_exists="replace",
        )

        # Build a SqlAlchemyDataset using that database
        return SqlAlchemyDataset(
            table_name, engine=engine, profiler=profiler, caching=caching
        )

    elif dataset_type == "mysql":
        if not create_engine:
            return None

        db_hostname = os.getenv("GE_TEST_LOCAL_DB_HOSTNAME", "localhost")
        engine = create_engine(f"mysql+pymysql://root@{db_hostname}/test_ci")

        sql_dtypes = {}
        if (
            schemas
            and "mysql" in schemas
            and isinstance(engine.dialect, mysqltypes.dialect)
        ):
            schema = schemas["mysql"]
            sql_dtypes = {col: MYSQL_TYPES[dtype] for (col, dtype) in schema.items()}
            for col in schema:
                type_ = schema[col]
                if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                    df[col] = pd.to_numeric(df[col], downcast="signed")
                elif type_ in ["FLOAT", "DOUBLE", "DOUBLE_PRECISION"]:
                    df[col] = pd.to_numeric(df[col])
                    min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=True
                    )
                    max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=False
                    )
                    for api_schema_type in ["api_np", "api_cast"]:
                        min_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=True
                        )
                        max_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=False
                        )
                        df.replace(
                            to_replace=[min_value_api, max_value_api],
                            value=[min_value_dbms, max_value_dbms],
                            inplace=True,
                        )
                elif type_ in ["DATETIME", "TIMESTAMP"]:
                    df[col] = pd.to_datetime(df[col])

        if table_name is None:
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )
        df.to_sql(
            name=table_name,
            con=engine,
            index=False,
            dtype=sql_dtypes,
            if_exists="replace",
        )

        # Will - 20210126
        # For mysql we want our tests to know when a temp_table is referred to more than once in the
        # same query. This has caused problems in expectations like expect_column_values_to_be_unique().
        # Here we instantiate a SqlAlchemyDataset with a custom_sql, which causes a temp_table to be created,
        # rather than referring the table by name.
        custom_sql = "SELECT * FROM " + table_name
        return SqlAlchemyDataset(
            custom_sql=custom_sql, engine=engine, profiler=profiler, caching=caching
        )

    elif dataset_type == "mssql":
        if not create_engine:
            return None

        db_hostname = os.getenv("GE_TEST_LOCAL_DB_HOSTNAME", "localhost")
        engine = create_engine(
            f"mssql+pyodbc://sa:ReallyStrongPwd1234%^&*@{db_hostname}:1433/test_ci?"
            "driver=ODBC Driver 17 for SQL Server&charset=utf8&autocommit=true",
            # echo=True,
        )

        # If "autocommit" is not desired to be on by default, then use the following pattern when explicit "autocommit"
        # is desired (e.g., for temporary tables, "autocommit" is off by default, so the override option may be useful).
        # engine.execute(sa.text(sql_query_string).execution_options(autocommit=True))

        sql_dtypes = {}
        if (
            schemas
            and dataset_type in schemas
            and isinstance(engine.dialect, mssqltypes.dialect)
        ):
            schema = schemas[dataset_type]
            sql_dtypes = {col: MSSQL_TYPES[dtype] for (col, dtype) in schema.items()}
            for col in schema:
                type_ = schema[col]
                if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                    df[col] = pd.to_numeric(df[col], downcast="signed")
                elif type_ in ["FLOAT"]:
                    df[col] = pd.to_numeric(df[col])
                    min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=True
                    )
                    max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                        schema=dataset_type, negative=False
                    )
                    for api_schema_type in ["api_np", "api_cast"]:
                        min_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=True
                        )
                        max_value_api = get_sql_dialect_floating_point_infinity_value(
                            schema=api_schema_type, negative=False
                        )
                        df.replace(
                            to_replace=[min_value_api, max_value_api],
                            value=[min_value_dbms, max_value_dbms],
                            inplace=True,
                        )
                elif type_ in ["DATETIME", "TIMESTAMP"]:
                    df[col] = pd.to_datetime(df[col])

        if table_name is None:
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )
        df.to_sql(
            name=table_name,
            con=engine,
            index=False,
            dtype=sql_dtypes,
            if_exists="replace",
        )

        # Build a SqlAlchemyDataset using that database
        return SqlAlchemyDataset(
            table_name, engine=engine, profiler=profiler, caching=caching
        )

    elif dataset_type == "SparkDFDataset":
        import pyspark.sql.types as sparktypes

        SPARK_TYPES = {
            "StringType": sparktypes.StringType,
            "IntegerType": sparktypes.IntegerType,
            "LongType": sparktypes.LongType,
            "DateType": sparktypes.DateType,
            "TimestampType": sparktypes.TimestampType,
            "FloatType": sparktypes.FloatType,
            "DoubleType": sparktypes.DoubleType,
            "BooleanType": sparktypes.BooleanType,
            "DataType": sparktypes.DataType,
            "NullType": sparktypes.NullType,
        }
        spark = get_or_create_spark_application(
            spark_config={
                "spark.sql.catalogImplementation": "hive",
                "spark.executor.memory": "450m",
                # "spark.driver.allowMultipleContexts": "true",  # This directive does not appear to have any effect.
            }
        )
        # We need to allow null values in some column types that do not support them natively, so we skip
        # use of df in this case.
        data_reshaped = list(
            zip(*[v for _, v in data.items()])
        )  # create a list of rows
        if schemas and "spark" in schemas:
            schema = schemas["spark"]
            # sometimes first method causes Spark to throw a TypeError
            try:
                spark_schema = sparktypes.StructType(
                    [
                        sparktypes.StructField(
                            column, SPARK_TYPES[schema[column]](), True
                        )
                        for column in schema
                    ]
                )
                # We create these every time, which is painful for testing
                # However nuance around null treatment as well as the desire
                # for real datetime support in tests makes this necessary
                data = copy.deepcopy(data)
                if "ts" in data:
                    print(data)
                    print(schema)
                for col in schema:
                    type_ = schema[col]
                    if type_ in ["IntegerType", "LongType"]:
                        # Ints cannot be None...but None can be valid in Spark (as Null)
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(int(val))
                        data[col] = vals
                    elif type_ in ["FloatType", "DoubleType"]:
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(float(val))
                        data[col] = vals
                    elif type_ in ["DateType", "TimestampType"]:
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(parse(val))
                        data[col] = vals
                # Do this again, now that we have done type conversion using the provided schema
                data_reshaped = list(
                    zip(*[v for _, v in data.items()])
                )  # create a list of rows
                spark_df = spark.createDataFrame(data_reshaped, schema=spark_schema)
            except TypeError:
                string_schema = sparktypes.StructType(
                    [
                        sparktypes.StructField(column, sparktypes.StringType())
                        for column in schema
                    ]
                )
                spark_df = spark.createDataFrame(data_reshaped, string_schema)
                for c in spark_df.columns:
                    spark_df = spark_df.withColumn(
                        c, spark_df[c].cast(SPARK_TYPES[schema[c]]())
                    )
        elif len(data_reshaped) == 0:
            # if we have an empty dataset and no schema, need to assign an arbitrary type
            columns = list(data.keys())
            spark_schema = sparktypes.StructType(
                [
                    sparktypes.StructField(column, sparktypes.StringType())
                    for column in columns
                ]
            )
            spark_df = spark.createDataFrame(data_reshaped, spark_schema)
        else:
            # if no schema provided, uses Spark's schema inference
            columns = list(data.keys())
            spark_df = spark.createDataFrame(data_reshaped, columns)
        return SparkDFDataset(spark_df, profiler=profiler, caching=caching)

    else:
        raise ValueError("Unknown dataset_type " + str(dataset_type))


def get_test_validator_with_data(
    execution_engine,
    data,
    schemas=None,
    profiler=ColumnsExistProfiler,
    caching=True,
    table_name=None,
    sqlite_db_path=None,
):
    """Utility to create datasets for json-formatted tests."""
    df = pd.DataFrame(data)
    if execution_engine == "pandas":
        if schemas and "pandas" in schemas:
            schema = schemas["pandas"]
            pandas_schema = {}
            for (key, value) in schema.items():
                # Note, these are just names used in our internal schemas to build datasets *for internal tests*
                # Further, some changes in pandas internal about how datetimes are created means to support pandas
                # pre- 0.25, we need to explicitly specify when we want timezone.

                # We will use timestamp for timezone-aware (UTC only) dates in our tests
                if value.lower() in ["timestamp", "datetime64[ns, tz]"]:
                    df[key] = pd.to_datetime(df[key], utc=True)
                    continue
                elif value.lower() in ["datetime", "datetime64", "datetime64[ns]"]:
                    df[key] = pd.to_datetime(df[key])
                    continue
                try:
                    type_ = np.dtype(value)
                except TypeError:
                    type_ = getattr(pd.core.dtypes.dtypes, value)
                    # If this raises AttributeError it's okay: it means someone built a bad test
                pandas_schema[key] = type_
            # pandas_schema = {key: np.dtype(value) for (key, value) in schemas["pandas"].items()}
            df = df.astype(pandas_schema)

        if table_name is None:
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )

        return _build_pandas_validator_with_data(df=df)

    elif execution_engine in ["sqlite", "postgresql", "mysql", "mssql"]:
        if not create_engine:
            return None
        return _build_sa_validator_with_data(
            df=df,
            sa_engine_name=execution_engine,
            schemas=schemas,
            caching=caching,
            table_name=table_name,
            sqlite_db_path=sqlite_db_path,
        )

    elif execution_engine == "spark":
        import pyspark.sql.types as sparktypes
        from pyspark.sql import SparkSession

        SPARK_TYPES = {
            "StringType": sparktypes.StringType,
            "IntegerType": sparktypes.IntegerType,
            "LongType": sparktypes.LongType,
            "DateType": sparktypes.DateType,
            "TimestampType": sparktypes.TimestampType,
            "FloatType": sparktypes.FloatType,
            "DoubleType": sparktypes.DoubleType,
            "BooleanType": sparktypes.BooleanType,
            "DataType": sparktypes.DataType,
            "NullType": sparktypes.NullType,
        }

        spark = get_or_create_spark_application(
            spark_config={
                "spark.sql.catalogImplementation": "hive",
                "spark.executor.memory": "450m",
                # "spark.driver.allowMultipleContexts": "true",  # This directive does not appear to have any effect.
            }
        )
        # We need to allow null values in some column types that do not support them natively, so we skip
        # use of df in this case.
        data_reshaped = list(
            zip(*[v for _, v in data.items()])
        )  # create a list of rows
        if schemas and "spark" in schemas:
            schema = schemas["spark"]
            # sometimes first method causes Spark to throw a TypeError
            try:
                spark_schema = sparktypes.StructType(
                    [
                        sparktypes.StructField(
                            column, SPARK_TYPES[schema[column]](), True
                        )
                        for column in schema
                    ]
                )
                # We create these every time, which is painful for testing
                # However nuance around null treatment as well as the desire
                # for real datetime support in tests makes this necessary
                data = copy.deepcopy(data)
                if "ts" in data:
                    print(data)
                    print(schema)
                for col in schema:
                    type_ = schema[col]
                    if type_ in ["IntegerType", "LongType"]:
                        # Ints cannot be None...but None can be valid in Spark (as Null)
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(int(val))
                        data[col] = vals
                    elif type_ in ["FloatType", "DoubleType"]:
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(float(val))
                        data[col] = vals
                    elif type_ in ["DateType", "TimestampType"]:
                        vals = []
                        for val in data[col]:
                            if val is None:
                                vals.append(val)
                            else:
                                vals.append(parse(val))
                        data[col] = vals
                # Do this again, now that we have done type conversion using the provided schema
                data_reshaped = list(
                    zip(*[v for _, v in data.items()])
                )  # create a list of rows
                spark_df = spark.createDataFrame(data_reshaped, schema=spark_schema)
            except TypeError:
                string_schema = sparktypes.StructType(
                    [
                        sparktypes.StructField(column, sparktypes.StringType())
                        for column in schema
                    ]
                )
                spark_df = spark.createDataFrame(data_reshaped, string_schema)
                for c in spark_df.columns:
                    spark_df = spark_df.withColumn(
                        c, spark_df[c].cast(SPARK_TYPES[schema[c]]())
                    )
        elif len(data_reshaped) == 0:
            # if we have an empty dataset and no schema, need to assign an arbitrary type
            columns = list(data.keys())
            spark_schema = sparktypes.StructType(
                [
                    sparktypes.StructField(column, sparktypes.StringType())
                    for column in columns
                ]
            )
            spark_df = spark.createDataFrame(data_reshaped, spark_schema)
        else:
            # if no schema provided, uses Spark's schema inference
            columns = list(data.keys())
            spark_df = spark.createDataFrame(data_reshaped, columns)

        if table_name is None:
            # noinspection PyUnusedLocal
            table_name = "test_data_" + "".join(
                [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
            )

        return build_spark_validator_with_data(df=spark_df, spark=spark)

    else:
        raise ValueError("Unknown dataset_type " + str(execution_engine))


def build_spark_validator_with_data(df, spark):
    if isinstance(df, pd.DataFrame):
        df = spark.createDataFrame(
            [
                tuple(
                    None if isinstance(x, (float, int)) and np.isnan(x) else x
                    for x in record.tolist()
                )
                for record in df.to_records(index=False)
            ],
            df.columns.tolist(),
        )
    batch = Batch(data=df)
    conf: List[tuple] = spark.sparkContext.getConf().getAll()
    spark_config: Dict[str, str] = dict(conf)
    execution_engine: SparkDFExecutionEngine = SparkDFExecutionEngine(
        spark_config=spark_config
    )
    execution_engine.load_batch_data(batch_id=batch.id, batch_data=df)
    return Validator(execution_engine=execution_engine, batches=(batch,))


# Builds a Spark Execution Engine
def build_spark_engine(spark, df, batch_id):
    df = spark.createDataFrame(
        [
            tuple(
                None if isinstance(x, (float, int)) and np.isnan(x) else x
                for x in record.tolist()
            )
            for record in df.to_records(index=False)
        ],
        df.columns.tolist(),
    )
    conf: List[tuple] = spark.sparkContext.getConf().getAll()
    spark_config: Dict[str, str] = dict(conf)
    execution_engine: SparkDFExecutionEngine = SparkDFExecutionEngine(
        spark_config=spark_config
    )
    execution_engine.load_batch_data(batch_id=batch_id, batch_data=df)
    return execution_engine


def _build_sa_engine(df, sa):
    eng = sa.create_engine("sqlite://", echo=False)
    df.to_sql("test", eng)
    engine = SqlAlchemyExecutionEngine(engine=eng)
    batch_data = SqlAlchemyBatchData(execution_engine=engine, table_name="test")
    batch = Batch(data=batch_data)
    engine.load_batch_data(
        batch_id=batch.batch_definition.to_id(), batch_data=batch_data
    )
    return engine


def _build_pandas_engine(df):
    batch = Batch(data=df)
    engine = PandasExecutionEngine(batch_data_dict={batch.id: batch.data})
    return engine


def _build_pandas_validator_with_data(df):
    batch = Batch(data=df)

    return Validator(execution_engine=PandasExecutionEngine(), batches=(batch,))


def _build_sa_validator_with_data(
    df, sa_engine_name, schemas=None, caching=True, table_name=None, sqlite_db_path=None
):
    dialect_classes = {
        "sqlite": sqlitetypes.dialect,
        "postgresql": postgresqltypes.dialect,
        "mysql": mysqltypes.dialect,
        "mssql": mssqltypes.dialect,
    }
    dialect_types = {
        "sqlite": SQLITE_TYPES,
        "postgresql": POSTGRESQL_TYPES,
        "mysql": MYSQL_TYPES,
        "mssql": MSSQL_TYPES,
    }
    db_hostname = os.getenv("GE_TEST_LOCAL_DB_HOSTNAME", "localhost")
    if sa_engine_name == "sqlite":
        if sqlite_db_path is not None:
            engine = create_engine(f"sqlite:////{sqlite_db_path}")
        else:
            engine = create_engine("sqlite://")
    elif sa_engine_name == "postgresql":
        engine = connection_manager.get_engine(
            f"postgresql://postgres@{db_hostname}/test_ci"
        )
    elif sa_engine_name == "mysql":
        engine = create_engine(f"mysql+pymysql://root@{db_hostname}/test_ci")
    elif sa_engine_name == "mssql":
        engine = create_engine(
            f"mssql+pyodbc://sa:ReallyStrongPwd1234%^&*@{db_hostname}:1433/test_ci?"
            "driver=ODBC Driver 17 for SQL Server&charset=utf8&autocommit=true",
            # echo=True,
        )
    else:
        engine = None

    # If "autocommit" is not desired to be on by default, then use the following pattern when explicit "autocommit"
    # is desired (e.g., for temporary tables, "autocommit" is off by default, so the override option may be useful).
    # engine.execute(sa.text(sql_query_string).execution_options(autocommit=True))

    # Add the data to the database as a new table

    sql_dtypes = {}
    if (
        schemas
        and sa_engine_name in schemas
        and isinstance(engine.dialect, dialect_classes.get(sa_engine_name))
    ):
        schema = schemas[sa_engine_name]
        sql_dtypes = {
            col: dialect_types.get(sa_engine_name)[dtype]
            for (col, dtype) in schema.items()
        }
        for col in schema:
            type_ = schema[col]
            if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                df[col] = pd.to_numeric(df[col], downcast="signed")
            elif type_ in ["FLOAT", "DOUBLE", "DOUBLE_PRECISION"]:
                df[col] = pd.to_numeric(df[col])
                min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                    schema=sa_engine_name, negative=True
                )
                max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                    schema=sa_engine_name, negative=False
                )
                for api_schema_type in ["api_np", "api_cast"]:
                    min_value_api = get_sql_dialect_floating_point_infinity_value(
                        schema=api_schema_type, negative=True
                    )
                    max_value_api = get_sql_dialect_floating_point_infinity_value(
                        schema=api_schema_type, negative=False
                    )
                    df.replace(
                        to_replace=[min_value_api, max_value_api],
                        value=[min_value_dbms, max_value_dbms],
                        inplace=True,
                    )
            elif type_ in ["DATETIME", "TIMESTAMP"]:
                df[col] = pd.to_datetime(df[col])

    if table_name is None:
        table_name = "test_data_" + "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
        )
    df.to_sql(
        name=table_name,
        con=engine,
        index=False,
        dtype=sql_dtypes,
        if_exists="replace",
    )

    # Will - 20210126
    # For mysql we want our tests to know when a temp_table is referred to more than once in the
    # same query. This has caused problems in expectations like expect_column_values_to_be_unique().
    # Here we instantiate a SqlAlchemyBatchData with a query, which causes a temp_table to be created.
    if sa_engine_name == "mysql":
        query = "SELECT * FROM " + table_name
        batch_data = SqlAlchemyBatchData(execution_engine=engine, query=query)
    else:
        batch_data = SqlAlchemyBatchData(execution_engine=engine, table_name=table_name)

    batch = Batch(data=batch_data)
    execution_engine = SqlAlchemyExecutionEngine(caching=caching, engine=engine)
    batch_data = SqlAlchemyBatchData(
        execution_engine=execution_engine, table_name=table_name
    )
    batch = Batch(data=batch_data)
    return Validator(execution_engine=execution_engine, batches=(batch,))


def candidate_getter_is_on_temporary_notimplemented_list(context, getter):
    if context in ["sqlite"]:
        return getter in ["get_column_modes", "get_column_stdev"]
    if context in ["postgresql", "mysql", "mssql"]:
        return getter in ["get_column_modes"]
    if context == "spark":
        return getter in []


def candidate_test_is_on_temporary_notimplemented_list(context, expectation_type):
    if context in ["sqlite", "postgresql", "mysql", "mssql"]:
        return expectation_type in [
            # "expect_column_to_exist",
            # "expect_table_row_count_to_be_between",
            # "expect_table_row_count_to_equal",
            # "expect_table_columns_to_match_ordered_list",
            # "expect_table_columns_to_match_set",
            # "expect_column_values_to_be_unique",
            # "expect_column_values_to_not_be_null",
            # "expect_column_values_to_be_null",
            # "expect_column_values_to_be_of_type",
            # "expect_column_values_to_be_in_type_list",
            # "expect_column_values_to_be_in_set",
            # "expect_column_values_to_not_be_in_set",
            # "expect_column_distinct_values_to_be_in_set",
            # "expect_column_distinct_values_to_equal_set",
            # "expect_column_distinct_values_to_contain_set",
            # "expect_column_values_to_be_between",
            "expect_column_values_to_be_increasing",
            "expect_column_values_to_be_decreasing",
            # "expect_column_value_lengths_to_be_between",
            # "expect_column_value_lengths_to_equal",
            # "expect_column_values_to_match_regex",
            # "expect_column_values_to_not_match_regex",
            # "expect_column_values_to_match_regex_list",
            # "expect_column_values_to_not_match_regex_list",
            # "expect_column_values_to_match_like_pattern",
            # "expect_column_values_to_not_match_like_pattern",
            # "expect_column_values_to_match_like_pattern_list",
            # "expect_column_values_to_not_match_like_pattern_list",
            "expect_column_values_to_match_strftime_format",
            "expect_column_values_to_be_dateutil_parseable",
            "expect_column_values_to_be_json_parseable",
            "expect_column_values_to_match_json_schema",
            # "expect_column_mean_to_be_between",
            # "expect_column_median_to_be_between",
            # "expect_column_quantile_values_to_be_between",
            "expect_column_stdev_to_be_between",
            # "expect_column_unique_value_count_to_be_between",
            # "expect_column_proportion_of_unique_values_to_be_between",
            "expect_column_most_common_value_to_be_in_set",
            # "expect_column_sum_to_be_between",
            # "expect_column_min_to_be_between",
            # "expect_column_max_to_be_between",
            # "expect_column_chisquare_test_p_value_to_be_greater_than",
            "expect_column_bootstrapped_ks_test_p_value_to_be_greater_than",
            # "expect_column_kl_divergence_to_be_less_than",
            "expect_column_parameterized_distribution_ks_test_p_value_to_be_greater_than",
            "expect_column_pair_values_to_be_equal",
            "expect_column_pair_values_A_to_be_greater_than_B",
            "expect_column_pair_values_to_be_in_set",
            "expect_select_column_values_to_be_unique_within_record",
            "expect_compound_columns_to_be_unique",
            "expect_multicolumn_values_to_be_unique",
            "expect_column_pair_cramers_phi_value_to_be_less_than",
            # "expect_table_row_count_to_equal_other_table",
            "expect_multicolumn_sum_to_equal",
        ]
    if context == "SparkDFDataset":
        return expectation_type in [
            # "expect_column_to_exist",
            # "expect_table_row_count_to_be_between",
            # "expect_table_row_count_to_equal",
            # "expect_table_columns_to_match_ordered_list",
            # "expect_table_columns_to_match_set",
            # "expect_column_values_to_be_unique",
            # "expect_column_values_to_not_be_null",
            # "expect_column_values_to_be_null",
            # "expect_column_values_to_be_of_type",
            # "expect_column_values_to_be_in_type_list",
            # "expect_column_values_to_be_in_set",
            # "expect_column_values_to_not_be_in_set",
            # "expect_column_distinct_values_to_be_in_set",
            # "expect_column_distinct_values_to_equal_set",
            # "expect_column_distinct_values_to_contain_set",
            # "expect_column_values_to_be_between",
            # "expect_column_values_to_be_increasing",
            # "expect_column_values_to_be_decreasing",
            # "expect_column_value_lengths_to_be_between",
            # "expect_column_value_lengths_to_equal",
            # "expect_column_values_to_match_regex",
            # "expect_column_values_to_not_match_regex",
            # "expect_column_values_to_match_regex_list",
            # "expect_column_values_to_not_match_regex_list",
            # "expect_column_values_to_match_strftime_format",
            "expect_column_values_to_be_dateutil_parseable",
            "expect_column_values_to_be_json_parseable",
            # "expect_column_values_to_match_json_schema",
            # "expect_column_mean_to_be_between",
            # "expect_column_median_to_be_between",
            # "expect_column_quantile_values_to_be_between",
            # "expect_column_stdev_to_be_between",
            # "expect_column_unique_value_count_to_be_between",
            # "expect_column_proportion_of_unique_values_to_be_between",
            # "expect_column_most_common_value_to_be_in_set",
            # "expect_column_sum_to_be_between",
            # "expect_column_min_to_be_between",
            # "expect_column_max_to_be_between",
            # "expect_column_chisquare_test_p_value_to_be_greater_than",
            "expect_column_bootstrapped_ks_test_p_value_to_be_greater_than",
            # "expect_column_kl_divergence_to_be_less_than",
            "expect_column_parameterized_distribution_ks_test_p_value_to_be_greater_than",
            # "expect_column_pair_values_to_be_equal",
            # "expect_column_pair_values_A_to_be_greater_than_B",
            # "expect_column_pair_values_to_be_in_set",
            # "expect_select_column_values_to_be_unique_within_record",
            "expect_compound_columns_to_be_unique",
            # "expect_multicolumn_values_to_be_unique",
            "expect_column_pair_cramers_phi_value_to_be_less_than",
            "expect_table_row_count_to_equal_other_table",
            # "expect_multicolumn_sum_to_equal",
        ]
    if context == "PandasDataset":
        return expectation_type in [
            "expect_table_row_count_to_equal_other_table",
        ]
    return False


def evaluate_json_test(data_asset, expectation_type, test):
    """
    This method will evaluate the result of a test build using the Great Expectations json test format.

    NOTE: Tests can be suppressed for certain data types if the test contains the Key 'suppress_test_for' with a list
        of DataAsset types to suppress, such as ['SQLAlchemy', 'Pandas'].

    :param data_asset: (DataAsset) A great expectations DataAsset
    :param expectation_type: (string) the name of the expectation to be run using the test input
    :param test: (dict) a dictionary containing information for the test to be run. The dictionary must include:
        - title: (string) the name of the test
        - exact_match_out: (boolean) If true, match the 'out' dictionary exactly against the result of the expectation
        - in: (dict or list) a dictionary of keyword arguments to use to evaluate the expectation or a list of positional arguments
        - out: (dict) the dictionary keys against which to make assertions. Unless exact_match_out is true, keys must\
            come from the following list:
              - success
              - observed_value
              - unexpected_index_list
              - unexpected_list
              - details
              - traceback_substring (if present, the string value will be expected as a substring of the exception_traceback)
    :return: None. asserts correctness of results.
    """

    data_asset.set_default_expectation_argument("result_format", "COMPLETE")
    data_asset.set_default_expectation_argument("include_config", False)

    if "title" not in test:
        raise ValueError("Invalid test configuration detected: 'title' is required.")

    if "exact_match_out" not in test:
        raise ValueError(
            "Invalid test configuration detected: 'exact_match_out' is required."
        )

    if "in" not in test:
        raise ValueError("Invalid test configuration detected: 'in' is required.")

    if "out" not in test:
        raise ValueError("Invalid test configuration detected: 'out' is required.")

    # Support tests with positional arguments
    if isinstance(test["in"], list):
        result = getattr(data_asset, expectation_type)(*test["in"])
    # As well as keyword arguments
    else:
        result = getattr(data_asset, expectation_type)(**test["in"])

    check_json_test_result(test=test, result=result, data_asset=data_asset)


def evaluate_json_test_cfe(validator, expectation_type, test):
    """
    This method will evaluate the result of a test build using the Great Expectations json test format.

    NOTE: Tests can be suppressed for certain data types if the test contains the Key 'suppress_test_for' with a list
        of DataAsset types to suppress, such as ['SQLAlchemy', 'Pandas'].

    :param data_asset: (DataAsset) A great expectations DataAsset
    :param expectation_type: (string) the name of the expectation to be run using the test input
    :param test: (dict) a dictionary containing information for the test to be run. The dictionary must include:
        - title: (string) the name of the test
        - exact_match_out: (boolean) If true, match the 'out' dictionary exactly against the result of the expectation
        - in: (dict or list) a dictionary of keyword arguments to use to evaluate the expectation or a list of positional arguments
        - out: (dict) the dictionary keys against which to make assertions. Unless exact_match_out is true, keys must\
            come from the following list:
              - success
              - observed_value
              - unexpected_index_list
              - unexpected_list
              - details
              - traceback_substring (if present, the string value will be expected as a substring of the exception_traceback)
    :return: None. asserts correctness of results.
    """
    expectation_suite = ExpectationSuite("json_test_suite")
    validator._initialize_expectations(expectation_suite=expectation_suite)
    # validator.set_default_expectation_argument("result_format", "COMPLETE")
    # validator.set_default_expectation_argument("include_config", False)

    if "title" not in test:
        raise ValueError("Invalid test configuration detected: 'title' is required.")

    if "exact_match_out" not in test:
        raise ValueError(
            "Invalid test configuration detected: 'exact_match_out' is required."
        )

    if "in" not in test:
        raise ValueError("Invalid test configuration detected: 'in' is required.")

    if "out" not in test:
        raise ValueError("Invalid test configuration detected: 'out' is required.")

    kwargs = copy.deepcopy(test["in"])

    if isinstance(test["in"], list):
        result = getattr(validator, expectation_type)(*kwargs)
    # As well as keyword arguments
    else:
        runtime_kwargs = {"result_format": "COMPLETE", "include_config": False}
        runtime_kwargs.update(kwargs)
        result = getattr(validator, expectation_type)(**runtime_kwargs)

    check_json_test_result(
        test=test,
        result=result,
        data_asset=validator.execution_engine.active_batch_data,
    )


def check_json_test_result(test, result, data_asset=None):
    # Check results
    if test["exact_match_out"] is True:
        assert result == expectationValidationResultSchema.load(test["out"])
    else:
        # Convert result to json since our tests are reading from json so cannot easily contain richer types (e.g. NaN)
        # NOTE - 20191031 - JPC - we may eventually want to change these tests as we update our view on how
        # representations, serializations, and objects should interact and how much of that is shown to the user.
        result = result.to_json_dict()
        for key, value in test["out"].items():
            # Apply our great expectations-specific test logic

            if key == "success":
                assert result["success"] == value

            elif key == "observed_value":
                if "tolerance" in test:
                    if isinstance(value, dict):
                        assert set(result["result"]["observed_value"].keys()) == set(
                            value.keys()
                        )
                        for k, v in value.items():
                            assert np.allclose(
                                result["result"]["observed_value"][k],
                                v,
                                rtol=test["tolerance"],
                            )
                    else:
                        assert np.allclose(
                            result["result"]["observed_value"],
                            value,
                            rtol=test["tolerance"],
                        )
                else:
                    assert result["result"]["observed_value"] == value

            # NOTE: This is a key used ONLY for testing cases where an expectation is legitimately allowed to return
            # any of multiple possible observed_values. expect_column_values_to_be_of_type is one such expectation.
            elif key == "observed_value_list":
                assert result["result"]["observed_value"] in value

            elif key == "unexpected_index_list":
                if isinstance(data_asset, (SqlAlchemyDataset, SparkDFDataset)):
                    pass
                elif isinstance(data_asset, (SqlAlchemyBatchData, SparkDFBatchData)):
                    pass
                else:
                    assert result["result"]["unexpected_index_list"] == value

            elif key == "unexpected_list":
                # check if value can be sorted; if so, sort so arbitrary ordering of results does not cause failure
                if (isinstance(value, list)) & (len(value) >= 1):
                    if type(value[0].__lt__(value[0])) != type(NotImplemented):
                        value = value.sort()
                        result["result"]["unexpected_list"] = result["result"][
                            "unexpected_list"
                        ].sort()

                assert result["result"]["unexpected_list"] == value, (
                    "expected "
                    + str(value)
                    + " but got "
                    + str(result["result"]["unexpected_list"])
                )

            elif key == "details":
                assert result["result"]["details"] == value

            elif key == "value_counts":
                for val_count in value:
                    assert val_count in result["result"]["details"]["value_counts"]

            elif key.startswith("observed_cdf"):
                if "x_-1" in key:
                    if key.endswith("gt"):
                        assert (
                            result["result"]["details"]["observed_cdf"]["x"][-1] > value
                        )
                    else:
                        assert (
                            result["result"]["details"]["observed_cdf"]["x"][-1]
                            == value
                        )
                elif "x_0" in key:
                    if key.endswith("lt"):
                        assert (
                            result["result"]["details"]["observed_cdf"]["x"][0] < value
                        )
                    else:
                        assert (
                            result["result"]["details"]["observed_cdf"]["x"][0] == value
                        )
                else:
                    raise ValueError(
                        "Invalid test specification: unknown key " + key + " in 'out'"
                    )

            elif key == "traceback_substring":
                assert result["exception_info"]["raised_exception"]
                assert value in result["exception_info"]["exception_traceback"], (
                    "expected to find "
                    + value
                    + " in "
                    + result["exception_info"]["exception_traceback"]
                )

            elif key == "expected_partition":
                assert np.allclose(
                    result["result"]["details"]["expected_partition"]["bins"],
                    value["bins"],
                )
                assert np.allclose(
                    result["result"]["details"]["expected_partition"]["weights"],
                    value["weights"],
                )
                if "tail_weights" in result["result"]["details"]["expected_partition"]:
                    assert np.allclose(
                        result["result"]["details"]["expected_partition"][
                            "tail_weights"
                        ],
                        value["tail_weights"],
                    )

            elif key == "observed_partition":
                assert np.allclose(
                    result["result"]["details"]["observed_partition"]["bins"],
                    value["bins"],
                )
                assert np.allclose(
                    result["result"]["details"]["observed_partition"]["weights"],
                    value["weights"],
                )
                if "tail_weights" in result["result"]["details"]["observed_partition"]:
                    assert np.allclose(
                        result["result"]["details"]["observed_partition"][
                            "tail_weights"
                        ],
                        value["tail_weights"],
                    )

            else:
                raise ValueError(
                    "Invalid test specification: unknown key " + key + " in 'out'"
                )


def safe_remove(path):
    if path is not None:
        try:
            os.remove(path)
        except OSError as e:
            print(e)


def create_files_for_regex_partitioner(
    root_directory_path: str, directory_paths: list = None, test_file_names: list = None
):
    if not directory_paths:
        return

    if not test_file_names:
        test_file_names: list = [
            "alex_20200809_1000.csv",
            "eugene_20200809_1500.csv",
            "james_20200811_1009.csv",
            "abe_20200809_1040.csv",
            "will_20200809_1002.csv",
            "james_20200713_1567.csv",
            "eugene_20201129_1900.csv",
            "will_20200810_1001.csv",
            "james_20200810_1003.csv",
            "alex_20200819_1300.csv",
        ]

    base_directories = []
    for dir_path in directory_paths:
        if dir_path is None:
            base_directories.append(dir_path)
        else:
            data_dir_path = os.path.join(root_directory_path, dir_path)
            os.makedirs(data_dir_path, exist_ok=True)
            base_dir = str(data_dir_path)
            # Put test files into the directories.
            for file_name in test_file_names:
                file_path = os.path.join(base_dir, file_name)
                with open(file_path, "w") as fp:
                    fp.writelines([f'The name of this file is: "{file_path}".\n'])
            base_directories.append(base_dir)


def create_files_in_directory(
    directory: str, file_name_list: List[str], file_content_fn=lambda: "x,y\n1,2\n2,3"
):
    subdirectories = []
    for file_name in file_name_list:
        splits = file_name.split("/")
        for i in range(1, len(splits)):
            subdirectories.append(os.path.join(*splits[:i]))
    subdirectories = set(subdirectories)

    for subdirectory in subdirectories:
        os.makedirs(os.path.join(directory, subdirectory), exist_ok=True)

    for file_name in file_name_list:
        file_path = os.path.join(directory, file_name)
        with open(file_path, "w") as f_:
            f_.write(file_content_fn())


def create_fake_data_frame():
    return pd.DataFrame(
        {
            "x": range(10),
            "y": list("ABCDEFGHIJ"),
        }
    )


def validate_uuid4(uuid_string: str) -> bool:
    """
    Validate that a UUID string is in fact a valid uuid4.
    Happily, the uuid module does the actual checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    From https://gist.github.com/ShawnMilo/7777304

    Args:
        uuid_string: string to check whether it is a valid UUID or not

    Returns:
        True if uuid_string is a valid UUID or False if not
    """
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code,
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string.replace("-", "")


def get_sqlite_temp_table_names(engine):
    result = engine.execute(
        """
SELECT
    name
FROM
    sqlite_temp_master
"""
    )
    rows = result.fetchall()
    return {row[0] for row in rows}


def build_in_memory_store_backend(
    module_name: str = "great_expectations.data_context.store",
    class_name: str = "InMemoryStoreBackend",
    **kwargs,
) -> StoreBackend:
    logger.debug("Starting data_context/store/util.py#build_in_memory_store_backend")
    store_backend_config: dict = {"module_name": module_name, "class_name": class_name}
    store_backend_config.update(**kwargs)
    return build_store_from_config(
        store_config=store_backend_config,
        module_name=module_name,
        runtime_environment=None,
    )


def build_tuple_filesystem_store_backend(
    base_directory: str,
    *,
    module_name: str = "great_expectations.data_context.store",
    class_name: str = "TupleFilesystemStoreBackend",
    **kwargs,
) -> StoreBackend:
    logger.debug(
        f"""Starting data_context/store/util.py#build_tuple_filesystem_store_backend using base_directory:
"{base_directory}"""
    )
    store_backend_config: dict = {
        "module_name": module_name,
        "class_name": class_name,
        "base_directory": base_directory,
    }
    store_backend_config.update(**kwargs)
    return build_store_from_config(
        store_config=store_backend_config,
        module_name=module_name,
        runtime_environment=None,
    )


def build_tuple_s3_store_backend(
    bucket: str,
    *,
    module_name: str = "great_expectations.data_context.store",
    class_name: str = "TupleS3StoreBackend",
    **kwargs,
) -> StoreBackend:
    logger.debug(
        f"""Starting data_context/store/util.py#build_tuple_s3_store_backend using bucket: {bucket}
        """
    )
    store_backend_config: dict = {
        "module_name": module_name,
        "class_name": class_name,
        "bucket": bucket,
    }
    store_backend_config.update(**kwargs)
    return build_store_from_config(
        store_config=store_backend_config,
        module_name=module_name,
        runtime_environment=None,
    )


def build_checkpoint_store_using_filesystem(
    store_name: str,
    base_directory: str,
    overwrite_existing: bool = False,
) -> CheckpointStore:
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    return build_checkpoint_store_using_store_backend(
        store_name=store_name,
        store_backend=store_backend_obj,
        overwrite_existing=overwrite_existing,
    )


def save_checkpoint_config_to_filesystem(
    store_name: str,
    base_directory: str,
    checkpoint_name: str,
    checkpoint_configuration: CheckpointConfig,
):
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    save_checkpoint_config_to_store_backend(
        store_name=store_name,
        store_backend=store_backend_obj,
        checkpoint_name=checkpoint_name,
        checkpoint_configuration=checkpoint_configuration,
    )


def load_checkpoint_config_from_filesystem(
    store_name: str,
    base_directory: str,
    checkpoint_name: str,
) -> CheckpointConfig:
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    return load_checkpoint_config_from_store_backend(
        store_name=store_name,
        store_backend=store_backend_obj,
        checkpoint_name=checkpoint_name,
    )


def delete_checkpoint_config_from_filesystem(
    store_name: str,
    base_directory: str,
    checkpoint_name: str,
):
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    delete_checkpoint_config_from_store_backend(
        store_name=store_name,
        store_backend=store_backend_obj,
        checkpoint_name=checkpoint_name,
    )


def save_config_to_filesystem(
    configuration_store_class_name: str,
    configuration_store_module_name: str,
    store_name: str,
    base_directory: str,
    configuration_key: str,
    configuration: BaseYamlConfig,
):
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    save_config_to_store_backend(
        class_name=configuration_store_class_name,
        module_name=configuration_store_module_name,
        store_name=store_name,
        store_backend=store_backend_obj,
        configuration_key=configuration_key,
        configuration=configuration,
    )


def load_config_from_filesystem(
    configuration_store_class_name: str,
    configuration_store_module_name: str,
    store_name: str,
    base_directory: str,
    configuration_key: str,
) -> BaseYamlConfig:
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    return load_config_from_store_backend(
        class_name=configuration_store_class_name,
        module_name=configuration_store_module_name,
        store_name=store_name,
        store_backend=store_backend_obj,
        configuration_key=configuration_key,
    )


def delete_config_from_filesystem(
    configuration_store_class_name: str,
    configuration_store_module_name: str,
    store_name: str,
    base_directory: str,
    configuration_key: str,
):
    store_config: dict = {"base_directory": base_directory}
    store_backend_obj: StoreBackend = build_tuple_filesystem_store_backend(
        **store_config
    )
    delete_config_from_store_backend(
        class_name=configuration_store_class_name,
        module_name=configuration_store_module_name,
        store_name=store_name,
        store_backend=store_backend_obj,
        configuration_key=configuration_key,
    )
