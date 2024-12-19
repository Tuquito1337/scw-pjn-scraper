from capmonster_python import RecaptchaV2Task
from config import CAP_MONSTER_APIKEY


def resolve_captcha(base_url, site_key):
    """Resuelve un captcha utilizando el servicio de CapMonster."""
    capmonster = RecaptchaV2Task(CAP_MONSTER_APIKEY)
    return capmonster.join_task_result(capmonster.create_task(base_url, site_key)).get(
        "gRecaptchaResponse"
    )
