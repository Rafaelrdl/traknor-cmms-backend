from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from typing import Dict


def update_query_params(url: str, **params: int | str) -> str:
    """Retorna a URL com os parâmetros de query atualizados."""
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key, value in params.items():
        query[key] = str(value)
    return urlunparse(parsed._replace(query=urlencode(query)))


def build_link_header(links: Dict[str, str | None]) -> str:
    """Monta o header ``Link`` seguindo o RFC5988."""
    parts = [f"<{url}>; rel=\"{rel}\"" for rel, url in links.items() if url]
    return ", ".join(parts)
