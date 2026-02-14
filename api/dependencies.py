from fastapi import Request

from src.philo_chat import PhiloChat


def get_philo_chat(request: Request):
    return PhiloChat(
        base_url=request.app.state.base_url,
        api_key=request.app.state.openai_api_key,
        model_name=request.app.state.model_name,
    )
