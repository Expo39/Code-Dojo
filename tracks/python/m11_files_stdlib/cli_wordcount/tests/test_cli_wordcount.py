import importlib.util
import runpy
import sys

import pytest
import cli_wordcount
from cli_wordcount import main


def write(tmp_path, text):
    f = tmp_path / "notes.txt"
    f.write_text(text, encoding="utf-8")
    return str(f)


def test_report_with_top(tmp_path):
    path = write(tmp_path, "the cat saw the dog the end")
    assert main([path, "--top", "2"]) == "words: 7\nunique: 5\nthe 3\ncat 1"


def test_default_top_and_case(tmp_path):
    path = write(tmp_path, "Up up down Up left up, UP!")
    assert main([path]) == "words: 7\nunique: 5\nUp 2\nup 2\nUP 1"
    assert main([path, "--ignore-case"]) == "words: 7\nunique: 3\nup 5\ndown 1\nleft 1"


def test_top_larger_than_vocabulary_and_empty(tmp_path):
    path = write(tmp_path, "b a b")
    assert main([path, "--top", "10"]) == "words: 3\nunique: 2\nb 2\na 1"
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    assert main([str(empty)]) == "words: 0\nunique: 0"


def test_bad_arguments_exit(tmp_path, capsys):
    path = write(tmp_path, "a b c")
    for bad in (["--top", "abc"], ["--top", "0"], ["--top", "-2"]):
        with pytest.raises(SystemExit):
            main([path, *bad])
    with pytest.raises(SystemExit):
        main([])
    with pytest.raises(FileNotFoundError):
        main([str(tmp_path / "missing.txt")])


def test_import_runs_nothing_and_script_prints(tmp_path, capsys, monkeypatch):
    source = cli_wordcount.__spec__.origin
    spec = importlib.util.spec_from_file_location("cli_wordcount_reimport", source)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setattr(sys, "argv", ["prog"])
    spec.loader.exec_module(module)  # must not parse argv or print
    assert capsys.readouterr().out == ""

    path = write(tmp_path, "x y x")
    monkeypatch.setattr(sys, "argv", ["prog", path, "--top", "1"])
    runpy.run_path(source, run_name="__main__")
    assert capsys.readouterr().out.strip() == "words: 3\nunique: 2\nx 2"
