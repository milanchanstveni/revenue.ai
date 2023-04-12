from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator



class Country(Model):
    code = fields.CharField(unique=True, pk=True, max_length=5)
    name = fields.CharField(index=True, max_length=255)
    description = fields.TextField()
    region = fields.TextField()


class PriorityCode(Model):
    code = fields.CharField(unique=True, pk=True, max_length=1)
    description = fields.TextField()


CountryModel = pydantic_model_creator(Country)
PriorityCodeModel = pydantic_model_creator(PriorityCode)