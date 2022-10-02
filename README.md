# Chess Practice Bot
A python implementation for a playable chess GUI - the code uses the pygame and python-chess libraries.

The chess positions are represented by FEN: a notation describing piece layout, castling and turn status, etc. If a piece is dragged to a legal square, the FEN updates with the visual chess board display. All of the information required to generate legal moves and enforce the proper functions of a chess match are produced from the FEN information.

When the script is activated, a starting menu prompts the user to choose the settings for the chess match. These options include the ability to play against an AI (with adjustable rating approximations) and a specific color. The AI uses the negamax algorithim with alpha-beta pruning to generate a best move for the rating ranges of 1500 to 1700. If the user chooses an AI rating above 1700, the moves will be generated by the Stockfish chess engine, using varying depths of search to model different ratings. For all AI ratings, the first moves are played from an opening database until a unique position is reached. The bot offers great practice for different opening theory and enables players to play a full game after their opening play.


![chess menu](https://thumbs.gfycat.com/RecklessDarlingIcelandgull-max-1mb.gif)

## Downloading the Chess Bot:

1.
2.
3.
