from database import get_connection
from fastapi import APIRouter

router = APIRouter(
    prefix="/sql_health",
    tags=["SQL Health"]
)

@router.get("")
def sql_health_check():
    # Here you would typically check the health of your SQL database connection
    # For demonstration purposes, we'll return a static response
    connection = get_connection()
    if not connection:
        return {
            "status": "DOWN",
            "message": "Failed to connect to SQL database"
        }
    else:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT status, message FROM URL.HealthCheck;")
            row = cursor.fetchone()
            return {
                        "status": row.status,
                        "message": row.message
                    }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)            }

        finally:
            connection.close()