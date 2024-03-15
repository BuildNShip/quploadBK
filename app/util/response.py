from typing import Any, Dict, List, Union

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.websockets import WebSocket


class CustomResponse:
    """
    Utility class for creating custom JSON responses with error handling.

    Attributes:
    - message (Dict[str, Any]): Custom messages for the response.
    - general_message (Union[str, List[str]]): General messages for the response.
    - response (Dict[str, Any]): Additional response data.

    Methods:
    - get_success_response() -> JSONResponse:
      Generates a successful JSON response.

    - get_failure_response(
        status_code: int = 400,
        http_status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> JSONResponse:
      Generates a failed JSON response with customizable status codes.
    """

    def __init__(
            self,
            message: Dict[str, Any] = None,
            general_message: Union[str, List[str]] = None,
            response: Dict[str, Any] = None,
    ) -> None:
        """
        Initializes a CustomResponse instance.

        Parameters:
        - message (Dict[str, Any]): Custom messages for the response.
        - general_message (List[str]): General messages for the response.
        - response (Dict[str, Any]): Additional response data.
        """

        self.message = {} if message is None else message
        self.general_message = [] if general_message is None else general_message
        self.response = {} if response is None else response

        if not isinstance(self.general_message, list):
            self.general_message = [self.general_message]

        self.message.update({"general": self.general_message})

    def get_success_response(self) -> JSONResponse:
        """
        Generates a successful JSON response.

        Returns:
        - JSONResponse: Successful JSON response.
        """
        return JSONResponse(
            content={
                "hasError": False,
                "statusCode": status.HTTP_200_OK,
                "message": self.message,
                "response": self.response,
            },
            status_code=status.HTTP_200_OK,
        )

    def get_failure_response(
            self,
            status_code: int = 400,
            http_status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> JSONResponse:
        """
        Generates a failed JSON response with customizable status codes.

        Parameters:
        - status_code (int): Custom status code for the response.
        - http_status_code (int): HTTP status code for the response.

        Returns:
        - JSONResponse: Failed JSON response.
        """
        return JSONResponse(
            content={
                "hasError": True,
                "statusCode": status_code,
                "message": self.message,
                "response": self.response,
            },
            status_code=http_status_code,
        )


class WSCustomResponse:
    """
    Utility class for creating custom JSON responses with error handling.

    Attributes:
    - message (Dict[str, Any]): Custom messages for the response.
    - general_message (Union[str, List[str]]): General messages for the response.
    - response (Dict[str, Any]): Additional response data.

    Methods:
    - get_success_response() -> JSONResponse:
      Generates a successful JSON response.

    - get_failure_response(
        status_code: int = 400,
        http_status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> JSONResponse:
      Generates a failed JSON response with customizable status codes.
    """

    def __init__(
            self,
            websocket_connection: WebSocket,
            message: Dict[str, Any] = None,
            general_message: Union[str, List[str]] = None,
            response: Dict[str, Any] = None,
    ) -> None:
        """
        Initializes a CustomResponse instance.

        Parameters:
        - message (Dict[str, Any]): Custom messages for the response.
        - general_message (List[str]): General messages for the response.
        - response (Dict[str, Any]): Additional response data.
        """

        self.websocket_connection = websocket_connection
        self.message = {} if message is None else message
        self.general_message = [] if general_message is None else general_message
        self.response = {} if response is None else response

        if not isinstance(self.general_message, list):
            self.general_message = [self.general_message]

        self.message.update({"general": self.general_message})

    async def get_success_response(self) -> None:
        """
        Generates a successful JSON response.

        Returns:
        - JSONResponse: Successful JSON response.
        """
        await self.websocket_connection.send_json({
            "hasError": False,
            "statusCode": status.HTTP_200_OK,
            "message": self.message,
            "response": self.response,
        })

    async def get_failure_response(
            self,
            status_code: int = 1000
    ) -> None:
        """
        Generates a failed JSON response with customizable status codes.

        Parameters:
        - status_code (int): Custom status code for the response.

        Returns:
        - JSONResponse: Failed JSON response.
        """
        await self.websocket_connection.send_json({
            "hasError": True,
            "statusCode": status_code,
            "message": self.message,
            "response": self.response,
        })
