# mkdocs-replace-markdown

An MkDocs plugin to replace text in Markdown on build.

## Installation & Setup

Install the package with pip:

```
pip install mkdocs-replace-markdown
```

Enable the plugin in your mkdocs.yml:

```yaml
plugins:
    - search
    - replace_markdown:
        patterns:        
            - pattern_1: # Pattern name, can be anything
                url: "my/url/scheme" # Only replace text on pages that match the given URL
                oldvalue: "replace me"
                newvalue: "with this"
            - pattern_2: # Next pattern
                url: "my/other/url/scheme"
                oldvalue: "other text"
                newvalue: "new value"
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.
