from models.user import UserCredentials

STANDARD_USER = UserCredentials(
    username="standard_user",
    password="secret_sauce"
)
VISUAL_USER = UserCredentials(
    username="visual_user",
    password="secret_sauce"
)

# LOCKED_USER = UserCredentials(
#     username="locked_out_user",
#     password="secret_sauce"
# )

# PROBLEM_USER = UserCredentials(
#     username="problem_user",
#     password="secret_sauce"
# )

LOGIN_USERS = [
    STANDARD_USER,
    VISUAL_USER
]
