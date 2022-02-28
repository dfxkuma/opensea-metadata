from typing import List, Union, Type, Optional
import dataclasses

from tortoise.models import Model
from tortoise import fields


@dataclasses.dataclass
class Trait:
    display_type: str
    trait_type: str
    value: Union[str, int]


class AttributesField(fields.JSONField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self,
        value: Optional[List[Union[Trait, None]]],
        instance: "Union[Type[Model], Model]",
    ) -> Optional[str]:
        traits_packed = {"traits": []}
        for trait in value:
            packed_json = dataclasses.asdict(trait)
            traits_packed["traits"].append(packed_json)
        encode = super().to_db_value(value=traits_packed, instance=instance)
        return encode

    def to_python_value(
        self, value: Optional[Union[str, bytes, dict, list]]
    ) -> Optional[List[Union[Trait, None]]]:
        decode = super().to_python_value(value=value)
        traits_unpacked = []
        if not type(decode) == dict:
            return []
        for packed_trait in decode["traits"]:
            unpacked = Trait(**packed_trait)
            traits_unpacked.append(unpacked)
        return traits_unpacked


class SampleNFT(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.TextField(default="Sample NFT")
    description = fields.TextField(default="Opensea Sample NFT")
    image = fields.TextField(default="http://localhost/api/image/$id")
    external_url = fields.TextField(default="https://localhost/info/$id")
    attributes = AttributesField(default=[])
