import markdown
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

MARKDOWN_EXTENSIONS = ["extra", "sane_lists"]


@register.filter
def convert_markdown(value):
    escaped_value = conditional_escape(value or "")
    rendered_html = markdown.markdown(escaped_value, extensions=MARKDOWN_EXTENSIONS)
    return mark_safe(rendered_html)