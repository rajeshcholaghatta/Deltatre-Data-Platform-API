import json
import logging
import os
import time
import allure
from behave import *
import requests
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
import logger

@given(u'the season details to be fetched based on ID from deltatre sports platform with parameter {locale} variable')
def step_impl(context,locale):
    context.url = f"{context.base_url}/v1/{context.projectCode}/football/seasons/{context.seasonId}"
    context.params = {
        "locale": locale
    }


@when(u'we execute the Get season by ID GETAPI method')
def step_impl(context):
    try:
        start_time = time.time()
        context.response = requests.get(context.url, params=context.params, timeout=5)
        elapsed_time = time.time() - start_time
        assert context.response.status_code == 200, "❌ Status code is not 200"
        context.logger.debug(context.response.json())
        assert context.response.status_code == 200, f"❌ Status code is {context.response.status_code}, expected 200"
        allure.attach("✅ Status code is 200")
        context.logger.debug(context.response.status_code)

        assert elapsed_time < 60, "❌ API took too long to respond"
        allure.attach("✅ API took less than a minute to respond")

    except requests.exceptions.Timeout:
        allure.attach("❌ Request timed out!")



@then(u'season details is displayed based on ID')
def step_impl(context):
    logger=logging.getLogger()
    context.json_data = context.response.text
    context.json_data = json.loads(context.response.text)
    season = context.json_data.get("season", {})
    seasonId = context.json_data.get("season", {}).get("seasonId")
    context.logger.debug(season)

    if season:
        seasonId = season.get("seasonId")
        assert seasonId.startswith("cpl::Football_Season::"), f"❌ Unexpected competitionId format: {seasonId}"
        allure.attach("✅ seasonId Validation is Passed")
        context.logger.debug(seasonId)

        startDateUtc = season.get("startDateUtc")
        assert startDateUtc is None, "❌ startDateUtc is not null"
        allure.attach("✅ startDateUtc Validation is Passed")
        context.logger.debug(startDateUtc)

        endDateUtc = season.get("endDateUtc")
        assert endDateUtc is None, "❌ endDateUtc is not null"
        allure.attach("✅ endDateUtc Validation is Passed")
        context.logger.debug(endDateUtc)

        seasonName = season.get("seasonName")
        assert seasonName.startswith("20"), f"❌ seasonName doesn't start with '20': {seasonName}"
        allure.attach("✅ seasonName Validation is Passed")
        context.logger.debug(seasonName)

        competitionId = season.get("competitionId")
        assert competitionId.startswith("cpl::Football_Competition::"), f"❌ competitionId doesn't start with: {competitionId}"
        allure.attach("✅ competitionId Validation is Passed")
        context.logger.debug(competitionId)

        providerId = season.get("providerId")
        assert providerId.startswith("opta:Season:"), f"❌ providerId doesn't start with : {providerId}"
        allure.attach("✅ providerId Validation is Passed")
        context.logger.debug(providerId)

        name = season.get("name")
        assert isinstance(name, str), f"❌ name is not a string: {type(name)}"
        allure.attach("✅ name Validation is Passed")
        context.logger.debug(name)

        officialName = season.get("officialName")
        assert isinstance(officialName, str), f"❌ officialName is not a string: {type(officialName)}"
        allure.attach("✅ officialName Validation is Passed")
        context.logger.debug(officialName)

        shortName = season.get("shortName")
        assert isinstance(shortName, str), f"❌ shortName is not a string: {type(shortName)}"
        allure.attach("✅ officialName Validation is Passed")
        context.logger.debug(shortName)

        acronymName = season.get("acronymName")
        assert isinstance(acronymName, str), f"❌ acronymName is not a string: {type(acronymName)}"
        allure.attach("✅ acronymName Validation is Passed")
        context.logger.debug(acronymName)

    else:
        allure.attach("❌ No seasons by ID found in the response.")
        context.logger.debug("No seasons by ID found in the response.")

    try:
        schema_path = os.path.join("resources", "schema", "seasonschema.json")
        with open(schema_path, "r") as schema_file:schema = json.load(schema_file)
        validate(instance=context.response.json(), schema=schema)
        context.logger.debug("✅ Schema validation passed.")

    except ValidationError as e:
        allure.attach(f"❌ Season by ID Schema validation failed: {e.message}")
        context.logger.error(e.message)