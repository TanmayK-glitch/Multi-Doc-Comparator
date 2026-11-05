from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = APP_DIR / "src"
DEFAULT_EVAL_SET = Path(__file__).with_name("eval_set.json")

sys.path.insert(0, str(SRC_DIR))

from retrieval import retrieve_from_providers  # pyright: ignore[reportMissingImports]  # noqa: E402
from reranking import build_candidates, rerank  # pyright: ignore[reportMissingImports]  # noqa: E402


def canonical_section(section: str) -> str:
    """Make evaluation section names comparable to document filename stems."""
    return section.replace("-", "_").lower()


def source_key(source: dict[str, str]) -> tuple[str, str]:
    return source["provider"].lower(), canonical_section(source["section"])


def evaluate_question(
    question: dict[str, Any],
    retrieval_top_k: int,
    rerank_top_k: int,
    use_reranker: bool,
) -> dict[str, Any]:
    expected_sources = question["expected_sources"]
    providers = list(dict.fromkeys(source["provider"] for source in expected_sources))
    provider_results = retrieve_from_providers(
        query=question["question"],
        providers=providers,
        top_k=retrieval_top_k,
    )
    candidates = build_candidates(provider_results)
    results = (
        rerank(
            query=question["question"],
            candidates=candidates,
            top_k=rerank_top_k,
        )
        if use_reranker
        else candidates
    )

    retrieved_sources = [
        {
            "provider": result.get("metadata", {}).get("provider", ""),
            "section": result.get("metadata", {}).get("section", ""),
        }
        for result in results
    ]
    retrieved_keys = {source_key(source) for source in retrieved_sources}
    expected_keys = {source_key(source) for source in expected_sources}
    covered_keys = expected_keys & retrieved_keys
    missing_sources = [
        source
        for source in expected_sources
        if source_key(source) not in retrieved_keys
    ]

    return {
        "id": question["id"],
        "type": question["type"],
        "difficulty": question["difficulty"],
        "question": question["question"],
        "expected_source_count": len(expected_keys),
        "covered_source_count": len(covered_keys),
        "coverage": len(covered_keys) / len(expected_keys) if expected_keys else 1.0,
        "passed": not missing_sources,
        "missing_sources": missing_sources,
        "retrieved_sources": retrieved_sources,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    expected_count = sum(result["expected_source_count"] for result in results)
    covered_count = sum(result["covered_source_count"] for result in results)

    by_group: dict[str, dict[str, Any]] = {}
    for group_name, group_results in (
        ("type", results),
        ("difficulty", results),
    ):
        groups = {}
        for result in group_results:
            group = result[group_name]
            groups.setdefault(group, []).append(result)
        by_group[group_name] = {
            group: {
                "questions": len(group_results),
                "passed": sum(result["passed"] for result in group_results),
                "coverage": (
                    sum(result["covered_source_count"] for result in group_results)
                    / sum(result["expected_source_count"] for result in group_results)
                ),
            }
            for group, group_results in groups.items()
        }

    return {
        "questions": len(results),
        "passed_questions": sum(result["passed"] for result in results),
        "question_pass_rate": (
            sum(result["passed"] for result in results) / len(results)
            if results
            else 1.0
        ),
        "expected_sources": expected_count,
        "covered_sources": covered_count,
        "source_coverage": covered_count / expected_count if expected_count else 1.0,
        "by": by_group,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--eval-set",
        type=Path,
        default=DEFAULT_EVAL_SET,
        help="Path to the evaluation JSON file.",
    )
    parser.add_argument(
        "--retrieval-top-k",
        type=int,
        default=5,
        help="Chunks retrieved per provider before reranking.",
    )
    parser.add_argument(
        "--rerank-top-k",
        type=int,
        default=5,
        help="Ranked chunks retained per question.",
    )
    parser.add_argument(
        "--rerank",
        action="store_true",
        help="Use the Cohere reranker after local retrieval.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for the detailed JSON report.",
    )
    args = parser.parse_args()

    if args.retrieval_top_k < 1 or args.rerank_top_k < 1:
        parser.error("top-k values must be positive")

    questions = json.loads(args.eval_set.read_text(encoding="utf-8"))
    results = [
        evaluate_question(
            question,
            retrieval_top_k=args.retrieval_top_k,
            rerank_top_k=args.rerank_top_k,
            use_reranker=args.rerank,
        )
        for question in questions
    ]
    report = {
        "config": {
            "eval_set": str(args.eval_set),
            "retrieval_top_k": args.retrieval_top_k,
            "rerank_top_k": args.rerank_top_k,
            "rerank": args.rerank,
        },
        "summary": summarize(results),
        "results": results,
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )

    summary = report["summary"]
    print(
        f"Questions: {summary['passed_questions']}/{summary['questions']} passed | "
        f"source coverage: {summary['covered_sources']}/"
        f"{summary['expected_sources']} "
        f"({summary['source_coverage']:.1%})"
    )
    for result in results:
        status = "PASS" if result["passed"] else "MISS"
        print(
            f"{status} {result['id']:>2}: "
            f"{result['covered_source_count']}/{result['expected_source_count']} "
            f"({result['coverage']:.1%})"
        )
        if result["missing_sources"]:
            missing = ", ".join(
                f"{source['provider']}/{source['section']}"
                for source in result["missing_sources"]
            )
            print(f"       missing: {missing}")


if __name__ == "__main__":
    main()
