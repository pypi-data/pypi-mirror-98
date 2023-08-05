import re
from pathlib import Path
from urllib.request import urlopen

from yaml import load, add_constructor, Loader

from foliant.config.base import BaseParser


class Parser(BaseParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_constructor('!include', self._resolve_include_tag)

    def _resolve_include_tag(self, _, node) -> str:
        '''Replace value after ``!include`` with the content of the referenced file.'''

        parts = node.value.split('#')

        if len(parts) == 1:
            path_ = parts[0]

            include_content = self._get_file_or_url_content(path_)
            return load(include_content, Loader)

        elif len(parts) == 2:
            path_, section = parts[0], parts[1]

            include_content = self._get_file_or_url_content(path_)
            return load(include_content, Loader)[section]

        else:
            raise ValueError('Invalid include syntax')

    def _get_file_or_url_content(self, path_: str) -> str or bytes:
        """
        Determine whether path_ is a path to local file or url. And return its content.
        """

        link_pattern = re.compile(r'https?://\S+')
        if link_pattern.search(path_):  # path_ is a URL
            result = urlopen(path_).read()
        else:
            with open(self.project_path / Path(path_).expanduser(),
                      encoding='utf8') as f:
                result = f.read()
        return result
