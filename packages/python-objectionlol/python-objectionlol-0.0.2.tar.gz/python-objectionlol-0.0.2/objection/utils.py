import json
from .types import User, Evidence


def make_data(payload, req):
    return payload + json.dumps(req, separators=(',', ':'))


def clear_json(text):
    return text.strip("1234567890:")


def parse_users(users):
    return {u["id"]: User.from_raw(u)
            for u in users}


def parse_evidence(evidence):
    return [Evidence.from_raw(e) for e in evidence]
