from typing import Dict, Union

DB_CONFIG: Dict[str, Union[str, int]] = {
    "development": {
        'host': 'mysql',
        'port': 3306,
        'username': 'martin',
        'password': 'Penis123@',
        'database': 'rbac_fastapi',
    },
    "test": {
    }
}
