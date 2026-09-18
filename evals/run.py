#!/usr/bin/env python3
"""Prepare and inspect small agent evals. Standard library only; no model calls."""

import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "evals" / "cases"
SKILL = ROOT / "skills" / "stop-writing-tests" / "SKILL.md"
ONE_LINE = (
    "Avoid redundant tests; reuse existing coverage and add the smallest test "
    "needed for a real coverage gap."
)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def files(folder):
    return {
        p.relative_to(folder).as_posix(): p.read_bytes()
        for p in sorted(folder.rglob("*"))
        if p.is_file() and not any(part in {"__pycache__", ".git"} for part in p.parts)
        and p.suffix not in {".pyc", ".pyo"}
    }


def digest(mapping):
    value = hashlib.sha256()
    for name, data in sorted(mapping.items()):
        value.update(name.encode("utf-8") + b"\0" + data + b"\0")
    return value.hexdigest()


def lines(data):
    if data is None:
        return []
    return data.decode("utf-8", errors="replace").replace("\r\n", "\n").splitlines(keepends=True)


def case_path(name):
    path = CASES / name
    if path.parent != CASES or not (path / "case.json").is_file():
        raise ValueError(f"Unknown case: {name}")
    return path


def run_checks(workspace, oracle=None):
    # Execute in a disposable copy so measurement never includes grader files.
    with tempfile.TemporaryDirectory(prefix="swt-check-") as temp:
        target = Path(temp) / "workspace"
        shutil.copytree(workspace, target, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        if oracle is None:
            command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", ".", "-p", "test*.py", "-v"]
        else:
            shutil.copy2(oracle, target / "_eval_oracle.py")
            command = [sys.executable, "-B", "_eval_oracle.py"]
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        try:
            result = subprocess.run(command, cwd=target, env=environment, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=30)
            return {"passed": result.returncode == 0, "exit_code": result.returncode,
                    "output": result.stdout + result.stderr}
        except subprocess.TimeoutExpired:
            return {"passed": False, "exit_code": None, "output": "Timed out after 30 seconds."}


def prepare(args):
    case = case_path(args.case)
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError(f"Refusing to overwrite {output}")
    output.mkdir(parents=True)
    shutil.copytree(case / "workspace", output / "workspace")
    prompt = (case / "task.md").read_text(encoding="utf-8").strip()
    prompt += "\n\nWork only in the provided workspace. Report changes and verification.\n"
    instruction = ""
    if args.condition == "one-line":
        instruction = ONE_LINE
    elif args.condition == "skill":
        instruction = "Apply the following skill while completing this task:\n\n" + SKILL.read_text(encoding="utf-8")
    if instruction:
        prompt += "\n" + instruction + "\n"
    (output / "PROMPT.md").write_text(prompt, encoding="utf-8")
    write_json(output / "run.json", {
        "case": args.case, "condition": args.condition,
        "baseline_sha256": digest(files(case / "workspace")),
        "case_sha256": digest(files(case)),
        "skill_sha256": hashlib.sha256(SKILL.read_bytes()).hexdigest() if args.condition == "skill" else None,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "agent": None, "model": None, "reasoning": None, "host_version": None,
        "repetition": None, "elapsed_seconds": None, "tokens": None,
        "activation_confirmed": None,
    })
    print(f"Prepared {output}\nStart a fresh agent in {output / 'workspace'} and supply PROMPT.md.")


def is_test_asset(name):
    path = Path(name)
    return path.name.startswith("test") or any(p in {"tests", "fixtures", "snapshots"} for p in path.parts) or path.name == "conftest.py"


def inspect_run(args):
    run = Path(args.run).resolve()
    report_path = run / "report.json"
    if report_path.exists():
        raise ValueError("report.json already exists; move it aside before a fresh inspection.")
    meta = read_json(run / "run.json")
    case = case_path(meta["case"])
    before, after = files(case / "workspace"), files(run / "workspace")
    if digest(files(case)) != meta["case_sha256"]:
        raise ValueError("Case changed since preparation; restore that case version before grading.")
    if digest(before) != meta["baseline_sha256"]:
        raise ValueError("Baseline changed since preparation.")
    changes = []
    diff = []
    for name in sorted(before.keys() | after.keys()):
        # Normalize line endings so an editor rewriting LF as CRLF does not
        # count as rewriting every line.
        old, new = lines(before.get(name)), lines(after.get(name))
        if old == new and (name in before) == (name in after):
            continue
        added = removed = 0
        for tag, i, j, k, l in difflib.SequenceMatcher(a=old, b=new, autojunk=False).get_opcodes():
            if tag != "equal":
                removed += j - i
                added += l - k
        changes.append({"path": name, "added_lines": added, "removed_lines": removed,
                        "test_asset_heuristic": is_test_asset(name),
                        "new_file": name not in before, "deleted_file": name not in after})
        diff.extend(difflib.unified_diff(old, new, fromfile="before/" + name, tofile="after/" + name))
    report = {
        "run": meta,
        "metrics": {
            "new_test_files_heuristic": sum(c["new_file"] and c["test_asset_heuristic"] for c in changes),
            "added_test_lines_heuristic": sum(c["added_lines"] for c in changes if c["test_asset_heuristic"]),
            "removed_test_lines_heuristic": sum(c["removed_lines"] for c in changes if c["test_asset_heuristic"]),
        },
        "changes": changes,
        "checks": {"submitted_suite": run_checks(run / "workspace"),
                   "acceptance_subset": run_checks(run / "workspace", case / "oracle.py")},
        "manual_review": {
            "task_correct": None, "necessary_coverage_retained": None,
            "missed_required_regression": None, "redundant_tests": None,
            "duplicate_coverage": None, "invented_requirements": None,
            "unnecessary_infrastructure": None, "existing_protection_weakened": None,
            "verification_adequate": None, "per_addition_evidence": [], "notes": "",
        },
    }
    # Do not overwrite a review already filled in by a human.
    write_json(report_path, report)
    (run / "changes.diff").write_text("".join(diff), encoding="utf-8")
    print(json.dumps({"metrics": report["metrics"],
                      "checks": {k: v["passed"] for k, v in report["checks"].items()},
                      "manual_review": "required; consult case.json and evals/README.md"}, indent=2))


def check_fixtures():
    failures = []
    for case in sorted(CASES.iterdir()):
        if not case.is_dir():
            continue
        spec = read_json(case / "case.json")
        baseline_suite = run_checks(case / "workspace")
        baseline_oracle = run_checks(case / "workspace", case / "oracle.py")
        with tempfile.TemporaryDirectory(prefix="swt-reference-") as temp:
            target = Path(temp) / "workspace"
            shutil.copytree(case / "workspace", target)
            shutil.copytree(case / "reference", target, dirs_exist_ok=True)
            reference_suite = run_checks(target)
            reference_oracle = run_checks(target, case / "oracle.py")
        with tempfile.TemporaryDirectory(prefix="swt-red-") as temp:
            target = Path(temp) / "workspace"
            shutil.copytree(case / "workspace", target)
            for path in (case / "reference").rglob("test*.py"):
                destination = target / path.relative_to(case / "reference")
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            reference_tests_on_baseline = run_checks(target)
        checks = {
            "baseline_suite": (baseline_suite, spec["baseline_suite_passes"]),
            "baseline_acceptance": (baseline_oracle, spec["baseline_acceptance_passes"]),
            "reference_suite": (reference_suite, True),
            "reference_acceptance": (reference_oracle, True),
            "reference_tests_on_baseline": (reference_tests_on_baseline,
                                            not spec["reference_tests_fail_on_baseline"]),
        }
        bad = [name for name, (result, expected) in checks.items() if result["passed"] != expected]
        print(f"{'FAIL' if bad else 'OK'} {case.name}")
        for name in bad:
            failures.append(f"{case.name}: {name}\n{checks[name][0]['output']}")
    if failures:
        raise ValueError("\n".join(failures))
    print("Fixture baselines and reference edits validated. No model benchmark was run.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    sub.add_parser("check-fixtures")
    prep = sub.add_parser("prepare")
    prep.add_argument("case")
    prep.add_argument("--condition", choices=["baseline", "one-line", "skill"], required=True)
    prep.add_argument("--output", required=True)
    inspect = sub.add_parser("inspect", help="Runs workspace Python tests; use only trusted eval output.")
    inspect.add_argument("run")
    args = parser.parse_args()
    if args.command == "list":
        for path in sorted(CASES.glob("*/case.json")):
            print(path.parent.name)
    elif args.command == "check-fixtures":
        check_fixtures()
    elif args.command == "prepare":
        prepare(args)
    else:
        inspect_run(args)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
