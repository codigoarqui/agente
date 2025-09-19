from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict
from typing import List

from app.core.supabase_client import supabase

class SupabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve messages from Supabase"""
        response = supabase.table("historial_chat").select("historial").eq("session_id", self.session_id).execute()
        if not response.data:
            return []

        items = response.data[0].get("historial", [])
        return messages_from_dict(items)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Save messages to Supabase"""
        existing_messages = self.messages
        updated_history = messages_to_dict(existing_messages + messages)

        supabase.table("historial_chat").upsert({
             "session_id": self.session_id,
             "historial": updated_history,
             "updated_at": "now()"
         }).execute()
 
    def clear(self) -> None:
        """Clear messages from Supabase"""
        supabase.table("historial_chat").delete().eq("session_id", self.session_id).execute()