from typing import Optional, List
from enum import Enum

from .base import BaseModel
from .attachments import Like, Repost, Attachments, Geo

from .additional import PostSource

# https://vk.com/dev/objects/post


class WallPostComments(BaseModel):
    count: int
    can_post: int
    groups_can_post: int
    can_close: bool
    can_open: bool


class Copyright(BaseModel):
    id: int
    link: str
    name: str
    type: str


class View(BaseModel):
    count: int


class PostType(Enum):
    post = 'post'
    copy = 'copy'
    reply = 'reply'
    postpone = 'postpone'
    suggest = 'suggest'


class WallPost(BaseModel):
    id: int
    owner_id: int
    from_id: int
    created_by: int
    date: int
    text: str
    reply_owner_id: int
    reply_post_id: int
    friends_only: int
    comments: WallPostComments
    copyright: Copyright
    likes: Like
    reposts: Repost
    views: View
    post_type: PostType
    post_source: PostSource
    attachments: Attachments
    geo: Geo
    signer_id: int
    copy_history: Optional['WallPost']
    can_pin: int
    can_delete: int
    can_edit: int
    is_pinned: int
    marked_as_ads: int
    is_favorite: bool
    donut: Donut
    postponed_id: Optional[int]
