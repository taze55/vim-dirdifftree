# Vim global plugin for diff two directories and represent them as a tree
# Maintainer: taze55 <taze_a28391214@icloud.com>
# URL: https://github.com/taze55/vim-dirdifftree

import os
import functools
from typing import Callable, Literal, Union, List, Dict, NamedTuple

DirOrFile = Literal["dir", "file"]

LeftOrRight = Literal["left", "right"]

ExistsIn = Union[LeftOrRight, Literal["both"]]


class DiffTargets(NamedTuple):
    left: str
    right: str


class TreeNode:
    def __init__(self, relativePath: str, name: str, dirOrFile: DirOrFile, existsIn: ExistsIn) -> None:
        self.relativePath = relativePath
        self.name = name
        self.dirOrFile: DirOrFile = dirOrFile
        self.children: List[TreeNode] = []
        self.existsIn: ExistsIn = existsIn

    def childIsAloneDir(self) -> bool:
        return len(self.children) == 1 and self.children[0].dirOrFile == "dir"

    def getMarker(self, newerSide: LeftOrRight) -> str:
        if self.existsIn == "both":
            return ""
        if self.existsIn == newerSide:
            return " [+]"
        return " [-]"

    def getDiffTargets(self, left: str, right: str) -> DiffTargets:
        if self.existsIn == "left":
            return DiffTargets(left + self.relativePath, "")
        if self.existsIn == "right":
            return DiffTargets("", right + self.relativePath)
        return DiffTargets(left + self.relativePath, right + self.relativePath)


TreeNodeComparison = Callable[[TreeNode, TreeNode], int]

NodeMap = Dict[str, TreeNode]

ThreadKey = Literal["blank", "vertical", "branch", "corner"]

IconKey = DirOrFile


class RenderOption(NamedTuple):
    comparison: TreeNodeComparison
    newerSide: LeftOrRight
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

    la = a.name.lower()
    lb = b.name.lower()

    # https://stackoverflow.com/questions/22490366/how-to-use-cmp-in-python-3
    return (la > lb) - (la < lb)


def normalizeDirectory(directory: str) -> str:
    directoryTrimed = directory.rstrip(os.sep)
    if not os.path.isdir(directoryTrimed):
        raise NotADirectoryError(f"{directoryTrimed} is not a directory")
    return os.path.abspath(directoryTrimed)


def buildTree(left: str, right: str, excludeDirs: List[str]) -> TreeNode:
    leftName = os.path.basename(left)
    rightName = os.path.basename(right)

    topNode = TreeNode("", f"{leftName}/{rightName}", "dir", "both")
    nodeMap = {"": topNode}
    _buildRight(right, excludeDirs, nodeMap)
    _buildLeft(left, excludeDirs, nodeMap)

    return topNode


def _buildRight(right: str, excludeDirs: List[str], nodeMap: NodeMap) -> None:
    rightResult = os.walk(right)

    for parentPath, dirNames, fileNames in rightResult:
        relativeParentPath = parentPath.replace(right, "", 1)
        parentNode = nodeMap[relativeParentPath]

        dirNames[:] = [d for d in dirNames if d not in excludeDirs]
        for dirName in dirNames:
            _buildRightNode(dirName, relativeParentPath, parentNode, nodeMap, "dir")

        for fileName in fileNames:
            _buildRightNode(fileName, relativeParentPath, parentNode, nodeMap, "file")


def _buildRightNode(
    name: str, relativeParentPath: str, parentNode: TreeNode, nodeMap: NodeMap, dirOrFile: DirOrFile
) -> None:
    relativePath = relativeParentPath + os.sep + name
    newNode = TreeNode(relativePath, name, dirOrFile, "right")
    nodeMap[relativePath] = newNode
    parentNode.children.append(newNode)


def _buildLeft(left: str, excludeDirs: List[str], nodeMap: NodeMap) -> None:
    leftResult = os.walk(left)

    for parentPath, dirNames, fileNames in leftResult:
        relativeParentPath = parentPath.replace(left, "", 1)
        parentNode = nodeMap[relativeParentPath]

        dirNames[:] = [d for d in dirNames if d not in excludeDirs]
        for dirName in dirNames:
            _buildLeftNode(dirName, relativeParentPath, parentNode, nodeMap, "dir")

        for fileName in fileNames:
            _buildLeftNode(fileName, relativeParentPath, parentNode, nodeMap, "file")


def _buildLeftNode(
    name: str, relativeParentPath: str, parentNode: TreeNode, nodeMap: NodeMap, dirOrFile: DirOrFile
) -> None:
    relativePath = relativeParentPath + os.sep + name
    if relativePath in nodeMap:
        foundNode = nodeMap[relativePath]
        foundNode.existsIn = "both"
    else:
        newNode = TreeNode(relativePath, name, dirOrFile, "left")
        nodeMap[relativePath] = newNode
        parentNode.children.append(newNode)


def renderNode(node: TreeNode, renderOption: RenderOption) -> List[RenderResultDetail]:
    resultList: List[RenderResultDetail] = []
    nodeNameEndCol = len(node.name.encode())
    resultList.append(RenderResultDetail(node.name, node, 0, nodeNameEndCol))

    node.children.sort(key=functools.cmp_to_key(renderOption.comparison))
    lastIndex = len(node.children) - 1
    childIsAloneDir = renderOption.concatTopAloneDir and renderOption.concatAloneDir and node.childIsAloneDir()
    for i, child in enumerate(node.children):
        _renderNodeChildren(resultList, child, i == lastIndex, childIsAloneDir, [], renderOption)

    return resultList


def _renderNodeChildren(
    resultList: List[RenderResultDetail],
    node: TreeNode,
    isLast: bool,
    isAloneDir: bool,
    threadStack: List[str],
    renderOption: RenderOption,
) -> None:
    marker = node.getMarker(renderOption.newerSide)
    if isAloneDir:
        text = f"{resultList[-1].text} {os.sep} {node.name}"
        nodeNameEndCol = len(text.encode())
        text += marker
        resultList[-1] = RenderResultDetail(text, node, resultList[-1].nodeNameStartCol, nodeNameEndCol)
    else:
        threads = "".join(threadStack)
        threads += renderOption.threadStrs["corner"] if isLast else renderOption.threadStrs["branch"]
        icon = renderOption.iconStrs["dir"] if node.dirOrFile == "dir" else renderOption.iconStrs["file"]

        text = f"{threads}{icon}"
        nodeNameStartCol = len(text.encode())
        text += node.name
        nodeNameEndCol = len(text.encode())
        text += marker
        resultList.append(RenderResultDetail(text, node, nodeNameStartCol, nodeNameEndCol))

    if node.dirOrFile == "dir":
        if not isAloneDir:
            threadStack.append(renderOption.threadStrs["blank"] if isLast else renderOption.threadStrs["vertical"])

        node.children.sort(key=functools.cmp_to_key(renderOption.comparison))
        lastIndex = len(node.children) - 1
        childIsAloneDir = renderOption.concatAloneDir and node.childIsAloneDir()
        for i, child in enumerate(node.children):
            _renderNodeChildren(resultList, child, i == lastIndex, childIsAloneDir, threadStack, renderOption)

        if not isAloneDir:
            threadStack.pop()


if __name__ == "__main__":
    pass
