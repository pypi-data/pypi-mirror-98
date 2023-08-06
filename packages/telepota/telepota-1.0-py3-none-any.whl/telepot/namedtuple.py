import collections
import warnings
import sys


class _Field(object):
    def __init__(self, name, constructor=None, default=None):
        self.name = name
        self.constructor = constructor
        self.default = default


# Function to produce namedtuple classes.
def _create_class(typename, fields):
    # extract field names
    field_names = [e.name if type(e) is _Field else e for e in fields]

    # Some dictionary keys are Python keywords and cannot be used as field names, e.g. `from`.
    # Get around by appending a '_', e.g. dict['from'] => namedtuple.from_
    keymap = [(k.rstrip('_'), k) for k in filter(lambda e: e in ['from_'], field_names)]

    # extract (non-simple) fields that need conversions
    conversions = [(e.name, e.constructor) for e in fields if type(e) is _Field and e.constructor is not None]

    # extract default values
    defaults = [e.default if type(e) is _Field else None for e in fields]

    # Create the base tuple class, with defaults.
    base = collections.namedtuple(typename, field_names)
    base.__new__.__defaults__ = tuple(defaults)

    class sub(base):
        def __new__(cls, **kwargs):
            # Map keys.
            for oldkey, newkey in keymap:
                if oldkey in kwargs:
                    kwargs[newkey] = kwargs[oldkey]
                    del kwargs[oldkey]

            # Any unexpected arguments?
            unexpected = set(kwargs.keys()) - set(super(sub, cls)._fields)

            # Remove unexpected arguments and issue warning.
            if unexpected:
                for k in unexpected:
                    del kwargs[k]

                s = ('Unexpected fields: ' + ', '.join(unexpected) + ''
                     '\nBot API seems to have added new fields to the returned data.'
                     ' This version of namedtuple is not able to capture them.'
                     '\n\nPlease upgrade telepot by:'
                     '\n  sudo pip install telepot --upgrade'
                     '\n\nIf you still see this message after upgrade, that means I am still working to '
                     'bring the code up-to-date.'
                     ' Please try upgrade again a few days later.'
                     ' In the meantime, you can access the new fields the old-fashioned way, '
                     'through the raw dictionary.')

                warnings.warn(s, UserWarning)

            # Convert non-simple values to namedtuples.
            for key, func in conversions:
                if key in kwargs:
                    if type(kwargs[key]) is dict:
                        kwargs[key] = func(**kwargs[key])
                    elif type(kwargs[key]) is list:
                        kwargs[key] = func(kwargs[key])
                    else:
                        raise RuntimeError('Can only convert dict or list')

            return super(sub, cls).__new__(cls, **kwargs)

    # https://bugs.python.org/issue24931
    # Python 3.4 bug: namedtuple subclass does not inherit __dict__ properly.
    # Fix it manually.
    if sys.version_info >= (3, 4):
        def _asdict(self):
            return collections.OrderedDict(zip(self._fields, self))

        sub._asdict = _asdict

    sub.__name__ = typename

    return sub


"""
Different treatments for incoming and outgoing namedtuples:

- Incoming ones require type declarations for certain fields for deeper parsing.
- Outgoing ones need no such declarations because users are expected to put the correct object in place.
"""


# Namedtuple class will reference other namedtuple classes. Due to circular
# dependencies, it is impossible to have all class definitions ready at
# compile time. We have to dynamically obtain class reference at runtime.
# For example, the following function acts like a constructor for `Message`
# so any class can reference the Message namedtuple even before the Message
# namedtuple is defined.
def _Message(**kwargs):
    return getattr(sys.modules[__name__], 'Message')(**kwargs)


# incoming
User = _create_class('User', [
    'id',
    'is_bot',
    'first_name',
    'last_name',
    'username',
    'language_code',
    'can_join_groups',
    'can_read_all_group_messages',
    'supports_inline_queries'
])


def UserArray(data):
    return [User(**p) for p in data]


# incoming
ChatPermissions = _create_class('ChatPermissions', [
    'can_send_messages',
    'can_send_media_messages',
    'can_send_polls',
    'can_send_other_messages',
    'can_add_web_page_previews',
    'can_change_info',
    'can_invite_users',
    'can_pin_messages'
])

