# Vim global plugin for diff two directories and represent them as a tree
# Maintainer: taze55 <taze_a28391214@icloud.com>
# URL: https://github.com/taze55/vim-dirdifftree

# It assumes that build_test_data.sh is working properly, so Windows is not taken into account.
# Please use WSL2 or something.
import os
import pytest
from python3.dirdifftree_lib import *

defaultThreadStrs: Dict[ThreadKey, str] = {"blank": "    ", "vertical": "│  ", "branch": "├─", "corner": "└─"}
defaultIconStrs: Dict[IconKey, str] = {"dir": "🇩 ", "file": "🇫 "}
defaultRenderOption = RenderOption(fileLexicalOrder, True, False, defaultThreadStrs, defaultIconStrs)

defaultExcludeDirs: List[str] = [".git", "node_modules", "__pycache__"]
defaultIgnoreCase = True
defaultNewerSide = "right"
defaultBuildTreeOption = BuildTreeOption(defaultExcludeDirs, defaultIgnoreCase, defaultNewerSide)

# https://stackoverflow.com/questions/4934806/how-can-i-find-scripts-directory
baseDir = f"{os.path.dirname(os.path.realpath(__file__))}/test_data"


def renderTree(
    argDir: str,
    renderOption: RenderOption = defaultRenderOption,
    buildTreeOption: BuildTreeOption = defaultBuildTreeOption,
) -> str:
    result = renderTreeByLeftRight(f"{argDir}/left", f"{argDir}/right", renderOption, buildTreeOption)
    return result


def renderTreeByLeftRight(left: str, right: str, renderOption: RenderOption, buildTreeOption: BuildTreeOption) -> str:
    topNode = buildTree(f"{baseDir}/{left}", f"{baseDir}/{right}", buildTreeOption)
    renderResultList = renderNode(topNode, renderOption)
    textList = [renderResult.text for renderResult in renderResultList]
    result = "\n".join(textList) + "\n"
    return result


def normalizeDirectoryTest(argDir: str) -> str:
    result = normalizeDirectory(f"{baseDir}/{argDir}")
    return result


# Note: You must run build_test_data.sh before run tests.
# Tips: A command like "tree test_data/test_1xx" can help you see structure.
def test_100_empty():
    expected = """\
left/right
"""
    actual = renderTree("test_1xx")
    assert actual == expected


def test_200_files_in_left_only():
    expected = """\
left/right
├─🇫 a [-]
├─🇫 b [-]
└─🇫 c [-]
"""
    actual = renderTree("test_2xx")
    assert actual == expected


def test_300_files_in_right_only():
    expected = """\
left/right
├─🇫 a [+]
├─🇫 b [+]
└─🇫 c [+]
"""
    actual = renderTree("test_3xx")
    assert actual == expected


def test_400_files_in_both():
    expected = """\
left/right
├─🇫 a [-]
├─🇫 b [+]
└─🇫 c
"""
    actual = renderTree("test_4xx")
    assert actual == expected


def test_500_dirs_in_left_only():
    expected = """\
left/right
├─🇩 A [-]
├─🇩 B [-]
└─🇩 C [-]
"""
    actual = renderTree("test_5xx")
    assert actual == expected


def test_600_dirs_in_right_only():
    expected = """\
left/right
├─🇩 A [+]
├─🇩 B [+]
└─🇩 C [+]
"""
    actual = renderTree("test_6xx")
    assert actual == expected


def test_700_dirs_in_both():
    expected = """\
left/right
├─🇩 A [-]
├─🇩 B [+]
└─🇩 C
"""
    actual = renderTree("test_7xx")
    assert actual == expected


def test_800_dir_files_in_left_only():
    expected = """\
left/right
├─🇩 A [-]
│  └─🇫 a [-]
├─🇩 B [-]
│  ├─🇫 a [-]
│  └─🇫 b [-]
└─🇩 C [-]
    ├─🇫 a [-]
    ├─🇫 b [-]
    └─🇫 c [-]
"""
    actual = renderTree("test_8xx")
    assert actual == expected


def test_900_dir_files_in_right_only():
    expected = """\
left/right
├─🇩 A [+]
│  └─🇫 a [+]
├─🇩 B [+]
│  ├─🇫 a [+]
│  └─🇫 b [+]
└─🇩 C [+]
    ├─🇫 a [+]
    ├─🇫 b [+]
    └─🇫 c [+]
"""
    actual = renderTree("test_9xx")
    assert actual == expected


