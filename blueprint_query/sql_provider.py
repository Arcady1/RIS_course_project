import os
from string import Template

class SQLProvider:
    def __init__(self, file_path: str) -> None:
        # = > _scripts = {'query_1.database: "select * from waybill where id = ///'
        self._scripts = {}

        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())

    # = > get ('user_by_operation.ssql', id = ..., ... = ..., ...)
    def get(self, name, **kwargs):
        return self._scripts[name].substitute(**kwargs)