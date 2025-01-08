from pydantic import BaseModel
from typing import List, Optional

# Pydantic models for response validation
class Product(BaseModel):
    id: Optional[int]
    url: str
    name: str
    discountPrice: float
    basePrice: float
    nameFa: str
    nameEn: str
    imageUrl: str

# Pydantic models for request validation
class ProductCreate(BaseModel):
    url:str
    name: str
    nameFa: str
    nameEn: Optional[str] = None
    discountPrice: Optional[float] = None
    basePrice: Optional[float] = None
    nameFa: str
    nameEn: str
    imageUrl: Optional[str] = None