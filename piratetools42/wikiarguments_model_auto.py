#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine(builtins.SQLALCHEMY_DATABASE_URI, echo=False)  # @UndefinedVariable
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

badwords = Table(u'badwords', metadata,
    Column(u'badwordId', INTEGER(), nullable=False),
    Column(u'category', Integer(), nullable=False),
    Column(u'word', VARCHAR(length=50), nullable=False),
)

user_groups = Table(u'user_groups', metadata,
    Column(u'userId', INTEGER(), nullable=False),
    Column(u'groupId', INTEGER(), nullable=False),
    Column(u'dateAdded', BigInteger(), nullable=False),
)

class Argument(DeclarativeBase):
    __tablename__ = 'arguments'

    __table_args__ = {}

    #column definitions
    abstract = Column(u'abstract', VARCHAR(length=200), nullable=False)
    argumentId = Column(u'argumentId', INTEGER(), primary_key=True, nullable=False)
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    details = Column(u'details', TEXT(), nullable=False)
    headline = Column(u'headline', VARCHAR(length=100), nullable=False)
    parentId = Column(u'parentId', INTEGER(), nullable=False)
    questionId = Column(u'questionId', INTEGER(), nullable=False)
    score = Column(u'score', INTEGER(), nullable=False)
    type = Column(u'type', Integer(), nullable=False)
    url = Column(u'url', VARCHAR(length=200), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class ConfirmationCode(DeclarativeBase):
    __tablename__ = 'confirmation_codes'

    __table_args__ = {}

    #column definitions
    code = Column(u'code', VARCHAR(length=128), nullable=False)
    confirmationId = Column(u'confirmationId', INTEGER(), primary_key=True, nullable=False)
    dateAdded = Column(u'dateAdded', INTEGER(), nullable=False)
    type = Column(u'type', VARCHAR(length=64), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class Group(DeclarativeBase):
    __tablename__ = 'groups'

    __table_args__ = {}

    #column definitions
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    groupId = Column(u'groupId', INTEGER(), primary_key=True, nullable=False)
    ownerId = Column(u'ownerId', INTEGER(), nullable=False)
    title = Column(u'title', VARCHAR(length=250), nullable=False)
    url = Column(u'url', VARCHAR(length=250), nullable=False)
    visibility = Column(u'visibility', Integer(), nullable=False)

    #relation definitions


class GroupPermission(DeclarativeBase):
    __tablename__ = 'group_permissions'

    __table_args__ = {}

    #column definitions
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    groupId = Column(u'groupId', INTEGER(), nullable=False)
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    permission = Column(u'permission', INTEGER(), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class Localization(DeclarativeBase):
    __tablename__ = 'localization'

    __table_args__ = {}

    #column definitions
    loc_key = Column(u'loc_key', VARCHAR(length=255), primary_key=True, nullable=False)
    loc_language = Column(u'loc_language', VARCHAR(length=4), primary_key=True, nullable=False)
    loc_val = Column(u'loc_val', TEXT(), nullable=False)

    #relation definitions


class Notification(DeclarativeBase):
    __tablename__ = 'notifications'

    __table_args__ = {}

    #column definitions
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    flags = Column(u'flags', INTEGER(), nullable=False)
    notificationId = Column(u'notificationId', INTEGER(), primary_key=True, nullable=False)
    questionId = Column(u'questionId', INTEGER(), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class Page(DeclarativeBase):
    __tablename__ = 'pages'

    __table_args__ = {}

    #column definitions
    className = Column(u'className', VARCHAR(length=100), nullable=False)
    pageId = Column(u'pageId', INTEGER(), primary_key=True, nullable=False)
    pageTitle = Column(u'pageTitle', VARCHAR(length=100), nullable=False)
    templateFile = Column(u'templateFile', VARCHAR(length=100), nullable=False)
    url = Column(u'url', VARCHAR(length=100), nullable=False)

    #relation definitions


class Permission(DeclarativeBase):
    __tablename__ = 'permissions'

    __table_args__ = {}

    #column definitions
    action = Column(u'action', VARCHAR(length=50), nullable=False)
    groupId = Column(u'groupId', INTEGER(), nullable=False)
    permissionId = Column(u'permissionId', INTEGER(), primary_key=True, nullable=False)
    state = Column(u'state', Integer(), nullable=False)

    #relation definitions


class Question(DeclarativeBase):
    __tablename__ = 'questions'

    __table_args__ = {}

    #column definitions
    additionalData = Column(u'additionalData', TEXT(), nullable=False)
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    details = Column(u'details', String(), nullable=False)
    flags = Column(u'flags', Integer(), nullable=False)
    groupId = Column(u'groupId', INTEGER(), nullable=False)
    questionId = Column(u'questionId', INTEGER(), primary_key=True, nullable=False)
    score = Column(u'score', INTEGER(), nullable=False)
    scoreTop = Column(u'scoreTop', INTEGER(), nullable=False)
    scoreTrending = Column(u'scoreTrending', INTEGER(), nullable=False)
    title = Column(u'title', VARCHAR(length=100), nullable=False)
    type = Column(u'type', Integer(), nullable=False)
    url = Column(u'url', VARCHAR(length=200), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class Session(DeclarativeBase):
    __tablename__ = 'sessions'

    __table_args__ = {}

    #column definitions
    sessionData = Column(u'sessionData', TEXT(), nullable=False)
    sessionDate = Column(u'sessionDate', INTEGER(), nullable=False)
    sessionId = Column(u'sessionId', VARCHAR(length=32), primary_key=True, nullable=False)

    #relation definitions


class SignupToken(DeclarativeBase):
    __tablename__ = 'signup_tokens'

    __table_args__ = {}

    #column definitions
    token = Column(u'token', VARCHAR(length=64), nullable=False)
    tokenId = Column(u'tokenId', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


class Sponsor(DeclarativeBase):
    __tablename__ = 'sponsors'

    __table_args__ = {}

    #column definitions
    amount = Column(u'amount', INTEGER(), nullable=False)
    logoHeight = Column(u'logoHeight', INTEGER(), nullable=False)
    logoWidth = Column(u'logoWidth', INTEGER(), nullable=False)
    sId = Column(u'sId', INTEGER(), primary_key=True, nullable=False)
    sort = Column(u'sort', INTEGER(), nullable=False)
    sponsorId = Column(u'sponsorId', INTEGER(), nullable=False)
    title = Column(u'title', VARCHAR(length=255), nullable=False)
    url = Column(u'url', VARCHAR(length=255), nullable=False)

    #relation definitions


class SponsorsData(DeclarativeBase):
    __tablename__ = 'sponsors_data'

    __table_args__ = {}

    #column definitions
    additionalInformation = Column(u'additionalInformation', VARCHAR(length=255), nullable=False)
    amount = Column(u'amount', INTEGER(), nullable=False)
    approved = Column(u'approved', INTEGER(), nullable=False)
    city = Column(u'city', VARCHAR(length=255), nullable=False)
    companyName = Column(u'companyName', VARCHAR(length=255), nullable=False)
    currentLogoApproved = Column(u'currentLogoApproved', INTEGER(), nullable=False)
    dateAdded = Column(u'dateAdded', INTEGER(), nullable=False)
    email = Column(u'email', VARCHAR(length=255), nullable=False)
    logoHeight = Column(u'logoHeight', INTEGER(), nullable=False)
    logoWidth = Column(u'logoWidth', INTEGER(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    password = Column(u'password', VARCHAR(length=255), nullable=False)
    paymentData = Column(u'paymentData', TEXT(), nullable=False)
    paymentMethod = Column(u'paymentMethod', INTEGER(), nullable=False)
    phone = Column(u'phone', VARCHAR(length=255), nullable=False)
    slogan = Column(u'slogan', VARCHAR(length=255), nullable=False)
    sponsorId = Column(u'sponsorId', INTEGER(), primary_key=True, nullable=False)
    street = Column(u'street', VARCHAR(length=255), nullable=False)
    url = Column(u'url', VARCHAR(length=255), nullable=False)
    zip = Column(u'zip', VARCHAR(length=255), nullable=False)

    #relation definitions


class SponsorsPayment(DeclarativeBase):
    __tablename__ = 'sponsors_payments'

    __table_args__ = {}

    #column definitions
    amount = Column(u'amount', INTEGER(), nullable=False)
    dateApproved = Column(u'dateApproved', INTEGER(), nullable=False)
    dateEnd = Column(u'dateEnd', INTEGER(), nullable=False)
    dateStart = Column(u'dateStart', INTEGER(), nullable=False)
    paymentId = Column(u'paymentId', INTEGER(), primary_key=True, nullable=False)
    sponsorId = Column(u'sponsorId', INTEGER(), nullable=False)

    #relation definitions


class Tag(DeclarativeBase):
    __tablename__ = 'tags'

    __table_args__ = {}

    #column definitions
    groupId = Column(u'groupId', INTEGER(), nullable=False)
    questionId = Column(u'questionId', INTEGER(), nullable=False)
    tag = Column(u'tag', VARCHAR(length=50), nullable=False)
    tagId = Column(u'tagId', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


class User(DeclarativeBase):
    __tablename__ = 'users'

    __table_args__ = {}

    #column definitions
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    email = Column(u'email', VARCHAR(length=200), nullable=False)
    group = Column(u'group', INTEGER(), nullable=False)
    password = Column(u'password', VARCHAR(length=256), nullable=False)
    salt = Column(u'salt', VARCHAR(length=128), nullable=False)
    scoreArguments = Column(u'scoreArguments', INTEGER(), nullable=False)
    scoreQuestions = Column(u'scoreQuestions', INTEGER(), nullable=False)
    userId = Column(u'userId', INTEGER(), primary_key=True, nullable=False)
    userName = Column(u'userName', VARCHAR(length=200), nullable=False)
    user_last_action = Column(u'user_last_action', BigInteger(), nullable=False)

    #relation definitions


class UserFaction(DeclarativeBase):
    __tablename__ = 'user_factions'

    __table_args__ = {}

    #column definitions
    factionId = Column(u'factionId', INTEGER(), primary_key=True, nullable=False)
    questionId = Column(u'questionId', INTEGER(), nullable=False)
    state = Column(u'state', Integer(), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)

    #relation definitions


class UserVote(DeclarativeBase):
    __tablename__ = 'user_votes'

    __table_args__ = {}

    #column definitions
    argumentId = Column(u'argumentId', INTEGER(), nullable=False)
    dateAdded = Column(u'dateAdded', BigInteger(), nullable=False)
    questionId = Column(u'questionId', INTEGER(), nullable=False)
    userId = Column(u'userId', INTEGER(), nullable=False)
    vote = Column(u'vote', INTEGER(), nullable=False)
    voteId = Column(u'voteId', INTEGER(), primary_key=True, nullable=False)

    #relation definitions


