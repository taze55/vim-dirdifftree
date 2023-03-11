# Vim global plugin for diff two directories and represent them as a tree
# Maintainer: taze55 <taze_a28391214@icloud.com>
# URL: https://github.com/taze55/vim-dirdifftree

import os
import functools
from typing import Callable, Literal, Union, List, Dict, NamedTuple

DirOrFile = Literal["dir", "file"]

LeftOrRight = Literal["left", "right"]

Place = Union[LeftOrRight, Literal["both"]]

ExistsIn = Literal["old", "new", "both"]


class DiffTargets(NamedTuple):
    left: str
    right: str


class TreeNode:
    def __init__(self, relativePath: str, name: str, dirOrFile: DirOrFile, place: Place, existsIn: ExistsIn) -> None:
        self.relativePath = relativePath
        self.name = name
        self.dirOrFile: DirOrFile = dirOrFile
        self.children: List[TreeNode] = []
        self.place: Place = place
        self.existsIn: ExistsIn = existsIn

    def childIsAloneDir(self) -> bool:
        return len(self.children) == 1 and self.children[0].dirOrFile == "dir"

    def getMarker(self) -> str:
        if self.existsIn == "both":
            return ""
        if self.existsIn == "new":
            return " [+]"
        return " [-]"

    def getDiffTargets(self, left: str, right: str) -> DiffTargets:
        if self.place == "left":
            return DiffTargets(left + self.relativePath, "")
        if self.place == "right":
            return DiffTargets("", right + self.relativePath)
        return DiffTargets(left + self.relativePath, right + self.relativePath)


TreeNodeComparison = Callable[[TreeNode, TreeNode], int]

NodeMap = Dict[str, TreeNode]

ThreadKey = Literal["blank", "vertical", "branch", "corner"]

IconKey = DirOrFile


class BuildTreeOption(NamedTuple):
    excludeDirs: List[str]
    ignoreCase: bool
    newerSide: LeftOrRight


class RenderOption(NamedTuple):
    comparison: TreeNodeComparison
    concatAloneDir: bool
    concatTopAloneDir: bool
    threadStrs: Dict[ThreadKey, str]
    iconStrs: Dict[IconKey, str]


# Just extracted what we need from RenderResultDetail
class RenderResult(NamedTuple):
    node: TreeNode
    nodeNameStartCol: int
    nodeNameEndCol: int


class RenderResultDetail(NamedTuple):
    text: str
    node: TreeNode
    nodeNameStartCol: int
    nodeNameEndCol: int


def fileLexicalOrder(a: TreeNode, b: TreeNode) -> int:
    if a.dirOrFile == "file" and b.dirOrFile == "dir":
        return -1
    elif a.dirOrFile == "dir" and b.dirOrFile == "file":
        return 1

    na = a.name
    nb = b.name

    la = na.lower()
    lb = nb.lower()

    # https://stackoverflow.com/questions/22490366/how-to-use-cmp-in-python-3
    l_diff = (la > lb) - (la < lb)
    if l_diff != 0:
        return l_diff

    n_diff = (na > nb) - (na < nb)
    return n_diff


def normalizeDirectory(directory: str) -> str:
    directoryTrimed = directory.rstrip(os.sep)
    if not os.path.isdir(directoryTrimed):
        raise NotADirectoryError(f"{directoryTrimed} is not a directory")
    return os.path.abspath(directoryTrimed)


def buildTree(left: str, right: str, option: BuildTreeOption) -> TreeNode:
    leftName = os.path.basename(left)
    rightName = os.path.basename(right)

    topNode = TreeNode("", f"{leftName}/{rightName}", "dir", "both", "both")
    nodeMap = {"": topNode}

    if option.newerSide == "right":
        _buildNew(right, nodeMap, option)
        _buildOld(left, nodeMap, option)
    else:
        _buildNew(left, nodeMap, option)
        _buildOld(right, nodeMap, option)

    return topNode


def _buildNew(new: str, nodeMap: NodeMap, option: BuildTreeOption) -> None:
    newResult = os.walk(new)

    for parentPath, dirNames, fileNames in newResult:
        relativeParentPath = parentPath.replace(new, "", 1)
        key = relativeParentPath.lower() if option.ignoreCase else relativeParentPath
        parentNode = nodeMap[key]

        dirNames[:] = [d for d in dirNames if d not in option.excludeDirs]
        for dirName in dirNames:
            _buildNewNode(dirName, relativeParentPath, parentNode, nodeMap, "dir", option)

        for fileName in fileNames:
            _buildNewNode(fileName, relativeParentPath, parentNode, nodeMap, "file", option)


