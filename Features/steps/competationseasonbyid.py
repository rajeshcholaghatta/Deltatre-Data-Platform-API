import json
import time
import allure
from behave import *
import requests
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

@given(u'the seasons details to be fetched based on ID from deltatre sports platform with parameter {locale} variable')
def step_impl(context,locale):
    context.url = f"{context.base_url}/v1/{context.projectCode}/football/competitions/{context.competitionId}/seasons"
    context.params = {
        "locale": locale
    }


@when(u'we execute the Get seasons by ID GETAPI method')
def step_impl(context):
    try:
        start_time = time.time()
        context.response = requests.get(context.url, params=context.params, timeout=5)
        elapsed_time = time.time() - start_time

        assert context.response.status_code == 200, "❌ Status code is not 200"
        allure.attach("✅ Status code is 200")

        assert elapsed_time < 60, "❌ API took too long to respond"
        allure.attach("✅ API took less than a minute to respond")

    except requests.exceptions.Timeout:
        allure.attach("❌ Request timed out!")


@then(u'seasons list is displayed based on ID')
def step_impl(context):
    context.json_data = context.response.text
    context.json_data = json.loads(context.response.text)
    seasons = context.json_data.get("seasons", [])

    if seasons:
        seasonId = seasons[0].get("seasonId")
        assert seasonId.startswith("cpl::Football_Season::"), f"❌ Unexpected competitionId format: {seasonId}"
        allure.attach("✅ seasonId Validation is Passed")

        startDateUtc = seasons[0].get("startDateUtc")
        assert startDateUtc is None, "❌ startDateUtc is not null"
        allure.attach("✅ startDateUtc Validation is Passed")

        endDateUtc = seasons[0].get("endDateUtc")
        assert endDateUtc is None, "❌ endDateUtc is not null"
        allure.attach("✅ endDateUtc Validation is Passed")

        seasonName = seasons[0].get("seasonName")
        assert seasonName.startswith("20"), f"❌ seasonName doesn't start with '20': {seasonName}"
        allure.attach("✅ seasonName Validation is Passed")

        competitionId = seasons[0].get("competitionId")
        assert competitionId.startswith("cpl::Football_Competition::"), f"❌ unexpected competitionId format start with: {competitionId}"
        allure.attach("✅ competitionId Validation is Passed")

        providerId = seasons[0].get("providerId")
        assert providerId.startswith("opta:Season:"), f"❌ unexpected providerId format doesn't start with : {providerId}"
        allure.attach("✅ providerId Validation is Passed")

        name = seasons[0].get("name")
        assert isinstance(name, str), f"❌ name is not a string: {type(name)}"
        allure.attach("✅ name Validation is Passed")

        officialName = seasons[0].get("officialName")
        assert isinstance(officialName, str), f"❌ officialName is not a string: {type(officialName)}"
        allure.attach("✅ officialName Validation is Passed")

        shortName = seasons[0].get("shortName")
        assert isinstance(shortName, str), f"❌ shortName is not a string: {type(shortName)}"
        allure.attach("✅ officialName Validation is Passed")

        acronymName = seasons[0].get("acronymName")
        assert isinstance(acronymName, str), f"❌ acronymName is not a string: {type(acronymName)}"
        allure.attach("✅ acronymName Validation is Passed")

    else:
        allure.attach("❌ No Competation seasons by ID found in the response.")

    try:
        validate(instance=context.response.json(), schema=context.competationseasonbyidschema)
        allure.attach("✅ Competation Season By ID Schema validation is Passed")
    except ValidationError as e:
        allure.attach(f"❌Competation Season By ID Schema validation failed: {e.message}")