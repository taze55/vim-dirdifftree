# Vim global plugin for diff two directories and represent them as a tree
# Maintainer: taze55 <taze_a28391214@icloud.com>
# URL: https://github.com/taze55/vim-dirdifftree

import sys
from dirdifftree_lib import *


def _validatePythonVersion(*, neededVersion):
    actualVersion = sys.version_info[:3]
    if actualVersion < neededVersion:
        version = ".".join([str(x) for x in list(neededVersion)])
        raise RuntimeError(f"Please use Python {version} or later for dirdifftree.")


_validatePythonVersion(neededVersion=(3, 8, 10))

import os
from typing import List, Dict, Any, Optional, Tuple, Iterable, NamedTuple
import vim

NODE_START_INDEX = 3


class ExecutionState:
    def __init__(self, left: str, right: str) -> None:
        self.left = left
        self.right = right
        self.tabpage: Any = None
        self.mainWindow: Any = None
        self.mainBuffer: Any = None
        self.leftWindow: Any = None
        self.leftBuffer: Any = None
        self.rightWindow: Any = None
        self.rightBuffer: Any = None
        self.renderResultList: List[RenderResult] = []


class DirDiffTreeState:
    def __init__(self) -> None:
        self.mainWindowFileNameSequence = 1
        self.executionStateMap: Dict[int, ExecutionState] = {}


_state: DirDiffTreeState = DirDiffTreeState()


def dirDiffTreeExecute(leftArg: str, rightArg: str) -> None:
    # preparing
    try:
        left = normalizeDirectory(leftArg)
        right = normalizeDirectory(rightArg)
    except NotADirectoryError as ex:
        _printVimError(str(ex))
        return
    if left == right:
        _printVimWarning("both are the same directory")

    # rendering
    topNode = buildTree(left, right)
    threadStrs = vim.eval("g:DirDiffTreeThreads")
    iconsStrs = vim.eval("g:DirDiffTreeIcons")
    renderOption = RenderOption(fileLexicalOrder, "right", True, False, threadStrs, iconsStrs)
    renderResultDetailList = renderNode(topNode, renderOption)

    # starting
    fileName = _getMainWindowFileName()
    if not _isTabpageReusable():
        vim.command("tabnew")
    vim.command(f"setlocal filetype=dirdifftree | setlocal noreadonly | setlocal modifiable | silent file {fileName}")

    # save state
    state = ExecutionState(left, right)
    _state.executionStateMap[vim.current.buffer.number] = state
    state.tabpage = vim.current.tabpage
    state.mainWindow = vim.current.window
    state.mainBuffer = vim.current.buffer
    state.renderResultList = [RenderResult(*rrd[1:]) for rrd in renderResultDetailList]
    textList = [renderResultDetail.text for renderResultDetail in renderResultDetailList]

    # building buffer
    vim.current.line = "// Usage: o:open, <C-N>:next, <C-P>:previous"
    vim.current.buffer.append("")
    vim.current.buffer.append(textList)

    # finishing
    vim.command("setlocal readonly | setlocal nomodifiable")
    vim.command("silent! normal! zR")
    dirDiffTreeGotoNextFile()
    dirDiffTreeOpen()


def dirDiffTreeGotoNextFile() -> None:
    state = _state.executionStateMap[vim.current.buffer.number]

    currentLineIndex = vim.current.window.cursor[0] - NODE_START_INDEX
    getNextFileResult = _getNextFileIndex(enumerate(state.renderResultList), currentLineIndex)
    if getNextFileResult is None:
        return

    if getNextFileResult.cycled:
        _printVimWarning("search hit BOTTOM, continuing at TOP")

    nextFileIndex = getNextFileResult.index
    row = nextFileIndex + NODE_START_INDEX
    col = state.renderResultList[nextFileIndex].nodeNameStartCol
    vim.current.window.cursor = (row, col)
    vim.command("silent! normal! zv")


def dirDiffTreeGotoPreviousFile() -> None:
    state = _state.executionStateMap[vim.current.buffer.number]

    currentLineIndex = vim.current.window.cursor[0] - NODE_START_INDEX
    reversedCurrentLineIndex = len(state.renderResultList) - currentLineIndex - 1
    getPreviousFileResult = _getNextFileIndex(enumerate(reversed(state.renderResultList)), reversedCurrentLineIndex)

    if getPreviousFileResult is None:
        return

    if getPreviousFileResult.cycled:
        _printVimWarning("search hit TOP, continuing at BOTTOM")

    previousFileIndex = len(state.renderResultList) - getPreviousFileResult.index - 1
    row = previousFileIndex + NODE_START_INDEX
    col = state.renderResultList[previousFileIndex].nodeNameStartCol
    vim.current.window.cursor = (row, col)
    vim.command("silent! normal! zv")


class GetNextFileResult(NamedTuple):
    index: int
    cycled: bool


def _getNextFileIndex(renderResults: Iterable[Tuple[int, RenderResult]], startAt: int) -> Optional[GetNextFileResult]:
    result = None
    for i, renderResult in renderResults:
        if renderResult.node.dirOrFile == "file":
            if result is None:
                result = GetNextFileResult(i, True)
            if i > startAt:
                return GetNextFileResult(i, False)
    return result


def dirDiffTreeToggleFold() -> None:
    row = vim.current.window.cursor[0]
    renderResult = _getRenderResultByRow(row)
    if renderResult is None:
        return
    if renderResult.node.dirOrFile == "dir":
        vim.command("silent! normal! za")


