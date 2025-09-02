from core.config import settings


def auth_login() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.auth,
        "/login",
    )
    path = "".join(parts)
    return path.removeprefix("/")


def auth_register() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.auth,
        "/register",
    )
    path = "".join(parts)
    return path.removeprefix("/")


def resume() -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.resumes,
    )
    path = "".join(parts)
    return path


def resume_for_id(resume_id: int) -> str:
    parts = (
        settings.api.prefix,
        settings.api.v1.prefix,
        settings.api.v1.resumes,
        f"/{resume_id}",
    )
    path = "".join(parts)
    return path
