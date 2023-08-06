from enum import Enum, auto
from . import Pair, Permissions, User, Frame, Evidence, Background, Offset
from ..utils import parse_users, parse_evidence


class AuthType(Enum):
    Password = auto()
    NoPassword = 0


class RoomData:
    _key = "room_data"

    def __init__(self, frame_time_limit, allow_custom_characters,
                 title, users, spectators,
                 evidence, background, pairs,
                 slow_mode_seconds,
                 restrict_evidence, restrict_custom_audio,
                 permissions, auth_type):
        self.frame_time_limit = frame_time_limit
        self.allow_custom_characters = allow_custom_characters
        self.restrict_evidence = restrict_evidence
        self.restrict_custom_audio = restrict_custom_audio
        self.title = title
        self.spectators = spectators
        self.slow_mod_seconds = slow_mode_seconds

        self.evidence = evidence
        self.background = background
        self.pairs = pairs
        self.permissions = permissions

        self.users = users

        self.auth_type = AuthType(auth_type)

    @classmethod
    def from_raw(cls, data):
        permissions = Permissions.from_raw(data["permissions"])
        users = parse_users(data["users"])
        evidence = parse_evidence(data["evidence"])
        pairs = [Pair.from_raw(p) for p in data["pairs"]]
        background = [Background.from_raw(p["background"])
                      for p in data["background"]]

        return cls(
            frame_time_limit=data['frameTimeLimit'],
            allow_custom_characters=data['allowCustomCharacters'],
            title=data['title'],
            users=users,
            spectators=data['spectators'],
            evidence=evidence,
            background=background,
            pairs=pairs,
            slow_mode_seconds=data['slowModeSeconds'],
            restrict_evidence=data['restrictEvidence'],
            restrict_custom_audio=data['restrictCustomAudio'],
            permissions=permissions,
            auth_type=data['authType'])


class NewOwner:
    _key = "new_owner"

    def __init__(self, user):
        self.user = user

    @classmethod
    def from_raw(cls, data):
        return cls(user=User.from_raw(data))


class UserJoined:
    _key = "user_joined"

    def __init__(self, user):
        self.user = user

    @classmethod
    def from_raw(cls, data):
        return cls(user=User.from_raw(data))


class JoinError:
    _key = "join_error"

    def __init__(self, msg):
        self.msg = msg

    @classmethod
    def from_raw(cls, data):
        return cls(msg=data)


class JoinSuccess:
    _key = "join_success"

    def __init__(self, user):
        self.user = user

    @classmethod
    def from_raw(cls, data):
        return cls(user=User.from_raw(data))


class UserLeft:
    _key = "user_left"

    def __init__(self, user):
        self.user = user

    @classmethod
    def from_raw(cls, data):
        return cls(user=User.from_raw(data))


class ChangeRoomProperty:
    _key = "change_room_property"

    def __init__(self, type, value):
        self.type = type
        self.value = value

    @classmethod
    def from_raw(cls, data):
        return cls(data["type"], data["value"])


class RemoveBackground:
    _key = "remove_background"

    def __init__(self, id):
        self.id = id

    @classmethod
    def from_raw(cls, data):
        return cls(data)


class RemoveEvidence:
    _key = "remove_evidence"

    def __init__(self, id):
        self.id = id

    @classmethod
    def from_raw(cls, data):
        return cls(data)


class AddBackground:
    _key = "add_background"

    def __init__(self, background, side, username, user_id):
        self.background = background
        self.side = side
        self.username = username
        self.user_id = user_id

    @classmethod
    def from_raw(cls, data):
        return cls(
            background=Background.from_raw(data['background']),
            side=data['side'],
            username=data['username'],
            user_id=data['userId'],
        )


class AddEvidence:
    _key = "add_evidence"

    def __init__(self, evidence):
        self.evidence = evidence

    @classmethod
    def from_raw(cls, data):
        return cls(evidence=Evidence.from_raw(data))


class AddPairing:
    _key = "add_pairing"

    def __init__(self, pairing):
        self.pairing = pairing

    @classmethod
    def from_raw(cls, data):
        return cls(pairing=Pair.from_raw(data))


class PairRequest:
    _key = "pair_request"

    def __init__(self, id, user_id, username):
        self.id = id
        self.user_id = user_id
        self.username = username

    @classmethod
    def from_raw(cls, data):
        return cls(
            id=data['id'],
            user_id=data['userId'],
            username=data['username']
        )


class CancelPair:
    _key = "cancel_pair"

    def __init__(self, id):
        self.id = id

    @classmethod
    def from_raw(cls, data):
        return cls(data)


class UpdatePairOffset:
    _key = "update_pair_offset"

    def __init__(self, id, offset1, offset2):
        self.id = id
        self.offset1 = offset1
        self.offset2 = offset2

    @classmethod
    def from_raw(cls, data):
        return cls(
            id=data['id'],
            offset1=Offset.from_raw(data['offset1']),
            offset2=Offset.from_raw(data['offset2']),
        )


class GetJoinOptions:
    _key = "get_join_options"

    def __init__(self, password_required, spectate, auth_type):
        self.password_required = password_required
        self.spectate = spectate
        self.auth_type = AuthType(auth_type)

    @classmethod
    def from_raw(cls, data):
        return cls(password_required=data["passwordRequired"],
                   spectate=data["spectate"],
                   auth_type=data["authType"])


class CriticalError:
    _key = "critical_error"

    def __init__(self, title, text):
        self.title = title
        self.text = text

    @classmethod
    def from_raw(cls, data):
        return cls(
            title=data['title'],
            text=data['text']
        )


class SetBanned:
    _key = "set_bans"

    def __init__(self, bans):
        self.banned = bans

    @classmethod
    def from_raw(cls, data):
        return cls(data)


class SetMods:
    _key = "set_mods"

    def __init__(self, mods):
        self.mods = mods

    @classmethod
    def from_raw(cls, data):
        return cls(data)


class ReceiveMessage:
    _key = "receive_message"

    def __init__(self, user_id, frame):
        self.user_id = user_id
        self.frame = frame

    @classmethod
    def from_raw(cls, data):
        return cls(user_id=data["userId"],
                   frame=Frame.from_raw(data["frame"]))


class ReceivePlainMessage:
    _key = "receive_plain_message"

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id

    @classmethod
    def from_raw(cls, data):
        return cls(
            text=data['text'],
            user_id=data['userId'],
        )


events = [UserJoined, UserLeft, NewOwner,
          JoinSuccess, JoinError,
          RoomData, GetJoinOptions, ChangeRoomProperty,
          SetMods, SetBanned,
          CancelPair, PairRequest, AddPairing,
          UpdatePairOffset,
          CriticalError,
          RemoveEvidence, AddEvidence,
          RemoveBackground, AddBackground,
          ReceiveMessage, ReceivePlainMessage]


def parse_event(event, data):
    for e in events:
        if e._key == event:
            return e.from_raw(data)
    raise TypeError(f"unknown event type {event}")
