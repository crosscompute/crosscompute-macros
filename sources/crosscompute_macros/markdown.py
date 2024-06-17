import re

from markdown2 import markdown


EXTRAS = [
    'break-on-newline',
    'code-friendly',
    'cuddled-lists',
    'fenced-code-blocks',
    'footnotes',
    'markdown-in-html',
    'strike',
    'target-blank-links',
    'tables',
    'use-file-vars',
    'task_list']
TAGS = [
    'a',
    'button',
    'div',
    'input',
    'span']


def get_html_from_markdown(text, extras=EXTRAS):
    return markdown(text, extras=extras).strip()


def remove_parent_paragraphs(html, tags=TAGS):
    if tags:
        tags_text = '|'.join(tags)
        html = re.sub(r'<p>(\s*<(?:%s))' % tags_text, r'\g<1>', html)
        html = re.sub(r'((?:%s)[^>]*>\s*)</p>' % tags_text, r'\g<1>', html)
    return html