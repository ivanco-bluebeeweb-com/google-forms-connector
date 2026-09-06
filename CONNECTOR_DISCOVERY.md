# Google Forms Connector — Discovery & API Specification

**Vendor:** Google Forms  
**Catalog URL:** https://workspace.google.com/products/forms  
**API Base URL:** `https://forms.googleapis.com/v1`  
**Authentication:** Google OAuth 2.0 (Scopes: forms.body, forms.responses.readonly)

## Core Entities & Endpoints
формы (/forms/{formId}), метаданные формы, блоки вопросов, ответы респондентов (/responses), вотчеры

## Verified Read Operation
- **Эндпоинт проверки:** `GET /v1/forms/{formId}`
- **Метод:** GET
- **Ожидаемый ответ:** HTTP 200 OK со структурой метаданных сущности.

## Rate Limits & Pagination
- Стандартная курсорная или offset/limit пагинация вендора.
- Обработка HTTP 429 Too Many Requests с экспоненциальным backoff.
- Защита от тайм-аутов: ограничение на сетевые запросы 15-30 секунд.
