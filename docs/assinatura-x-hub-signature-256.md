# Validação da Assinatura `X-Hub-Signature-256`

A Meta assina todas as requisições `POST` enviadas ao webhook da WhatsApp Cloud API utilizando o cabeçalho HTTP `X-Hub-Signature-256`. Validar essa assinatura garante que o payload foi enviado pela Meta e não foi adulterado em trânsito.

## Como funciona

1. A Meta calcula o HMAC-SHA256 sobre os **bytes brutos do corpo da requisição** (`raw body`), usando o **App Secret** do aplicativo na Meta for Developers como chave.
2. O valor do cabeçalho segue o formato:

   ```text
   X-Hub-Signature-256: sha256=<digest_hexadecimal>
   ```

3. No servidor receptor, você deve:
   - Ler o corpo bruto exatamente como chegou (sem fazer parse/re-serialização JSON antes do HMAC, pois espaços ou ordem de chaves alteram o hash).
   - Calcular `HMAC-SHA256(app_secret, raw_body)`.
   - Comparar o resultado com o cabeçalho utilizando comparação em tempo constante (`hmac.compare_digest` em Python ou `crypto.timingSafeEqual` em Node.js).

## Atenção ao usar no n8n

No nó **Webhook** do n8n, **ative a opção `Raw Body`** (`Add Option` > `Raw Body` = `true`), caso contrário o n8n disponibiliza apenas o objeto JSON já parseado e o cálculo do HMAC não baterá com o hash enviado pela Meta.

Alternativas para produção:

- **No próprio n8n (self-hosted):** com `Raw Body` ativado no nó Webhook e `NODE_FUNCTION_ALLOW_BUILTIN=crypto` habilitado no ambiente do n8n, valide a assinatura em um nó `Code` antes de processar a mensagem.
- **No proxy reverso / API Gateway (recomendado):** valide `X-Hub-Signature-256` antes de encaminhar o `POST` para o endpoint do n8n, rejeitando requisições inválidas com HTTP `401` ou `403`.

## Implementação de referência em Python

Veja a implementação com biblioteca padrão (`hmac` e `hashlib`) em [`scripts/verify_signature.py`](../scripts/verify_signature.py):

```bash
python scripts/verify_signature.py
```
