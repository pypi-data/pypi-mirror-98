from enum import Enum, auto


class Permission(Enum):
    Anyone = 0
    Mods = auto()
    Owner = auto()


class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_raw(cls, data):
        return cls(x=data["x"],
                   y=data["y"])


class User:
    def __init__(self, id, username, discord_username,
                 is_mod, is_owner, is_spectator):
        self.id = id
        self.username = username
        self.discord_username = discord_username
        self.is_mod = is_mod
        self.is_owner = is_owner
        self.is_spectator = is_spectator

    @classmethod
    def from_raw(cls, data):
        return cls(id=data['id'], username=data['username'],
                   discord_username=data['discordUsername'],
                   is_mod=data['isMod'], is_owner=data['isOwner'],
                   is_spectator=data['isSpectator'])


class Evidence:
    def __init__(self, id, user_id, name, url, description):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.url = url
        self.description = description

    @classmethod
    def from_raw(cls, data):
        return cls(id=data["id"], name=data["name"],
                   user_id=data["userId"],
                   url=data["url"], description=data.get("description"))


class Background:
    _key = "background"

    def __init__(self, id, name, url, desk_url):
        self.id = id
        self.name = name
        self.url = url
        self.desk_url = desk_url

    @classmethod
    def from_raw(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            url=data['url'],
            desk_url=data['deskUrl'],
        )


class Pair:
    def __init__(self, id, user_id1, user_id2, offset1, offset2, front,
                 status):
        self.id = id
        self.user_id1 = user_id1
        self.user_id2 = user_id2
        self.offset1 = offset1
        self.offset2 = offset2
        self.front = front
        self.status = status

    @classmethod
    def from_raw(cls, data):
        return cls(id=data['id'],
                   user_id1=data['userId1'], user_id2=data['userId2'],
                   offset1=Offset.from_raw(data['offset1']),
                   offset2=Offset.from_raw(data['offset2']),
                   front=data['front'], status=data['status'])


class Permissions:
    def __init__(self, add_evidence, add_background):
        self.add_evidence = Permission(add_evidence)
        self.add_background = Permission(add_background)

    @classmethod
    def from_raw(cls, data):
        return cls(data["addEvidence"], data["addBackground"])


class Frame:
    def __init__(self, id, text, pose_id,
                 bubble_type, username, merge_next,
                 do_not_talk, go_next, pose_animation,
                 flipped, frame_actions, frame_fades, background,
                 character_id, popup_id):
        self.id = id
        self.text = text
        self.pose_id = pose_id
        self.bubble_type = bubble_type
        self.username = username
        self.merge_next = merge_next
        self.do_not_talk = do_not_talk
        self.go_next = go_next
        self.pose_animation = pose_animation
        self.flipped = flipped
        self.frame_actions = frame_actions
        self.frame_fades = frame_fades
        self.background = background
        self.character_id = character_id
        self.popup_id = popup_id

    @classmethod
    def from_raw(cls, data):
        return cls(
            id=data['id'],
            text=data['text'],
            pose_id=data['poseId'],
            bubble_type=data['bubbleType'],
            username=data['username'],
            merge_next=data['mergeNext'],
            do_not_talk=data['doNotTalk'],
            go_next=data['goNext'],
            pose_animation=data['poseAnimation'],
            flipped=data['flipped'],
            frame_actions=data['frameActions'],
            frame_fades=data['frameFades'],
            background=data['background'],
            character_id=data['characterId'],
            popup_id=data['popupId'])
