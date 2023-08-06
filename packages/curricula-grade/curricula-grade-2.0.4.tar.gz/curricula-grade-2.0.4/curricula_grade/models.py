import importlib.util
import json
import sys
from pathlib import Path
from typing import List
from dataclasses import field
from decimal import Decimal

from curricula.models import Assignment, Problem
from curricula.structure import Files
from .grader import Grader

__all__ = ("import_grader", "GradingProblem", "GradingAssignment")


def import_grader(grading_path: Path, problem: "GradingProblem", grader_name: str = "grader") -> Grader:
    """Import a grader from a tests file."""

    # Try to import as a module
    if grading_path.joinpath("__init__.py").is_file():
        name = f"_curricula_grading_{grading_path.parts[-1]}"
        spec = importlib.util.spec_from_file_location(name, str(grading_path.joinpath("__init__.py")))
        module = importlib.util.module_from_spec(spec)

    # Otherwise there's a tests.py
    else:
        name = f"_curricula_grading_{grading_path.parts[-1]}_tests"
        spec = importlib.util.spec_from_file_location(name, str(grading_path.joinpath("tests.py")))
        module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)
    grader = getattr(module, grader_name)
    grader.problem = problem

    return grader


class GradingProblem(Problem):
    """Additional details for grading."""

    path: Path = field(init=False)
    grader: Grader = field(init=False)

    @property
    def automated_point_ratio(self) -> Decimal:
        return self.grading.automated.points / self.grader.register.weight()

    def percentage(self) -> Decimal:
        """Percentage weight of the problem in the assignment."""

        if self.assignment.grading.weight() == 0:
            return Decimal(0)
        return self.grading.weight / self.assignment.grading.weight()

    @classmethod
    def read(cls, data: dict, path: Path) -> "GradingProblem":
        """Import the grader."""

        self = GradingProblem.load(data)
        self.path = path
        if self.grading.is_automated:
            self.grader = import_grader(path, self)
        return self


class GradingAssignment(Assignment):
    """Additional details for grading."""

    path: Path

    problems: List[GradingProblem]

    @classmethod
    def read(cls, path: Path) -> "GradingAssignment":
        """Read the assignment.json and rebuild the models."""

        with path.joinpath(Files.INDEX).open("r") as file:
            data = json.load(file)

        problems = []
        for problem_data in data.pop("problems"):
            problems.append(GradingProblem.read(
                data=problem_data,
                path=path.joinpath(problem_data["short"])))

        assignment = GradingAssignment.load(data, problems=problems)
        assignment.path = path

        return assignment
