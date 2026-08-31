import os
from dotenv import load_dotenv

load_dotenv()

account = os.getenv("SNOWFLAKE_ACCOUNT", "")
user = os.getenv("SNOWFLAKE_USER", "")
password = os.getenv("SNOWFLAKE_PASSWORD", "")
warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "")
database = os.getenv("SNOWFLAKE_DATABASE", "")

print(f"Credentials loaded for user {user} at account {account}, warehouse {warehouse}, DB {database}")
