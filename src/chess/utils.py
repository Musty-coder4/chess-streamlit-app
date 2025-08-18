from typing import Optional, Tuple

def parse_position(pos_str: str) -> Optional[Tuple[int, int]]:
    """Parse chess algebraic notation to board indices."""
    files = "abcdefgh"
    if len(pos_str) != 2:
        return None
    file, rank = pos_str[0], pos_str[1]
    if file in files and rank.isdigit():
        x = 8 - int(rank)
        y = files.index(file)
        if 0 <= x < 8 and 0 <= y < 8:
            return (x, y)
    return None
