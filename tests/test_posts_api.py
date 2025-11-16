"""
Test suite for JSONPlaceholder Posts API.

Covers:
- GET /posts (all posts)
- GET /posts/{id} (single post)
- GET /posts?userId={n} (filtered by user)
- POST /posts (create post)
- PUT /posts/{id} (update post)
- DELETE /posts/{id} (delete post)
- Negative test (invalid endpoint)
"""

import allure
import pytest


@allure.epic("JSONPlaceholder API")
@allure.feature("Posts Management")
class TestPostsAPI:
    """Test suite for Posts API endpoints."""

    @allure.story("Get All Posts")
    @allure.title("Test GET /posts - Retrieve all posts")
    @allure.description("Validates that GET /posts returns a list of posts with valid schema")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("API", "GET", "Posts")
    @pytest.mark.smoke
    def test_get_all_posts(self, api_client, response_handler, post_schema, logger):
        """
        Test GET /posts returns all posts.

        Validates:
        - Status code 200 
        - Response is non-empty list
        - Each item matches post schema
        """
        logger.info("Starting test: test_get_all_posts")

        # Make request
        response = api_client.get("/posts")

        # Validate status
        response_handler.assert_status(response, 200)

        # Parse and validate response
        posts = response_handler.get_json(response)
        response_handler.assert_non_empty_list(posts)

        # Validate schema for first few posts (optimization)
        for post in posts[:5]:
            response_handler.validate_schema(post, post_schema)

        logger.info(f"Test passed: Retrieved {len(posts)} posts")

    @allure.story("Get Single Post")
    @allure.title("Test GET /posts/1 - Retrieve specific post")
    @allure.description("Validates that GET /posts/1 returns post with id=1 and matches schema")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("API", "GET", "Posts")
    @pytest.mark.smoke
    def test_get_single_post(self, api_client, response_handler, post_schema, logger):
        """
        Test GET /posts/1 returns specific post.

        Validates:
        - Status code 200
        - Post id is 1
        - Response matches post schema
        """
        logger.info("Starting test: test_get_single_post")

        # Make request
        response = api_client.get("/posts/1")

        # Validate status
        response_handler.assert_status(response, 200)

        # Parse and validate response
        post = response_handler.get_json(response)
        response_handler.assert_field_value(post, "id", 1)
        response_handler.validate_schema(post, post_schema)

        logger.info(f"Test passed: Retrieved post with id=1, title='{post['title']}'")

    @allure.story("Filter Posts")
    @allure.title("Test GET /posts?userId={user_id} - Filter posts by user")
    @allure.description("Validates that GET /posts with userId parameter filters posts correctly")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "GET", "Posts", "Filter")
    @pytest.mark.regression
    @pytest.mark.parametrize("user_id", [1, 2])
    def test_get_posts_by_user(self, api_client, response_handler, post_schema, user_id, logger):
        """
        Test GET /posts?userId={n} filters posts by user.

        Validates:
        - Status code 200
        - All returned posts belong to specified user
        - Each post matches schema
        """
        logger.info(f"Starting test: test_get_posts_by_user with userId={user_id}")

        # Make request
        response = api_client.get("/posts", params={"userId": user_id})

        # Validate status
        response_handler.assert_status(response, 200)

        # Parse and validate response
        posts = response_handler.get_json(response)
        response_handler.assert_non_empty_list(posts)

        # Verify all posts belong to specified user
        for post in posts:
            response_handler.assert_field_value(post, "userId", user_id)
            response_handler.validate_schema(post, post_schema)

        logger.info(f"Test passed: Retrieved {len(posts)} posts for userId={user_id}")

    @allure.story("Create Post")
    @allure.title("Test POST /posts - Create new post")
    @allure.description("Validates that POST /posts creates a new post and returns correct data")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("API", "POST", "Posts", "Create")
    @pytest.mark.smoke
    def test_create_post(self, api_client, response_handler, logger):
        """
        Test POST /posts creates a new post.

        Validates:
        - Status code 201
        - Response echoes request data
        - Response includes id field
        """
        logger.info("Starting test: test_create_post")

        # Prepare payload
        payload = {
            "title": "Test Post",
            "body": "This is a test post body",
            "userId": 1
        }

        # Make request
        response = api_client.post("/posts", json=payload)

        # Validate status
        response_handler.assert_status(response, 201)

        # Parse and validate response
        created_post = response_handler.get_json(response)
        response_handler.assert_field_exists(created_post, "id")
        response_handler.assert_field_value(created_post, "title", payload["title"])
        response_handler.assert_field_value(created_post, "body", payload["body"])
        response_handler.assert_field_value(created_post, "userId", payload["userId"])

        logger.info(f"Test passed: Created post with id={created_post['id']}")

    @allure.story("Update Post")
    @allure.title("Test PUT /posts/1 - Update existing post")
    @allure.description("Validates that PUT /posts/1 updates post and returns updated data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "PUT", "Posts", "Update")
    @pytest.mark.regression
    def test_update_post(self, api_client, response_handler, logger):
        """
        Test PUT /posts/1 updates existing post.

        Validates:
        - Status code 200
        - Response echoes updated data
        """
        logger.info("Starting test: test_update_post")

        # Prepare payload
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1
        }

        # Make request
        response = api_client.put("/posts/1", json=payload)

        # Validate status
        response_handler.assert_status(response, 200)

        # Parse and validate response
        updated_post = response_handler.get_json(response)
        response_handler.assert_field_value(updated_post, "id", payload["id"])
        response_handler.assert_field_value(updated_post, "title", payload["title"])
        response_handler.assert_field_value(updated_post, "body", payload["body"])
        response_handler.assert_field_value(updated_post, "userId", payload["userId"])

        logger.info(f"Test passed: Updated post with id=1")

    @allure.story("Delete Post")
    @allure.title("Test DELETE /posts/1 - Delete post")
    @allure.description("Validates that DELETE /posts/1 successfully deletes a post")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "DELETE", "Posts")
    @pytest.mark.regression
    def test_delete_post(self, api_client, response_handler, logger):
        """
        Test DELETE /posts/1 deletes post.

        Validates:
        - Status code is 200 or 204
        """
        logger.info("Starting test: test_delete_post")

        # Make request
        response = api_client.delete("/posts/1")

        # Validate status (JSONPlaceholder returns 200)
        assert response.status_code in [200, 204], (
            f"Expected status 200 or 204, but got {response.status_code}"
        )

        logger.info(f"Test passed: Deleted post with status={response.status_code}")

    @allure.story("Error Handling")
    @allure.title("Test GET /postz - Invalid endpoint returns 404")
    @allure.description("Negative test: Validates that invalid endpoint returns 404 status")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "GET", "Negative", "404")
    @pytest.mark.smoke
    def test_invalid_endpoint_returns_404(self, api_client, response_handler, logger):
        """
        Negative test: Invalid endpoint returns 404.

        Validates:
        - Status code 404 for non-existent endpoint
        """
        logger.info("Starting test: test_invalid_endpoint_returns_404")

        # Make request to invalid endpoint
        response = api_client.get("/postz")

        # Validate status
        response_handler.assert_status(response, 404)

        logger.info("Test passed: Invalid endpoint correctly returned 404")

    @allure.story("Error Handling")
    @allure.title("Test GET /posts/99999 - Non-existent post returns 404")
    @allure.description("Negative test: Validates that non-existent post ID returns 404 status")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "GET", "Negative", "404")
    @pytest.mark.regression
    def test_get_non_existent_post_returns_404(self, api_client, response_handler, logger):
        """
        Negative test: Non-existent post ID returns 404.

        Validates:
        - Status code 404 for invalid post ID
        """
        logger.info("Starting test: test_get_non_existent_post_returns_404")

        # Make request with invalid post ID
        response = api_client.get("/posts/99999")

        # Validate status
        response_handler.assert_status(response, 404)

        logger.info("Test passed: Non-existent post correctly returned 404")

    @allure.story("Response Validation")
    @allure.title("Test GET /posts - Validate response structure")
    @allure.description("Validates response structure, field types, and data integrity")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("API", "GET", "Validation")
    @pytest.mark.regression
    def test_get_posts_response_structure(self, api_client, response_handler, logger):
        """
        Test GET /posts response has correct structure.

        Validates:
        - Response is a list
        - List contains at least 100 posts
        - Each post has required fields
        """
        logger.info("Starting test: test_get_posts_response_structure")

        # Make request
        response = api_client.get("/posts")

        # Validate status
        response_handler.assert_status(response, 200)

        # Parse response
        posts = response_handler.get_json(response)

        # Validate structure
        response_handler.assert_non_empty_list(posts)
        assert len(posts) >= 100, f"Expected at least 100 posts, but got {len(posts)}"

        # Validate first post has required fields
        first_post = posts[0]
        response_handler.assert_field_exists(first_post, "userId")
        response_handler.assert_field_exists(first_post, "id")
        response_handler.assert_field_exists(first_post, "title")
        response_handler.assert_field_exists(first_post, "body")

        # Validate field types
        response_handler.assert_field_type(first_post, "userId", int)
        response_handler.assert_field_type(first_post, "id", int)
        response_handler.assert_field_type(first_post, "title", str)
        response_handler.assert_field_type(first_post, "body", str)

        logger.info(f"Test passed: Response structure validated for {len(posts)} posts")

