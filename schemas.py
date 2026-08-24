from pydantic import BaseModel, Field
from typing import Optional

class HousePredictRequest(BaseModel):
    carpet_area_sqft: float = Field(..., gt=0, description="Carpet area in sqft")
    floor_num: int = Field(0, ge=0)
    bathroom: int = Field(1, ge=0)
    balcony: int = Field(0, ge=0)
    location_grouped: str = Field("other")
    Furnishing: Optional[str] = "Unfurnished"
    Transaction: Optional[str] = "Resale"
    Ownership: Optional[str] = "Freehold"

class HousePredictResponse(BaseModel):
    predicted_price: float
    currency: str = "INR"