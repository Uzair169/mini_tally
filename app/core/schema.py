from pydantic import BaseModel

class FinancialResponse(BaseModel):
    net_income: str
    revenue: str
    period: str