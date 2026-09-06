# Google Forms Connector — Auth & Credentials Standard

**App ID:** `google-forms-connector`  
**Standard Compliance:** AUTH_AND_CREDENTIALS_STANDARD.md (B1–B10)

## Authentication Architecture
- **Тип авторизации:** Google OAuth 2.0 (Scopes: forms.body, forms.responses.readonly)
- **Принцип BYOC:** Пользователь подключает собственный аккаунт/ключи.
- **Хранение секретов:** Зашифрованные переменные окружения / Vault. Токены никогда не логируются и маскируются в ответах API.
- **Верификация подключения:** При сохранении ключа выполняется тестовый запрос `GET /v1/forms/{formId}`.
- **Отключение:** Удаление локальных ключей по команде пользователя без повреждения данных на стороне Google Forms.
