from __future__ import annotations
# > Standard Modules
from pathlib import Path, PurePath
from typing import Iterable, Mapping, Tuple, Union, Optional, List
# > Graphics
from PIL import Image as PILImageModule
from PIL.Image import Image
from PIL.Image import Resampling
from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment, Segments
from rich.style import Style

# ! Just Pixels
class Pixels:
    def __init__(self) -> None:
        self._segments: Optional[Segments] = None
    
    @staticmethod
    def from_image(
        image: Image,
        resize: Optional[Tuple[int, int]] = None,
        resample: Optional[Resampling] = None
    ) -> Pixels:
        resample = resample or Resampling.NEAREST
        segments = Pixels._segments_from_image(image, resize, resample)
        return Pixels.from_segments(segments)
    
    @staticmethod
    def from_image_path(
        path: Union[PurePath, str],
        resize: Optional[Tuple[int, int]] = None,
        resample: Optional[Resampling] = None
    ) -> Pixels:
        """Create a Pixels object from an image. Requires 'image' extra dependencies.
        
        Args:
            path: The path to the image file.
            resize: A tuple of (width, height) to resize the image to.
        """
        resample = resample or Resampling.NEAREST
        with PILImageModule.open(Path(path)) as image:
            segments = Pixels._segments_from_image(image, resize, resample)
        return Pixels.from_segments(segments)
    
    @staticmethod
    def _segments_from_image(
        image: Image,
        resize: Optional[Tuple[int, int]] = None,
        resample: Optional[Resampling] = None
    ) -> List[Segment]:
        if resize is not None:
            image = image.resize(resize, resample=resample)
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        height, width = image.size
        null_style = Style.null()
        segments = []
        for y in range(width):
            this_row = []
            for x in range(height):
                r, g, b, a = image.getpixel((x, y))
                style = Style.parse(f"on rgb({r},{g},{b})") if a > 0 else null_style
                this_row.append(Segment(style))
            this_row.append(Segment("\n", null_style))
            segments += this_row
        return segments
    
    @staticmethod
    def from_segments(
        segments: Iterable[Segment],
    ) -> Pixels:
        """Create a Pixels object from an Iterable of Segments instance."""
        pixels = Pixels()
        pixels._segments = Segments(segments)
        return pixels
    
    @staticmethod
    def from_ascii(
        grid: str,
        mapping: Optional[Mapping[str, Segment]] = None
    ) -> Pixels:
        """
        Create a Pixels object from a 2D-grid of ASCII characters.
        Each ASCII character can be mapped to a Segment (a character and style combo),
        allowing you to add a splash of colour to your grid.
        
        Args:
            grid: A 2D grid of characters (a multi-line string).
            mapping: Maps ASCII characters to Segments. Occurrences of a character will be replaced with the corresponding Segment.
        """
        if mapping is None:
            mapping = {}
        if not grid:
            return Pixels.from_segments([])
        segments = []
        for character in grid:
            segment = mapping.get(character, Segment(character))
            segments.append(segment)
        return Pixels.from_segments(segments)
    
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield self._segments or ""

# ! Asynchronous Pixels
class AsyncPixels:
    def __init__(self) -> None:
        self._segments: Optional[Segments] = None
    
    @staticmethod
    async def from_image(
        image: Image,
        resize: Optional[Tuple[int, int]] = None,
        resample: Optional[Resampling] = None
    ) -> AsyncPixels:
        resample = resample or Resampling.NEAREST
        segments = await AsyncPixels._segments_from_image(image, resize, resample)
        return await AsyncPixels.from_segments(segments)
    
    @staticmethod
    async def from_image_path(
        path: Union[PurePath, str],
        resize: Optional[Tuple[int, int]] = None,
        resample: Optional[Resampling] = None
    ) -> AsyncPixels:
        """Create a Pixels object from an image. Requires 'image' extra dependencies.
        
        Args:
            path: The path to the image file.
            resize: A tuple of (width, height) to resize the image to.
        """
        resample = resample or Resampling.NEAREST
        with PILImageModule.open(Path(path)) as image:
            segments = await AsyncPixels._segments_from_image(image, resize, resample)
        return await AsyncPixels.from_segments(segments)
    
    @staticmethod
    async def _segments_from_image(
        image: Image,
        resize: Optional[Tuple[int, int]]=None,
        resample: Optional[Resampling]=None
    ) -> List[Segment]:
        if resize is not None:
            image = image.resize(resize, resample=resample)
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        height, width = image.size
        null_style = Style.null()
        segments = []
        for y in range(width):
            this_row = []
            for x in range(height):
                r, g, b, a = image.getpixel((x, y))
                style = Style.parse(f"on rgb({r},{g},{b})") if a > 0 else null_style
                this_row.append(Segment(style))
            this_row.append(Segment("\n", null_style))
            segments += this_row
        return segments
    
    @staticmethod
    async def from_segments(
        segments: Iterable[Segment],
    ) -> AsyncPixels:
        """Create a Pixels object from an Iterable of Segments instance."""
        pixels = AsyncPixels()
        pixels._segments = Segments(segments)
        return pixels
    
    @staticmethod
    async def from_ascii(
        grid: str,
        mapping: Optional[Mapping[str, Segment]] = None
    ) -> AsyncPixels:
        """
        Create a Pixels object from a 2D-grid of ASCII characters.
        Each ASCII character can be mapped to a Segment (a character and style combo),
        allowing you to add a splash of colour to your grid.
        
        Args:
            grid: A 2D grid of characters (a multi-line string).
            mapping: Maps ASCII characters to Segments. Occurrences of a character
                will be replaced with the corresponding Segment.
        """
        if mapping is None:
            mapping = {}
        if not grid:
            return await AsyncPixels.from_segments([])
        segments = []
        async for character in grid:
            segment = mapping.get(character, Segment(character))
            segments.append(segment)
        return await AsyncPixels.from_segments(segments)
    
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield self._segments or ""