def _buildNewNode(
    name: str,
    relativeParentPath: str,
    parentNode: TreeNode,
    nodeMap: NodeMap,
    dirOrFile: DirOrFile,
    option: BuildTreeOption,
) -> None:
    relativePath = relativeParentPath + os.sep + name
    newNode = TreeNode(relativePath, name, dirOrFile, option.newerSide, "new")
    key = relativePath.lower() if option.ignoreCase else relativePath
    nodeMap[key] = newNode
    parentNode.children.append(newNode)


def _buildOld(old: str, nodeMap: NodeMap, option: BuildTreeOption) -> None:
    oldResult = os.walk(old)

    for parentPath, dirNames, fileNames in oldResult:
        relativeParentPath = parentPath.replace(old, "", 1)
        key = relativeParentPath.lower() if option.ignoreCase else relativeParentPath
        parentNode = nodeMap[key]

        dirNames[:] = [d for d in dirNames if d not in option.excludeDirs]
        for dirName in dirNames:
            _buildOldNode(dirName, relativeParentPath, parentNode, nodeMap, "dir", option)

        for fileName in fileNames:
            _buildOldNode(fileName, relativeParentPath, parentNode, nodeMap, "file", option)


def _buildOldNode(
    name: str,
    relativeParentPath: str,
    parentNode: TreeNode,
    nodeMap: NodeMap,
    dirOrFile: DirOrFile,
    option: BuildTreeOption,
) -> None:
    relativePath = relativeParentPath + os.sep + name
    key = relativePath.lower() if option.ignoreCase else relativePath
    if key in nodeMap:
        foundNode = nodeMap[key]
        foundNode.place = "both"
        foundNode.existsIn = "both"
    else:
        place = "left" if option.newerSide == "right" else "right"
        newNode = TreeNode(relativePath, name, dirOrFile, place, "old")
        nodeMap[key] = newNode
        parentNode.children.append(newNode)


def renderNode(node: TreeNode, option: RenderOption) -> List[RenderResultDetail]:
    resultList: List[RenderResultDetail] = []
    nodeNameEndCol = len(node.name.encode())
    resultList.append(RenderResultDetail(node.name, node, 0, nodeNameEndCol))

    node.children.sort(key=functools.cmp_to_key(option.comparison))
    lastIndex = len(node.children) - 1
    childIsAloneDir = option.concatTopAloneDir and option.concatAloneDir and node.childIsAloneDir()
    for i, child in enumerate(node.children):
        _renderNodeChildren(resultList, child, i == lastIndex, childIsAloneDir, [], option)

    return resultList


def _renderNodeChildren(
    resultList: List[RenderResultDetail],
    node: TreeNode,
    isLast: bool,
    isAloneDir: bool,
    threadStack: List[str],
    option: RenderOption,
) -> None:
    marker = node.getMarker()
    if isAloneDir:
        text = f"{resultList[-1].text} {os.sep} {node.name}"
        nodeNameEndCol = len(text.encode())
        text += marker
        resultList[-1] = RenderResultDetail(text, node, resultList[-1].nodeNameStartCol, nodeNameEndCol)
    else:
        threads = "".join(threadStack)
        threads += option.threadStrs["corner"] if isLast else option.threadStrs["branch"]
        icon = option.iconStrs["dir"] if node.dirOrFile == "dir" else option.iconStrs["file"]

        text = f"{threads}{icon}"
        nodeNameStartCol = len(text.encode())
        text += node.name
        nodeNameEndCol = len(text.encode())
        text += marker
        resultList.append(RenderResultDetail(text, node, nodeNameStartCol, nodeNameEndCol))

    if node.dirOrFile == "dir":
        if not isAloneDir:
            threadStack.append(option.threadStrs["blank"] if isLast else option.threadStrs["vertical"])

        node.children.sort(key=functools.cmp_to_key(option.comparison))
        lastIndex = len(node.children) - 1
        childIsAloneDir = option.concatAloneDir and node.childIsAloneDir()
        for i, child in enumerate(node.children):
            _renderNodeChildren(resultList, child, i == lastIndex, childIsAloneDir, threadStack, option)

        if not isAloneDir:
            threadStack.pop()


if __name__ == "__main__":
    pass
