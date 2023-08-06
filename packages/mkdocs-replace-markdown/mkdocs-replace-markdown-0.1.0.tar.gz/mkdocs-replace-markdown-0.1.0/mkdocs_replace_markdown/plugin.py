import os
import sys

from mkdocs import utils as mkdocs_utils
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options, Config


class ReplaceMarkdownPlugin(BasePlugin):

    # Each entry in patterns must have 3 subentries:
    #
    # patterns:
    #   - pattern_1:   < pattern name, can be anything
    #     url: "my/url/scheme"   < only replace text on pages that match the given URL
    #     oldvalue: "replace me"
    #     newvalue: "with this"
    config_scheme = (
        ('patterns', config_options.Type((str, list), default={})),
    )

    def on_page_markdown(self, markdown, page, config, files):
        patterns = self.config.get('patterns', [])
        for pattern in patterns:
            pattern = list(pattern.values())[0]
            url = pattern.get('url', '')
            oldvalue = pattern.get('oldvalue', '')
            newvalue = pattern.get('newvalue', '')
            if url in page.url:
                markdown = markdown.replace(oldvalue, newvalue)
        return markdown
