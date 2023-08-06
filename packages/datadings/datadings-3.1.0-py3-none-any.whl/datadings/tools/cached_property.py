"""
MIT License

Copyright (c) 2020 Alexey Stepanov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Backport of python 3.8 functools.cached_property.

cached_property() - computed once per instance, cached as attribute
"""

__all__ = ("cached_property",)

# Standard Library
from sys import version_info

if version_info >= (3, 8):
    from functools import cached_property  # pylint: disable=no-name-in-module
else:
    from threading import RLock
    from typing import Any
    from typing import Callable
    from typing import Optional
    from typing import Type
    from typing import TypeVar

    _NOT_FOUND = object()
    _T = TypeVar("_T")
    _S = TypeVar("_S")

    # noinspection PyPep8Naming
    class cached_property:  # NOSONAR  # pylint: disable=invalid-name  # noqa: N801
        """Cached property implementation.

        Transform a method of a class into a property whose value is computed once
        and then cached as a normal attribute for the life of the instance.
        Similar to property(), with the addition of caching.
        Useful for expensive computed properties of instances
        that are otherwise effectively immutable.
        """

        def __init__(self, func: Callable[[Any], _T]) -> None:
            """Cached property implementation."""
            self.func = func
            self.attrname: Optional[str] = None
            self.__doc__ = func.__doc__
            self.lock = RLock()

        def __set_name__(self, owner: Type[Any], name: str) -> None:
            """Assign attribute name and owner."""
            if self.attrname is None:
                self.attrname = name
            elif name != self.attrname:
                raise TypeError(
                    "Cannot assign the same cached_property to two different names "
                    f"({self.attrname!r} and {name!r})."
                )

        def __get__(self, instance, owner=None) -> Any:
            """Property-like getter implementation.

            :return: property instance if requested on class or value/cached value if requested on instance.
            :rtype: Union[cached_property[_T], _T]
            :raises TypeError: call without calling __set_name__ or no '__dict__' attribute
            """
            if instance is None:
                return self
            if self.attrname is None:
                raise TypeError("Cannot use cached_property instance without calling __set_name__ on it.")
            try:
                cache = instance.__dict__
            except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
                msg = (
                    f"No '__dict__' attribute on {type(instance).__name__!r} "
                    f"instance to cache {self.attrname!r} property."
                )
                raise TypeError(msg) from None
            val = cache.get(self.attrname, _NOT_FOUND)
            if val is _NOT_FOUND:
                with self.lock:
                    # check if another thread filled cache while we awaited lock
                    val = cache.get(self.attrname, _NOT_FOUND)
                    if val is _NOT_FOUND:
                        val = self.func(instance)
                        try:
                            cache[self.attrname] = val
                        except TypeError:
                            msg = (
                                f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                                f"does not support item assignment for caching {self.attrname!r} property."
                            )
                            raise TypeError(msg) from None
            return val
