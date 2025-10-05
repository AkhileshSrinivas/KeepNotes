"""
This script defines a `FastAPIServer` class for managing and configuring FastAPI application server.
It utilizes `decouple` library to read environment variables from a `.env` file for configuration.

Features:
- Dynamically loads server configuration (e.g., host, port, reload, workers) from a `.env` file.
- Validates server configuration for correctness.
- Logs server events and configuration updates.
- Provides an easy-to-use interface to start the server with uvicorn.
"""

import multiprocessing
from decouple import config
import uvicorn


class FastAPIServer:
    """
    A class to configure and manage a FastAPI application server using uvicorn.

    Attributes:
        config (dict): A dictionary containing server configurations.

    Methods:
        run(): Starts the server.
        update_config(): Dynamically updates the server configuration.
        validate_config(): Validates the current server configuration.
        log(): Logs server events or configuration details.
    """

    def __init__(self):
        """
        Initializes the server with configuration from the .env file.
        """
        self.config = {
            "module_app": config("MODULE_APP", default="index:app"),
            "host": config("HOST", default="localhost"),
            "port": config("PORT", cast=int, default=8000),
            "reload": config("RELOAD", cast=bool, default=False),
            "workers": config("WORKERS", cast=int, default=1),
        }

    def run(self):
        """
        Starts the FastAPI application server with the current configuration.
        """
        self.log("Starting server...")
        uvicorn.run(
            self.config["module_app"],
            host=self.config["host"],
            port=self.config["port"],
            reload=self.config["reload"],
            workers=self.config["workers"],
        )

    def update_config(self, **kwargs):
        """
        Dynamically updates the server configuration.

        Args:
            **kwargs: Key-value pairs for configuration parameters.
        """
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                self.log(f"Updated {key} to {value}")

    def validate_config(self):
        """
        Validates the current server configuration.

        Raises:
            ValueError: If any configuration is invalid.
        """
        if not isinstance(self.config["port"], int) or not 1 <= self.config["port"] <= 65535:
            raise ValueError("Port must be an integer between 1 and 65535.")
        if self.config["workers"] < 1:
            raise ValueError("Workers must be at least 1.")
        self.log("Configuration is valid.")

    def log(self, message):
        """
        Logs server events or configuration details.

        Args:
            message (str): The message to log.
        """
        print(f"[SERVER LOG]: {message}")


# Entry point for running the application
if __name__ == "__main__":

    # Initialize and run the server
    multiprocessing.freeze_support()
    server = FastAPIServer()
    server.validate_config()
    server.run()
