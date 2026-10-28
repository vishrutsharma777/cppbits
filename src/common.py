def P(pid, section, title, lang, kind, statement, starter, solution, test, hint, expected=None):
    """One problem. kind: 'func' (hidden test program includes the solution)
    or 'stdout' (the solution's own main() must print `expected`)."""
    assert lang in ("c", "cpp") and kind in ("func", "stdout")
    assert (kind == "stdout") == (expected is not None) == (test is None)
    return dict(id=pid, section=section, title=title, lang=lang, kind=kind,
                statement=statement.strip(), starter=starter, solution=solution,
                test=test, hint=hint, expected=expected)


def Q(pid, section, title, lang, code, expected, explain, statement=""):
    """A predict-the-output question: the page shows `code` (a whole program), the user types
    what it prints. `expected` is checked against a real compile-and-run by tools/grade.mjs;
    `explain` (HTML) is shown after the answer is checked."""
    assert lang in ("c", "cpp")
    return dict(id=pid, section=section, title=title, lang=lang, kind="predict",
                statement=(statement or "<p>What does this program print?</p>").strip(),
                starter="", solution=code, test=None, hint=explain.strip(), expected=expected)