# incoming
ChatPhoto = _create_class('ChatPhoto', [
    'small_file_id',
    'small_file_unique_id',
    'big_file_id',
    'big_file_unique_id'
])

# incoming
Chat = _create_class('Chat', [
    'id',
    'type',
    'title',
    'username',
    'first_name',
    'last_name',
    _Field('permissions', constructor=ChatPermissions),
    _Field('photo', constructor=ChatPhoto),
    'description',
    'invite_link',
    'slow_mode_delay',
    _Field('pinned_message', constructor=_Message),
    'sticker_set_name',
    'can_set_sticker_set',
])

# incoming
PhotoSize = _create_class('PhotoSize', [
    'file_id',
    'width',
    'height',
    'file_unique_id',
    'file_size',
    'file_path',  # undocumented
])

# incoming
Audio = _create_class('Audio', [
    'file_id',
    'file_unique_id',
    'duration',
    'performer',
    'title',
    'file_name',
    'mime_type',
    'file_size',
    _Field('thumb', constructor=PhotoSize)
])

# incoming
Document = _create_class('Document', [
    'file_id',
    _Field('thumb', constructor=PhotoSize),
    'file_unique_id',
    'file_name',
    'mime_type',
    'file_size',
    'file_path',  # undocumented
])

# incoming and outgoing
MaskPosition = _create_class('MaskPosition', [
    'point',
    'x_shift',
    'y_shift',
    'scale',
])

# incoming
Sticker = _create_class('Sticker', [
    'file_id',
    'width',
    'height',
    'is_animated',
    'file_unique_id',
    _Field('thumb', constructor=PhotoSize),
    'emoji',
    'set_name',
    _Field('mask_position', constructor=MaskPosition),
    'file_size',
])


def StickerArray(data):
    return [Sticker(**p) for p in data]


# incoming
StickerSet = _create_class('StickerSet', [
    'name',
    'title',
    'is_animated',
    'contains_masks',
    _Field('stickers', constructor=StickerArray),
    _Field('thumb', constructor=PhotoSize),
])

# incoming
BotCommand = _create_class('BotCommand', [
    'command',
    'description'
])

# incoming
PassportFile = _create_class('PassportFile', [
    'file_id',
    'file_unique_id',
    'file_size',
    'file_date'
])


def PassportFileArray(data):
    return [PassportFile(**p) for p in data]


# incoming
Video = _create_class('Video', [
    'file_id',
    'width',
    'height',
    'duration',
    _Field('thumb', constructor=PhotoSize),
    'file_name',
    'mime_type',
    'file_unique_id',
    'file_size',
    'file_path',  # undocumented
])

# incoming
Voice = _create_class('Voice', [
    'file_id',
    'duration',
    'mime_type',
    'file_size',
    'file_unique_id'
])

# incoming
VideoNote = _create_class('VideoNote', [
    'file_id',
    'length',
    'duration',
    _Field('thumb', constructor=PhotoSize),
    'file_size',
    'file_unique_id'
])

# incoming
Contact = _create_class('Contact', [
    'phone_number',
    'first_name',
    'last_name',
    'user_id',
    'vcard'
])

# incoming
Location = _create_class('Location', [
    'longitude',
    'latitude',
    'horizontal_accuracy',
    'live_period',
    'heading',
    'proximity_alert_radius'
])

# incoming
Venue = _create_class('Venue', [
    _Field('location', constructor=Location),
    'title',
    'address',
    'foursquare_id',
    'foursquare_type'
])

# incoming
File = _create_class('File', [
    'file_id',
    'file_size',
    'file_path',
    'file_unique_id'
])


def PhotoSizeArray(data):
    return [PhotoSize(**p) for p in data]


def PhotoSizeArrayArray(data):
    return [[PhotoSize(**p) for p in array] for array in data]


# incoming
UserProfilePhotos = _create_class('UserProfilePhotos', [
    'total_count',
    _Field('photos', constructor=PhotoSizeArrayArray)
])

