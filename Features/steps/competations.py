import json
import os
import time
import allure
from behave import *
import requests
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from utils.logger import get_logger

@given('the competations details to be fetched from deltatre sports platform with parameter {locale} variable')
def api(context,locale):
    context.url = f"{context.base_url}/v1/{context.projectCode}/football/competitions"
    context.params = {
        "locale": locale
    }

@when('we execute the Get Competations GETAPI method')
def step_apicall(context):
    try:
        start_time = time.time()
        context.response = requests.get(context.url, params=context.params,timeout=5)
        elapsed_time = time.time() - start_time
        context.logger.debug(f"API call took {elapsed_time} seconds")

        assert context.response.status_code == 200, "❌ Status code is not 200"
        context.logger.debug(f"Response code {context.response.status_code} seconds")
        assert context.response.status_code == 200, f"❌ Status code is {context.response.status_code}, expected 200"
        allure.attach("✅ Status code is 200")
        context.logger.debug(context.response.json())


        assert elapsed_time < 60, "❌ API took too long to respond"
        allure.attach("✅ API took less than a minute to respond")

    except requests.exceptions.Timeout:
        allure.attach("❌ Request timed out!")

@then('competations list is displayed')
def step_verification(context):
    context.json_data = context.response.text
    context.json_data = json.loads(context.response.text)
    competitions = context.json_data.get("competitions", [])
    context.logger.debug(f"competitions: {competitions}")

    if competitions:
        competitionId = competitions[0].get("competitionId")
        assert competitionId.startswith("cpl::Football_Competition::"), f"❌ Unexpected competitionId format: {competitionId}"
        allure.attach("✅ competitionId Validation is Passed")
        context.logger.debug(f"competitionId: {competitionId}")

        providerId = competitions[0].get("providerId")
        assert providerId.startswith("opta:Competition:"), f"❌ Unexpected competitionId format: {providerId}"
        allure.attach("✅ providerId Validation is Passed")
        context.logger.debug(f"providerId: {providerId}")

        name = competitions[0].get("name")
        assert isinstance(name, str), f"❌ name is not a string: {type(name)}"
        allure.attach("✅ name Validation is Passed")
        context.logger.debug(f"name: {name}")

        officialName = competitions[0].get("officialName")
        assert isinstance(officialName, str), f"❌ officialName is not a string: {type(officialName)}"
        allure.attach("✅ officialName Validation is Passed")
        context.logger.debug(f"officialName: {officialName}")

        shortName = competitions[0].get("shortName")
        assert isinstance(shortName, str), f"❌ shortName is not a string: {type(shortName)}"
        allure.attach("✅ shortName Validation is Passed")
        context.logger.debug(f"shortName: {shortName}")

        acronymName = competitions[0].get("acronymName")
        assert isinstance(acronymName, str), f"❌ acronymName is not a string: {type(acronymName)}"
        allure.attach("✅ acronymName Validation is Passed")
        context.logger.debug(f"acronymName: {acronymName}")

    else:
        allure.attach("❌ No competitions found in the response.")
        context.logger.debug(f"no competitions found in the response.")


    try:
        schema_path = os.path.join("resources", "schema", "competationschema.json")
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)
        validate(instance=context.response.json(), schema=schema)
        context.logger.debug("✅ Schema validation passed.")

    except ValidationError as e:
        allure.attach(f"❌ Competations Schema validation failed: {e.message}")
        context.logger.error(e.message)




