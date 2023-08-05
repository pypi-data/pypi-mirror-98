import os

from invenio_indexer.utils import schema_to_index
from invenio_records_rest.loaders.marshmallow import MarshmallowErrors
from invenio_search import current_search
from jsonschema import ValidationError as SchemaValidationError
from oarepo_validate import after_marshmallow_validate

from oarepo_records_draft.exceptions import FatalDraftException
from oarepo_records_draft.merge import draft_merger
from oarepo_records_draft.proxies import current_drafts
from oarepo_records_draft.types import RecordEndpointConfiguration

RUNNING_IN_TRAVIS = os.environ.get('TRAVIS', False)


@after_marshmallow_validate.connect
def after_validation(sender, record=None, context=None, result=None, error=None, **validate_kwargs):
    # update the result even if there is an error
    if validate_kwargs.get('draft_validation', False):
        if error and getattr(error, 'valid_data', None):
            r = dict(record)
            draft_merger.merge(r, error.valid_data)
            record.update(r)


class InvalidRecordAllowedMixin:

    IGNORE_MARSHMALLOW_ERRORS = True
    IGNORE_SCHEMA_ERRORS = True
    IGNORE_OTHER_ERRORS = False
    IGNORED_ERROR_HANDLER = None

    def validate(self, **kwargs):
        force_validation = kwargs.pop('force_validation', False)
        if force_validation:
            return super().validate(**kwargs)

        try:
            return super().validate(**kwargs)
        except MarshmallowErrors as e:
            if self.IGNORED_ERROR_HANDLER:
                return self.IGNORED_ERROR_HANDLER(self, e)
            if not self.IGNORE_MARSHMALLOW_ERRORS:
                raise
        except SchemaValidationError as e:
            if self.IGNORED_ERROR_HANDLER:
                return self.IGNORED_ERROR_HANDLER(self, e)
            if not self.IGNORE_SCHEMA_ERRORS:
                raise
        except Exception as e:
            if self.IGNORED_ERROR_HANDLER:
                return self.IGNORED_ERROR_HANDLER(self, e)
            if not self.IGNORE_OTHER_ERRORS:
                raise


class DraftRecordMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['oarepo:draft'] = True

    def validate(self, **kwargs):
        try:
            if 'oarepo:validity' in self:
                del self['oarepo:validity']
            if 'oarepo:draft' in self:
                del self['oarepo:draft']
            ret = super().validate(draft_validation=True, **kwargs)
            self['oarepo:validity'] = {
                'valid': True
            }
            return ret
        except FatalDraftException as e:
            if getattr(e, '__cause__', None):
                raise e.__cause__
            raise e
        except MarshmallowErrors as e:
            self.save_marshmallow_error(e)
        except SchemaValidationError as e:
            self.save_schema_error(e)
        except Exception as e:
            if RUNNING_IN_TRAVIS:
                import traceback
                traceback.print_exc()
            self.save_generic_error(e)
        finally:
            self['oarepo:draft'] = True

    def save_marshmallow_error(self, err: MarshmallowErrors):
        errors = []
        for e in err.errors:
            if e['parents']:
                errors.append(
                    {'field': '.'.join(str(x) for x in e['parents']) + '.' + str(e['field']), 'message': e['message']})
            else:
                errors.append({'field': str(e['field']), 'message': e['message']})

        self['oarepo:validity'] = {
            'valid': False,
            'errors': {
                'marshmallow': errors
            }
        }

    def save_schema_error(self, err: SchemaValidationError):
        self['oarepo:validity'] = {
            'valid': False,
            'errors': {
                'jsonschema': [{
                    'field': '.'.join(str(path_element) for path_element in err.path),
                    'message': err.message
                }]
            }
        }

    def save_generic_error(self, err):
        self['oarepo:validity'] = {
            'valid': False,
            'errors': {
                'other': str(err)
            }
        }


def record_to_index(record):
    """Get index/doc_type given a record.

    It tries to extract from `record['$schema']` the index and doc_type.
    If it fails, return the default values.

    :param record: The record object.
    :returns: Tuple (index, doc_type).
    """
    index_names = current_search.mappings.keys()
    schema = record.get('$schema', '')
    if isinstance(schema, dict):
        schema = schema.get('$ref', '')

    endpoint: RecordEndpointConfiguration = current_drafts.endpoint_for_record(record)
    if endpoint:
        return endpoint.get_index(schema), '_doc'

    index = schema_to_index(schema, index_names=index_names)[0]
    return index, '_doc'
