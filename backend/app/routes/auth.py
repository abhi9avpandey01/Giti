from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from app.database.supabase import get_supabase_client

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Retrieves authenticated user profile.
    Verifies Supabase JWT token if provided.
    """
    if not authorization:
        # Return mock / dev user for simple initial development
        return {
            "id": "dev-user-00000000-0000-0000-0000-000000000001",
            "email": "developer@giti.local",
            "authenticated": True
        }

    token = authorization.replace("Bearer ", "")
    supabase = get_supabase_client()
    if not supabase:
        return {
            "id": "dev-user-00000000-0000-0000-0000-000000000001",
            "email": "developer@giti.local",
            "authenticated": True
        }

    try:
        user_res = supabase.auth.get_user(token)
        if not user_res.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {
            "id": user_res.user.id,
            "email": user_res.user.email,
            "authenticated": True
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
