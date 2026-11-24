# n8n-whatsapp-meta-cloud-api-starter

Workflow inicial para **n8n** integrado à **WhatsApp Cloud API oficial da Meta** (Graph API v21.0), com verificação de webhook (`GET`), resposta imediata `200 OK` (`POST`), filtragem de callbacks de status e envio de resposta em texto.

## O que faz

O arquivo [`workflow/whatsapp-meta-cloud-api-starter.json`](workflow/whatsapp-meta-cloud-api-starter.json) contém dois fluxos no mesmo endpoint `/webhook/whatsapp`:

1. **Verificação do webhook (`GET`):** valida `hub.mode === "subscribe"` e compara `hub.verify_token` com `$env.WHATSAPP_VERIFY_TOKEN`, retornando `hub.challenge` com status `200` (ou `403` se inválido).
2. **Recebimento e resposta (`POST`):** responde `200 EVENT_RECEIVED` imediatamente para evitar retentativas da Meta, extrai a primeira mensagem de texto (`entry[0].changes[0].value.messages[0]`), ignora callbacks de status (`delivered`, `read`, `sent`) e envia uma resposta de eco via `https://graph.facebook.com/v21.0/<PHONE_NUMBER_ID>/messages` usando credencial `Header Auth` do n8n.

## Política de API oficial

Este projeto utiliza **exclusivamente a WhatsApp Business Platform (Cloud API oficial da Meta)**. Não utilize conectores não oficiais (como Baileys, Evolution API ou automações baseadas em leitura de QR Code / WhatsApp Web): além de violarem os Termos de Serviço do WhatsApp, expõem o número da empresa a bloqueios e banimentos definitivos.

## Pré-requisitos

- Conta no **Meta Business** (Portfólio Empresarial)
- Aplicativo criado em **Meta for Developers** com o produto **WhatsApp** adicionado
- Instância **n8n self-hosted** acessível via **HTTPS válido** (a Meta exige TLS válido para entrega de webhooks)

## Início rápido (passo a passo)

1. **Crie o aplicativo na Meta:** acesse o painel do Meta for Developers, crie um app do tipo Business e adicione o produto **WhatsApp**.
2. **Obtenha o `Phone Number ID`:** em *WhatsApp > API Setup*, copie o **Phone number ID** (não confundir com o número de telefone nem com o WABA ID).
3. **Gere o Access Token:**
   - Para testes rápidos, use o **token temporário** (expira em 24 horas) em *API Setup*.
   - Para produção, crie um **System User** no *Business Settings* da Meta, atribua o ativo do WhatsApp e gere um **token permanente** com as permissões `whatsapp_business_messaging` e `whatsapp_business_management`.
4. **Configure as variáveis de ambiente no n8n:** use [`.env.example`](.env.example) como referência para definir `WHATSAPP_VERIFY_TOKEN` e `WHATSAPP_PHONE_NUMBER_ID` no ambiente do n8n.
5. **Importe o workflow e crie a credencial:**
   - No n8n, importe [`workflow/whatsapp-meta-cloud-api-starter.json`](workflow/whatsapp-meta-cloud-api-starter.json).
   - No nó **Enviar Resposta WhatsApp**, selecione ou crie uma credencial **Header Auth** com:
     - `Name`: `Authorization`
     - `Value`: `Bearer SEU_ACCESS_TOKEN_DA_META`
   - Salve e ative o workflow.
6. **Configure o Webhook na Meta:**
   - Em *WhatsApp > Configuration > Webhook*, informe a URL HTTPS de produção do nó `Webhook Verificacao (GET)` / `Webhook Mensagens (POST)` (ex.: `https://seu-n8n.exemplo.com/webhook/whatsapp`) e o mesmo `WHATSAPP_VERIFY_TOKEN`.
   - Clique em *Verify and save*.
   - Em *Webhook fields*, assine o campo **`messages`**.
7. **Validação de assinatura (`X-Hub-Signature-256`):** consulte [`docs/assinatura-x-hub-signature-256.md`](docs/assinatura-x-hub-signature-256.md) e a referência em [`scripts/verify_signature.py`](scripts/verify_signature.py) para verificar a autenticidade das requisições em produção.

## Janela de 24 horas, templates e custos

- **Janela de atendimento de 24 horas:** mensagens livres de texto (como a enviada por este starter) só são entregues dentro de uma janela de 24 horas após a última mensagem enviada pelo usuário. Para iniciar conversas ou responder após 24 horas, é obrigatório usar **Message Templates** previamente aprovados pela Meta.
- **Custos e limites:** a cobrança da Cloud API segue o modelo oficial da Meta por conversa/mensagem e categoria. Consulte sempre a documentação oficial de preços: <https://developers.facebook.com/docs/whatsapp/pricing>.

## Limitações e aviso legal

- Este repositório é um ponto de partida mínimo para testes e adaptação em ambiente próprio; não inclui fila de processamento, persistência de estado de conversa, tratamento de mídia (áudio/imagem/documento) nem verificação de `X-Hub-Signature-256` embutida no JSON (documentada em separado por exigir `Raw Body` no Webhook).
- Mantenha tokens, App Secret e credenciais fora de controle de versão.

## Sobre a Operanza

Este projeto é mantido pela [Operanza](https://www.operanza.com.br), empresa brasileira especializada em agentes de IA e automação de processos com integração oficial.

Conteúdos relacionados:

- [API Oficial do WhatsApp vs. Não Oficial](https://www.operanza.com.br/conteudos/api-oficial-whatsapp-vs-nao-oficial)
- [Qualificar Leads no WhatsApp e CRM com IA](https://www.operanza.com.br/conteudos/qualificar-leads-whatsapp-crm-com-ia)
- [n8n vs. Make vs. Zapier](https://www.operanza.com.br/conteudos/n8n-vs-make-vs-zapier)
- [Agentes de IA para WhatsApp e CRM](https://www.operanza.com.br/agentes-ia-whatsapp-crm)

Contato: contato@operanza.com.br
