"""
Response Handler module.

Responsible for all response validation and parsing logic.
Provides reusable methods for status validation, JSON parsing, and schema validation.
"""

import requests
from typing import Any, Dict, List, Union
from jsonschema import validate, ValidationError
from utils.logger import get_logger


class ResponseHandler:
    """
    Handler for API response validation and parsing.

    Follows Single Responsibility Principle - handles only response processing.
    """

    def __init__(self):
        """Initialize response handler."""
        self.logger = get_logger(__name__)

    def assert_status(self, response: requests.Response, expected_status: int) -> None:
        """
        Assert response status code matches expected value.

        Args:
            response: Response object
            expected_status: Expected HTTP status code

        Raises:
            AssertionError: If status code doesn't match
        """
        actual_status = response.status_code
        assert actual_status == expected_status, (
            f"Expected status {expected_status}, but got {actual_status}. "
            f"Response: {response.text}"
        )
        self.logger.info(f"Status code validation passed: {expected_status}")

    def get_json(self, response: requests.Response) -> Union[Dict[str, Any], List[Any]]:
        """
        Parse response JSON with error handling.

        Args:
            response: Response object

        Returns:
            Parsed JSON data (dict or list)

        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            json_data = response.json()
            self.logger.debug(f"Successfully parsed JSON response")
            return json_data
        except requests.exceptions.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            raise ValueError(f"Response is not valid JSON: {response.text}") from e

    def validate_schema(self, json_data: Union[Dict, List], schema: Dict[str, Any]) -> None:
        """
        Validate JSON data against schema.

        Args:
            json_data: JSON data to validate
            schema: JSON schema definition

        Raises:
            ValidationError: If validation fails
        """
        try:
            validate(instance=json_data, schema=schema)
            self.logger.info("Schema validation passed")
        except ValidationError as e:
            self.logger.error(f"Schema validation failed: {e.message}")
            raise

    def assert_field_exists(self, json_data: Dict[str, Any], field_name: str) -> None:
        """
        Assert that a field exists in JSON data.

        Args:
            json_data: JSON data dictionary
            field_name: Field name to check

        Raises:
            AssertionError: If field doesn't exist
        """
        assert field_name in json_data, f"Field '{field_name}' not found in response"
        self.logger.debug(f"Field '{field_name}' exists in response")

    def assert_field_value(
                            self,
                            json_data: Dict[str, Any],
                            field_name: str,
                            expected_value: Any
                        ) -> None:
        """
        Assert that a field has an expected value.

        Args:
            json_data: JSON data dictionary
            field_name: Field name to check
            expected_value: Expected value

        Raises:
            AssertionError: If value doesn't match
        """
        self.assert_field_exists(json_data, field_name)
        actual_value = json_data[field_name]
        assert actual_value == expected_value, (
            f"Field '{field_name}': expected '{expected_value}', "
            f"but got '{actual_value}'"
        )
        self.logger.info(f"Field '{field_name}' has expected value: {expected_value}")

    def assert_field_type(
                            self,
                            json_data: Dict[str, Any],
                            field_name: str,
                            expected_type: type
                        ) -> None:
        """
        Assert that a field has an expected type.

        Args:
            json_data: JSON data dictionary
            field_name: Field name to check
            expected_type: Expected Python type

        Raises:
            AssertionError: If type doesn't match
        """
        self.assert_field_exists(json_data, field_name)
        actual_value = json_data[field_name]
        assert isinstance(actual_value, expected_type), (
            f"Field '{field_name}': expected type {expected_type.__name__}, "
            f"but got {type(actual_value).__name__}"
        )
        self.logger.debug(f"Field '{field_name}' has expected type: {expected_type.__name__}")

    def assert_non_empty_list(self, json_data: List[Any]) -> None:
        """
        Assert that response is a non-empty list.

        Args:
            json_data: JSON data (should be a list)

        Raises:
            AssertionError: If not a list or empty
        """
        assert isinstance(json_data, list), f"Expected list, but got {type(json_data).__name__}"
        assert len(json_data) > 0, "Expected non-empty list, but got empty list"
        self.logger.info(f"Response is a non-empty list with {len(json_data)} items")

    def assert_list_length(self, json_data: List[Any], expected_length: int) -> None:
        """
        Assert that list has expected length.

        Args:
            json_data: JSON data (should be a list)
            expected_length: Expected list length

        Raises:
            AssertionError: If length doesn't match
        """
        assert isinstance(json_data, list), f"Expected list, but got {type(json_data).__name__}"
        actual_length = len(json_data)
        assert actual_length == expected_length, (
            f"Expected list length {expected_length}, but got {actual_length}"
        )
        self.logger.info(f"List has expected length: {expected_length}")


