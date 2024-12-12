# Creditsafe Company Report API

## Overview
The **Creditsafe Company Report API** provides endpoints to authenticate, search for companies, and generate credit reports using the Creditsafe API. This application is built with FastAPI, providing asynchronous operations for scalability and efficiency.

## Features
- **Authentication**: Authenticate and obtain a JWT token to access the Creditsafe API.
- **Company Search**: Search for a company by name and country.
- **Credit Report**: Generate a detailed credit report for a specific company.

---

## Base URL
**Local Development**: `http://localhost:8000`

---

## Authentication
Authentication with the Creditsafe API is handled internally. No additional user action is required to manage tokens.

---

## Endpoints

### 1. **Search Company**
Search for a company by its name and country.

- **URL**: `/company/search`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "name": "string",
    "country": "string",
    "exact": true
  }
  ```
  - `name` (required): The name of the company to search for.
  - `country` (optional): The country code (e.g., "US").
  - `exact` (optional): Whether to perform an exact name match (default: `false`).

- **Response**:
  ```json
  {
    "connectId": "string",
    "name": "string",
    "address": "string",
    "status": "string"
  }
  ```
  - `connectId`: Unique ID for the company.
  - `name`: Name of the company.
  - `address`: Company address.
  - `status`: Current company status (e.g., "Active").

- **Example**:
  ```bash
  curl -X POST http://localhost:8000/company/search \
  -H "Content-Type: application/json" \
  -d '{"name": "Apple", "country": "US", "exact": true}'
  ```

---

### 2. **Generate Credit Report**
Retrieve a detailed credit report for a specific company using its `connectId`.

- **URL**: `/company/report`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "connect_id": "string"
  }
  ```
  - `connect_id` (required): The unique ID of the company obtained from the `/company/search` endpoint.

- **Response**:
  ```json
  {
    "company_name": "string",
    "credit_score": 85,
    "credit_limit": 5000000,
    "report_details": {...}
  }
  ```
  - `company_name`: Name of the company.
  - `credit_score`: The company's credit score (if available).
  - `credit_limit`: Credit limit of the company (if available).
  - `report_details`: Detailed report data.

- **Example**:
  ```bash
  curl -X POST http://localhost:8000/company/report \
  -H "Content-Type: application/json" \
  -d '{"connect_id": "12345"}'
  ```

---

## Error Handling
All errors are returned in the following format:
```json
{
  "detail": "Error message"
}
```
- **401 Unauthorized**: Authentication failed.
- **404 Not Found**: No data found for the requested resource.
- **500 Internal Server Error**: An unexpected error occurred.

---

## Running Locally
1. Build and run the Docker container:
   ```bash
   docker build -t divineod/credit-report-api:latest .
   docker run -p 8000:8000 divineod/credit-report-api:latest
   ```

2. Access the API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

---

## Notes
- Ensure valid credentials are set for Creditsafe authentication.
- Use the Swagger UI for interactive testing and debugging.
- Optimize requests to avoid exceeding API rate limits.
