from typing import Optional, List

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class IndustrySummary:
    id: str = attr.ib()
    name: str = attr.ib()


class IndustrySummarySchema(AttrsSchema):
    class Meta:
        target = IndustrySummary
        register_as_scheme = True