# incoming
ChatMember = _create_class('ChatMember', [
    _Field('user', constructor=User),
    'status',
    'custom_title',
    'is_anonymous',
    'is_member',
    'until_date',
    'can_be_edited',
    'can_manage_chat',
    'can_manage_voice_chats',
    'can_change_info',
    'can_post_messages',
    'can_edit_messages',
    'can_delete_messages',
    'can_invite_users',
    'can_restrict_members',
    'can_pin_messages',
    'can_promote_members',
    'can_send_messages',
    'can_send_media_messages',
    'can_send_other_messages',
    'can_add_web_page_previews',
    'can_send_polls'
])


def ChatMemberArray(data):
    return [ChatMember(**p) for p in data]

# incoming
ChatInviteLink = _create_class('ChatInviteLink', [
    'invite_link',
    _Field('creator', constructor=User),
    'is_primary',
    'date',
    'is_revoked',
    'expire_date',
    'member_limit'
])

# incoming
ChatMemberUpdated = _create_class('ChatMemberUpdated', [
    _Field('chat', constructor=Chat),
    _Field('from_', constructor=User),
    'date',
    _Field('old_chat_member', constructor=ChatMember),
    _Field('new_chat_member', constructor=ChatMember),
    _Field('invite_link', constructor=ChatInviteLink),
])

# outgoing
ReplyKeyboardMarkup = _create_class('ReplyKeyboardMarkup', [
    'keyboard',
    'resize_keyboard',
    'one_time_keyboard',
    'selective',
])

KeyboardButtonPollType = _create_class('KeyboardButtonPollType', [
    'type'
])

# outgoing
KeyboardButton = _create_class('KeyboardButton', [
    'text',
    'request_contact',
    'request_location',
    _Field('request_poll', constructor=KeyboardButtonPollType)
])

# outgoing
ReplyKeyboardRemove = _create_class('ReplyKeyboardRemove', [
    _Field('remove_keyboard', default=True),
    'selective',
])

# outgoing
ForceReply = _create_class('ForceReply', [
    _Field('force_reply', default=True),
    'selective',
])

LoginUrl = _create_class('LoginUrl', [
    'url',
    'forward_text',
    'bot_username',
    'request_write_access'
])

# outgoing
InlineKeyboardButton = _create_class('InlineKeyboardButton', [
    'text',
    'url',
    _Field('login_url', constructor=LoginUrl),
    'callback_data',
    'switch_inline_query',
    'switch_inline_query_current_chat',
    'callback_game',
    'pay',
])

# outgoing
InlineKeyboardMarkup = _create_class('InlineKeyboardMarkup', [
    'inline_keyboard',
])

# incoming
MessageEntity = _create_class('MessageEntity', [
    'type',
    'offset',
    'length',
    'url',
    _Field('user', constructor=User),
    'language'
])


# incoming
def MessageEntityArray(data):
    return [MessageEntity(**p) for p in data]


# incoming
GameHighScore = _create_class('GameHighScore', [
    'position',
    _Field('user', constructor=User),
    'score',
])


PollOption = _create_class('PollOption', [
    'text',
    'voter_count'
])

PollAnswer = _create_class('PollAnswer', [
    'poll_id',
    _Field('user', constructor=User),
    'option_ids'
])

# outgoing
Poll = _create_class('Poll', [
    'id',
    'question',
    _Field('options', constructor=PollOption),
    'total_voter_count',
    'is_closed',
    'is_anonymous',
    'type',
    'allows_multiple_answers',
    'correct_option_id',
    'explanation',
    _Field('explanation_entities', constructor=MessageEntity),
    'open_period',
    'close_date',
])



# incoming
Animation = _create_class('Animation', [
    'file_id',
    'file_unique_id',
    'width',
    'height',
    'duration',
    _Field('thumb', constructor=PhotoSize),
    'file_name',
    'mime_type',
    'file_size',
])

# incoming
Game = _create_class('Game', [
    'title',
    'description',
    _Field('photo', constructor=PhotoSizeArray),
    'text',
    _Field('text_entities', constructor=MessageEntityArray),
    _Field('animation', constructor=Animation),
])

# incoming
Invoice = _create_class('Invoice', [
    'title',
    'description',
    'start_parameter',
    'currency',
    'total_amount',
])

# outgoing
LabeledPrice = _create_class('LabeledPrice', [
    'label',
    'amount',
])

