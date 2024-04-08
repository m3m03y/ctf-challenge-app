"""Azure Function API for flag submitter"""
import logging
import azure.functions as func
from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.azure_proxy import AzureProxy
from ctf_server.model.flag import Flag
from ctf_server.model.state import State
from ctf_server.service.flag_service import FlagService

app = func.FunctionApp()


@app.route(route="submit", auth_level=func.AuthLevel.ANONYMOUS)
def submit(req: func.HttpRequest) -> func.HttpResponse:
    """Based on user input request to check whether  flag is valid"""
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
        value = req_body.get("value")
        task_id = req_body.get("task_id")
        challenge_id = req_body.get("challenge_id")
    except ValueError:
        pass

    if value and task_id and challenge_id:
        flag = Flag(value=value, challenge_id=challenge_id, task_id=task_id)
        flag_service = FlagService(AzureProxy(), PlainInputStoredHashedStrategy())
        state = flag_service.submit_flag(flag=flag)
        return func.HttpResponse(state, status_code=200)

    return func.HttpResponse(
        State.INVALID_FLAG,
        status_code=200,
    )
