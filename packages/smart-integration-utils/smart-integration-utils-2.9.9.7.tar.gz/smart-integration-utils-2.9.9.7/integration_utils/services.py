import csv
from hashlib import md5
from datetime import datetime, timedelta
from typing import Optional, Any, Union, Generator
from rest_framework.response import Response

from .exceptions import InvalidDateParams
from .tools import (
    get_file_link,
    check_file_exist,
    upload_to_s3,
    delete_file,
    has_items,
)


class BaseDataManager(object):
    model: Any = None
    serializer: Any = None
    default_limit: int = 150000
    query_limit: int = 1000
    with_last_id: bool = True
    last_id_field: str = 'id'

    def __init__(self, integration_id: int, date_from: str, date_to: str):
        self.integration_id = integration_id
        self.date_from = date_from
        self.date_to = date_to

    def get_serializer_class(self) -> Any:
        if not self.serializer:
            raise NotImplementedError(
                'get_serializer_class or serializer must be implemented.'
            )
        return self.serializer

    def get_model(self) -> Any:
        if not self.model:
            raise NotImplementedError('get_model or model must be implemented.')
        return self.model

    def get_count(self) -> int:
        raise NotImplementedError('get_count must be implemented.')

    def get_data(self, skip: int = 0, **kwargs) -> list:
        raise NotImplementedError('get_data must be implemented.')

    def get_default_serializer_fields(self) -> list:
        serializer = self.get_serializer_class()
        fields = list(serializer().fields.keys())
        return fields

    def serialize_data(self, data: Any, fields: list) -> Union[Generator, list, dict]:
        raise NotImplementedError('serialize_data must be implemented.')

    def _generate_file(self, s3_filename: str, fields: list, skip: int):
        with open(s3_filename, 'w') as f:
            writer = csv.DictWriter(f, delimiter='\t', fieldnames=fields)
            writer.writeheader()
            last_id = None
            while True:
                result = self.get_data(skip=skip, last_id=last_id)
                exist, data = has_items(result)
                if not exist:
                    break
                if self.with_last_id:
                    last_id = (
                        getattr(data[-1], self.last_id_field)
                        if isinstance(data, list)
                        else getattr(list(data)[-1], self.last_id_field)
                    )
                data = self.serialize_data(data, fields)
                for row in data:
                    writer.writerow(row)
                skip += self.query_limit

    def _generate_file_link(self, skip: int, s3_filename: str, fields: list) -> tuple:
        if check_file_exist(s3_filename):
            skip += self.default_limit
            return get_file_link(s3_filename)
        self._generate_file(s3_filename, fields, skip)
        s3_file_data = upload_to_s3(s3_filename)
        return skip, get_file_link(s3_file_data['s3_filename'])

    def _generate_result(self, filename: str, fields: list) -> dict:
        skip = 0
        part = 0
        count = self.get_count()
        links = []
        if self.default_limit >= count:
            skip, link = self._generate_file_link(skip, f'{filename}.tsv', fields)
            links.append(link)
            delete_file(f'{filename}.tsv')
        else:
            while skip <= count:
                while skip <= self.default_limit:
                    part += 1
                    part_filename = f'{filename}_{part}'
                    s3_filename = f"{part_filename}.tsv"
                    skip, link = self._generate_file_link(
                        skip, f'{filename}.tsv', fields
                    )
                    links.append(link)
                    delete_file(s3_filename)
        return {'links': links}

    def generate(self, filename: str, fields: Optional[list] = None) -> dict:
        fields: list = fields if fields else self.get_default_serializer_fields()
        return self._generate_result(filename=filename, fields=fields)


class BaseStatisticSelector(object):
    selector_type: str = 'base'

    def __init__(
        self,
        data: dict,
        integration_id: int,
        admin: int,
        platform_id: str = 'prod',
        values: list = [],
    ):
        self.data = data
        self.integration_id = integration_id
        self.admin = admin
        self.platform_id = platform_id
        self.values = values

    def get_date_params(self) -> any:
        date_from = None
        date_to = None
        if self.data.get("last_week", "").lower() == 'true':
            date_to = datetime.today().strftime('%Y-%m-%d')
            last_date = datetime.today() - timedelta(days=7)
            date_from = last_date.strftime('%Y-%m-%d')
        elif self.data.get("last_3_days", "").lower() == 'true':
            date_to = datetime.today().strftime('%Y-%m-%d')
            last_date = datetime.today() - timedelta(days=3)
            date_from = last_date.strftime('%Y-%m-%d')

        elif self.data.get('date_from') and self.data.get('date_to'):
            date_to = self.data['date_to']
            date_from = self.data['date_from']

        if not date_to or not date_from:
            raise InvalidDateParams(
                {
                    "status": "error",
                    "message": "Miss date param (like last_week,last_3_days, date_from and date_to)",
                }
            )
        return date_from, date_to

    def generate_statistic_response(
        self, date_from: str, date_to: str, filename: str
    ) -> Response:
        raise NotImplementedError()

    def generate_file_name(self, date_from: str, date_to: str) -> str:
        if self.values:
            hash_ = md5(str(self.values).encode('utf-8')).hexdigest()
            filename = f'/tmp/{self.selector_type}_{self.admin}_{self.integration_id}_{hash_}{date_from}:{date_to}'
        else:
            filename = f'/tmp/{self.selector_type}_{self.admin}_{self.integration_id}_{date_from}:{date_to}'
        return filename

    def response(self) -> Response:
        date_from, date_to = self.get_date_params()
        filename = self.generate_file_name(date_from=date_from, date_to=date_to)
        return self.generate_statistic_response(
            date_from=date_from, date_to=date_to, filename=filename,
        )

