"""
    Data models.
"""

from typing import List, Optional

# from flask_login import UserMixin
from pydantic import BaseModel


# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id

#     def get_id(self):
#         return str(self.id)


class ResultRow(BaseModel):
    """定义查询结果行的类型.

    使用过 TypedDict, dataclasses.dataclass, pydantic.dataclasses.class, 最终确定使用普通 pydantic.BaseModel .

    Example:
        {
            "rowid": 1,
            "es": 'español',
            "zh": '中文',
        }

    """

    rowid: int
    es: str
    zh: str


class QueryResponse(BaseModel):
    """定义所有查询结果的类型.

    使用过 TypedDict, dataclasses.dataclass, pydantic.dataclasses.class, 最终确定使用普通 pydantic.BaseModel .

    Example:
        {
            "count": 2,
            "duration": 1.1,  // 秒
            "page": 1,
            "total_pages": 5,
            "error": null,
            "results": [
                {
                    "rowid": 1,
                    "es": 'español1',
                    "zh": '中文1',
                },
                {
                    "rowid": 2,
                    "es": 'español2',
                    "zh": '中文2',
                }
            ]
        }

    """

    count: int
    duration: float
    page: int
    total_pages: int
    error: Optional[str]
    results: Optional[List[ResultRow]]


class UrlParams(BaseModel):
    """使用 pydantic 包装 query_all 的参数, 确保 url 参数为 int 格式.

    使用过 TypedDict, dataclasses.dataclass, pydantic.dataclasses.class, 最终确定使用普通 pydantic.BaseModel .

    Examples:
        /api/?keywords=联合国
        /api/?keywords=联合国&page=1
        /api/?keywords=联合国&language=zh&order_by=rowid&page_size=100&page=1

    """

    keywords: str
    language: str = "zh"
    order_by: str = "rank"
    page_size: int = 50
    page: int = 1
