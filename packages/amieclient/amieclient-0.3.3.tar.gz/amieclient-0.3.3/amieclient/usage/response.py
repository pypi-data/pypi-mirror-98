import json
from .message import UsageMessage, UsageMessageError
from .record import UsageRecordError


class UsageResponseError(Exception):
    pass


class UsageResponse:
    def __init__(self, message, failed_records):
        self.message = message
        self.failed_records = failed_records

    @classmethod
    def from_dict(cls, input_dict):
        records = [UsageRecordError.from_dict(d) for d in
                   input_dict.get('ValidationFailedRecords', [])]
        message = input_dict['Message']
        return cls(message=message, failed_records=records)

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        d = {
            'Message': self.message,
            'ValidationFailedRecords': [r.as_dict() for r in self.failed_records]
        }
        return d

    def json(self, **json_kwargs):
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def __repr__(self):
        return "<UsageResponse: {s.message}>".format(s=self)


class FailedUsageResponse:
    def __init__(self, failed_records):
        self.failed_records = failed_records

    @classmethod
    def from_dict(cls, input_dict):
        records = [UsageRecordError.from_dict(d) for d in
                   input_dict.get('ValidationFailedRecords', [])]
        return cls(failed_records=records)

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        d = {
            'FailedRecords': [r.as_dict() for r in self.failed_records]
        }
        return d

    def json(self, **json_kwargs):
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def __repr__(self):
        return "<FailedUsageResponse: {r} records>".format(r=len(self.failed_records))


class UsageStatusResource:
    def __init__(self, resource, loaded_record_count, failed_job_count,
                 total_charge, errors=None):
        self.resource = resource
        self.loaded_record_count = loaded_record_count
        self.failed_job_count = failed_job_count
        self.total_charge = total_charge
        self.errors = errors if errors is not None else []

    @classmethod
    def from_dict(cls, input_dict):
        errors = [UsageMessageError.from_dict(d) for d in input_dict.get('Errors', [])]
        return cls(
            resource=input_dict['Resource'],
            loaded_record_count=input_dict['LoadedRecordCount'],
            failed_job_count=input_dict['FailedJobCount'],
            total_charge=input_dict['TotalCharge'],
            errors=errors
        )

    @classmethod
    def from_json(cls, input_json):
        d = json.loads(input_json)
        return cls.from_dict(d)

    def as_dict(self):
        return {
            'Resource': self.resource,
            'LoadedRecordCount': self.loaded_record_count,
            'FailedJobCount': self.failed_job_count,
            'TotalCharge': self.total_charge,
            'Errors': [e.as_dict() for e in self.errors]
        }

    def json(self, **json_kwargs):
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def __repr__(self):
        return "<UsageStatusResource: {s.resource}, {n} errors>".format(s=self, n=len(self.errors))


class UsageStatus:
    def __init__(self, resources):
        self.resources = resources

    @classmethod
    def from_list(cls, input_list):
        resources = input_list
        return cls(
            resources=[UsageStatusResource.from_dict(d) for d in resources]
            )

    @classmethod
    def from_json(cls, input_list):
        d = json.loads(input_list)
        return cls.from_list(d)

    def as_list(self):
        return [r.as_dict() for r in self.resources]

    def json(self, **json_kwargs):
        return json.dumps(self.as_dict(), **json_kwargs)

    def pretty_print(self):
        """
        prints() a pretty version of the JSON of this packet
        """
        print(self.json(indent=4, sort_keys=True))

    def __repr__(self):
        return "<UsageStatus: {n} resources>".format(n=len(self.resources))
