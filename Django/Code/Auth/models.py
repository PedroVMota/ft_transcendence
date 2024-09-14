from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
import random
import os

# Default profile image
DEFAULT_IMAGE = 'Auth/defaultAssets/ProfilePicture.png'

# User states for online/offline tracking
USERSTATES = (
    (1, 'Online'),
    (2, 'Offline'),
)

# Game states to represent the progress of the game
GameStates = (
    (1, 'In Progress'),
    (2, 'Not Started'),
    (3, 'Completed'),
)

# Helper function to upload profile images to a dynamic path
def upload_to(instance, filename):
    """
    Generates a unique file path for user profile images.

    Parameters:
    ----------
    instance : MyUser
        The instance of the user uploading the profile image.
    
    filename : str
        The original name of the file being uploaded.

    Returns:
    -------
    str
        A dynamic path for storing the profile image, unique to the user's username.
    """
    extension = filename.split('.')[-1]
    new_filename = f'profile_{instance.username}.{extension}'
    return os.path.join('Auth', instance.username, new_filename)

# Helper function to generate random numbers for user social codes
def RandomNumber(min=1000, max=9999):
    """
    Generates a random number between the specified range.

    Parameters:
    ----------
    min : int
        Minimum value for the random number (default 1000).
    
    max : int
        Maximum value for the random number (default 9999).

    Returns:
    -------
    int
        A randomly generated number within the specified range.
    """
    return random.randint(min, max)