# outgoing
ShippingOption = _create_class('ShippingOption', [
    'id',
    'title',
    'prices',
])

# incoming
ShippingAddress = _create_class('ShippingAddress', [
    'country_code',
    'state',
    'city',
    'street_line1',
    'street_line2',
    'post_code',
])

# incoming
OrderInfo = _create_class('OrderInfo', [
    'name',
    'phone_number',
    'email',
    _Field('shipping_address', constructor=ShippingAddress),
])

# incoming
ShippingQuery = _create_class('ShippingQuery', [
    'id',
    _Field('from_', constructor=User),
    'invoice_payload',
    _Field('shipping_address', constructor=ShippingAddress),
])

# incoming
PreCheckoutQuery = _create_class('PreCheckoutQuery', [
    'id',
    _Field('from_', constructor=User),
    'currency',
    'total_amount',
    'invoice_payload',
    'shipping_option_id',
    _Field('order_info', constructor=OrderInfo),
])

# incoming
SuccessfulPayment = _create_class('SuccessfulPayment', [
    'currency',
    'total_amount',
    'invoice_payload',
    'shipping_option_id',
    _Field('order_info', constructor=OrderInfo),
    'telegram_payment_charge_id',
    'provider_payment_charge_id',
])

# incoming
EncryptedCredentials = _create_class('EncryptedCredentials', [
    'data',
    'hash',
    'secret'
])

# incoming
EncryptedPassportElement = _create_class('EncryptedPassportElement', [
    'type',
    'data',
    'phone_number',
    'email',
    _Field('files', constructor=PassportFile),
    _Field('front_side', constructor=PassportFile),
    _Field('reverse_side', constructor=PassportFile),
    _Field('selfie', constructor=PassportFile),
    _Field('translation', constructor=PassportFileArray),
    'hash'
])

# incoming
PassportData = _create_class('PassportData', [
    _Field('data', constructor=EncryptedPassportElement),
    _Field('credentials', constructor=EncryptedCredentials),
])

Dice = _create_class('Dice', [
    'emoji',
    'value',
])

MessageAutoDeleteTimerChanged = _create_class('MessageAutoDeleteTimerChanged', [
    'message_auto_delete_time'
])

VoiceChatStarted = _create_class('VoiceChatStarted', [

])

VoiceChatEnded = _create_class('VoiceChatEnded', [
    'duration'
])

VoiceChatParticipantsInvited = _create_class('VoiceChatParticipantsInvited', [
    _Field('users', constructor=UserArray)
])

ProximityAlertTriggered = _create_class('ProximityAlertTriggered', [
    _Field('traveler', constructor=User),
    _Field('watcher', constructor=User),
    'distance'
])
# incoming
Message = _create_class('Message', [
    'message_id',
    _Field('from_', constructor=User),
    _Field('via_bot', constructor=User),
    'date',
    _Field('sender_chat', constructor=Chat),
    _Field('chat', constructor=Chat),
    _Field('forward_from', constructor=User),
    _Field('forward_from_chat', constructor=Chat),
    'forward_from_message_id',
    'forward_sender_name',
    'forward_signature',
    'forward_date',
    _Field('reply_to_message', constructor=_Message),
    'edit_date',
    'author_signature',
    'text',
    _Field('entities', constructor=MessageEntityArray),
    _Field('caption_entities', constructor=MessageEntityArray),
    _Field('animation', constructor=Animation),
    _Field('audio', constructor=Audio),
    _Field('document', constructor=Document),
    _Field('game', constructor=Game),
    _Field('photo', constructor=PhotoSizeArray),
    _Field('sticker', constructor=Sticker),
    _Field('video', constructor=Video),
    _Field('voice', constructor=Voice),
    _Field('video_note', constructor=VideoNote),
    _Field('new_chat_members', constructor=UserArray),
    'caption',
    _Field('contact', constructor=Contact),
    _Field('dice', constructor=Dice),
    _Field('location', constructor=Location),
    _Field('venue', constructor=Venue),
    _Field('poll', constructor=Poll),
    _Field('new_chat_member', constructor=User),
    _Field('left_chat_member', constructor=User),
    'new_chat_title',
    _Field('new_chat_photo', constructor=PhotoSizeArray),
    'delete_chat_photo',
    'group_chat_created',
    'supergroup_chat_created',
    'channel_chat_created',
    _Field('message_auto_delete_timer_changed', constructor=MessageAutoDeleteTimerChanged),
    'migrate_to_chat_id',
    'migrate_from_chat_id',
    _Field('pinned_message', constructor=_Message),
    _Field('invoice', constructor=Invoice),
    _Field('successful_payment', constructor=SuccessfulPayment),
    'connected_website',
    _Field('passport_data', constructor=PassportData),
    _Field('proximity_alert_triggered', constructor=ProximityAlertTriggered),
    _Field('voice_chat_started', constructor=VoiceChatStarted),
    _Field('voice_chat_ended', constructor=VoiceChatEnded),
    _Field('voice_chat_participants_invited', constructor=VoiceChatParticipantsInvited),
    'reply_markup'
])