def test_1000_dir_files_in_both():
    expected = """\
left/right
├─🇩 A
│  └─🇫 a
├─🇩 B
│  ├─🇫 a [-]
│  └─🇫 b [+]
└─🇩 C
    ├─🇫 a [-]
    ├─🇫 b [+]
    └─🇫 c
"""
    actual = renderTree("test_10xx")
    assert actual == expected


def test_1100_dir_files_mixed_nested_same_name():
    expected = """\
left/right
├─🇫 left
└─🇩 right
    ├─🇫 left
    └─🇩 right
        ├─🇫 left
        └─🇩 right
            ├─🇫 left
            └─🇩 right
"""
    actual = renderTree("test_11xx")
    assert actual == expected


def test_1200_alone_dir_only():
    expected = """\
left/right
└─🇩 A / B / C / D
"""
    actual = renderTree("test_12xx")
    assert actual == expected


def test_1300_alone_dir_files():
    expected = """\
left/right
└─🇩 A / B / C / D
    ├─🇫 a [-]
    ├─🇫 b [+]
    └─🇫 c
"""
    actual = renderTree("test_13xx")
    assert actual == expected


def test_1400_nested_alone_dir_nested():
    expected = """\
left/right
├─🇩 A / B / C / D
│  ├─🇫 a
│  └─🇩 E / F / G / H
│      └─🇫 a
└─🇩 I / J / K / L
"""
    actual = renderTree("test_14xx")
    assert actual == expected


def test_1500_alone_dir_in_left_only():
    expected = """\
left/right
└─🇩 A [-] / B [-] / C [-] / D [-] / E [-]
"""
    actual = renderTree("test_15xx")
    assert actual == expected


def test_1600_alone_dir_in_right_only_from_the_middle():
    expected = """\
left/right
└─🇩 A / B / C / D [+] / E [+]
"""
    actual = renderTree("test_16xx")
    assert actual == expected


def test_1700_alone_dir_from_the_middle_mixed_nested():
    expected = """\
left/right
├─🇩 A / B / C / D [+]
│  ├─🇫 a [+]
│  └─🇩 E [+] / F [+] / G [+] / H [+]
│      └─🇫 a [+]
└─🇩 I / J / K [-] / L [-]
    └─🇫 a [-]
"""
    actual = renderTree("test_17xx")
    assert actual == expected


def test_1800_file_lexical_order():
    expected = """\
left/right
├─🇫 1
├─🇫 11
├─🇫 2
├─🇫 333
├─🇫 9
├─🇩 A
├─🇩 AA
├─🇩 B
├─🇩 CCC
└─🇩 Z
"""
    actual = renderTree("test_18xx")
    assert actual == expected


def test_1900_concat_top_alone_dir_only_dir():
    expected = """\
left/right / A / B / C
"""
    actual = renderTree("test_19xx", RenderOption(fileLexicalOrder, True, True, defaultThreadStrs, defaultIconStrs))
    assert actual == expected


def test_2000_concat_top_alone_dir_files():
    expected = """\
left/right / A / B / C
├─🇫 1
├─🇫 11 [-]
└─🇫 z [+]
"""
    actual = renderTree("test_20xx", RenderOption(fileLexicalOrder, True, True, defaultThreadStrs, defaultIconStrs))
    assert actual == expected


def test_2100_mixed_default_option():
    expected = """\
left/right
├─🇫 1
├─🇫 11
├─🇫 z [-]
├─🇩 A
│  ├─🇫 1 [+]
│  ├─🇫 11
│  ├─🇫 z
│  └─🇩 B
│      ├─🇩 C [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      ├─🇩 D / E
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z
│      ├─🇩 F / G / H [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      ├─🇩 I / J [-] / K [-]
│      │  ├─🇫 1 [-]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z [-]
│      └─🇩 L / M / N
└─🇩 O
    ├─🇫 1
    ├─🇫 11 [-]
    ├─🇫 z [+]
    └─🇩 P / Q / R [-]
"""
    actual = renderTree("test_21xx")
    assert actual == expected


# Expected is same as default option's one, because top directory's child is not alone.
def test_2101_mixed_concat_top_alone_dir():
    expected = """\
left/right
├─🇫 1
├─🇫 11
├─🇫 z [-]
├─🇩 A
│  ├─🇫 1 [+]
│  ├─🇫 11
│  ├─🇫 z
│  └─🇩 B
│      ├─🇩 C [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      ├─🇩 D / E
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z
│      ├─🇩 F / G / H [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      ├─🇩 I / J [-] / K [-]
│      │  ├─🇫 1 [-]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z [-]
│      └─🇩 L / M / N
└─🇩 O
    ├─🇫 1
    ├─🇫 11 [-]
    ├─🇫 z [+]
    └─🇩 P / Q / R [-]
"""
    actual = renderTree("test_21xx", RenderOption(fileLexicalOrder, True, True, defaultThreadStrs, defaultIconStrs))
    assert actual == expected


