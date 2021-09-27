"""
    0.3 迁移至 Flask.
    0.2 迁移至 Django.
    0.1 原版 Bottle.
"""

# Create your views here.
import os
import re

from flask import Blueprint, jsonify, render_template

blueprint = Blueprint(
    "ccp",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/ccp",
)


#################################################################


base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "ccp_todo.txt"), "r", encoding="utf-8") as f:
    ccp = f.read()


class RegExConcordanceIndex(object):
    "Class to mimic nltk's ConcordanceIndex.print_concordance."

    def __init__(self, text):
        self._text = text
        self._regex = r"(?<=\s){0}[A-z\u00C0-\u00ff]*[^\s\.\,\?\!\(\)]*"
        self.matches_count = 0
        self.pages = 0
        self.page = 0

    def _transcribe_character(self, character):
        """过滤生成帽子字母正则"""
        transcription = {
            "a": "[a|á]",  # if
            "é": "[e|é]",  # elif ...
            "i": "[i|í]",
            "o": "[o|ó]",
            "u": "[u|ú|ü]",
            "n": "[n|ñ]",
            "c": "[c|ç]",
            "*": "[A-z\u00C0-\u00ff]+",
            None: character,  # else
        }
        return transcription.get(character, transcription[None])

    def _transcribe_keyword(self, keyword):
        """返回 正则表达式 transcribed_keyword，解决帽子字母问题"""
        keyword = keyword.lower()  # 统一成小写
        transcribed_keyword = "".join(list(map(self._transcribe_character, keyword)))
        transcribed_keyword = self._regex.format(transcribed_keyword)
        return transcribed_keyword

    def _paged_match(self, keyword, lines=50, page=1):
        """返回match对象的分页列表"""
        self.page = page

        # 因为要统计所有的match，所以不能用iterator了
        matches = list(
            re.finditer(
                self._transcribe_keyword(keyword), self._text, flags=re.M | re.I
            )
        )

        matches_count = len(matches)
        self.matches_count = matches_count

        pages = matches_count // lines + 1
        self.pages = pages

        # 分页
        if page == 1:
            if matches_count <= lines:
                return matches
            else:
                return matches[0:lines]
        elif page == pages:  # 假设109条 共3页 第3页 9条
            return matches[
                lines * (page - 1) : lines * (page - 1) + matches_count % lines
            ]
        else:  # 假设109条 共3页 第2页 50条
            return matches[lines * (page - 1) : lines * page]

    def print_concordance(self, keyword, width=250, lines=50, page=1, demarcation="b"):
        """
        Prints n <= @lines contexts for @regex with a context <= @width".
        Make @lines 0 to display all matches.
        Designate @demarcation to enclose matches in demarcating characters.
        """
        concordance = []
        matches = self._paged_match(keyword, lines=lines, page=page)
        if matches:
            for match in matches:
                start, end = match.start(), match.end()
                match_width = end - start
                remaining = (width - match_width) // 2
                if start - remaining > 0:
                    context_start = self._text[start - remaining : start]
                    #  cut the string short if it contains a newline character
                    # context_start = context_start.split('\n')[-1]
                    first_bracket_index = context_start.find("[")
                    context_start = context_start[first_bracket_index:]

                else:
                    context_start = self._text[0 : start + 1].split("\n")[-1]
                # context_end = self._text[end:end + remaining].split('\n')[0]
                context_end = self._text[end : end + remaining]
                last_bracket_index = context_end.rfind("[")
                context_end = context_end[0:last_bracket_index]  # 过滤掉最后一行的开头[
                concordance.append(
                    context_start
                    + "<"
                    + demarcation
                    + ">"
                    + self._text[start:end]
                    + "</"
                    + demarcation
                    + ">"
                    + context_end
                )
                if lines and len(concordance) >= lines:
                    break
            # return ("Displaying %s matches:\n" % (len(concordance)))
            # return ('\n'.join(concordance))
            return (
                '<h4>找到 <span id="matches_count">%s</span> 条记录, 第 <span id="page">%s</span> 页, 共 <span id="pages">%s</span> 页.</h4>'
                % (self.matches_count, self.page, self.pages)
            ) + ("\n".join(concordance))
        else:
            return "<h4>没有找到.</h4>"


ci = RegExConcordanceIndex(ccp)

# url(r'^feed_ajax_data/(?P<keyword>\w+)/(?P<page>[0-9]+)/$', views.feed_ajax_data),


@blueprint.route("/feed_ajax_data/<keyword>/<int:page>")
def feed_ajax_data(keyword, page=1):
    """生成 raw_html 供 ajax 调用"""
    # 前方必须以空格开始; 关键字; 拉丁字符*; 标点符号除外;
    output = ci.print_concordance(keyword, page=int(page))

    output = output.replace("\n", "<br>")
    # print(keyword)
    # return HttpResponse( ci.matches_count, ci.pages, output )
    return jsonify(
        {
            "matches_count": ci.matches_count,
            "pages": ci.pages,
            "output": output,
        }
    )


# url(r'^$', views.index, name='index.html'),
# url(r'^(?P<keyword>\w+)$', views.index, name='index.html'),
# url(r'^(?P<keyword>\w+)/(?P<page>[0-9]+)$', views.index, name='index.html'),


@blueprint.route("/")
def index(keyword=None, page=1):  # 默认打开到 功能介绍 页面
    # keyword = request.query.keyword
    # page =request.query.page
    # if page:
    #     page = int(page)
    # else:
    #     page = 1
    # if keyword == '':
    #     return template(html, output=instruction)
    # else:
    #     return feed_ajax_data(keyword=keyword, page=page)[2]

    return render_template("ccp.html")
