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

# Configure these only for an OrangeHRM instance
# where you are authorized to use its API.
ORANGEHRM_API_BASE_URL = os.getenv(
    "ORANGEHRM_API_BASE_URL",
    ""
)
