from typing import Dict, Union

DB_CONFIG: Dict[str, Union[str, int]] = {
    "development": {
        'host': 'mysql',
        'port': 3306,
        'username': '',
        'password': '',
        'database': '',
    },
    "test": {
    }
}
