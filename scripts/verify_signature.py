"""Implementação de referência para validar o cabeçalho X-Hub-Signature-256 da Meta."""

from __future__ import annotations

import hashlib
import hmac


def verify_hub_signature(
    raw_body: bytes,
    signature_header: str | None,
    app_secret: str,
) -> bool:
    """Valida a assinatura HMAC-SHA256 enviada pela Meta em ``X-Hub-Signature-256``.

    >>> secret = "meu_app_secret"
    >>> body = b'{"object":"whatsapp_business_account"}'
    >>> sig = "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    >>> verify_hub_signature(body, sig, secret)
    True
    >>> verify_hub_signature(body, sig.upper(), secret)
    False
    >>> verify_hub_signature(body + b" ", sig, secret)
    False
    >>> verify_hub_signature(body, "sha1=deadbeef", secret)
    False
    >>> verify_hub_signature(body, None, secret)
    False
    >>> verify_hub_signature(body, sig, "")
    False
    """
    if not signature_header or not app_secret:
        return False

    prefix = "sha256="
    if not signature_header.startswith(prefix):
        return False

    expected_digest = hmac.new(
        app_secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    expected_header = f"{prefix}{expected_digest}"

    return hmac.compare_digest(expected_header, signature_header)


if __name__ == "__main__":
    import doctest

    failures, attempted = doctest.testmod(verbose=True)
    if failures:
        raise SystemExit(1)
    print(f"Doctests OK ({attempted} checks).")
