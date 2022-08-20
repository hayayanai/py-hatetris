from dataclasses import dataclass
from Game.Game import Orientation, WellState
from Game.Game import RotationSystem


@dataclass
class WellProps:
    bar: int
    rotationSystem: RotationSystem
    wellDepth: int
    wellWidth: int
    wellState: WellState


@dataclass
class Cell:
    landed: bool
    live: bool


def Well(props: WellProps):

    # bar = props.bar
    rotationSystem = props.rotationSystem
    wellDepth = props.wellDepth
    wellWidth = props.wellWidth
    wellState = props.wellState

    well = wellState and wellState.core.well
    piece = wellState and wellState.piece

    cellses: list[list[Cell]] = []

    for y in range(0, wellDepth):
        cells = []
        for x in range(0, wellWidth):
            landed = (well is not None) and (well[y] & (1 << x)) != 0

            live: bool
            if (piece is None):
                live = False
            else:
                orientation: Orientation = rotationSystem.rotations[piece.id][piece.o]
                y2 = y - piece.y - orientation.yMin
                x2 = x - piece.x - orientation.xMin
                live = (y2 >= 0 and y2 < orientation.yDim and x2 >= 0 and x2 <
                        orientation.xDim and (orientation.rows[y2] & (1 << x2)) != 0)

            cells.append({landed, live})
        cellses.append(cells)

# return (
#     <table >
#       <tbody >
#         {cellses.map((cells, y)= > (
#           < tr key={y} >
#             {cells.map((cell, x)= > (
#               < td
#                 key={x}
#                 className={classnames({
#                   well__cell: true,
#                   'well__cell--bar': y === bar,
#                   'well__cell--landed': cell.landed,
#                   'well__cell--live': cell.live
#                 })} / >
#             ))}
#           < /tr >
#         ))}
#       </tbody >
#     </table >
#   )
