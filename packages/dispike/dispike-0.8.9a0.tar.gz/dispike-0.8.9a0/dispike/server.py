from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
from loguru import logger
from .middlewares.verification import DiscordVerificationMiddleware
from .models.incoming import (
    IncomingDiscordInteraction,
    IncomingDiscordOptionList,
    SubcommandIncomingDiscordOptionList,
    IncomingDiscordOption,
)
from .eventer import EventHandler
from .eventer_helpers.determine_event_information import determine_event_information
from .response import DiscordResponse
import json
import typing


router = APIRouter()
interaction = EventHandler()


_RAISE_FOR_TESTING = False


@router.get("/ping")
async def ping():
    return PlainTextResponse(
        "If you see this, Your instance is working and accepting requests."
    )


@router.post("/interactions")
async def handle_interactions(request: Request) -> Response:
    logger.info("interaction recieved.")

    _get_request_body = json.loads(request.state._cached_body.decode())
    logger.info(_get_request_body)
    if _get_request_body["type"] == 1:
        logger.info("handling ACK Ping.")
        return {"type": 1}

    _parse_to_object = IncomingDiscordInteraction(**_get_request_body)
    _event_name, arguments = determine_event_information(_parse_to_object)
    logger.info(f"event name: {_event_name}")
    if interaction.check_event_exists(_event_name) == False:
        logger.debug("discarding event not existing.")
        return {"type": 5}

    # _event_settings = interaction.return_event_settings(_event_name)

    arguments[router._user_defined_setting_ctx_value] = _parse_to_object

    # Check the type hint for the return type, fallback for checking the type if no hints are provided
    try:
        _type_hinted_request = interaction.view_event_function_return_type(_event_name)
        _type_hinted_returned_value = _type_hinted_request["return"]
        if _type_hinted_returned_value == DiscordResponse:
            _get_res = await interaction.emit(_event_name, **arguments)

            logger.debug(_get_res.response)
            return _get_res.response
        elif _type_hinted_returned_value == dict:
            return await interaction.emit(_event_name, **arguments)
    except KeyError:
        logger.error(
            "unable to find return value for type hint.. resorting to guessing.."
        )
        if _RAISE_FOR_TESTING == True:
            raise AssertionError("No hinting!")  # pragma: no cover
    except Exception:
        logger.exception("unhandled exception for returning hinted value")
        raise

    interaction_data = await interaction.emit(_event_name, **arguments)
    if isinstance(interaction_data, DiscordResponse):
        interaction_data: DiscordResponse
        return interaction_data.response

    if isinstance(interaction_data, dict):
        return interaction_data

    # Backup response, simply acknowledge. (Type 5)
    return {"type": 5}
