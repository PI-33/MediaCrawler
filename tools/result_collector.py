from typing import Dict, List

_memory_output_enabled = False
_collector = None


class ResultCollector:
    def __init__(self):
        self.contents: List[Dict] = []
        self.comments: List[Dict] = []
        self.creators: List[Dict] = []

    def add_content(self, item: Dict):
        if item:
            self.contents.append(item)

    def add_comment(self, item: Dict):
        if item:
            self.comments.append(item)

    def add_creator(self, item: Dict):
        if item:
            self.creators.append(item)

    def dump(self) -> Dict:
        return {
            "contents": self.contents,
            "comments": self.comments,
            "creators": self.creators,
        }


def get_collector() -> ResultCollector:
    global _collector
    if _collector is None:
        _collector = ResultCollector()
    return _collector


def enable_memory_output(flag: bool):
    global _memory_output_enabled
    _memory_output_enabled = bool(flag)


def is_memory_output() -> bool:
    return _memory_output_enabled