ЧАСТЬ А. ФУНКЦИИ

#1. НОРМАЛИЗАЦИЯ ИМЕЙЛ
def normalize_addresses(value: str) -> str:
    return value.strip().lower()


print(normalize_addresses("  Hello@Mail.RU  "))

#2. КОРОТКАЯ ВЕРСИЯ ПИСЬМА
def add_short_body(email: dict) -> dict:
    email["short_body"] = email["body"][:10] + "..."
    return email


test_email = {"body": "Привет, коллега! Как дела?"}
print(add_short_body(test_email))

#3. ОЧИСТКА ТЕКСТА ПИСЬМА
def clean_body_text(body: str) -> str:
    return body.replace("\n", " ").replace("\t", " ")


print(clean_body_text("Привет,\nколлега!\tКак дела?"))

#4. ИТОГОВЫЙ ТЕКСТ ПИСЬМА
def build_sent_text(email: dict) -> str:
    text = (
        f"Кому: {email['recipient']}, от {email['sender']}\n"
        f"Тема: {email['subject']}, дата {email['date']}\n"
        f"{email['short_body']}"
    )
    return text

#5. ПРОВЕРКА ПУСТОТЫ ТЕМЫ И ТЕЛА
def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    return subject.strip() == "", body.strip() == ""


print(check_empty_fields("", "Текст"))
print(check_empty_fields("Тема", ""))

#6. МАСКА ИМЕЙЛ ОТПРАВИТЕЛЯ
def mask_sender_email(login: str, domain: str) -> str:
    return login[:2] + "***@" + domain


print(mask_sender_email("default", "study.com"))

#7. ПРОВЕРКА КОРРЕКТНОСТИ ИМЕЙЛ
def get_correct_email(email_list: list[str]) -> list[str]:
    correct = []
    for email in email_list:
        email = email.strip()
        if "@" in email and (email.endswith(".com") or email.endswith(".ru") or email.endswith(".net")):
            correct.append(email)
    return correct

test_emails = [
    "user@gmail.com",
    "admin@company.ru",
    "usergmail.com",
    "user@domain.org",
    " hello@corp.ru  ",
]

print(get_correct_email(test_emails))

#8. СОЗДАНИЕ СЛОВАРЯ ПИСЬМА
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }


print(create_email("a@mail.ru", "b@mail.ru", "Тема", "Текст"))

#9. ДОБАВЛЕНИЕ ДАТЫ
from datetime import date

def add_send_date(email: dict) -> dict:
    email["date"] = str(date.today())
    return email


print(add_send_date({"test": 1}))

#10. ПОЛУЧЕНИЕ ЛОГИНА И ДОМЕНА
def extract_login_domain(address: str) -> tuple[str, str]:
    parts = address.split("@")
    return parts[0], parts[1]


print(extract_login_domain("user@mail.ru"))


ЧАСТЬ В. ОТПРАВКА ПИСЬМА


def sender_email(recipient_list: list[str], subject: str, message: str, *, sender="default@study.com") -> list[dict]:
    # 1. Проверка пустого списка
    if not recipient_list:
        return []

    # 2. Проверка корректности email
    recipient_list = get_correct_email(recipient_list)
    sender_list = get_correct_email([sender])
    if not sender_list:
        return []
    sender = sender_list[0]

    # 3. Проверка темы и тела
    is_subject_empty, is_body_empty = check_empty_fields(subject, message)
    if is_subject_empty or is_body_empty:
        return []

    # 4. Исключить отправку самому себе
    recipient_list = [r for r in recipient_list if r != sender]

    # 5. Нормализация
    subject = clean_body_text(subject)
    message = clean_body_text(message)
    recipient_list = [normalize_addresses(r) for r in recipient_list]
    sender = normalize_addresses(sender)

    emails = []

    for recipient in recipient_list:
        # 6. Создать письмо
        email = create_email(sender, recipient, subject, message)

        # 7. Дата
        email = add_send_date(email)

        # 8. Маска отправителя
        login, domain = extract_login_domain(sender)
        email["masked_sender"] = mask_sender_email(login, domain)

        # 9. Короткое тело
        email = add_short_body(email)

        # 10. Итоговый текст
        email["sent_text"] = build_sent_text(email)

        emails.append(email)

    return emails

## ПРОВЕРКА
recipients = [
    "admin@company.ru",
    "user@gmail.com",
    "default@study.com",   # проверка отправки самому себе
    "wrongmail",
]

result = sender_email(
    recipients,
    "Hello!\n",
    "Привет,\nколлега!\tКак дела?"
)

for email in result:
    print(email["sent_text"])
    print("-" * 40)
