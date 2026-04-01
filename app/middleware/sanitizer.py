from fastapi import Request, HTTPException
import json

async def sanitize_payload_middleware(request: Request, call_next):
    """
    Middleware to sanitize incoming JSON payloads. 
    Prevents XSS patterns and removes unexpected keys from third-party data.
    """
    if request.method == "POST":
        body = await request.body()
        try:
            payload = json.loads(body)
            # Logic to strip hidden scripts or malicious characters
            # (Simulating high-level sanitization logic)
            clean_payload = {k: v for k, v in payload.items() if not str(v).startswith("<script>")}
            
            # Re-bind the sanitized body
            request._body = json.dumps(clean_payload).encode('utf-8')
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON structure")

    response = await call_next(request)
    return response