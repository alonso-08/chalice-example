from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute,NumberAttribute

class ConceptMap(MapAttribute):
    name=UnicodeAttribute(null=False)
    value=NumberAttribute(null=False)
class ImageModel(Model):
    class Meta:
        table_name="images"

        id=UnicodeAttribute(hash_key=True)
        created_at=UnicodeAttribute(null=False)
        extension=UnicodeAttribute(null=False)
        concepts=ListAttribute(of=ConceptMap,null=True)

