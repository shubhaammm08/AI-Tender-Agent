import json
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from models.tenant import AuditLog

class LLMClient:
    def __init__(self, provider: str = "gemini", model: str = "gemini-3.1-pro"):
        self.provider = provider
        self.model = model

    def generate(self, prompt: str, system_prompt: str, db: Session, tenant_id: UUID, actor: str = "ai_agent") -> str:
        # 1. Actually call the LLM using the configured provider.
        # (Mocking the response for the purpose of the MVP)
        response_text = '{"extracted": true}'
        
        # 2. Audit logging as required by AGENTS.md:
        # "Every AI output writes an audit_log entry (model, prompt version, sources, actor)."
        audit_entry = AuditLog(
            tenant_id=tenant_id,
            actor=actor,
            action="llm_generation",
            entity="LLMClient",
            detail={
                "model": self.model,
                "provider": self.provider,
                "prompt_length": len(prompt),
                # Storing hash or reference of prompt, avoiding storing PII directly if needed
                "response_length": len(response_text)
            },
            hash="mock_hash_chain" # In a real implementation, this hashes the previous row's hash + current data
        )
        db.add(audit_entry)
        db.commit()
        
        return response_text