# incoming
InlineQuery = _create_class('InlineQuery', [
    'id',
    _Field('from_', constructor=User),
    _Field('location', constructor=Location),
    'query',
    'offset',
])

# incoming
ChosenInlineResult = _create_class('ChosenInlineResult', [
    'result_id',
    _Field('from_', constructor=User),
    _Field('location', constructor=Location),
    'inline_message_id',
    'query',
])

# incoming
CallbackQuery = _create_class('CallbackQuery', [
    'id',
    _Field('from_', constructor=User),
    _Field('message', constructor=Message),
    'inline_message_id',
    'chat_instance',
    'data',
    'game_short_name',
])

# incoming
Update = _create_class('Update', [
    'update_id',
    _Field('message', constructor=Message),
    _Field('edited_message', constructor=Message),
    _Field('channel_post', constructor=Message),
    _Field('edited_channel_post', constructor=Message),
    _Field('inline_query', constructor=InlineQuery),
    _Field('chosen_inline_result', constructor=ChosenInlineResult),
    _Field('callback_query', constructor=CallbackQuery),
    _Field('shipping_query', constructor=ShippingQuery),
    _Field('pre_checkout_query', constructor=PreCheckoutQuery),
    _Field('poll', constructor=Poll),
    _Field('poll_answer', constructor=PollAnswer),
    _Field('my_chat_member', constructor=ChatMemberUpdated),
    _Field('chat_member', constructor=ChatMemberUpdated),
])


# incoming
def UpdateArray(data):
    return [Update(**u) for u in data]


# incoming
WebhookInfo = _create_class('WebhookInfo', [
    'url',
    'has_custom_certificate',
    'pending_update_count',
    'ip_address',
    'last_error_date',
    'last_error_message',
    'max_connections',
    'allowed_updates'
])

# outgoing
InputTextMessageContent = _create_class('InputTextMessageContent', [
    'message_text',
    'parse_mode',
    'disable_web_page_preview',
])

# outgoing
InputLocationMessageContent = _create_class('InputLocationMessageContent', [
    'latitude',
    'longitude',
    'live_period',
    'horizontal_accuracy',
    'heading',
    'proximity_alert_radius'
])

# outgoing
InputVenueMessageContent = _create_class('InputVenueMessageContent', [
    'latitude',
    'longitude',
    'title',
    'address',
    'foursquare_id',
    'foursquare_type',
    'google_place_id',
    'google_place_type'
])

# outgoing
InputContactMessageContent = _create_class('InputContactMessageContent', [
    'phone_number',
    'first_name',
    'last_name',
    'vcard'
])

# outgoing
InlineQueryResultArticle = _create_class('InlineQueryResultArticle', [
    _Field('type', default='article'),
    'id',
    'title',
    'input_message_content',
    'reply_markup',
    'url',
    'hide_url',
    'description',
    'thumb_url',
    'thumb_width',
    'thumb_height',
    'caption_entities'
])