def test_2102_mixed_do_not_concat_alone_dir():
    expected = """\
left/right
├─🇫 1
├─🇫 11
├─🇫 z [-]
├─🇩 A
│  ├─🇫 1 [+]
│  ├─🇫 11
│  ├─🇫 z
│  └─🇩 B
│      ├─🇩 C [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      ├─🇩 D
│      │  └─🇩 E
│      │      ├─🇫 1 [+]
│      │      ├─🇫 11 [-]
│      │      └─🇫 z
│      ├─🇩 F
│      │  └─🇩 G
│      │      └─🇩 H [+]
│      │          ├─🇫 1 [+]
│      │          ├─🇫 11 [+]
│      │          └─🇫 z [+]
│      ├─🇩 I
│      │  └─🇩 J [-]
│      │      └─🇩 K [-]
│      │          ├─🇫 1 [-]
│      │          ├─🇫 11 [-]
│      │          └─🇫 z [-]
│      └─🇩 L
│          └─🇩 M
│              └─🇩 N
└─🇩 O
    ├─🇫 1
    ├─🇫 11 [-]
    ├─🇫 z [+]
    └─🇩 P
        └─🇩 Q
            └─🇩 R [-]
"""
    actual = renderTree("test_21xx", RenderOption(fileLexicalOrder, False, False, defaultThreadStrs, defaultIconStrs))
    assert actual == expected


# Just flipped [+] and [-].
def test_2103_mixed_left_side_is_newer():
    expected = """\
left/right
├─🇫 1
├─🇫 11
├─🇫 z [+]
├─🇩 A
│  ├─🇫 1 [-]
│  ├─🇫 11
│  ├─🇫 z
│  └─🇩 B
│      ├─🇩 C [-]
│      │  ├─🇫 1 [-]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z [-]
│      ├─🇩 D / E
│      │  ├─🇫 1 [-]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z
│      ├─🇩 F / G / H [-]
│      │  ├─🇫 1 [-]
│      │  ├─🇫 11 [-]
│      │  └─🇫 z [-]
│      ├─🇩 I / J [+] / K [+]
│      │  ├─🇫 1 [+]
│      │  ├─🇫 11 [+]
│      │  └─🇫 z [+]
│      └─🇩 L / M / N
└─🇩 O
    ├─🇫 1
    ├─🇫 11 [+]
    ├─🇫 z [-]
    └─🇩 P / Q / R [+]
"""
    actual = renderTree("test_21xx", buildTreeOption=BuildTreeOption(defaultExcludeDirs, defaultIgnoreCase, "left"))
    assert actual == expected


def test_2104_mixed_another_threads():
    expected = """\
left/right
^$.*🇫 1
^$.*🇫 11
^$.*🇫 z [-]
^$.*🇩 A
BB()^$.*🇫 1 [+]
BB()^$.*🇫 11
BB()^$.*🇫 z
BB()?/\\~🇩 B
BB()[]AA^$.*🇩 C [+]
BB()[]AABB()^$.*🇫 1 [+]
BB()[]AABB()^$.*🇫 11 [+]
BB()[]AABB()?/\\~🇫 z [+]
BB()[]AA^$.*🇩 D / E
BB()[]AABB()^$.*🇫 1 [+]
BB()[]AABB()^$.*🇫 11 [-]
BB()[]AABB()?/\\~🇫 z
BB()[]AA^$.*🇩 F / G / H [+]
BB()[]AABB()^$.*🇫 1 [+]
BB()[]AABB()^$.*🇫 11 [+]
BB()[]AABB()?/\\~🇫 z [+]
BB()[]AA^$.*🇩 I / J [-] / K [-]
BB()[]AABB()^$.*🇫 1 [-]
BB()[]AABB()^$.*🇫 11 [-]
BB()[]AABB()?/\\~🇫 z [-]
BB()[]AA?/\\~🇩 L / M / N
?/\\~🇩 O
[]AA^$.*🇫 1
[]AA^$.*🇫 11 [-]
[]AA^$.*🇫 z [+]
[]AA?/\\~🇩 P / Q / R [-]
"""
    anotherThreadStrs: Dict[ThreadKey, str] = {"blank": "[]AA", "vertical": "BB()", "branch": "^$.*", "corner": "?/\\~"}
    actual = renderTree("test_21xx", RenderOption(fileLexicalOrder, True, False, anotherThreadStrs, defaultIconStrs))
    assert actual == expected


