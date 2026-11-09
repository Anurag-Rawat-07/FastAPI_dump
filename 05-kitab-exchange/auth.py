from fastapi import Header, HTTPException

# in production, you add this in .env
API_KEY = "my_secret_api_key"


def verify_api_key(x_api_key: str = Header()):            #middleware function to verify the API key from the request header
    """Verify the API key from the request header."""     #dependency injection to get the API key from the request header
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
