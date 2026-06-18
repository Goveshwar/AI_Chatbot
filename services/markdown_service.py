
import markdown
import bleach


ALLOWED_TAGS = set(
    bleach.sanitizer.ALLOWED_TAGS
).union(
    {
        "p",
        "pre",
        "code",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
        "br",
        "hr",
        "ul",
        "ol",
        "li",
        "span",
        "div"
    }
)

ALLOWED_ATTRIBUTES = {
    "*": ["class"],
    "a": ["href", "title"],
    "code": ["class"],
    "span": ["class"],
    "div": ["class"]
}


def render_markdown(
    text: str
) -> str:

    html = markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc"
        ]
    )

    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES
    )

