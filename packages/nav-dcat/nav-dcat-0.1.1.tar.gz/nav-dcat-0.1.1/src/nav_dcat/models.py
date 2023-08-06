from typing import Optional, Sequence
from datetime import date, datetime
from pydantic import BaseModel

from nav_dcat import doc_fields


class ESDocument(BaseModel):
    id: str
    title: str
    description: str
    type: doc_fields.Type
    uri: str
    format: Optional[doc_fields.Type]
    modified: Optional[str] = datetime.now().isoformat()
    issued: Optional[str] = datetime.now().isoformat()
    periodicity: Optional[str] = ""
    provenance: Optional[str] = ""
    contactpoint: Optional[str] = ""
    author: Optional[str] = ""
    repo: Optional[str] = ""
    readme: Optional[str] = ""
    spatial: Optional[str] = ""
    accessRights: Optional[doc_fields.AccessRights] = doc_fields.AccessRights.INTERNAL.value
    pii: Optional[doc_fields.Pii] = doc_fields.Pii.FALSE.value
    keyword: Optional[Sequence] = []
    theme: Optional[str] = ""
    temporal: Optional[dict] = {"from": f"{date.today().year}", "to": f"{date.today().year}"}
    language: Optional[str] = "NO"
    creator: Optional[dict] = {}
    publisher: Optional[dict] = {"name": "NAV"}
    license: Optional[dict] = {}
    rights: Optional[str] = f"Copyright {date.today().year}, NAV"
