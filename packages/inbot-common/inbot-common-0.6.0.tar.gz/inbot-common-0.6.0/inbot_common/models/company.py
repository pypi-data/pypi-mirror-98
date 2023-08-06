from typing import Optional, List

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class CompanySummary:
    id: str = attr.ib()
    name: str = attr.ib()
    profile_url: str = attr.ib()
    business_id_fi: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    employee_names: List[str] = attr.ib(factory=list)


class CompanySummarySchema(AttrsSchema):
    class Meta:
        target = CompanySummary
        register_as_scheme = True
