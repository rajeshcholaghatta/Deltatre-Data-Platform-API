@smoke
Feature: Getting competations names
  # This is to get data for the API getcompetations

  Scenario Outline: Verify get competations API functionality
    Given the competations details to be fetched from deltatre sports platform with parameter <locale> variable
    When we execute the Get Competations GETAPI method
    Then competations list is displayed
    Examples:
      | locale |
      | en-us  |