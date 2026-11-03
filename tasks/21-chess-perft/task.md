Write a chess move generator in `perft.py` (standard library only, no python-chess). Provide:
- `legal_moves(fen) -> list[str]`: all legal moves in the position, in UCI notation (`e2e4`, `e7e8q` for promotions using lowercase q/r/b/n, castling as the king's move e.g. `e1g1`), sorted alphabetically.
- `perft(fen, depth) -> int`: the number of leaf nodes of the legal move tree to the given depth (depth 0 = 1).

Full rules: castling (rights from the FEN; the king may not castle out of, through or into check; rights are lost when the king or that rook moves or the rook is captured on its corner), en passant (the FEN target square), promotion to all four pieces, and no move may leave your own king in check. FENs are standard 6-field FENs. It must be correct on tricky positions such as Kiwipete (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1`), and fast enough that perft depth 3 of Kiwipete (97,862 nodes) finishes in under a minute in CPython.
