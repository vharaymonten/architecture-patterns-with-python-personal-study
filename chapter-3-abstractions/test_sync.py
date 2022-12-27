from pathlib import Path
from sync import get_actions_for_sync
def test_file_should_be_remove():
    #Abstract the state if filesystem
    src_hash = {
        # "hash1" : 'fname1'
    }

    dst_hash = {
        'hash2' : "fname2"
    }

    actions = get_actions_for_sync(src_hash, dst_hash, Path("/src"), Path("/dest"))
    assert list(actions) == [("REMOVE", "", Path("/dest") / "fname2")]


    
def test_file_should_be_move():
    #Abstract the state if filesystem
    src_hash = {
        "hash1" : 'fname'
    }

    dst_hash = {
        'hash1' : "fname2"
    }

    actions = get_actions_for_sync(src_hash, dst_hash, Path("/src"), Path("/dest"))
    assert list(actions) == [("MOVE", Path('/dest') / 'fname2', Path("/dest") / "fname")]

def test_file_should_be_copy():
    #Abstract the state if filesystem
    src_hash = {
        "hash1" : 'fname'
    }

    dst_hash = {
        # 'hash2' : "fname2",
        # 'hash3' : "fname3",
    }

    actions = get_actions_for_sync(src_hash, dst_hash, Path("/src"), Path("/dest"))
    assert list(actions) == [("COPY", Path('/src') / 'fname', Path("/dest") / "fname")]