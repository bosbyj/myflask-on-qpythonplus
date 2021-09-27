"""
"""
import datetime
import math
import sqlite3
from typing import Optional

import jieba
from flask import g, current_app
from sqlitefts import fts5

from unpc.models import QueryResponse, ResultRow, UrlParams

DATABASE = "unpc/tmdata.db"


class JiebaTokenizer(fts5.FTS5Tokenizer):
    def tokenize(self, text, flags=None):
        return jieba.tokenize(text, mode="search")


def register_jieba_tokenizer(conn: sqlite3.Connection):
    name: str = "jieba_tokenizer"
    tk: fts5.FTS5Tokenizer = fts5.make_fts5_tokenizer(JiebaTokenizer())
    fts5.register_tokenizer(conn, name, tk)


def get_db():
    """Flask 获取数据库的最佳实践.

    参考: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/

    Returns:
        sqlite3.Connection 对象
    """

    # 运行于 Flask 上下文之中
    try:
        db: Optional[sqlite3.Connection]
        db = getattr(g, "_database", None)
        if db is None:  # 创建数据库连接
            db = g._database = sqlite3.connect(DATABASE)
            # 创建时就注册分词器
            register_jieba_tokenizer(db)
        return db
    # 运行于 Flask 上下文之外, 用来初始化数据库
    except RuntimeError as error:
        current_app.logger.error(error)
        db = sqlite3.connect(DATABASE)
        register_jieba_tokenizer(db)
        return db


def init_db():
    """初始化Sqlite3数据库.

    数据库: tmdata.db (数据库库文件) / zh (表) / rowid (列) chinese (列) <jieba_tokenizer>
                                    / es (表) / rowid (列) spanish (列) <unicode61>

    使用时通过 JOIN 获得双语输出.

    Example:

        >>> from app import init_db
        >>> init_db()

    """

    name: str = "jieba_tokenizer"
    conn = get_db()
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE VIRTUAL TABLE es USING fts5(spanish, tokenize=unicode61)")
    conn.execute(f"CREATE VIRTUAL TABLE zh USING fts5(chinese, tokenize={name})")

    # with open('G:/TMX/es-zh_split_1/OPUS_UNPC_es_zh_500k.txt',
    with open("OPUS_UN_es_zh_64k.tmx.txt", "r", encoding="utf-8") as f:
        # lines = f.readlines(10000000)
        lines = f.readlines()

    for i, line in enumerate(lines):
        # print(line.split('\t'))
        es: str = line.strip().split("\t")[0]
        zh: str = line.strip().split("\t")[1]

        conn.execute("INSERT INTO es (spanish) VALUES(?)", (es,))
        conn.execute("INSERT INTO zh (chinese) VALUES(?)", (zh,))
        if i % 1000 == 0:
            print(i, "行已经添加")

    conn.commit()
    conn.close()


########################


def query(params: UrlParams) -> QueryResponse:
    """查询所有命中行.

    方法论是, 首先查询命中条数, 然后通过命中条数计算出页码总数 `total_pages` .
    这是最快的方法, 比下面两种方法要快

    1. 直接 results = fetchall() 然后 len(results)
    2. 使用SQL窗口函数 count(*) OVER() AS full_count
       参考: https://stackoverflow.com/questions/28888375/run-a-query-with-a-limit-offset-and-also-get-the-total-number-of-rows

    Args:
        params:             由 pydantic 封装的查询请求参数对象.

    Note:
        params.keywords:    查询关键字. 自动使用 AND 连接.
        params.language:    查询语种. 默认值 'zh', 也可以设置成 'es'.
        params.order_by:    排序方式. 默认值 'rank', 也可以设置成 'rowid', 结果以数据库行数顺序排.
        params.page_size:   每页行数. 默认值 50.
        params.page:        页码. 默认值 1.

    Returns:
        查询结果 QueryResponse 对象.

    """
    sql: str
    count: int

    conn = get_db()

    keywords = params.keywords.replace('"', '""')  # 一个双引号括起来, 强制字符串搜索
    language = params.language
    order_by = params.order_by
    page_size = params.page_size
    page = params.page

    start_time = datetime.datetime.now()

    sql = f'SELECT COUNT(*) FROM {language} WHERE {language} MATCH "{keywords}"'

    try:
        count = conn.execute(sql).fetchone()[0]  # fetchone() 返回 tuple 类型
    except sqlite3.OperationalError as error:
        return QueryResponse(
            count=0, duration=0, page=0, total_pages=0, error=str(error), results=[]
        )

    total_pages: int = math.ceil(count / page_size)
    offset: int = (page - 1) * page_size

    if language == "zh":
        sql = f"""
            SELECT
                zh.rowid,
                es.spanish,
                zh.chinese
            FROM
                zh
                LEFT JOIN es ON zh.rowid = es.rowid
            WHERE
                zh.chinese MATCH "{keywords}"
            ORDER BY
                zh.{order_by}
            LIMIT
                {page_size} OFFSET {offset}
            """
    elif language == "es":
        sql = f"""
            SELECT
                es.rowid,
                es.spanish,
                zh.chinese
            FROM
                es
                LEFT JOIN zh ON es.rowid = zh.rowid
            WHERE
                es.spanish MATCH "{keywords}"
            ORDER BY
                es.{order_by}
            LIMIT
                {page_size} OFFSET {offset}
            """

    results = conn.execute(sql).fetchall()

    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    return QueryResponse(
        count=count,
        duration=duration,
        page=page,
        total_pages=total_pages,
        error=None,
        results=[ResultRow(rowid=rowid, es=es, zh=zh) for rowid, es, zh in results],
    )


def query_count_all():
    conn = get_db()

    results = conn.execute("SELECT COUNT(*) FROM zh").fetchone()
    for r in results:
        print(r)


def query_one_highlight():
    conn = get_db()
    keywords = "美国 AND 民主"
    results = conn.execute(
        f"SELECT COUNT(*) FROM tmdata WHERE tmdata MATCH '\"zh\" : {keywords}'"
    ).fetchone()
    for r in results:
        print(r, "*-*-*-*" * 10)
    results = conn.execute(
        f"SELECT * FROM tmdata WHERE tmdata MATCH '\"zh\" : {keywords}'"
    ).fetchone()
    # results = conn.execute("SELECT COUNT(*) FROM tmdata").fetchone()
    for r in results:
        print(r)
