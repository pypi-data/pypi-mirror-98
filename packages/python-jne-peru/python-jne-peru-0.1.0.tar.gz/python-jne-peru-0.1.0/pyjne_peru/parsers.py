from .entities import EntityFactory
from .error import JNEException


class EntityParser:

    def __init__(self):
        self.entity_factory = EntityFactory

    def parse(self, json, payload_list=False, payload_type=None):
        try:
            if payload_type is None:
                return
            entity = getattr(self.entity_factory, payload_type)
        except AttributeError:
            raise JNEException(f'No entity for this payload type: {payload_type}')

        data = json.get('data')
        if payload_list:
            result = entity.parse_list(data)
        else:
            result = entity.parse(data)
        return result