# outgoing
InlineQueryResultPhoto = _create_class('InlineQueryResultPhoto', [
    _Field('type', default='photo'),
    'id',
    'photo_url',
    'thumb_url',
    'photo_width',
    'photo_height',
    'title',
    'description',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultGif = _create_class('InlineQueryResultGif', [
    _Field('type', default='gif'),
    'id',
    'gif_url',
    'gif_width',
    'gif_height',
    'gif_duration',
    'thumb_url',
    'thumb_mime_type',
    'title',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultMpeg4Gif = _create_class('InlineQueryResultMpeg4Gif', [
    _Field('type', default='mpeg4_gif'),
    'id',
    'mpeg4_url',
    'mpeg4_width',
    'mpeg4_height',
    'mpeg4_duration',
    'thumb_url',
    'thumb_mime_type',
    'title',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultVideo = _create_class('InlineQueryResultVideo', [
    _Field('type', default='video'),
    'id',
    'video_url',
    'mime_type',
    'thumb_url',
    'title',
    'caption',
    'parse_mode',
    'video_width',
    'video_height',
    'video_duration',
    'description',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultAudio = _create_class('InlineQueryResultAudio', [
    _Field('type', default='audio'),
    'id',
    'audio_url',
    'title',
    'caption',
    'parse_mode',
    'performer',
    'audio_duration',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultVoice = _create_class('InlineQueryResultVoice', [
    _Field('type', default='voice'),
    'id',
    'voice_url',
    'title',
    'caption',
    'parse_mode',
    'voice_duration',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultDocument = _create_class('InlineQueryResultDocument', [
    _Field('type', default='document'),
    'id',
    'title',
    'caption',
    'parse_mode',
    'document_url',
    'mime_type',
    'description',
    'reply_markup',
    'input_message_content',
    'thumb_url',
    'thumb_width',
    'thumb_height',
    'caption_entities'
])

# outgoing
InlineQueryResultLocation = _create_class('InlineQueryResultLocation', [
    _Field('type', default='location'),
    'id',
    'latitude',
    'longitude',
    'title',
    'horizontal_accuracy',
    'live_period',
    'heading',
    'proximity_alert_radius',
    'reply_markup',
    'input_message_content',
    'thumb_url',
    'thumb_width',
    'thumb_height',
    'caption_entities'
])

# outgoing
InlineQueryResultVenue = _create_class('InlineQueryResultVenue', [
    _Field('type', default='venue'),
    'id',
    'latitude',
    'longitude',
    'title',
    'address',
    'foursquare_id',
    'foursquare_type',
    'google_place_id',
    'google_place_type',
    'reply_markup',
    'input_message_content',
    'thumb_url',
    'thumb_width',
    'thumb_height',
    'caption_entities'
])

# outgoing
InlineQueryResultContact = _create_class('InlineQueryResultContact', [
    _Field('type', default='contact'),
    'id',
    'phone_number',
    'first_name',
    'last_name',
    'vcard',
    'reply_markup',
    'input_message_content',
    'thumb_url',
    'thumb_width',
    'thumb_height',
    'caption_entities'
])

# outgoing
InlineQueryResultGame = _create_class('InlineQueryResultGame', [
    _Field('type', default='game'),
    'id',
    'game_short_name',
    'reply_markup',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedPhoto = _create_class('InlineQueryResultCachedPhoto', [
    _Field('type', default='photo'),
    'id',
    'photo_file_id',
    'title',
    'description',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedGif = _create_class('InlineQueryResultCachedGif', [
    _Field('type', default='gif'),
    'id',
    'gif_file_id',
    'title',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedMpeg4Gif = _create_class('InlineQueryResultCachedMpeg4Gif', [
    _Field('type', default='mpeg4_gif'),
    'id',
    'mpeg4_file_id',
    'title',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedSticker = _create_class('InlineQueryResultCachedSticker', [
    _Field('type', default='sticker'),
    'id',
    'sticker_file_id',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedDocument = _create_class('InlineQueryResultCachedDocument', [
    _Field('type', default='document'),
    'id',
    'title',
    'document_file_id',
    'description',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedVideo = _create_class('InlineQueryResultCachedVideo', [
    _Field('type', default='video'),
    'id',
    'video_file_id',
    'title',
    'description',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedVoice = _create_class('InlineQueryResultCachedVoice', [
    _Field('type', default='voice'),
    'id',
    'voice_file_id',
    'title',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InlineQueryResultCachedAudio = _create_class('InlineQueryResultCachedAudio', [
    _Field('type', default='audio'),
    'id',
    'audio_file_id',
    'caption',
    'parse_mode',
    'reply_markup',
    'input_message_content',
    'caption_entities'
])

# outgoing
InputMediaPhoto = _create_class('InputMediaPhoto', [
    _Field('type', default='photo'),
    'media',
    'caption',
    'parse_mode',
    'caption_entities'
])

common_input_media = [
    'media',
    _Field('thumb', constructor=PhotoSize),
    'caption',
    'parse_mode',
    'width',
    'height',
    'duration'
]

# outgoing
InputMediaVideo = _create_class('InputMediaVideo', [
    _Field('type', default='video'),
    *common_input_media,
    'supports_streaming',
    'caption_entities'
])

# outgoing
InputMediaAnimation = _create_class('InputMediaAnimation', [
    _Field('type', default='animation'),
    *common_input_media,
    'caption_entities'
])

# outgoing
InputMediaAudio = _create_class('InputMediaAudio', [
    _Field('type', default='audio'),
    'media',
    _Field('thumb', constructor=PhotoSize),
    'caption',
    'parse_mode',
    'duration',
    'performer',
    'title',
    'caption_entities'
])

# outgoing
InputMediaDocument = _create_class('InputMediaAudio', [
    _Field('type', default='document'),
    'media',
    _Field('thumb', constructor=PhotoSize),
    'caption',
    'parse_mode',
    'disable_content_type_detection',
    'caption_entities'
])

common_passport_fields = [
    'type',
    'file_hash',
    'message']

# outgoing
PassportElementErrorDataField = _create_class('PassportElementErrorDataField', [
    _Field('source', default='data'),
    'type',
    'field_name',
    'data_hash',
    'message'
])

#outgoing
PassportElementErrorFrontSide = _create_class('PassportElementErrorFrontSide', [
    _Field('source', default='front_side'),
    *common_passport_fields
])

#outgoing
PassportElementErrorReverseSide = _create_class('PassportElementErrorReverseSide', [
    _Field('source', default='reverse_side'),
    *common_passport_fields
])

#outgoing
PassportElementErrorSelfie = _create_class('PassportElementErrorSelfie', [
    _Field('source', default='selfie'),
    *common_passport_fields
])

#outgoing
PassportElementErrorFile = _create_class('PassportElementErrorFile', [
    _Field('source', default='file'),
    *common_passport_fields
])


#outgoing
PassportElementErrorFiles = _create_class('PassportElementErrorFiles', [
    _Field('source', default='files'),
    'type',
    'file_hashes'
    'message'
])

#outgoing
PassportElementErrorTranslationFile = _create_class('PassportElementErrorTranslationFile', [
    _Field('source', default='translation_file'),
    *common_passport_fields
])


#outgoing
PassportElementErrorTranslationFiles = _create_class('PassportElementErrorTranslationFiles', [
    _Field('source', default='translation_files'),
    'type',
    'file_hashes'
    'message'
])

PassportElementErrorUnspecified = _create_class('PassportElementErrorUnspecified', [
    _Field('source', default='unspecified'),
    'type',
    'element_hash'
    'message'
])

#outgoing
PassportElementError = _create_class('PassportElementError', [
    _Field('PassportElementErrorDataField', constructor=PassportElementErrorDataField),
    _Field('PassportElementErrorFrontSide', constructor=PassportElementErrorFrontSide),
    _Field('PassportElementErrorReverseSide', constructor=PassportElementErrorReverseSide),
    _Field('PassportElementErrorSelfie', constructor=PassportElementErrorSelfie),
    _Field('PassportElementErrorFile', constructor=PassportElementErrorFile),
    _Field('PassportElementErrorFiles', constructor=PassportElementErrorFiles),
    _Field('PassportElementErrorTranslationFile', constructor=PassportElementErrorTranslationFile),
    _Field('PassportElementErrorTranslationFiles', constructor=PassportElementErrorTranslationFiles),
    _Field('PassportElementErrorUnspecified', constructor=PassportElementErrorUnspecified)

])


# incoming
ResponseParameters = _create_class('ResponseParameters', [
    'migrate_to_chat_id',
    'retry_after',
])

