"""
2021/3/22 14:05
desc
"""
from model_utils import Choices

DINGDING_VERFIFY_TYPE = (
    ("SIGN", "SIGN", "加签"),
    ("KEYWORD", "KEYWORD", "关键词"),
    ("IP", "IP", "IP白名单"),
)

DINGDING_VERFIFY_TYPE_CHOICE = Choices(*DINGDING_VERFIFY_TYPE)
