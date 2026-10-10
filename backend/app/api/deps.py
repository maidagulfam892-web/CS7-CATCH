from fastapi import Security

from app.core.security import require_api_key

ApiKeyDep = Security(require_api_key)
