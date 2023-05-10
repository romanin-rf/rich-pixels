from typing import TypeVar, Iterable, AsyncGenerator, overload, SupportsIndex

# ! Types
T = TypeVar("T")

# ! Functions
async def aiter(it: Iterable[T]) -> AsyncGenerator[T]: ...

@overload
async def arange(__stop: SupportsIndex) -> AsyncGenerator[int]: ...
@overload
async def arange(__start: SupportsIndex, __stop: SupportsIndex, __step: SupportsIndex=...) -> AsyncGenerator[int]: ...