def test_2105_mixed_another_icons():
    expected = """\
left/right
├─1
├─11
├─z [-]
├─[D]A
│  ├─1 [+]
│  ├─11
│  ├─z
│  └─[D]B
│      ├─[D]C [+]
│      │  ├─1 [+]
│      │  ├─11 [+]
│      │  └─z [+]
│      ├─[D]D / E
│      │  ├─1 [+]
│      │  ├─11 [-]
│      │  └─z
│      ├─[D]F / G / H [+]
│      │  ├─1 [+]
│      │  ├─11 [+]
│      │  └─z [+]
│      ├─[D]I / J [-] / K [-]
│      │  ├─1 [-]
│      │  ├─11 [-]
│      │  └─z [-]
│      └─[D]L / M / N
└─[D]O
    ├─1
    ├─11 [-]
    ├─z [+]
    └─[D]P / Q / R [-]
"""
    anotherIconStrs: Dict[IconKey, str] = {"dir": "[D]", "file": ""}
    actual = renderTree("test_21xx", RenderOption(fileLexicalOrder, True, False, defaultThreadStrs, anotherIconStrs))
    assert actual == expected


def test_2200_exclude_dirs_empty():
    expected = """\
left/right
"""
    actual = renderTree("test_22xx")
    assert actual == expected


def test_2300_exclude_dirs():
    expected = """\
left/right
└─🇩 A
    ├─🇫 1
    └─🇩 B [+] / C [+]
        └─🇫 2 [+]
"""
    actual = renderTree("test_23xx")
    assert actual == expected


def test_2400_exclude_dirs_another_dirs():
    expected = """\
left/right
└─🇩 A
    ├─🇫 1
    └─🇩 B [+] / C [+]
        └─🇫 2 [+]
"""
    excludeDirs = ["AAA", "BBB"]
    actual = renderTree("test_24xx", buildTreeOption=BuildTreeOption(excludeDirs, defaultIgnoreCase, defaultNewerSide))
    assert actual == expected


def test_2500_ignore_case():
    expected = """\
left/right
├─🇩 A
│  └─🇫 B
├─🇩 c
│  └─🇫 d
├─🇩 E
│  └─🇫 F
├─🇩 g
│  └─🇫 H
└─🇩 I
    └─🇫 J
"""
    actual = renderTree("test_25xx")
    assert actual == expected


def test_2501_ignore_case_left_is_newer():
    expected = """\
left/right
├─🇩 a
│  └─🇫 b
├─🇩 C
│  └─🇫 D
├─🇩 E
│  └─🇫 f
├─🇩 G
│  └─🇫 H
└─🇩 I
    └─🇫 J
"""
    actual = renderTree("test_25xx", buildTreeOption=BuildTreeOption(defaultExcludeDirs, defaultIgnoreCase, "left"))
    assert actual == expected


def test_2502_case_sensitive():
    expected = """\
left/right
├─🇩 A [+]
│  └─🇫 B [+]
├─🇩 a [-]
│  └─🇫 b [-]
├─🇩 C [-]
│  └─🇫 D [-]
├─🇩 c [+]
│  └─🇫 d [+]
├─🇩 E
│  ├─🇫 F [+]
│  └─🇫 f [-]
├─🇩 G [-]
│  └─🇫 H [-]
├─🇩 g [+]
│  └─🇫 H [+]
└─🇩 I
    └─🇫 J
"""
    actual = renderTree("test_25xx", buildTreeOption=BuildTreeOption(defaultExcludeDirs, False, defaultNewerSide))
    assert actual == expected


def test_n1_normalize_directory_normal():
    actual = normalizeDirectoryTest("test_n1")
    expected = os.path.abspath(f"{baseDir}/test_n1")
    assert actual == expected


def test_n2_normalize_directory_with_sep():
    actual = normalizeDirectoryTest("test_n2/")
    expected = os.path.abspath(f"{baseDir}/test_n2")
    assert actual == expected


def test_n3_normalize_directory_not_found():
    with pytest.raises(NotADirectoryError) as ex:
        normalizeDirectoryTest("test_n3")

    expected = os.path.abspath(f"{baseDir}/test_n3")
    assert str(ex.value) == f"{expected} is not a directory"


def test_s1_never_infinite_loop_symbolic_link():
    expected = """\
left/right
└─🇩 A
    └─🇫 B
"""
    actual = renderTree("test_s1")
    assert actual == expected
