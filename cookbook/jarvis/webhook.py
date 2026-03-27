"""
Jarvis — Webhook WhatsApp

Recebe mensagens de clientes via WhatsApp Business API (Meta),
identifica o tenant, carrega o agente de atendimento e responde.

Fluxo:
  1. Meta envia POST /webhook/whatsapp com a mensagem do cliente
  2. O webhook extrai tenant_id, número e texto
  3. Carrega o agente de atendimento do tenant
  4. O agente processa a mensagem e envia a resposta via WhatsApp API

Configuracao no Meta:
  - URL: https://<seu-dominio>/webhook/whatsapp
  - Verify token: WHATSAPP_VERIFY_TOKEN (variável de ambiente)

Para adicionar ao app.py:
  from cookbook.jarvis.webhook import build_whatsapp_router
  app.include_router(build_whatsapp_router())
"""

import hashlib
import hmac
import logging
import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response

from cookbook.jarvis.agents.whatsapp_agent import get_whatsapp_agent
from cookbook.jarvis.config import get_tenant_config

logger = logging.getLogger("jarvis.webhook")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "jarvis-verify")
APP_SECRET = os.getenv("META_APP_SECRET", "")

# Tenant lookup: phone_number_id -> tenant_id
# In production, query the DB. For demo, use env or a hardcoded map.
_PHONE_TO_TENANT: Dict[str, str] = {
    os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""): os.getenv("JARVIS_TENANT_ID", "demo"),
}


def _resolve_tenant(phone_number_id: str) -> Optional[str]:
    """Return tenant_id for a given WhatsApp phone_number_id."""
    return _PHONE_TO_TENANT.get(phone_number_id)


def _verify_signature(payload: bytes, signature_header: Optional[str]) -> bool:
    """Verify X-Hub-Signature-256 from Meta. Skip if APP_SECRET not set."""
    if not APP_SECRET:
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = (
        "sha256=" + hmac.new(APP_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    )
    return hmac.compare_digest(expected, signature_header)


# ---------------------------------------------------------------------------
# Background task: run agent and reply
# ---------------------------------------------------------------------------


async def _handle_message(
    tenant_id: str,
    sender_phone: str,
    message_text: str,
    message_id: str,
) -> None:
    """Process inbound message and send reply via the WhatsApp agent."""
    try:
        tenant = get_tenant_config(tenant_id)
        agent = get_whatsapp_agent(tenant)

        prompt = (
            f"[Mensagem recebida de {sender_phone}]\n"
            f"ID da mensagem: {message_id}\n\n"
            f"{message_text}"
        )

        response = await agent.arun(prompt)

        if response and response.content:
            logger.info(
                "Replied to %s on tenant %s: %s chars",
                sender_phone,
                tenant_id,
                len(response.content),
            )
        else:
            logger.warning("Agent returned empty response for message %s", message_id)

    except Exception:
        logger.exception(
            "Error handling WhatsApp message %s for tenant %s",
            message_id,
            tenant_id,
        )


# ---------------------------------------------------------------------------
# Router factory
# ---------------------------------------------------------------------------


def build_whatsapp_router(prefix: str = "/webhook") -> APIRouter:
    """Return a FastAPI router with WhatsApp webhook endpoints."""
    router = APIRouter(prefix=prefix, tags=["WhatsApp Webhook"])

    @router.get("/whatsapp")
    async def verify_webhook(request: Request) -> Response:
        """
        Verificacao do webhook pelo Meta.
        GET /webhook/whatsapp?hub.mode=subscribe&hub.verify_token=...&hub.challenge=...
        """
        params = request.query_params
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully")
            return Response(content=challenge, media_type="text/plain")

        raise HTTPException(status_code=403, detail="Verification failed")

    @router.post("/whatsapp")
    async def receive_message(
        request: Request,
        background_tasks: BackgroundTasks,
    ) -> Dict[str, Any]:
        """
        Recebe eventos do WhatsApp Business API.
        Responde 200 imediatamente e processa em background.
        """
        raw_body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256")

        if not _verify_signature(raw_body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        try:
            payload: Dict[str, Any] = await request.json()
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Invalid JSON") from exc

        # Parse Meta webhook structure
        # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                phone_number_id = value.get("metadata", {}).get("phone_number_id", "")
                tenant_id = _resolve_tenant(phone_number_id)

                if not tenant_id:
                    logger.warning(
                        "Unknown phone_number_id: %s — ignoring", phone_number_id
                    )
                    continue

                for msg in value.get("messages", []):
                    msg_type = msg.get("type")
                    sender_phone = msg.get("from", "")
                    message_id = msg.get("id", "")

                    if msg_type == "text":
                        text = msg.get("text", {}).get("body", "").strip()
                    elif msg_type == "interactive":
                        # Button reply or list reply
                        interactive = msg.get("interactive", {})
                        if interactive.get("type") == "button_reply":
                            text = interactive["button_reply"].get("title", "")
                        elif interactive.get("type") == "list_reply":
                            text = interactive["list_reply"].get("title", "")
                        else:
                            text = ""
                    else:
                        # Ignore audio, image, sticker, etc. for now
                        logger.debug(
                            "Unsupported message type %s from %s",
                            msg_type,
                            sender_phone,
                        )
                        continue

                    if text:
                        background_tasks.add_task(
                            _handle_message,
                            tenant_id,
                            sender_phone,
                            text,
                            message_id,
                        )

        return {"status": "ok"}

    return router
