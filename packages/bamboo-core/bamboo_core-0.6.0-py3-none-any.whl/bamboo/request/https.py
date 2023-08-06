
from __future__ import annotations

from http.client import HTTPSConnection
from ssl import SSLContext
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
)

from bamboo.api import BinaryApiData
from bamboo.base import HTTPMethods
from bamboo.request import ResponseData_t, Schemes
from bamboo.request.request_form import get_http_request_form
from bamboo.request.response import Response


__all__ = [
    "connect",
    "delete",
    "get",
    "head",
    "options",
    "patch",
    "post",
    "put",
    "trace",
]


def request(
    uri: str,
    method: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    form = get_http_request_form(
        Schemes.HTTPS,
        uri,
        method,
        headers=headers,
        body=body,
        json=json,
        query=query
    )
    conn = HTTPSConnection(
        form.host,
        form.port,
        key_file=key_file,
        cert_file=cert_file,
        context=context,
        timeout=timeout,
        blocksize=blocksize
    )
    conn.request(form.method, form.uri, body=form.body, headers=form.headers)
    _res = conn.getresponse()
    return Response(conn, _res, datacls=datacls)


def get(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the GET method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.GET,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def post(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the POST method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.POST,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def put(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the PUT method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.PUT,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def delete(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the DELETE method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.DELETE,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def head(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the HEAD method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.HEAD,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def options(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the OPTIONS method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.OPTIONS,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def patch(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the PATCH method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.PATCH,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def trace(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the TRACE method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.TRACE,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )


def connect(
    uri: str,
    headers: Dict[str, str] = {},
    body: Optional[bytes] = None,
    json: Optional[Dict[str, Any]] = None,
    query: Dict[str, List[str]] = {},
    timeout: Optional[float] = None,
    blocksize: int = 8192,
    datacls: Type[ResponseData_t] = BinaryApiData,
    key_file: Optional[str] = None,
    cert_file: Optional[str] = None,
    context: Optional[SSLContext] = None
) -> Response[ResponseData_t]:
    """Request with the CONNECT method on HTTPS.

    Note:
        Sometimes your specified arguments may cause security problems in
        communications with the function. It is strongly recommended to
        reference Python ssl module security considerations documents.
        Link: https://docs.python.org/3/library/ssl.html#ssl-security

    Args:
        uri: URI to be requested.
        headers: Request headers.
        body: Request body of bytes.
        json: Request body of JSON.
        query: Query parameters to be attached to the URI.
        timeout: Seconds waiting for the connection.
        blocksize: Block size of sending data.
        datacls: `ApiData` or its subclass to be attached from the response body.
        key_file: Path of a public key file.
        cert_file: Path of a certification file.
        context: SSLContext of your communication.

    Returns:
        Response object generated with the response.
    """
    return request(
        uri,
        HTTPMethods.CONNECT,
        headers=headers,
        body=body,
        json=json,
        query=query,
        timeout=timeout,
        blocksize=blocksize,
        datacls=datacls,
        key_file=key_file,
        cert_file=cert_file,
        context=context
    )
