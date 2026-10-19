def P(pid, section, title, lang, kind, statement, starter, solution, test, hint, expected=None):
    """One problem. kind: 'func' (hidden test program includes the solution)
    or 'stdout' (the solution's own main() must print `expected`)."""
    assert lang in ("c", "cpp") and kind in ("func", "stdout")
    assert (kind == "stdout") == (expected is not None) == (test is None)
    return dict(id=pid, section=section, title=title, lang=lang, kind=kind,
                statement=statement.strip(), starter=starter, solution=solution,
                test=test, hint=hint, expected=expected)
