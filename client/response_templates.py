from pydantic import BaseModel, Field, conint, constr


class GetUpdatesModel(BaseModel):
    """Класс, соответствующий входному update-у из tg"""

    offset: conint(ge=0) = Field(
        None, description="Identifier of the first update to be returned"
    )
    limit: conint(ge=1, le=100) = Field(
        100, description="Limits the number of updates to be retrieved"
    )
    timeout: conint(ge=0) = Field(0, description="Timeout in seconds for long polling")

    class Config:
        """Содержит пример update'a"""

        schema_extra = {"example": {"offset": 123456789, "limit": 50, "timeout": 60}}


class SendMessageModel(BaseModel):
    """Класс, соответствующий сообщению, которое будет отправлено в tg"""

    chat_id: str = Field(
        ...,
        description="Unique identifier for the target chat or username of the target channel",
    )
    text: constr(strip_whitespace=True) = Field(
        ..., description="Text of the message to be sent"
    )
    parse_mode: str = Field(
        None,
        description="Mode for parsing entities in the message text",
        regex="^(Markdown|HTML)$",
    )
    disable_web_page_preview: bool = Field(
        False, description="Disables link previews for links in this message"
    )
    disable_notification: bool = Field(False, description="Sends the message silently")

    @validator("chat_id")
    def chat_id_must_be_digit_or_start_with_at(cls, v):
        if not v.isdigit() and not v.startswith("@"):
            raise ValueError("chat_id must be a number or start with @ for channels")
        return v
