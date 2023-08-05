import re
import typing


class Mention:
    user: bool
    club: bool
    id: int
    text: str

    regex = re.compile(r"\[(id|club)(\d{1,16})\|(.+?)\]")

    def __init__(
        self,
        id: int,
        text: str = "mention",
        user: bool = False,
        club: bool = False,
    ):
        self.id = id
        self.text = text
        self.user = user
        self.club = club

        if not self.user and not self.club:
            if self.id > 0:
                self.user = True
            elif self.id < 0:
                self.club = True

    @classmethod
    def find(cls, text: str) -> typing.Optional["Mention"]:
        match = cls.regex.search(text)
        if match is not None:
            return cls(
                id=int(match[2]),
                user=match[1] == "id",
                club=match[1] == "club",
                text=match[3]
            )
        return None

    @classmethod
    def finditer(cls, text: str) -> typing.Iterator["Mention"]:
        iterator = cls.regex.finditer(text)
        for i in iterator:
            yield cls(
                id=int(i[2]),
                user=i[1] == "id",
                club=i[1] == "club",
                text=i[3]
            )

    def __str__(self) -> str:
        return f"[{'id' if self.user else 'club'}{self.id}|{self.text}]"
