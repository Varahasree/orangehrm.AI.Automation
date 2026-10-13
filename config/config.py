import os

BASE_URL = os.getenv(
    "ORANGEHRM_URL",
    "https://opensource-demo.orangehrmlive.com/"
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://jsonplaceholder.typicode.com"
)

API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))