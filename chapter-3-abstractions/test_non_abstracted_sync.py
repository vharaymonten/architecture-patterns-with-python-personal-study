import tempfile
from pathlib import Path
from non_abstracted_sync import sync
import shutil
def test_when_file_exist_exists_in_source_but_not_in_destination():
    try:
        source = tempfile.mkdtemp(suffix="testsourcedir")
        dest =tempfile.mkdtemp(suffix="testdestdir")

        content = "Sexy voice is not sexy"

        path = Path(source) / "myfile.txt"
        path.write_text(content)

        print(source)
        sync(source, dest)

        expected_path = Path(dest) / "myfile.txt"
        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

def test_when_a_file_has_been_renamed_in_the_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a file that was renamed"
        source_path = Path(source) / 'test'
        dest_path = Path(dest) / 'dest'

        expected_dest_path = Path(dest) / 'test'
        source_path.write_text(content)
        dest_path.write_text(content)
        
        sync(source, dest)

        assert expected_dest_path.exists()
        assert expected_dest_path.read_text() == content

    
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)