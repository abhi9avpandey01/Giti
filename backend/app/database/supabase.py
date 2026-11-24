from supabase import create_client, Client
from app.config import settings

_supabase_client: Client | None = None


def get_supabase_client() -> Client:
    """Return Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
            # Fallback or raise helpful warning if credentials not yet configured
            return None
        _supabase_client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
    return _supabase_client
