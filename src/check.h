/* check.h -- tiny test helpers used by every hidden test program.
   Each check prints a MISMATCH line on failure; ck_done() prints the
   @@RESULT line that the website reads. */
#ifndef CHECK_H
#define CHECK_H
#pragma clang system_header
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#ifdef __cplusplus
#include <cmath>
#include <cstdio>
#endif

static int ck_total = 0, ck_fail = 0;
static unsigned ck_state = 2463534242u;

/* xorshift32: the same "random" tests on every run */
static unsigned ck_rand(void) {
    ck_state ^= ck_state << 13; ck_state ^= ck_state >> 17; ck_state ^= ck_state << 5;
    return ck_state;
}
static int ck_range(int lo, int hi) { return (int)((long long)lo + (long long)(ck_rand() % (unsigned)((long long)hi - lo + 1))); }
static double ck_unit(void) { return (double)(ck_rand() >> 8) / 16777216.0 * 2.0 - 1.0; } /* [-1, 1) */

static void ck_bad(void) { ck_fail++; }
static int ck_show(void) { return ck_fail < 10; }

static void ck_int(const char *what, long long got, long long want) {
    ck_total++;
    if (got != want) { if (ck_show()) printf("MISMATCH %s | expected %lld | got %lld\n", what, want, got); ck_bad(); }
}
static void ck_hex(const char *what, unsigned long long got, unsigned long long want) {
    ck_total++;
    if (got != want) { if (ck_show()) printf("MISMATCH %s | expected 0x%llX | got 0x%llX\n", what, want, got); ck_bad(); }
}
/* |got - want| <= tol * max(1, |want|) */
static void ck_dbl(const char *what, double got, double want, double tol) {
    ck_total++;
    double scale = fabs(want) > 1.0 ? fabs(want) : 1.0;
    int bad = (got != got) || !(fabs(got - want) <= tol * scale);
    if (bad) { if (ck_show()) printf("MISMATCH %s | expected %.9g | got %.9g\n", what, want, got); ck_bad(); }
}
static void ck_true(const char *what, int ok) {
    ck_total++;
    if (!ok) { if (ck_show()) printf("MISMATCH %s\n", what); ck_bad(); }
}
static void ck_str(const char *what, const char *got, const char *want) {
    ck_total++;
    if (got == 0 || strcmp(got, want) != 0) {
        if (ck_show()) printf("MISMATCH %s | expected \"%s\" | got \"%s\"\n", what, want, got ? got : "(null)");
        ck_bad();
    }
}
static int ck_done(void) {
    printf("@@RESULT %d %d\n", ck_total - ck_fail, ck_total);
    return ck_fail ? 1 : 0;
}
#define CK_FMT(buf, ...) snprintf(buf, sizeof buf, __VA_ARGS__)
#endif
