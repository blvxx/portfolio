from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.application.enquiries import EnquiryPolicyError
from src.config import Settings
from src.handlers import list_leads, receive_details


def make_message(*, full_name: str = "Demo Customer"):
    bot = SimpleNamespace(send_message=AsyncMock())
    return SimpleNamespace(
        from_user=SimpleNamespace(
            id=12345,
            username="demo_user",
            full_name=full_name,
        ),
        text="<b>Please contact me</b> about the service.",
        answer=AsyncMock(),
        bot=bot,
    )


def make_state():
    return SimpleNamespace(
        get_data=AsyncMock(
            return_value={
                "consent": True,
                "contact": "demo@example.com",
                "service": "Приём заявок",
            }
        ),
        clear=AsyncMock(),
    )


@pytest.mark.asyncio
async def test_receive_details_submits_enquiry_and_notifies_admin() -> None:
    message = make_message(full_name="<b>Demo Customer</b>")
    state = make_state()
    enquiry_service = SimpleNamespace(submit=AsyncMock(return_value=17))
    settings = Settings(bot_token="test-token", admin_chat_id=98765)

    await receive_details(message, state, enquiry_service, settings)

    command = enquiry_service.submit.await_args.args[0]
    assert command.telegram_user_id == 12345
    assert command.username == "demo_user"
    assert command.customer_name == "<b>Demo Customer</b>"
    assert command.contact == "demo@example.com"
    assert command.service == "Приём заявок"
    assert command.consent_given is True
    assert command.admin_chat_id == 98765

    state.clear.assert_awaited_once()
    message.answer.assert_awaited_once()
    assert "Заявка №17 сохранена" in message.answer.await_args.args[0]
    assert "очередь доставки" in message.answer.await_args.args[0]
    message.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_details_keeps_flow_open_when_application_policy_rejects() -> None:
    message = make_message()
    state = make_state()
    enquiry_service = SimpleNamespace(
        submit=AsyncMock(side_effect=EnquiryPolicyError("policy rejected"))
    )
    settings = Settings(bot_token="test-token", admin_chat_id=98765)

    await receive_details(message, state, enquiry_service, settings)

    message.answer.assert_awaited_once_with("policy rejected")
    state.clear.assert_not_awaited()
    message.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_details_skips_notification_when_admin_chat_is_not_configured() -> None:
    message = make_message()
    state = make_state()
    enquiry_service = SimpleNamespace(submit=AsyncMock(return_value=18))
    settings = Settings(bot_token="test-token")

    await receive_details(message, state, enquiry_service, settings)

    state.clear.assert_awaited_once()
    message.answer.assert_awaited_once()
    command = enquiry_service.submit.await_args.args[0]
    assert command.admin_chat_id is None
    assert "очередь доставки" not in message.answer.await_args.args[0]
    message.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_receive_details_rejects_message_without_sender() -> None:
    message = make_message()
    message.from_user = None
    state = make_state()
    enquiry_service = SimpleNamespace(submit=AsyncMock(return_value=19))
    settings = Settings(bot_token="test-token", admin_chat_id=98765)

    await receive_details(message, state, enquiry_service, settings)

    message.answer.assert_awaited_once()
    assert "Не удалось определить отправителя" in message.answer.await_args.args[0]
    state.get_data.assert_not_awaited()
    state.clear.assert_not_awaited()
    enquiry_service.submit.assert_not_awaited()
    message.bot.send_message.assert_not_awaited()



@pytest.mark.asyncio
async def test_list_leads_rejects_non_admin_without_reading_database() -> None:
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=111),
        chat=SimpleNamespace(type="private"),
        answer=AsyncMock(),
    )
    database = SimpleNamespace(get_recent_leads=AsyncMock(return_value=[]))
    settings = Settings(bot_token="test-token", admin_user_id=12345)

    await list_leads(message, database, settings)

    message.answer.assert_awaited_once()
    assert "настроенному администратору" in message.answer.await_args.args[0]
    database.get_recent_leads.assert_not_awaited()


@pytest.mark.asyncio
async def test_list_leads_rejects_admin_command_in_group_chat() -> None:
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=12345),
        chat=SimpleNamespace(type="supergroup"),
        answer=AsyncMock(),
    )
    database = SimpleNamespace(get_recent_leads=AsyncMock(return_value=[]))
    settings = Settings(bot_token="test-token", admin_user_id=12345)

    await list_leads(message, database, settings)

    message.answer.assert_awaited_once()
    assert "личном чате" in message.answer.await_args.args[0]
    database.get_recent_leads.assert_not_awaited()


@pytest.mark.asyncio
async def test_list_leads_allows_configured_admin_in_private_chat_and_escapes_data() -> None:
    message = SimpleNamespace(
        from_user=SimpleNamespace(id=12345),
        chat=SimpleNamespace(type="private"),
        answer=AsyncMock(),
    )
    database = SimpleNamespace(
        get_recent_leads=AsyncMock(
            return_value=[
                {
                    "id": 9,
                    "service": "<script>service</script>",
                    "customer_name": "<b>Customer</b>",
                    "contact": "demo@example.com",
                    "details": "Need <i>help</i> & advice",
                    "created_at": "2026-11-22T12:00:00+00:00",
                }
            ]
        )
    )
    settings = Settings(bot_token="test-token", admin_user_id=12345)

    await list_leads(message, database, settings)

    database.get_recent_leads.assert_awaited_once_with(limit=10)
    message.answer.assert_awaited_once()
    response = message.answer.await_args.args[0]
    assert "&lt;script&gt;service&lt;/script&gt;" in response
    assert "&lt;b&gt;Customer&lt;/b&gt;" in response
    assert "Need &lt;i&gt;help&lt;/i&gt; &amp; advice" in response
    assert "<script>" not in response