class Conversation(models.Model):
    """
    Conversation Model

    Represents a single message within a chat. Each conversation has an author, 
    a message, and a timestamp for when the message was created.

    Attributes:
    ----------
    id : AutoField
        Unique identifier for the conversation.

    AuthorOfTheMessage : ForeignKey
        A foreign key to the user who sent the message.

    Message : TextField
        The content of the message.

    create_date : DateTimeField
        The timestamp for when the message was created, automatically set.

    Methods:
    -------
    __str__():
        Returns a string representation of the conversation.
    """
    id = models.AutoField(primary_key=True)
    AuthorOfTheMessage = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='AuthorOfTheMessage'
    )
    Message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class currentChat(models.Model):
    """
    currentChat Model

    Represents a chat session that can include multiple users. Each chat has a unique ID,
    can be a group or individual chat, and contains multiple conversations.

    Attributes:
    ----------
    id : AutoField
        Unique identifier for the chat.

    members : ManyToManyField
        A many-to-many relationship with users, representing the participants of the chat.

    is_group : BooleanField
        Indicates whether the chat is a group chat (default is False).

    currentMessage : ManyToManyField
        A relationship with Conversation, representing all messages within the chat.

    unique_id : UUIDField
        A unique UUID for each chat session.

    Methods:
    -------
    __str__():
        Returns a string representation of the chat.
    """
    id = models.AutoField(primary_key=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_group = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    currentMessage = models.ManyToManyField(Conversation, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Conversation {self.id}"

class MyUser(AbstractUser):
    """
    MyUser Model

    Custom user model that extends Django's AbstractUser to include additional fields like profile picture,
    social code, friend list, and chat history.

    Attributes:
    ----------
    profile_picture : ImageField
        The user's profile picture, with a default image path.

    about_me : TextField
        A brief biography about the user, optional.

    friendlist : ManyToManyField
        A many-to-many relationship representing the user's list of friends.

    userSocialCode : BigIntegerField
        A unique code for identifying users in social interactions.

    allChat : ManyToManyField
        A relationship with the currentChat model, representing all chat rooms the user is involved in.

    state : IntegerField
        Indicates whether the user is online or offline (default is offline).

    walletCoins : IntegerField
        A virtual currency counter for the user (default is 0).

    Methods:
    -------
    getJson():
        Returns a JSON-friendly representation of the user.
        
    save(*args, **kwargs):
        Overridden save method to ensure the userSocialCode is generated if not present.
        
    newImageUpdate(image):
        Updates the user's profile picture with the provided image.

    __str__():
        Returns the username of the user.
    """
    profile_picture = models.ImageField(upload_to=upload_to, default=DEFAULT_IMAGE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    friendlist = models.ManyToManyField('self', blank=True)
    userSocialCode = models.BigIntegerField(unique=True, null=True, blank=True)
    allChat = models.ManyToManyField(currentChat, blank=True)
    state = models.IntegerField(choices=USERSTATES, default=2)
    walletCoins = models.IntegerField(default=0)
    
    def getJson(self):
        """
        Returns a JSON-friendly representation of the user, including details like
        username, email, profile picture URL, and friend list.

        Returns:
        -------
        dict
            A dictionary representing the user's information.
        """
        return {
            'user_id': self.id,
            'username': self.username,
            'usercode': self.userSocialCode,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_picture': self.profile_picture.url,
            'about_me': self.about_me,
            'create_date': self.create_date,
            'update_date': self.update_date,
            'friendlist': [friend.username for friend in self.friendlist.all()]
        }
    
    def save(self, *args, **kwargs):
        """
        Overridden save method to generate a user social code if it's not already assigned.
        """
        if self.userSocialCode is None:
            self.userSocialCode = RandomNumber(min=1000, max=9999)
        super().save(*args, **kwargs)

    def newImageUpdate(self, image):
        """
        Updates the profile picture of the user and saves the change.

        Parameters:
        ----------
        image : ImageFile
            The new image to be set as the user's profile picture.
        """
        self.profile_picture = image
        self.save()

    def __str__(self):
        return self.username

class serverLogs(models.Model):
    """
    serverLogs Model

    Tracks server requests, including the user who made the request, the HTTP method, and the request status.

    Attributes:
    ----------
    user : ForeignKey
        The user who made the request (optional).

    mehod : CharField
        The HTTP method used (GET, POST, etc.).

    path : CharField
        The path of the request.

    status : BigIntegerField
        The HTTP status code of the response.

    create_date : DateTimeField
        Timestamp for when the log was created.

    update_date : DateTimeField
        Timestamp for when the log was last updated.

    Methods:
    -------
    __str__():
        Returns the username associated with the log.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mehod = models.CharField(max_length=10, default='GET')
    path = models.CharField(max_length=100, default='/')
    status = models.BigIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username if self.user else 'Anonymous'

class FriendRequest(models.Model):
    """
    FriendRequest Model

    Represents a friend request between two users. Tracks the status of the request (pending, accepted, rejected).

    Attributes:
    ----------
    from_user : ForeignKey
        The user who sent the friend request.

    to_user : ForeignKey
        The user who received the friend request.

    status : CharField
        Indicates the status of the friend request (pending, accepted, rejected).

    created_at : DateTimeField
        Timestamp for when the friend request was created.

    updated_at : DateTimeField
        Timestamp for when the friend request was last updated.

    Methods:
    -------
    __str__():
        Returns a string representation of the friend request.
    """
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    def __str__(self):
        return f"{self.from_user.username} sent a friend request to {self.to_user.username}"



class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class GameRoom(models.Model):
    """
    GameRoom Model
    
    This model represents a room where a game takes place between two players, with an option for spectators.
    It tracks the game's name, state (e.g., in progress, not started, completed), and associated chat for the game.

    Attributes:
    ----------
    id : AutoField
        Auto-incremented unique identifier for the game room.
    
    GameName : CharField
        The name of the game, which can be set to identify different types of games or sessions.

    GameStates : IntegerField
        Represents the current state of the game with predefined choices:
        - 1: In Progress
        - 2: Not Started (default)
        - 3: Completed

    PlayerOne : ForeignKey
        A foreign key to the first player (user model) who participates in the game. Can be `None` initially, which means the game is open for player joining.

    PlayerTwo : ForeignKey
        A foreign key to the second player (user model) in the game. Can also be `None` if only one player has joined.

    GameChat : ForeignKey
        Represents a chat room specifically for this game session. This is an instance of the `currentChat` model, allowing players to communicate during the game. 
        If no chat exists at the time of room creation, a chat is created automatically upon saving.

    Spectators : ManyToManyField
        A many-to-many relationship allowing additional users to join as spectators. Spectators can watch the game without actively participating as players.

    Methods:
    -------
    add_user_to_spectators(user):
        Adds a user to the spectators of the game room.
        
    remove_user_from_spectators(user):
        Removes a user from the spectators of the game room.
        
    join_player(user):
        Adds a user to the game as a player if there's an available slot. If both player slots are filled, the user will be added as a spectator.
        
    leave_player(user):
        Removes the user from the game if they are one of the players or removes them from the spectators if they are a spectator.
        
    validate_players():
        Ensures that `PlayerOne` and `PlayerTwo` are not the same user. If they are, raises a `ValueError`.
        
    save(*args, **kwargs):
        Custom save method that validates players and, if no `GameChat` exists, creates one and adds both players (if present) to the chat.
    """

    GAME_STATES = [
        (1, 'In Progress'),
        (2, 'Not Started'),
        (3, 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    GameName = models.CharField(max_length=255)  # Name of the game
    GameStates = models.IntegerField(choices=GAME_STATES, default=2)  # Game state

    PlayerOne = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='player_one_games',
        blank=True, null=True  # Allow PlayerOne to be null initially
    )
    PlayerTwo = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='player_two_games',
        blank=True, null=True  # Allow PlayerTwo to be null initially
    )

    GameChat = models.ForeignKey(
        currentChat, 
        on_delete=models.CASCADE, 
        blank=True, null=True  # Allow the chat to be created dynamically
    )

    Spectators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='spectated_games', 
        blank=True  # Spectators are optional
    )

    def add_user_to_spectators(self, user):
        """
        Adds the given user to the Spectators list of the game room.
        Calls `save` to persist the change.
        """
        self.Spectators.add(user)
        self.save()

    def remove_user_from_spectators(self, user):
        """
        Removes the given user from the Spectators list of the game room.
        Calls `save` to persist the change.
        """
        self.Spectators.remove(user)
        self.save()

    def join_player(self, user):
        """
        Attempts to add the user to the game as a player.
        - If `PlayerOne` is not set, assigns `PlayerOne` to the user.
        - If `PlayerTwo` is not set and `PlayerOne` is a different user, assigns `PlayerTwo` to the user.
        - If both player slots are filled, the user is added as a spectator.
        Calls `save` to persist the change.
        """
        if not self.PlayerOne:
            self.PlayerOne = user
        elif not self.PlayerTwo and self.PlayerOne != user:
            self.PlayerTwo = user
        else:
            self.add_user_to_spectators(user)
        self.save()

    def leave_player(self, user):
        """
        Removes the user from the game as a player or spectator.
        - If the user is `PlayerOne`, they are removed from the game.
        - If the user is `PlayerTwo`, they are removed from the game.
        - Otherwise, the user is removed from the spectators list.
        Calls `save` to persist the change.
        """
        if self.PlayerOne == user:
            self.PlayerOne = None
        elif self.PlayerTwo == user:
            self.PlayerTwo = None
        else:
            self.remove_user_from_spectators(user)
        self.save()

    def validate_players(self):
        """
        Validates that `PlayerOne` and `PlayerTwo` are not the same user.
        If they are, raises a `ValueError`.
        """
        if self.PlayerOne and self.PlayerOne == self.PlayerTwo:
            raise ValueError("PlayerOne and PlayerTwo cannot be the same user")

    def save(self, *args, **kwargs):
        """
        Custom save method.
        - Validates that `PlayerOne` and `PlayerTwo` are different users.
        - If no `GameChat` exists, creates a new chat and assigns `PlayerOne` and `PlayerTwo` to it (if they exist).
        - Calls the parent class's `save` method to persist changes to the database.
        """
        self.validate_players()  # Ensure the players are valid
        if not self.GameChat:
            chat = currentChat.objects.create()
            if self.PlayerOne:
                chat.members.add(self.PlayerOne)
            if self.PlayerTwo:
                chat.members.add(self.PlayerTwo)
            self.GameChat = chat
        super().save(*args, **kwargs)