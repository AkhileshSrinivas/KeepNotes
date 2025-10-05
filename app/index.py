"""
Module for configuring and initializing the Keep Notes FastAPI application.

This module defines the `KeepNotesApplication` class, which wraps the FastAPI app 
and provides modular configuration such as API routing, middleware setup, 
and Cross-Origin Resource Sharing (CORS) support.

Classes:
    KeepNotesApplication: A class that encapsulates the FastAPI application configuration.

Usage:
    keep_notes_app = KeepNotesApplication()
    app = keep_notes_app.get_app()
"""

# Import the necessary modules
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth_router
from routers.home import home_router
from routers.notes import note_router

class KeepNotesApplication:
    """
    Encapsulates the configuration and initialization of a FastAPI application.

    Attributes:
        title (str): Title of the FastAPI application.
        description (str): Brief description of the application.
        version (str): Version of the application.
        app (FastAPI): The FastAPI application instance.

    Methods:
        get_app() -> FastAPI:
            Returns the FastAPI application instance.
        include_router(router, prefix: str = ""):
            Adds a router to the FastAPI application with an optional URL prefix.
        add_cors(origins: list[str]):
            Configures Cross-Origin Resource Sharing (CORS) with specified allowed origins.
    """

    def __init__(self):
        """
        Initializes the KeepNotesApplication instance with default configurations.

        The title, description, and version are retrieved from environment variables 
        or fallback to default values.
        """

        self.title = config("TITLE", default="KeepNotes_Application")
        self.description = config(
            "DESCRIPTION", default="A REST API for a Keep Notes application"
        )
        self.version = config("VERSION", default="v1")
        self.app = None
        self.initialize_app()

    def initialize_app(self):
        """
        Creates and initializes the FastAPI application instance with title, description and version.
        """

        self.app = FastAPI(
            title=self.title,
            description=self.description,
            version=self.version,
        )

    def get_app(self) -> FastAPI:
        """
        Retrieves the FastAPI application instance.

        Returns:
            FastAPI: Configured FastAPI application.
        """

        return self.app

    def include_router(self, router, prefix: str = ""):
        """
        Adds a router to the FastAPI application.

        Args:
            router (APIRouter): The router instance to include.
            prefix (str, optional): The URL prefix for the router's endpoints. Defaults to "".
        """
        self.app.include_router(router, prefix=prefix)

    def add_cors(self, origins: list[str]):
        """
        Configures Cross-Origin Resource Sharing (CORS) middleware.

        Args:
            origins (list[str]): List of allowed origins for cross-origin requests.
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


# Initialize the KeepNotes application with the required configurations
notes_app = KeepNotesApplication()

# Configure CORS with allowed origins
allowed_origins = config(
    "ALLOWED_ORIGINS", 
    default="http://localhost:8000"
).split(",")  # Default to localhost
notes_app.add_cors(allowed_origins)

# Include the routers in the application
notes_app.include_router(auth_router, prefix="/Homepage")
notes_app.include_router(home_router, prefix="/Homepage")
notes_app.include_router(note_router, prefix="/Homepage")

# Retrieve the FastAPI application instance
app = notes_app.get_app()
