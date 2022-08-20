# from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Literal
import gym
import numpy as np


minWidth = 4
moves = ["L", "R", "D", "U"]


@dataclass
class Piece:
    x: int
    y: int
    o: int
    id: str


@dataclass
class Orientation:
    yMin: int
    yDim: int
    xMin: int
    xDim: int
    rows: list[int]


@dataclass
class Rotations:
    pieceID: list[Orientation]


@dataclass
class RotationSystem:
    placeNewPiece: tuple[int, str]
    rotations: Rotations


@dataclass
class CoreState:
    score: int
    well: list[int]


@dataclass
class WellState:
    core: CoreState
    ai: Any
    piece: Piece


# @abstractmethod
# def GetNextCoreState(core: CoreState, pieceId: str) -> list[CoreState]:
#     pass


# @abstractmethod
# def EnemyAi(currentCoreState: CoreState,
#             currentAiState: Any,
#             getNextCoreStates: GetNextCoreStates) -> (str | [str, Any]):
#     pass

@dataclass
class Enemy:
    shortDescription: str
    buttonDescription: str
    # ai: EnemyAi
    ai: Any | Literal["def EnemyAi"]


@dataclass
class GameProps:
    bar: int
    replayTimeout: int | float
    rotationSystem: RotationSystem
    wellDepth: int
    wellWidth: int


@dataclass
class GameStateError:
    interpretation: str
    real: str


@dataclass
class GameState:
    error: GameStateError
    displayEnemy: bool
    enemy: Enemy
    customAiCode: str
    mode: str
    wellStateId: int
    wellStates: list[WellState]
    replay: list[Any]
    replayCopiedTimeoutId: Any | Literal["NodeJS Timeout"]
    replayTimeoutId: Any | Literal["NodeJS Timeout"]


lovetris: Enemy = Enemy(
    shortDescription="❤",
    buttonDescription="all 4x1",
    ai="lovetrisAi"
)

enemies = [lovetris]
pieceIds = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']


class Game(gym.Env):
    def __init__(self, props: GameProps) -> None:
        super().__init__()
        self.props = props
        bar = self.props.bar
        rotationSystem = self.props.rotationSystem
        wellDepth = self.props.wellDepth
        wellWidth = self.props.wellWidth
        if (wellDepth < bar):
            raise ValueError("Can't have well with depth " +
                             (wellDepth) + ' less than bar at ' + (bar))

        if (wellWidth < minWidth):
            raise ValueError("Can't have well with width " +
                             (wellWidth) + ' less than ' + (minWidth))

        self.state = GameState(
            error=None,
            displayEnemy=False,  # don't show it unless the user selects one manually
            enemy=lovetris,
            customAiCode="",
            mode="INITIAL",
            wellStateId=-1,
            wellStates=[],
            replay=[],
            replayCopiedTimeoutId=None,
            replayTimeoutId=None
        )

        self.ACTION_MAP = np.array(["L", "R", "D", "U"])
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = gym.spaces.Discrete(ACTION_NUM)
        LOW = np.array([np.float32(0)])
        HIGH = np.array([np.float32(ACTION_NUM - 1)])
        self.observation_space = gym.spaces.Box(low=LOW, high=HIGH)

    # def validateAiResult(coreState: CoreState, aiState: Any):
    #     enemy = self.state

    #     aiResult: Any = enemy.ai(coreState, aiState, self.getNextCoreStates)

    #     [unsafePieceId, nextAiState] = aiResult if (
    #         type(aiResult) is list) else [aiResult, aiState]

    #     if (pieceIds.includes(unsafePieceId)):
    #         return [unsafePieceId, nextAiState]

    #     raise ValueError(f"Bad piece ID: {unsafePieceId}")

    def step(self, action_index: int) -> tuple[float, float, bool, dict]:
        pass
