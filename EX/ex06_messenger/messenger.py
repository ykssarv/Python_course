"""Messenger."""


class User:
    """User class."""

    def __init__(self, name):
        """
        User constructor.

        :param name: Name of the user.
        """
        self.name = name


class Chat:
    """Chat class."""

    def __init__(self, name, users):
        """
        Chat constructor.

        :param name: Name of the chat.
        :param users: Users in the chat.
        """
        self.name = name
        self.users = users
        self.messages = []


class Message:
    """Message class."""

    def __init__(self, user, content):
        """
        Message constructor.

        :param user: Author of the message.
        :param content: Content of the message.
        """
        self.user = user
        self.content = content
        self.reactions = 0


def write_message(user: User, chat: Chat, content: str) -> None:
    """
    Write a message to given chat.

    Create a message with given values and then add it to the chat's messages.

    :param user: Author of the message.
    :param chat: Chat to write the message to.
    :param content: Content of the message.
    """
    if user in chat.users:
        message = Message(user, content)
        chat.messages.append(message)


def delete_message(chat: Chat, message: Message) -> None:
    """
    Delete message from chat.

    :param chat: Chat to delete the message from.
    :param message: Message to delete from chat.
    """
    if message in chat.messages:
        chat.messages.remove(message)


def get_messages_by_user(user: User, chat: Chat) -> list:
    """
    Get messages by user in chat.

    :param user: User whose messages to get.
    :param chat: Chat from where to get user's messages.
    :return: A list of messages.
    """
    return list(filter(lambda x: user == x.user, chat.messages))


def react_to_last_message(chat: Chat) -> None:
    """
    Add reaction to last message in chat.

    :param chat: Chat in which the message is.
    """
    if len(chat.messages) != 0:
        chat.messages[-1].reactions += 1


def find_most_reacted_message(chat: Chat) -> Message:
    """
    Find the most reacted message in chat.

    :param chat: Chat to get the message from.
    :return: Most reacted message.
    """
    return max(reversed(chat.messages), key=lambda x: x.reactions)


def count_reactions_in_chat(chat: Chat) -> int:
    """
    Count all reactions in chat.

    :param chat: Said chat.
    :return: The amount of reactions.
    """
    return sum(map(lambda x: x.reactions, chat.messages))


def count_reactions_by_chat(chats: list) -> dict:
    """
    Count reactions in every chat.

    The function should return a dict where the key is the name of a chat and the value is the amount of reactions.

    :param chats: The chats in question.
    :return: A dictionary as described.
    """
    chat_reactions = {}
    for chat in chats:
        reactions = count_reactions_in_chat(chat)
        chat_reactions[chat.name] = reactions
    return chat_reactions


if __name__ == '__main__':
    user1 = User("Alma")
    user2 = User("Ago")
    chat = Chat("Python 2020", [user1, user2])

    write_message(user1, chat, "Parim kohvipiim")
    write_message(user2, chat, "Eestimaa farmidest")
    write_message(user2, chat, "Piim")
    write_message(user1, chat, "Farmi")
    for message in chat.messages:
        print(f"{message.user.name}: {message.content}")
        # Alma: Parim kohvipiim
        # Ago: Eestimaa farmidest
        # Ago: Piim
        # Alma: Farmi

    to_be_deleted = get_messages_by_user(user2, chat)
    for message in to_be_deleted:
        delete_message(chat, message)
    for message in chat.messages:
        print(f"{message.user.name}: {message.content}")
        # Alma: Parim kohvipiim
        # Alma: Farmi

    react_to_last_message(chat)
    print(chat.messages[0].reactions)  # 0
    print(chat.messages[-1].reactions)  # 1

    most_reacted = find_most_reacted_message(chat)
    print(f"{most_reacted.content}: {most_reacted.reactions}")  # Farmi: 1

    print(count_reactions_in_chat(chat))  # 1
    print(count_reactions_by_chat([chat]))  # {"Python 2020": 1}
