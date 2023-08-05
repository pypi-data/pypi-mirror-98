# -----------------------------------------------------------------------------
#
# This file is the copyrighted property of Tableau Software and is protected
# by registered patents and other applicable U.S. and international laws and
# regulations.
#
# Unlicensed use of the contents of this file is prohibited. Please refer to
# the NOTICES.txt file for further details.
#
# -----------------------------------------------------------------------------
from ..tabledefinition import Nullability, Persistence, TableName, TableDefinition, SqlType
from ..resultschema import ResultSchema
from .dllutil import NativeTableDefinition, ConstNativeTableDefinition


class SchemaConverter:
    """ Converts between native hyper_table_definition_t and TableDefinition and ResultSchema. """

    @staticmethod
    def table_definition_from_native(native: ConstNativeTableDefinition) -> TableDefinition:
        table_def = TableDefinition(TableName(native.database_name, native.schema_name, native.table_name),
                                    persistence=Persistence._from_value(native.persistence))
        for i in range(native.column_count):
            collation = native.column_collation(i)
            if not collation:
                # C level uses empty string as default collation, but we want to return None for it
                collation = None
            type_tag = native.column_type_tag(i)
            type_oid = native.column_type_oid(i)
            modifier = native.column_type_modifier(i)
            table_def.add_column(native.column_name(i),
                                 SqlType._from_native(type_tag, type_oid, modifier),
                                 Nullability._from_bool_nullable(native.column_is_nullable(i)),
                                 collation)
        return table_def

    @staticmethod
    def table_definition_to_native(table_def: TableDefinition) -> NativeTableDefinition:
        full_name = table_def.table_name
        database_name, schema_name, table_name = full_name._unescaped_triple
        native = NativeTableDefinition.create(database_name, schema_name, table_name, table_def.persistence.value)
        for col in table_def.columns:
            native.add_column(col.name.unescaped, col.type.tag.value, col.type.internal_type_modifier, col.collation,
                              col.nullability == Nullability.NULLABLE)
        return native

    @staticmethod
    def result_schema_from_native(native: ConstNativeTableDefinition) -> ResultSchema:
        columns = []
        for i in range(native.column_count):
            type_tag = native.column_type_tag(i)
            type_oid = native.column_type_oid(i)
            modifier = native.column_type_modifier(i)
            columns.append(
                ResultSchema.Column(native.column_name(i),
                                    SqlType._from_native(type_tag, type_oid, modifier)))
        return ResultSchema(columns)
