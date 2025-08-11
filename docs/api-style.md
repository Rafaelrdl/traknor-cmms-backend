# Padrão de respostas da API

Este projeto utiliza um envelope JSON para todas as respostas de sucesso e o
formato [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) para erros.

## Envelope de sucesso

Listagens retornam o seguinte formato:

```
{
  "data": [/* itens */],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total_pages": 10,
    "total_items": 243
  },
  "links": {
    "self": "https://api.../resource?page=1&per_page=25",
    "first": "https://api.../resource?page=1&per_page=25",
    "prev": null,
    "next": "https://api.../resource?page=2&per_page=25",
    "last": "https://api.../resource?page=10&per_page=25"
  }
}
```

Para respostas de detalhe ou criação:

```
{ "data": { /* objeto */ } }
```

## Cabeçalhos de paginação

As listagens incluem os seguintes headers:

- `X-Total-Count`: total de itens disponíveis.
- `X-Total-Pages`: total de páginas.
- `X-Per-Page`: quantidade de itens por página.
- `X-Current-Page`: página atual.
- `Link`: links com `rel="first"`, `rel="prev"`, `rel="next"` e `rel="last"`.

## Erros

Erros seguem o padrão *Problem Details* (`application/problem+json`):

```
{
  "type": "https://traknor.dev/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "There were validation errors",
  "instance": "/recurso",
  "errors": [
    {"name": "campo", "reason": "mensagem"}
  ]
}
```

Outros erros (404, 403, 500...) utilizam o mesmo formato, sem o campo
`errors`.

## Parâmetros de paginação

- `page`: número da página (>=1, padrão 1).
- `per_page`: itens por página (padrão 25, máximo 100).
