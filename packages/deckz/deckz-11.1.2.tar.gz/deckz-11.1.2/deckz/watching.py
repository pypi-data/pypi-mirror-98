from logging import getLogger
from pathlib import Path
from threading import Thread
from time import time
from typing import FrozenSet, List, Optional

from watchdog.events import FileSystemEvent
from watchdog.observers import Observer

from deckz.exceptions import DeckzException
from deckz.paths import GlobalPaths, Paths
from deckz.running import run, run_standalones


_logger = getLogger(__name__)


class _BaseEventHandler:
    def __init__(self, minimum_delay: int):
        self._minimum_delay = minimum_delay
        self._last_compile = 0.0
        self._worker: Optional[Thread] = None
        self._first_build = True

    def run(self) -> None:
        raise NotImplementedError

    def __call__(self) -> None:
        try:
            self._compiling = True
            if self._first_build:
                self._first_build = False
                _logger.info("Initial build")
            else:
                _logger.info("Detected changes, starting a new build")
            try:
                self.run()
                _logger.info("Build finished")
            except Exception:
                _logger.exception("Build failed.")
        finally:
            self._compiling = False

    def dispatch(self, event: FileSystemEvent) -> None:
        current_time = time()
        if self._last_compile + self._minimum_delay > current_time:
            return
        elif self._worker is not None and self._worker.is_alive():
            _logger.info("Still on last build, not starting a new build")
            return
        else:
            self._last_compile = current_time
            self._worker = Thread(target=self.__call__)
            self._worker.start()


class _RunnerEventHandler(_BaseEventHandler):
    def __init__(
        self,
        minimum_delay: int,
        paths: Paths,
        build_handout: bool,
        build_presentation: bool,
        build_print: bool,
        target_whitelist: List[str],
    ):
        super().__init__(minimum_delay)
        self._paths = paths
        self._build_handout = build_handout
        self._build_presentation = build_presentation
        self._build_print = build_print
        self._target_whitelist = target_whitelist

    def run(self) -> None:
        run(
            paths=self._paths,
            build_handout=self._build_handout,
            build_presentation=self._build_presentation,
            build_print=self._build_print,
            target_whitelist=self._target_whitelist,
        )


class _StandalonesRunnerEventHandler(_BaseEventHandler):
    def __init__(self, minimum_delay: int, current_dir: Path):
        super().__init__(minimum_delay)
        self._current_dir = current_dir

    def run(self) -> None:
        run_standalones(self._current_dir)


def _watch(
    event_handler: _BaseEventHandler, watch: FrozenSet[Path], avoid: FrozenSet[Path]
) -> None:
    observer = Observer()
    dirs_to_avoid = avoid | {
        r_to_avoid
        for dir_to_avoid in avoid
        for p in dir_to_avoid.glob("**/*")
        if (r_to_avoid := p.resolve()).is_dir()
    }
    dirs_to_watch = watch | {
        r_to_watch
        for dir_to_watch in watch
        for p in dir_to_watch.glob("**/*")
        if (r_to_watch := p.resolve()).is_dir() and r_to_watch not in dirs_to_avoid
    }
    for dir_to_watch in dirs_to_watch:
        observer.schedule(event_handler, str(dir_to_watch.resolve()), recursive=False)
    event_handler()
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        _logger.info("Stopped watching")
    else:
        observer.join()
        raise DeckzException("Stopped watching abnormally")


def watch(
    minimum_delay: int,
    paths: Paths,
    build_handout: bool,
    build_presentation: bool,
    build_print: bool,
    target_whitelist: Optional[List[str]],
) -> None:
    _logger.info("Watching the shared, current, user and templates directories")
    _watch(
        _RunnerEventHandler(
            minimum_delay,
            paths,
            build_handout=build_handout,
            build_presentation=build_presentation,
            build_print=build_print,
            target_whitelist=target_whitelist,
        ),
        watch=frozenset(
            [
                paths.shared_dir,
                paths.current_dir,
                paths.templates_dir,
                paths.user_config_dir,
            ]
        ),
        avoid=frozenset([paths.shared_tikz_pdf_dir, paths.pdf_dir, paths.build_dir]),
    )


def watch_standalones(
    minimum_delay: int, current_dir: Path, paths: GlobalPaths
) -> None:
    _logger.info("Watching the shared tikz directory")
    _watch(
        _StandalonesRunnerEventHandler(minimum_delay, current_dir),
        watch=frozenset([paths.shared_tikz_dir]),
        avoid=frozenset([paths.shared_tikz_pdf_dir]),
    )
