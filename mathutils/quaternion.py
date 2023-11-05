from .matrix import Matrix
from .vector import Vector


class Quaternion(tuple):

    @staticmethod
    def to_matrix():
        return Matrix((Vector(), Vector(), Vector()))
