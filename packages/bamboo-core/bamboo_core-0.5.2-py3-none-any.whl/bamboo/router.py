
from typing import (
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from bamboo.location import (
    FlexibleLocation,
    Uri_t,
    is_flexible_uri,
    is_duplicated_uri,
)


__all__ = []


HTTPMethod_t = str
Endpoint_t = TypeVar("Endpoint_t")
Uri2Endpoints_t = Dict[Uri_t, Type[Endpoint_t]]


class DuplicatedUriRegisteredError(Exception):
    """Raised if duplicated URI is registered."""
    pass


class Router(Generic[Endpoint_t]):
    """Operator of routing request to `Endpoint` by URI.
    """

    def __init__(self) -> None:
        self.uri2endpoint: Uri2Endpoints_t = {}
        self.uris_flexible: List[Uri_t] = []

    def register(self, uri: Uri_t, endpoint: Type[Endpoint_t]) -> None:
        """Register combination of URI and `Endpoint`.

        Args:
            uri: URI pattern of the `Endpoint`.
            endpoint: `Endpoint` class to be registered.

        Raises:
            DuplicatedUriRegisteredError: Raised if given URI pattern
                matches one already registered.
        """
        for uri_registered in self.uri2endpoint.keys():
            if is_duplicated_uri(uri_registered, uri):
                raise DuplicatedUriRegisteredError(
                    "Duplicated URIs were detected.\n"
                    f"URI pattern 1: {uri_registered}\n"
                    f"URI pattern 2: {uri}"
                )

        if is_flexible_uri(uri):
            self.uris_flexible.append(uri)
        self.uri2endpoint[uri] = endpoint

    def validate(
        self,
        uri: str
    ) -> Tuple[Tuple[str, ...], Optional[Type[Endpoint_t]]]:
        """Validate specified `uri` and retrieved `Endpoint`.

        Note:
            This method returns pair of tuple of flexible locations specified as
            parts of URI pattern linked to `Endpoint` and its `Endpoint`. If any
            flexible locations are not included in the URI pattern, then empty
            tuple will be returned as a sequence of flexible locations, so if
            URI patterns is configured with only static locations, you will get
            the empty tuple.

            If invalid URI pattern is come, then also empty tuple will be return
            as sequence of flexible locations and `None` as `Endpoint`, or
            `((), None)`.

        Args:
            uri: Path of URI.

        Returns:
            Pair of values of flexible locations and `Endpoint` if specified
            `uri` is valid.
        """
        uri = tuple(uri[1:].split("/"))
        endpoint = self.uri2endpoint.get(uri)
        if endpoint:
            return ((), endpoint)

        depth = len(uri)
        for flexible in self.uris_flexible:
            if len(flexible) != depth:
                continue

            flexibles_received = []

            # Judging each locations
            for loc_req, loc_flex in zip(uri, flexible):
                if loc_req == loc_flex:
                    continue
                if isinstance(loc_flex, FlexibleLocation):
                    if not loc_flex.is_valid(loc_req):
                        break

                    flexibles_received.append(loc_req)
            else:
                # Correct case
                endpoint = self.uri2endpoint.get(flexible)
                return (tuple(flexibles_received), endpoint)

        # Could not find it
        return ((), None)

    def search_uris(self, endpoint: Type[Endpoint_t]) -> List[Uri_t]:
        """Search URI patterns of specified `endpoint`.

        Args:
        endpoint: `Endpoint` class whose URI patterns to be retrieved.

        Returns:
            Result of searching.
        """
        return [
            uri for uri, point in self.uri2endpoint.items()
            if point is endpoint
        ]
