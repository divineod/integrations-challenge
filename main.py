from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import httpx

app = FastAPI(title="Creditsafe Company Report API", version="1.0")

CREDITSAFE_USERNAME = "username@domain.com"
CREDITSAFE_PASSWORD = "^1gHySRA56aj>tf421o"
BASE_URL = "https://connect.creditsafe.com/v1"


# Models for Request and Response Validation
class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str = Field(..., description="JWT for API authentication")


class CompanySearchRequest(BaseModel):
    name: str
    country: Optional[str] = None
    exact: bool = False


class CompanySearchResponse(BaseModel):
    connectId: str = Field(..., description="Unique ID for the company")
    name: str
    address: Optional[str]
    status: Optional[str]


class CreditReportRequest(BaseModel):
    connect_id: str


class CreditReportResponse(BaseModel):
    company_name: str
    credit_score: Optional[int]
    credit_limit: Optional[float]
    report_details: dict


# Helper Functions
async def authenticate() -> str:
    """Authenticate with Creditsafe API and return a JWT token."""
    url = f"{BASE_URL}/authenticate"
    payload = {"username": CREDITSAFE_USERNAME, "password": CREDITSAFE_PASSWORD}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers={"Content-Type": "application/json"})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Authentication failed")
    
    token_data = response.json()
    return token_data.get("token")


async def get_authorization_header() -> dict:
    """Get the authorization header with a valid JWT token."""
    token = await authenticate()
    return {"Authorization": f"Bearer {token}"}


# Endpoints
@app.post("/company/search", response_model=CompanySearchResponse)
async def search_company(search_request: CompanySearchRequest):
    """
    Search for a company using the Creditsafe API.
    """
    url = f"{BASE_URL}/companies"
    headers = await get_authorization_header()
    query = {
        "name": search_request.name,
        "countries": search_request.country,
        "exact": str(search_request.exact).lower(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=query)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Company search failed")
    
    search_data = response.json()
    if not search_data.get("data"):
        raise HTTPException(status_code=404, detail="No companies found")

    # Simplified for single company; adapt for multiple results as needed
    company = search_data["data"][0]
    return CompanySearchResponse(
        connectId=company["connectId"],
        name=company["name"],
        address=company.get("address", {}).get("street", ""),
        status=company.get("status", "Unknown"),
    )


@app.post("/company/report", response_model=CreditReportResponse)
async def generate_credit_report(report_request: CreditReportRequest):
    """
    Generate a company credit report using the Creditsafe API.
    """
    url = f"{BASE_URL}/companies/{report_request.connect_id}"
    headers = await get_authorization_header()
    query = {"language": "en", "template": "full"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=query)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve credit report")
    
    report_data = response.json()
    return CreditReportResponse(
        company_name=report_data["company"]["name"],
        credit_score=report_data["scores"].get("creditScore"),
        credit_limit=report_data["scores"].get("creditLimit"),
        report_details=report_data,
    )
