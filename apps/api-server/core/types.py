"""
Shared type aliases used across Pydantic models.
"""

from typing import Annotated
from pydantic import BeforeValidator

# MongoDB stores IDs as ObjectId objects, but we want to work with plain strings.
# PyObjectId coerces any ObjectId value to str when a model is instantiated.
PyObjectId = Annotated[str, BeforeValidator(str)]
