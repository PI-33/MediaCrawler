# -*- coding: utf-8 -*-
# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import os
import sys

# 小红书平台配置

DEFAULT_SORT_TYPE = "popularity_descending"

def _get_cli_arg(name: str) -> str:
    try:
        argv = sys.argv
        for i, arg in enumerate(argv):
            if arg == f"--{name}" and i + 1 < len(argv):
                val = argv[i + 1]
                if not val.startswith("-"):
                    return val
        return ""
    except Exception:
        return ""

_sort_map = {
    "0": "general",
    "1": "popularity_descending",
    "2": "time_descending",
    "3": "comment_descending",
    "4": "collect_descending",
}

_note_type_map = {
    "0": "不限",
    "1": "视频笔记",
    "2": "普通笔记",
}

_note_time_map = {
    "0": "一天内",
    "1": "一周内",
    "2": "半年内",
}

_raw_sort = _get_cli_arg("sort_type").strip()
_raw_note_type = _get_cli_arg("filter_note_type").strip()
_raw_note_time = _get_cli_arg("filter_note_time").strip()

SORT_TYPE = _sort_map.get(_raw_sort, DEFAULT_SORT_TYPE)

FILTER_VALUES = {
    "sort_type": SORT_TYPE,
    "filter_note_type": _note_type_map.get(_raw_note_type, "不限"),
    "filter_note_time": _note_time_map.get(_raw_note_time, "不限"),
    "filter_note_range": "不限",
    "filter_pos_distance": "不限",
}

# 指定笔记URL列表, 必须要携带xsec_token参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/64b95d01000000000c034587?xsec_token=AB0EFqJvINCkj6xOCKCQgfNNh8GdnBC_6XecG4QOddo3Q=&xsec_source=pc_cfeed"
    # ........................
]

# 指定创作者URL列表，需要携带xsec_token和xsec_source参数

XHS_CREATOR_ID_LIST = [
    "https://www.xiaohongshu.com/user/profile/5f58bd990000000001003753?xsec_token=ABYVg1evluJZZzpMX-VWzchxQ1qSNVW3r-jOEnKqMcgZw=&xsec_source=pc_search"
    # ........................
]