def dirDiffTreeOpenOrToggleFold() -> None:
    row = vim.current.window.cursor[0]
    renderResult = _getRenderResultByRow(row)
    if renderResult is None:
        return
    if renderResult.node.dirOrFile == "dir":
        vim.command("silent! normal! za")
        return
    _dirDiffTreeOpenRenderResult(renderResult, row)


def dirDiffTreeOpen() -> None:
    row = vim.current.window.cursor[0]
    renderResult = _getRenderResultByRow(row)
    if renderResult is None:
        return
    _dirDiffTreeOpenRenderResult(renderResult, row)


def _dirDiffTreeOpenRenderResult(renderResult: RenderResult, row: int) -> None:
    # preparing
    node = renderResult.node
    if node.dirOrFile == "dir":
        return

    state = _state.executionStateMap[vim.current.buffer.number]
    if not state.mainWindow.valid:
        _printVimError("can't reuse closed window")
        return

    diffTargets = node.getDiffTargets(state.left, state.right)
    startCol = renderResult.nodeNameStartCol
    endCol = renderResult.nodeNameEndCol + 1

    # Delete previous buffer
    if state.leftBuffer is not None and state.leftBuffer.valid:
        vim.command(f"silent! bdelete {state.leftBuffer.number}")
    if state.rightBuffer is not None and state.rightBuffer.valid:
        vim.command(f"silent! bdelete {state.rightBuffer.number}")

    # create left side
    try:
        if diffTargets.left == "":
            tempfile = vim.eval("tempname()")
            vim.command(f"silent vsplit {tempfile} | setlocal buftype=nowrite | setlocal noswapfile")
        else:
            vim.command(f"silent vsplit {diffTargets.left}")
    except vim.error as ex:
        vim.command(f"silent! match DirDiffTreeFailed '\\%{row}l\\%>{startCol}c\\%<{endCol}c'")
        raise (ex)
    state.leftWindow = vim.current.window
    state.leftBuffer = vim.current.buffer

    # formatting main window
    vim.current.window = state.mainWindow
    dirDiffTreeMainWindowWidth = vim.eval("g:DirDiffTreeMainWindowWidth")
    vim.command(f"silent! vertical resize {dirDiffTreeMainWindowWidth}")
    vim.command(f"silent! match DirDiffTreeSelected '\\%{row}l\\%>{startCol}c\\%<{endCol}c'")

    # create right side
    vim.current.window = state.leftWindow
    try:
        if diffTargets.right == "":
            tempfile = vim.eval("tempname()")
            vim.command(f"silent vert diffsplit {tempfile} | setlocal buftype=nowrite | setlocal noswapfile")
        else:
            vim.command(f"silent vert diffsplit {diffTargets.right}")
    except vim.error as ex:
        vim.command(f"silent! bdelete {state.leftBuffer.number}")
        vim.command(f"silent! match DirDiffTreeFailed '\\%{row}l\\%>{startCol}c\\%<{endCol}c'")
        raise (ex)
    state.rightWindow = vim.current.window
    state.rightBuffer = vim.current.buffer

    # resize none file windows
    dirDiffTreeNoneFileWindowWidth = int(vim.eval("g:DirDiffTreeNoneFileWindowWidth"))
    if dirDiffTreeNoneFileWindowWidth > 0:
        if diffTargets.left == "":
            vim.current.window = state.leftWindow
            vim.command(f"vert resize {dirDiffTreeNoneFileWindowWidth}")
        if diffTargets.right == "":
            vim.current.window = state.rightWindow
            vim.command(f"vert resize {dirDiffTreeNoneFileWindowWidth}")

    # finishing
    vim.current.window = state.mainWindow


def dirDiffTreeReload() -> None:
    _printVimError("sorry, it's in development")


def dirDiffTreeCleanUp(abufArg: str) -> None:
    abuf = int(abufArg)
    if abuf in _state.executionStateMap:
        del _state.executionStateMap[abuf]


def dirDiffTreeDebug() -> None:
    # print("--------------------------------")
    # print("\n".join(dir(vim.current.window)))
    # print("--------------------------------")
    pass


def _getRenderResultByRow(row: int) -> Optional[RenderResult]:
    state = _state.executionStateMap[vim.current.buffer.number]
    index = row - NODE_START_INDEX
    if index >= 0 and index < len(state.renderResultList):
        return state.renderResultList[index]
    return None


def _isTabpageReusable() -> bool:
    if len(vim.current.tabpage.windows) != 1:
        return False
    if len(vim.current.buffer) != 1:
        return False
    if len(vim.current.line) != 0:
        return False
    if vim.eval("&modified") != "0":
        return False
    if vim.eval("expand('%')") != "":
        return False
    return True


def _getMainWindowFileName() -> str:
    checkNameBase = vim.eval("getcwd()") + os.sep + "DirDiffTree"
    i = _state.mainWindowFileNameSequence
    bufferNames = [b.name for b in vim.buffers]
    while True:
        seqStr = "" if i == 1 else str(i)
        checkName = checkNameBase + seqStr
        if checkName in bufferNames:
            i += 1
            continue

        _state.mainWindowFileNameSequence = i + 1
        return "DirDiffTree" + seqStr


def _printVimWarning(warningMsg: str) -> None:
    errorMsgSub = warningMsg.replace("'", "''")
    vim.command(f"echohl WarningMsg | echo '{errorMsgSub}' | echohl None")


def _printVimError(errorMsg: str) -> None:
    errorMsgSub = errorMsg.replace("'", "''")
    vim.command(f"echohl ErrorMsg | echo '{errorMsgSub}' | echohl None")


if __name__ == "__main__":
    pass
