from pathlib import Path
from typing import Literal, Optional, Sequence, cast

from invoke import Collection, Context, Result, UnexpectedExit, task
from outcome.devkit.invoke import env
from outcome.devkit.invoke.tasks import clean
from outcome.utils.env import is_ci
from pydantic import BaseModel, Field
from rich.console import Console


class PyrightDiagnosticRangeBoundary(BaseModel):
    line: int
    character: int


class PyrightDiagnosticRange(BaseModel):
    start: PyrightDiagnosticRangeBoundary
    end: PyrightDiagnosticRangeBoundary


class PyrightDiagnostic(BaseModel):
    file: str
    severity: Literal['error', 'warning', 'information']
    message: str
    rule: Optional[str]
    range: PyrightDiagnosticRange  # noqa: A003, WPS125


class PyrightOutputSummary(BaseModel):
    error_count: int = Field(..., alias='errorCount')
    files_analyzed: int = Field(..., alias='filesAnalyzed')
    warning_count: int = Field(..., alias='warningCount')


class PyrightOutput(BaseModel):
    class Config:
        extra = 'ignore'

    diagnostics: Sequence[PyrightDiagnostic]
    summary: PyrightOutputSummary


@env.add
def check_targets(e: env.Env) -> str:
    return ' '.join(d for d in ('./src', './bin', './test', './tasks.py') if Path(d).exists())


@task(clean.all)
def types(c: Context, show_information: bool = False):
    """Run type-checking."""
    directories = env.r(check_targets)
    res = cast(Result, c.run(f'poetry run pyright {directories} --outputjson', echo=True, hide=True, warn=True))

    assert isinstance(res.stdout, str)
    results = PyrightOutput.parse_raw(res.stdout)

    console = Console()

    files_analyzed = results.summary.files_analyzed
    warning_count = results.summary.warning_count
    error_count = results.summary.error_count

    console.print(
        f'pyright analyzed {files_analyzed} file(s), with {warning_count} warnings and {error_count} errors',  # noqa: E501
        style='cyan',
    )

    skipped_statuses = set()
    if not show_information:
        skipped_statuses.add('information')

    for d in (d for d in results.diagnostics if d.severity not in skipped_statuses):  # noqa: WPS335
        if d.severity == 'error':
            color = 'red'
        elif d.severity == 'warning':
            color = 'yellow'
        else:
            color = 'blue'

        message = f'[dim]({d.rule})[/dim] {d.message}' if d.rule else d.message
        file = d.file
        line = d.range.start.line + 1
        col = d.range.start.character + 1
        severity = d.severity

        console.print(f'{file}:{line}:{col} - [bold {color}]{severity}[/bold {color}] {message}')

    if results.summary.error_count > 0:
        res.hide = ()
        raise UnexpectedExit(res, 'Error checking types')


@task(clean.all)
def format(c: Context):  # noqa: A001, WPS125
    """Run formatter."""
    directories = env.r(check_targets)
    if is_ci():
        c.run(f'poetry run black --check {directories}')
    else:
        c.run(f'poetry run black {directories}')


@task(clean.all)
def isort(c: Context):
    """Run isort."""
    directories = env.r(check_targets)
    if is_ci():
        c.run(f'poetry run isort -rc {directories} --check-only')
    else:
        c.run(f'poetry run isort -rc {directories}')


@task(clean.all)
def lint(c: Context):
    """Run flake8."""
    directories = env.r(check_targets)
    c.run(f'poetry run flake8 {directories}')


@task(clean.all, types, isort, format, lint)
def all(c: Context):  # noqa: A001, WPS125
    """Run all checks."""
    ...


ns = Collection(lint, isort, format, types)
ns.add_task(all, default=True)
