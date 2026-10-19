# Problem bank, part A: Getting started, C basics, bits and bytes, pointers and memory.
# Each test program does  #include "solution.c"  (or .cpp) and then checks the user's code.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Getting started"

add(P("one", S, "Step one", "c", "func",
r"""<p>Every problem asks you to write some code. Your code is compiled together with a hidden
test program, which calls it and compares the answers with a reference solution. Click
<b>Submit</b> to compile and test.</p>
<p>Write <code>int one(void)</code> that returns <code>1</code>.</p>""",
r"""int one(void)
{
    // return 1 here
    return 0;
}
""",
r"""int one(void)
{
    return 1;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    ck_int("one()", one(), 1);
    return ck_done();
}
""",
"Change the 0 to a 1."))

add(P("hello", S, "Hello, world", "c", "stdout",
r"""<p>Some problems check what your program <em>prints</em>. Write a complete program whose
<code>main</code> prints exactly this line (with a newline at the end):</p>
<pre>Hello, world!</pre>""",
r"""#include <stdio.h>

int main(void)
{
    // print the line here
    return 0;
}
""",
r"""#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
""",
None,
"Use printf(\"...\\n\"). Capital H, comma, space, exclamation mark.",
expected="Hello, world!\n"))

add(P("squares", S, "A first loop", "c", "stdout",
r"""<p>Print the numbers 1 to 5 and their squares, one pair per line, separated by one space:</p>
<pre>1 1
2 4
3 9
4 16
5 25</pre>""",
r"""#include <stdio.h>

int main(void)
{
    return 0;
}
""",
r"""#include <stdio.h>

int main(void)
{
    for (int i = 1; i <= 5; i++)
        printf("%d %d\n", i, i * i);
    return 0;
}
""",
None,
"A for loop from 1 to 5 and printf(\"%d %d\\n\", i, i * i).",
expected="1 1\n2 4\n3 9\n4 16\n5 25\n"))

# ---------------------------------------------------------------------------
S = "C basics"

add(P("abs_diff", S, "Absolute difference", "c", "func",
r"""<p>Write <code>int abs_diff(int a, int b)</code> that returns |a &minus; b|.</p>
<p>Inputs stay between &minus;1,000,000 and 1,000,000.</p>
<pre>abs_diff(3, 10)  -> 7
abs_diff(-4, -9) -> 5</pre>""",
r"""int abs_diff(int a, int b)
{
    return 0;
}
""",
r"""int abs_diff(int a, int b)
{
    return a > b ? a - b : b - a;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int a, int b) { return a > b ? a - b : b - a; }
int main(void)
{
    char d[96];
    int fixed[][2] = {{3, 10}, {-4, -9}, {0, 0}, {5, 5}, {-1000000, 1000000}};
    for (int i = 0; i < 5; i++) {
        CK_FMT(d, "abs_diff(%d, %d)", fixed[i][0], fixed[i][1]);
        ck_int(d, abs_diff(fixed[i][0], fixed[i][1]), ref(fixed[i][0], fixed[i][1]));
    }
    for (int i = 0; i < 200; i++) {
        int a = ck_range(-1000000, 1000000), b = ck_range(-1000000, 1000000);
        CK_FMT(d, "abs_diff(%d, %d)", a, b);
        ck_int(d, abs_diff(a, b), ref(a, b));
    }
    return ck_done();
}
""",
"Subtract the smaller number from the larger one."))

add(P("clamp_int", S, "Clamp", "c", "func",
r"""<p>Write <code>int clamp_int(int x, int lo, int hi)</code>. It returns <code>lo</code> if
<code>x &lt; lo</code>, <code>hi</code> if <code>x &gt; hi</code>, and <code>x</code> otherwise.
You can assume <code>lo &lt;= hi</code>.</p>
<p>Clamping is everywhere in audio code: volume limits, array indices, sample values.</p>""",
r"""int clamp_int(int x, int lo, int hi)
{
    return x;
}
""",
r"""int clamp_int(int x, int lo, int hi)
{
    if (x < lo) return lo;
    if (x > hi) return hi;
    return x;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int x, int lo, int hi) { return x < lo ? lo : (x > hi ? hi : x); }
int main(void)
{
    char d[96];
    for (int i = 0; i < 300; i++) {
        int lo = ck_range(-100, 50), hi = lo + ck_range(0, 100), x = ck_range(-200, 200);
        CK_FMT(d, "clamp_int(%d, %d, %d)", x, lo, hi);
        ck_int(d, clamp_int(x, lo, hi), ref(x, lo, hi));
    }
    ck_int("clamp_int(7, 7, 7)", clamp_int(7, 7, 7), 7);
    return ck_done();
}
""",
"Two if statements are enough."))

add(P("sign_of", S, "Sign", "c", "func",
r"""<p>Write <code>int sign_of(int x)</code> that returns &minus;1 for negative numbers, 0 for zero
and 1 for positive numbers.</p>""",
r"""int sign_of(int x)
{
    return 0;
}
""",
r"""int sign_of(int x)
{
    return (x > 0) - (x < 0);
}
""",
r"""#include "check.h"
#include <limits.h>
#include "solution.c"
static int ref(int x) { return x > 0 ? 1 : (x < 0 ? -1 : 0); }
int main(void)
{
    char d[64];
    int v[] = {0, 1, -1, 5, -5, INT_MAX, INT_MIN, 123456, -98765};
    for (int i = 0; i < 9; i++) { CK_FMT(d, "sign_of(%d)", v[i]); ck_int(d, sign_of(v[i]), ref(v[i])); }
    return ck_done();
}
""",
"Comparisons in C give 0 or 1, so (x > 0) - (x < 0) works without any if."))

add(P("round_div", S, "Rounded division", "c", "func",
r"""<p>Integer division in C rounds towards zero: <code>7 / 2</code> is 3 and <code>-7 / 2</code> is
&minus;3. Write <code>int round_div(int a, int b)</code> that rounds to the <b>nearest</b> integer
instead, with halves rounded away from zero.</p>
<p><code>b</code> is always positive (1 to 1000) and <code>a</code> is between &minus;1,000,000 and
1,000,000.</p>
<pre>round_div(7, 2)  -> 4     (3.5 rounds up)
round_div(-7, 2) -> -4
round_div(5, 3)  -> 2     (1.67)
round_div(4, 3)  -> 1     (1.33)</pre>""",
r"""int round_div(int a, int b)
{
    return a / b;
}
""",
r"""int round_div(int a, int b)
{
    if (a >= 0)
        return (a + b / 2) / b;
    return -((-a + b / 2) / b);
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int a, int b)
{
    double q = (double)a / b;
    return q >= 0 ? (int)floor(q + 0.5) : -(int)floor(-q + 0.5);
}
int main(void)
{
    char d[96];
    int f[][2] = {{7, 2}, {-7, 2}, {5, 3}, {4, 3}, {0, 5}, {1, 2}, {-1, 2}, {6, 4}, {-6, 4}};
    for (int i = 0; i < 9; i++) {
        CK_FMT(d, "round_div(%d, %d)", f[i][0], f[i][1]);
        ck_int(d, round_div(f[i][0], f[i][1]), ref(f[i][0], f[i][1]));
    }
    for (int i = 0; i < 300; i++) {
        int a = ck_range(-1000000, 1000000), b = ck_range(1, 1000);
        CK_FMT(d, "round_div(%d, %d)", a, b);
        ck_int(d, round_div(a, b), ref(a, b));
    }
    return ck_done();
}
""",
"For a >= 0, adding b/2 before dividing turns truncation into rounding. Handle negative a by symmetry."))

add(P("swap_int", S, "Swap through pointers", "c", "func",
r"""<p>Write <code>void swap_int(int *a, int *b)</code> that swaps the two integers that
<code>a</code> and <code>b</code> point to.</p>
<p>C passes arguments by value, so a function can change the caller's variables only through
pointers.</p>""",
r"""void swap_int(int *a, int *b)
{
}
""",
r"""void swap_int(int *a, int *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    for (int i = 0; i < 50; i++) {
        int x = ck_range(-1000, 1000), y = ck_range(-1000, 1000), x0 = x, y0 = y;
        swap_int(&x, &y);
        CK_FMT(d, "after swap_int(&x, &y) with x=%d, y=%d: x", x0, y0); ck_int(d, x, y0);
        CK_FMT(d, "after swap_int(&x, &y) with x=%d, y=%d: y", x0, y0); ck_int(d, y, x0);
    }
    int z = 42; swap_int(&z, &z); ck_int("swap_int(&z, &z) with z=42", z, 42);
    return ck_done();
}
""",
"Use a temporary: t = *a; *a = *b; *b = t;"))

add(P("array_sum", S, "Sum of an array", "c", "func",
r"""<p>Write <code>long long array_sum(const int *x, int n)</code> that returns the sum of the
<code>n</code> numbers in <code>x</code>.</p>
<p>The values can be as large as 2,000,000,000, so the sum does not fit in an <code>int</code>.
On this site, signed overflow is caught and reported as a runtime error, so you will notice.</p>""",
r"""long long array_sum(const int *x, int n)
{
    int s = 0;
    for (int i = 0; i < n; i++)
        s += x[i];
    return s;
}
""",
r"""long long array_sum(const int *x, int n)
{
    long long s = 0;
    for (int i = 0; i < n; i++)
        s += x[i];
    return s;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static int x[1000];
    char d[96];
    int a[] = {1, 2, 3};
    ck_int("array_sum({1, 2, 3}, 3)", array_sum(a, 3), 6);
    ck_int("array_sum(x, 0)", array_sum(a, 0), 0);
    for (int t = 0; t < 5; t++) {
        int n = ck_range(1, 1000);
        long long want = 0;
        for (int i = 0; i < n; i++) { x[i] = ck_range(-2000000000, 2000000000); want += x[i]; }
        CK_FMT(d, "array_sum(random array of %d large values)", n);
        ck_int(d, array_sum(x, n), want);
    }
    return ck_done();
}
""",
"Make the accumulator a long long, not an int."))

add(P("argmax", S, "Index of the maximum", "c", "func",
r"""<p>Write <code>int argmax(const int *x, int n)</code> that returns the index of the largest
value. If the largest value appears more than once, return the <b>first</b> index.
<code>n</code> is at least 1.</p>
<pre>argmax({3, 9, 2, 9}, 4) -> 1</pre>""",
r"""int argmax(const int *x, int n)
{
    return 0;
}
""",
r"""int argmax(const int *x, int n)
{
    int best = 0;
    for (int i = 1; i < n; i++)
        if (x[i] > x[best])
            best = i;
    return best;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const int *x, int n) { int b = 0; for (int i = 1; i < n; i++) if (x[i] > x[b]) b = i; return b; }
int main(void)
{
    int a[] = {3, 9, 2, 9};
    ck_int("argmax({3, 9, 2, 9}, 4)", argmax(a, 4), 1);
    int neg[] = {-5, -2, -9};
    ck_int("argmax({-5, -2, -9}, 3)", argmax(neg, 3), 1);
    static int x[200];
    char d[96];
    for (int t = 0; t < 50; t++) {
        int n = ck_range(1, 200);
        for (int i = 0; i < n; i++) x[i] = ck_range(-20, 20);
        CK_FMT(d, "argmax(random array, n=%d)", n);
        ck_int(d, argmax(x, n), ref(x, n));
    }
    return ck_done();
}
""",
"Keep the index of the best value so far. Use > (not >=) so the first maximum wins."))

add(P("reverse", S, "Reverse in place", "c", "func",
r"""<p>Write <code>void reverse(int *x, int n)</code> that reverses the array in place, without a
second array.</p>
<pre>{1, 2, 3, 4, 5} -> {5, 4, 3, 2, 1}</pre>""",
r"""void reverse(int *x, int n)
{
}
""",
r"""void reverse(int *x, int n)
{
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        int t = x[i];
        x[i] = x[j];
        x[j] = t;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static int x[101], y[101];
    char d[96];
    for (int n = 0; n <= 101; n += (n < 6 ? 1 : 19)) {
        for (int i = 0; i < n; i++) x[i] = y[i] = ck_range(-99, 99);
        reverse(x, n);
        int ok = 1;
        for (int i = 0; i < n; i++) if (x[i] != y[n - 1 - i]) ok = 0;
        CK_FMT(d, "reverse(x, %d) gives the reversed array", n);
        ck_true(d, ok);
    }
    return ck_done();
}
""",
"Swap x[i] with x[n-1-i] while i < n-1-i."))

add(P("my_strlen", S, "String length", "c", "func",
r"""<p>A C string is an array of <code>char</code> that ends with a zero byte
(<code>'\0'</code>). Write <code>size_t my_strlen(const char *s)</code> that counts the
characters before the zero byte, without calling <code>strlen</code>.</p>""",
r"""#include <stddef.h>

size_t my_strlen(const char *s)
{
    return 0;
}
""",
r"""#include <stddef.h>

size_t my_strlen(const char *s)
{
    size_t n = 0;
    while (s[n] != '\0')
        n++;
    return n;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    const char *t[] = {"", "a", "hello", "Sony audio", "line\nbreak", "0123456789012345678901234567890123456789"};
    char d[96];
    for (int i = 0; i < 6; i++) {
        CK_FMT(d, "my_strlen(test string %d)", i);
        ck_int(d, (long long)my_strlen(t[i]), (long long)strlen(t[i]));
    }
    return ck_done();
}
""",
"Walk forward until you reach '\\0'."))

add(P("count_char", S, "Count a character", "c", "func",
r"""<p>Write <code>int count_char(const char *s, char c)</code> that returns how many times
<code>c</code> appears in the string <code>s</code>.</p>
<pre>count_char("banana", 'a') -> 3</pre>""",
r"""int count_char(const char *s, char c)
{
    return 0;
}
""",
r"""int count_char(const char *s, char c)
{
    int n = 0;
    for (; *s; s++)
        if (*s == c)
            n++;
    return n;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const char *s, char c) { int n = 0; for (; *s; s++) n += (*s == c); return n; }
int main(void)
{
    const char *t[] = {"banana", "", "aaaa", "mississippi", "C and C++"};
    const char c[] = {'a', 'a', 'a', 's', '+'};
    char d[96];
    for (int i = 0; i < 5; i++) {
        CK_FMT(d, "count_char(\"%s\", '%c')", t[i], c[i]);
        ck_int(d, count_char(t[i], c[i]), ref(t[i], c[i]));
    }
    return ck_done();
}
""",
"Loop until the zero byte and compare each character."))

add(P("to_upper", S, "Upper case", "c", "func",
r"""<p>Write <code>void to_upper(char *s)</code> that changes every lower-case ASCII letter
(<code>'a'</code> to <code>'z'</code>) in the string to upper case, in place. Leave every other
character unchanged. Do not use <code>toupper</code>.</p>""",
r"""void to_upper(char *s)
{
}
""",
r"""void to_upper(char *s)
{
    for (; *s; s++)
        if (*s >= 'a' && *s <= 'z')
            *s = (char)(*s - 'a' + 'A');
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    const char *in[] = {"hello", "Hello, World!", "", "abc-xyz_123", "ALREADY"};
    const char *out[] = {"HELLO", "HELLO, WORLD!", "", "ABC-XYZ_123", "ALREADY"};
    char buf[64], d[96];
    for (int i = 0; i < 5; i++) {
        strcpy(buf, in[i]);
        to_upper(buf);
        CK_FMT(d, "to_upper(\"%s\")", in[i]);
        ck_str(d, buf, out[i]);
    }
    return ck_done();
}
""",
"In ASCII, 'A' is 'a' - 32. Subtract 'a' and add 'A'."))

add(P("parse_int", S, "Parse an integer", "c", "func",
r"""<p>Write <code>int parse_int(const char *s)</code> that reads a whole number from the start of
a string:</p>
<ul><li>skip leading spaces;</li>
<li>accept one optional <code>+</code> or <code>-</code>;</li>
<li>read digits until the first non-digit;</li>
<li>if there are no digits, return 0.</li></ul>
<p>The value always fits in an <code>int</code>. Do not use <code>atoi</code> or
<code>strtol</code>.</p>
<pre>parse_int("  -42dB") -> -42
parse_int("+7")      -> 7
parse_int("abc")     -> 0</pre>""",
r"""int parse_int(const char *s)
{
    return 0;
}
""",
r"""int parse_int(const char *s)
{
    while (*s == ' ')
        s++;
    int neg = 0;
    if (*s == '+' || *s == '-') {
        neg = (*s == '-');
        s++;
    }
    int v = 0;
    while (*s >= '0' && *s <= '9') {
        v = v * 10 + (*s - '0');
        s++;
    }
    return neg ? -v : v;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    const char *in[] = {"  -42dB", "+7", "abc", "0", "123", "   ", "-0", "2147483647", "-2147483647", "12 34", "--5", "  +88x"};
    const int want[] = {-42, 7, 0, 0, 123, 0, 0, 2147483647, -2147483647, 12, 0, 88};
    char d[96];
    for (int i = 0; i < 12; i++) {
        CK_FMT(d, "parse_int(\"%s\")", in[i]);
        ck_int(d, parse_int(in[i]), want[i]);
    }
    return ck_done();
}
""",
"Build the value as v = v * 10 + digit. Apply the sign at the end. (Careful: building a negative value first and negating can overflow.)"))

add(P("dist2", S, "Structs: squared distance", "c", "func",
r"""<p>The starter code defines a struct for a 2-D point. Write
<code>long long dist2(Point a, Point b)</code> that returns the squared distance
(a.x &minus; b.x)&sup2; + (a.y &minus; b.y)&sup2;.</p>
<p>Coordinates go up to &plusmn;1,000,000, so the squares do not fit in an <code>int</code>.</p>""",
r"""typedef struct {
    int x;
    int y;
} Point;

long long dist2(Point a, Point b)
{
    return 0;
}
""",
r"""typedef struct {
    int x;
    int y;
} Point;

long long dist2(Point a, Point b)
{
    long long dx = (long long)a.x - b.x;
    long long dy = (long long)a.y - b.y;
    return dx * dx + dy * dy;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[128];
    Point p = {0, 0}, q = {3, 4};
    ck_int("dist2({0,0}, {3,4})", dist2(p, q), 25);
    for (int i = 0; i < 200; i++) {
        Point a = {ck_range(-1000000, 1000000), ck_range(-1000000, 1000000)};
        Point b = {ck_range(-1000000, 1000000), ck_range(-1000000, 1000000)};
        long long dx = (long long)a.x - b.x, dy = (long long)a.y - b.y;
        CK_FMT(d, "dist2({%d,%d}, {%d,%d})", a.x, a.y, b.x, b.y);
        ck_int(d, dist2(a, b), dx * dx + dy * dy);
    }
    return ck_done();
}
""",
"Convert to long long before subtracting and multiplying."))

# ---------------------------------------------------------------------------
S = "Bits and bytes"

add(P("bit_ops", S, "Set, clear, toggle, test", "c", "func",
r"""<p>Write four functions for bit <code>n</code> (0 to 31) of a 32-bit value:</p>
<pre>uint32_t set_bit(uint32_t x, int n);     // bit n becomes 1
uint32_t clear_bit(uint32_t x, int n);   // bit n becomes 0
uint32_t toggle_bit(uint32_t x, int n);  // bit n flips
int      test_bit(uint32_t x, int n);    // 1 if bit n is set, else 0</pre>
<p>These are the everyday operations on hardware registers.</p>""",
r"""#include <stdint.h>

uint32_t set_bit(uint32_t x, int n)    { return x; }
uint32_t clear_bit(uint32_t x, int n)  { return x; }
uint32_t toggle_bit(uint32_t x, int n) { return x; }
int      test_bit(uint32_t x, int n)   { return 0; }
""",
r"""#include <stdint.h>

uint32_t set_bit(uint32_t x, int n)    { return x | (1u << n); }
uint32_t clear_bit(uint32_t x, int n)  { return x & ~(1u << n); }
uint32_t toggle_bit(uint32_t x, int n) { return x ^ (1u << n); }
int      test_bit(uint32_t x, int n)   { return (int)((x >> n) & 1u); }
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    for (int i = 0; i < 64; i++) {
        uint32_t x = ck_rand();
        int n = i < 32 ? i : ck_range(0, 31);
        uint32_t m = (uint32_t)1 << n;
        CK_FMT(d, "set_bit(0x%08X, %d)", x, n);    ck_hex(d, set_bit(x, n), x | m);
        CK_FMT(d, "clear_bit(0x%08X, %d)", x, n);  ck_hex(d, clear_bit(x, n), x & ~m);
        CK_FMT(d, "toggle_bit(0x%08X, %d)", x, n); ck_hex(d, toggle_bit(x, n), x ^ m);
        CK_FMT(d, "test_bit(0x%08X, %d)", x, n);   ck_int(d, test_bit(x, n), (x & m) != 0);
    }
    return ck_done();
}
""",
"Use 1u << n, not 1 << n: shifting a signed 1 into bit 31 is undefined behaviour, and this site traps it."))

add(P("get_field", S, "Read a register field", "c", "func",
r"""<p>A hardware register packs several fields into one 32-bit word. Write
<code>uint32_t get_field(uint32_t reg, int pos, int width)</code> that returns the
<code>width</code>-bit field that starts at bit <code>pos</code>.</p>
<p><code>width</code> is 1 to 32 and <code>pos + width &lt;= 32</code>.</p>
<pre>get_field(0xABCD1234, 8, 8)  -> 0x12
get_field(0xABCD1234, 0, 32) -> 0xABCD1234</pre>""",
r"""#include <stdint.h>

uint32_t get_field(uint32_t reg, int pos, int width)
{
    return 0;
}
""",
r"""#include <stdint.h>

uint32_t get_field(uint32_t reg, int pos, int width)
{
    uint32_t v = reg >> pos;
    if (width == 32)
        return v;
    return v & ((1u << width) - 1u);
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref(uint32_t r, int p, int w) { return (uint32_t)(((uint64_t)r >> p) & ((((uint64_t)1) << w) - 1)); }
int main(void)
{
    char d[96];
    ck_hex("get_field(0xABCD1234, 8, 8)", get_field(0xABCD1234u, 8, 8), 0x12);
    ck_hex("get_field(0xABCD1234, 0, 32)", get_field(0xABCD1234u, 0, 32), 0xABCD1234u);
    ck_hex("get_field(0x80000000, 31, 1)", get_field(0x80000000u, 31, 1), 1);
    for (int i = 0; i < 300; i++) {
        uint32_t r = ck_rand();
        int w = ck_range(1, 32), p = ck_range(0, 32 - w);
        CK_FMT(d, "get_field(0x%08X, %d, %d)", r, p, w);
        ck_hex(d, get_field(r, p, w), ref(r, p, w));
    }
    return ck_done();
}
""",
"Shift right by pos, then mask with (1u << width) - 1. Careful: 1u << 32 is undefined, so width 32 needs its own case."))

add(P("set_field", S, "Write a register field", "c", "func",
r"""<p>Write <code>uint32_t set_field(uint32_t reg, int pos, int width, uint32_t value)</code>
that returns <code>reg</code> with its <code>width</code>-bit field at <code>pos</code>
replaced by the low <code>width</code> bits of <code>value</code>. All other bits stay as they
were. This is the classic <em>read-modify-write</em> of a register.</p>
<p><code>width</code> is 1 to 31 and <code>pos + width &lt;= 32</code>. <code>value</code> may
have extra high bits set; ignore them.</p>
<pre>set_field(0xFFFFFFFF, 4, 4, 0x0) -> 0xFFFFFF0F
set_field(0x00000000, 8, 4, 0x1F) -> 0x00000F00</pre>""",
r"""#include <stdint.h>

uint32_t set_field(uint32_t reg, int pos, int width, uint32_t value)
{
    return reg;
}
""",
r"""#include <stdint.h>

uint32_t set_field(uint32_t reg, int pos, int width, uint32_t value)
{
    uint32_t mask = ((1u << width) - 1u) << pos;
    return (reg & ~mask) | ((value << pos) & mask);
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref(uint32_t r, int p, int w, uint32_t v)
{
    uint32_t m = ((1u << w) - 1u) << p;
    return (r & ~m) | ((v << p) & m);
}
int main(void)
{
    char d[128];
    ck_hex("set_field(0xFFFFFFFF, 4, 4, 0x0)", set_field(0xFFFFFFFFu, 4, 4, 0), 0xFFFFFF0Fu);
    ck_hex("set_field(0x00000000, 8, 4, 0x1F)", set_field(0, 8, 4, 0x1F), 0xF00u);
    for (int i = 0; i < 300; i++) {
        uint32_t r = ck_rand(), v = ck_rand();
        int w = ck_range(1, 31), p = ck_range(0, 32 - w);
        CK_FMT(d, "set_field(0x%08X, %d, %d, 0x%X)", r, p, w, v);
        ck_hex(d, set_field(r, p, w, v), ref(r, p, w, v));
    }
    return ck_done();
}
""",
"Build mask = ((1u << width) - 1u) << pos. Clear the field with reg & ~mask, then OR in (value << pos) & mask."))

add(P("popcount", S, "Count the set bits", "c", "func",
r"""<p>Write <code>int popcount32(uint32_t x)</code> that returns how many bits of
<code>x</code> are 1. Try it without <code>__builtin_popcount</code>.</p>
<pre>popcount32(0xF0) -> 4</pre>""",
r"""#include <stdint.h>

int popcount32(uint32_t x)
{
    return 0;
}
""",
r"""#include <stdint.h>

int popcount32(uint32_t x)
{
    int n = 0;
    while (x) {
        x &= x - 1;   // clears the lowest set bit
        n++;
    }
    return n;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(uint32_t x) { int n = 0; for (int i = 0; i < 32; i++) n += (x >> i) & 1u; return n; }
int main(void)
{
    char d[64];
    uint32_t f[] = {0, 1, 0xF0, 0xFFFFFFFFu, 0x80000000u, 0x55555555u};
    for (int i = 0; i < 6; i++) { CK_FMT(d, "popcount32(0x%08X)", f[i]); ck_int(d, popcount32(f[i]), ref(f[i])); }
    for (int i = 0; i < 200; i++) { uint32_t x = ck_rand(); CK_FMT(d, "popcount32(0x%08X)", x); ck_int(d, popcount32(x), ref(x)); }
    return ck_done();
}
""",
"x & (x - 1) clears the lowest 1 bit. Count how many times you can do that before x is 0."))

add(P("is_pow2", S, "Power of two?", "c", "func",
r"""<p>Write <code>int is_pow2(uint32_t x)</code> that returns 1 if <code>x</code> is a power of
two (1, 2, 4, 8, ...) and 0 otherwise. Zero is not a power of two.</p>
<p>Buffer sizes are often powers of two, because then <code>i % N</code> becomes the much
cheaper <code>i &amp; (N - 1)</code>.</p>""",
r"""#include <stdint.h>

int is_pow2(uint32_t x)
{
    return 0;
}
""",
r"""#include <stdint.h>

int is_pow2(uint32_t x)
{
    return x != 0 && (x & (x - 1)) == 0;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(uint32_t x) { for (int i = 0; i < 32; i++) if (x == (1u << i)) return 1; return 0; }
int main(void)
{
    char d[64];
    uint32_t f[] = {0, 1, 2, 3, 4, 6, 1024, 1023, 0x80000000u, 0xFFFFFFFFu};
    for (int i = 0; i < 10; i++) { CK_FMT(d, "is_pow2(%u)", f[i]); ck_int(d, is_pow2(f[i]) != 0, ref(f[i])); }
    for (int i = 0; i < 200; i++) { uint32_t x = ck_rand() >> ck_range(0, 31); CK_FMT(d, "is_pow2(%u)", x); ck_int(d, is_pow2(x) != 0, ref(x)); }
    return ck_done();
}
""",
"A power of two has exactly one bit set, so x & (x - 1) is 0. Remember to exclude x == 0."))

add(P("bswap32", S, "Byte swap (endianness)", "c", "func",
r"""<p>Write <code>uint32_t bswap32(uint32_t x)</code> that reverses the order of the four bytes.
You need this when a device sends big-endian data to a little-endian CPU.</p>
<pre>bswap32(0x11223344) -> 0x44332211</pre>""",
r"""#include <stdint.h>

uint32_t bswap32(uint32_t x)
{
    return x;
}
""",
r"""#include <stdint.h>

uint32_t bswap32(uint32_t x)
{
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref(uint32_t x) { uint8_t b[4]; memcpy(b, &x, 4); uint8_t r[4] = {b[3], b[2], b[1], b[0]}; uint32_t y; memcpy(&y, r, 4); return y; }
int main(void)
{
    char d[64];
    ck_hex("bswap32(0x11223344)", bswap32(0x11223344u), 0x44332211u);
    for (int i = 0; i < 200; i++) { uint32_t x = ck_rand(); CK_FMT(d, "bswap32(0x%08X)", x); ck_hex(d, bswap32(x), ref(x)); }
    return ck_done();
}
""",
"Move each byte with shifts and masks, then OR the four pieces together."))

add(P("rotl32", S, "Rotate left", "c", "func",
r"""<p>Write <code>uint32_t rotl32(uint32_t x, int r)</code> that rotates <code>x</code> left by
<code>r</code> bits (0 to 31): bits that fall off the top come back in at the bottom.</p>
<pre>rotl32(0x80000001, 1) -> 0x00000003</pre>""",
r"""#include <stdint.h>

uint32_t rotl32(uint32_t x, int r)
{
    return x;
}
""",
r"""#include <stdint.h>

uint32_t rotl32(uint32_t x, int r)
{
    if (r == 0)
        return x;
    return (x << r) | (x >> (32 - r));
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref(uint32_t x, int r) { for (int i = 0; i < r; i++) x = (x << 1) | (x >> 31); return x; }
int main(void)
{
    char d[64];
    ck_hex("rotl32(0x80000001, 1)", rotl32(0x80000001u, 1), 3);
    ck_hex("rotl32(0x12345678, 0)", rotl32(0x12345678u, 0), 0x12345678u);
    for (int i = 0; i < 200; i++) { uint32_t x = ck_rand(); int r = ck_range(0, 31); CK_FMT(d, "rotl32(0x%08X, %d)", x, r); ck_hex(d, rotl32(x, r), ref(x, r)); }
    return ck_done();
}
""",
"(x << r) | (x >> (32 - r)). But for r = 0 that shifts by 32, which is undefined; handle it, or use (32 - r) & 31."))

add(P("sign_extend", S, "Sign-extend an ADC reading", "c", "func",
r"""<p>A 12-bit ADC sends two's-complement samples in the low 12 bits of a 32-bit word. To use
them you must <em>sign-extend</em>: copy the top bit of the field into all the higher bits.</p>
<p>Write <code>int32_t sign_extend(uint32_t x, int bits)</code> for any field width from 1 to 32.
Only the low <code>bits</code> bits of <code>x</code> are set.</p>
<pre>sign_extend(0x7FF, 12) -> 2047
sign_extend(0x800, 12) -> -2048
sign_extend(0xFFF, 12) -> -1</pre>""",
r"""#include <stdint.h>

int32_t sign_extend(uint32_t x, int bits)
{
    return (int32_t)x;
}
""",
r"""#include <stdint.h>

int32_t sign_extend(uint32_t x, int bits)
{
    if (bits == 32)
        return (int32_t)x;
    int64_t v = (int64_t)x;
    if (v & ((int64_t)1 << (bits - 1)))
        v -= (int64_t)1 << bits;
    return (int32_t)v;
}
""",
r"""#include "check.h"
#include "solution.c"
static int32_t ref(uint32_t x, int bits)
{
    int64_t v = (int64_t)x;
    if (v & ((int64_t)1 << (bits - 1))) v -= (int64_t)1 << bits;
    return (int32_t)v;
}
int main(void)
{
    char d[64];
    ck_int("sign_extend(0x7FF, 12)", sign_extend(0x7FF, 12), 2047);
    ck_int("sign_extend(0x800, 12)", sign_extend(0x800, 12), -2048);
    ck_int("sign_extend(0xFFF, 12)", sign_extend(0xFFF, 12), -1);
    ck_int("sign_extend(0x1, 1)", sign_extend(1, 1), -1);
    for (int i = 0; i < 300; i++) {
        int b = ck_range(1, 32);
        uint32_t x = b == 32 ? ck_rand() : ck_rand() & ((1u << b) - 1u);
        CK_FMT(d, "sign_extend(0x%X, %d)", x, b);
        ck_int(d, sign_extend(x, b), ref(x, b));
    }
    return ck_done();
}
""",
"If the field's top bit (bit bits-1) is set, subtract 2^bits. Do the arithmetic in int64_t to stay clear of overflow."))

add(P("reverse_bits8", S, "Reverse the bits of a byte", "c", "func",
r"""<p>Write <code>uint8_t reverse_bits8(uint8_t x)</code>: bit 0 goes to bit 7, bit 1 to bit 6,
and so on. (FFT code uses bit reversal to reorder its inputs.)</p>
<pre>reverse_bits8(0x01) -> 0x80
reverse_bits8(0xB0) -> 0x0D</pre>""",
r"""#include <stdint.h>

uint8_t reverse_bits8(uint8_t x)
{
    return x;
}
""",
r"""#include <stdint.h>

uint8_t reverse_bits8(uint8_t x)
{
    uint8_t r = 0;
    for (int i = 0; i < 8; i++)
        r = (uint8_t)((r << 1) | ((x >> i) & 1u));
    return r;
}
""",
r"""#include "check.h"
#include "solution.c"
static unsigned ref(unsigned x) { unsigned r = 0; for (int i = 0; i < 8; i++) if (x & (1u << i)) r |= 1u << (7 - i); return r; }
int main(void)
{
    char d[64];
    for (unsigned x = 0; x < 256; x++) { CK_FMT(d, "reverse_bits8(0x%02X)", x); ck_hex(d, reverse_bits8((uint8_t)x), ref(x)); }
    return ck_done();
}
""",
"Take the bits of x from the bottom one by one and push them into r from the right."))

add(P("next_pow2", S, "Next power of two", "c", "func",
r"""<p>Write <code>uint32_t next_pow2(uint32_t x)</code> that returns the smallest power of two
that is &ge; <code>x</code>, for <code>x</code> from 1 to 2<sup>31</sup>. Use it to choose an FFT
size or a ring-buffer size.</p>
<pre>next_pow2(1) -> 1    next_pow2(5) -> 8    next_pow2(1024) -> 1024</pre>""",
r"""#include <stdint.h>

uint32_t next_pow2(uint32_t x)
{
    return x;
}
""",
r"""#include <stdint.h>

uint32_t next_pow2(uint32_t x)
{
    x--;
    x |= x >> 1;
    x |= x >> 2;
    x |= x >> 4;
    x |= x >> 8;
    x |= x >> 16;
    return x + 1;
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref(uint32_t x) { uint64_t p = 1; while (p < x) p <<= 1; return (uint32_t)p; }
int main(void)
{
    char d[64];
    uint32_t f[] = {1, 2, 3, 5, 8, 1000, 1024, 1025, 0x80000000u, 0x40000001u};
    for (int i = 0; i < 10; i++) { CK_FMT(d, "next_pow2(%u)", f[i]); ck_int(d, next_pow2(f[i]), ref(f[i])); }
    for (int i = 0; i < 200; i++) { uint32_t x = (ck_rand() >> ck_range(1, 31)) + 1; CK_FMT(d, "next_pow2(%u)", x); ck_int(d, next_pow2(x), ref(x)); }
    return ck_done();
}
""",
"Simple way: start at 1 and double until >= x. Fast way: subtract 1, smear the top bit downwards with x |= x >> k, add 1."))

# ---------------------------------------------------------------------------
S = "Pointers and memory"

add(P("my_memcpy", S, "memcpy", "c", "func",
r"""<p>Write <code>void *my_memcpy(void *dst, const void *src, size_t n)</code> that copies
<code>n</code> bytes from <code>src</code> to <code>dst</code> and returns <code>dst</code>.
The two areas do not overlap.</p>""",
r"""#include <stddef.h>

void *my_memcpy(void *dst, const void *src, size_t n)
{
    return dst;
}
""",
r"""#include <stddef.h>

void *my_memcpy(void *dst, const void *src, size_t n)
{
    unsigned char *d = dst;
    const unsigned char *s = src;
    while (n--)
        *d++ = *s++;
    return dst;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    unsigned char a[300], b[300];
    char d[96];
    for (int t = 0; t < 20; t++) {
        size_t n = (size_t)ck_range(0, 256);
        for (int i = 0; i < 300; i++) { a[i] = (unsigned char)ck_rand(); b[i] = 0xEE; }
        void *r = my_memcpy(b + 8, a, n);
        CK_FMT(d, "my_memcpy returns dst (n=%zu)", n); ck_true(d, r == b + 8);
        CK_FMT(d, "bytes copied correctly (n=%zu)", n); ck_true(d, memcmp(b + 8, a, n) == 0);
        int ok = 1;
        for (int i = 0; i < 8; i++) if (b[i] != 0xEE) ok = 0;
        for (size_t i = 8 + n; i < 300; i++) if (b[i] != 0xEE) ok = 0;
        CK_FMT(d, "no bytes written outside dst[0..n) (n=%zu)", n); ck_true(d, ok);
    }
    return ck_done();
}
""",
"Cast both pointers to unsigned char * and copy one byte at a time."))

add(P("my_memmove", S, "memmove (overlap)", "c", "func",
r"""<p>Write <code>void *my_memmove(void *dst, const void *src, size_t n)</code>. It works like
memcpy, but the areas <b>may overlap</b>, as when you shift samples along inside one buffer.</p>
<p>Think about which direction to copy when <code>dst</code> is after <code>src</code>.</p>""",
r"""#include <stddef.h>

void *my_memmove(void *dst, const void *src, size_t n)
{
    return dst;
}
""",
r"""#include <stddef.h>

void *my_memmove(void *dst, const void *src, size_t n)
{
    unsigned char *d = dst;
    const unsigned char *s = src;
    if (d < s) {
        while (n--)
            *d++ = *s++;
    } else if (d > s) {
        d += n;
        s += n;
        while (n--)
            *--d = *--s;
    }
    return dst;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    unsigned char a[200], ref[200];
    char d[96];
    for (int t = 0; t < 40; t++) {
        for (int i = 0; i < 200; i++) a[i] = ref[i] = (unsigned char)ck_rand();
        int from = ck_range(0, 100), to = ck_range(0, 100), n = ck_range(0, 99);
        memmove(ref + to, ref + from, (size_t)n);
        void *r = my_memmove(a + to, a + from, (size_t)n);
        CK_FMT(d, "my_memmove(buf+%d, buf+%d, %d) returns dst", to, from, n); ck_true(d, r == a + to);
        CK_FMT(d, "my_memmove(buf+%d, buf+%d, %d) result", to, from, n); ck_true(d, memcmp(a, ref, 200) == 0);
    }
    return ck_done();
}
""",
"If dst is before src, copy forwards. If dst is after src, copy backwards from the end, so you never overwrite bytes you still need."))

add(P("find_negative", S, "Return a pointer", "c", "func",
r"""<p>Write <code>const int *find_first_negative(const int *x, int n)</code> that returns a
pointer to the first negative element, or <code>NULL</code> if there is none.</p>""",
r"""#include <stddef.h>

const int *find_first_negative(const int *x, int n)
{
    return NULL;
}
""",
r"""#include <stddef.h>

const int *find_first_negative(const int *x, int n)
{
    for (int i = 0; i < n; i++)
        if (x[i] < 0)
            return &x[i];
    return NULL;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    int x[50];
    char d[96];
    for (int t = 0; t < 40; t++) {
        int n = ck_range(0, 50), want = -1;
        for (int i = 0; i < n; i++) { x[i] = ck_range(-3, 30); if (want < 0 && x[i] < 0) want = i; }
        const int *p = find_first_negative(x, n);
        if (want < 0) { CK_FMT(d, "find_first_negative (n=%d, no negatives) returns NULL", n); ck_true(d, p == NULL); }
        else { CK_FMT(d, "find_first_negative (n=%d) points at index %d", n, want); ck_true(d, p == x + want); }
    }
    return ck_done();
}
""",
"Return &x[i] as soon as you find x[i] < 0."))

add(P("transpose", S, "2-D arrays: transpose", "c", "func",
r"""<p>A matrix with <code>rows</code> rows and <code>cols</code> columns is stored row by row in
a flat array, so element (r, c) is at <code>m[r * cols + c]</code>. Write</p>
<pre>void transpose(const int *in, int *out, int rows, int cols);</pre>
<p>so that <code>out</code> (cols rows by rows columns) holds the transpose: out(c, r) = in(r, c).</p>""",
r"""void transpose(const int *in, int *out, int rows, int cols)
{
}
""",
r"""void transpose(const int *in, int *out, int rows, int cols)
{
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            out[c * rows + r] = in[r * cols + c];
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static int in[400], out[400];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int R = ck_range(1, 20), C = ck_range(1, 20);
        for (int i = 0; i < R * C; i++) { in[i] = ck_range(-999, 999); out[i] = 12345; }
        transpose(in, out, R, C);
        int ok = 1;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) if (out[c * R + r] != in[r * C + c]) ok = 0;
        CK_FMT(d, "transpose of a %dx%d matrix", R, C); ck_true(d, ok);
    }
    return ck_done();
}
""",
"Element (r, c) of in goes to element (c, r) of out, and out has rows columns."))

add(P("linked_list", S, "Linked list", "c", "func",
r"""<p>The starter code defines a singly linked list node. Write two functions:</p>
<pre>int list_length(const struct Node *head);   // number of nodes
struct Node *list_reverse(struct Node *head); // reverse the links, return the new head</pre>
<p><code>list_reverse</code> must reuse the existing nodes (no <code>malloc</code>).</p>""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

int list_length(const struct Node *head)
{
    return 0;
}

struct Node *list_reverse(struct Node *head)
{
    return head;
}
""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

int list_length(const struct Node *head)
{
    int n = 0;
    for (; head; head = head->next)
        n++;
    return n;
}

struct Node *list_reverse(struct Node *head)
{
    struct Node *prev = NULL;
    while (head) {
        struct Node *next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    struct Node pool[40];
    char d[96];
    for (int n = 0; n <= 40; n += (n < 3 ? 1 : 9)) {
        for (int i = 0; i < n; i++) { pool[i].value = i * 7 - 3; pool[i].next = i + 1 < n ? &pool[i + 1] : NULL; }
        struct Node *h = n ? &pool[0] : NULL;
        CK_FMT(d, "list_length of a %d-node list", n); ck_int(d, list_length(h), n);
        struct Node *r = list_reverse(h);
        int ok = 1, k = n - 1;
        for (struct Node *p = r; p; p = p->next, k--) if (k < 0 || p != &pool[k]) { ok = 0; break; }
        if (k != -1) ok = 0;
        CK_FMT(d, "list_reverse of a %d-node list reuses the nodes in reverse order", n); ck_true(d, ok);
    }
    return ck_done();
}
""",
"Walk the list with three pointers: prev, current and next. Point current->next at prev, then move all three along."))

add(P("range_alloc", S, "malloc a buffer", "c", "func",
r"""<p>Write <code>int *range_alloc(int n)</code> that allocates an array of <code>n</code> ints
with <code>malloc</code>, fills it with 0, 1, ..., n&minus;1 and returns it. The caller frees it.
For <code>n == 0</code> you may return <code>NULL</code> or a valid pointer.</p>
<p>(In real-time audio code you allocate like this <em>once</em>, at start-up, never inside the
audio callback.)</p>""",
r"""#include <stdlib.h>

int *range_alloc(int n)
{
    return NULL;
}
""",
r"""#include <stdlib.h>

int *range_alloc(int n)
{
    int *p = malloc((size_t)n * sizeof *p);
    if (p == NULL)
        return NULL;
    for (int i = 0; i < n; i++)
        p[i] = i;
    return p;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    int sizes[] = {1, 2, 10, 1000, 100000};
    for (int t = 0; t < 5; t++) {
        int n = sizes[t];
        int *p = range_alloc(n);
        CK_FMT(d, "range_alloc(%d) returns a pointer", n); ck_true(d, p != NULL);
        if (p) {
            int ok = 1;
            for (int i = 0; i < n; i++) if (p[i] != i) { ok = 0; break; }
            CK_FMT(d, "range_alloc(%d) contents are 0..%d", n, n - 1); ck_true(d, ok);
            free(p);
        }
    }
    return ck_done();
}
""",
"malloc(n * sizeof(int)), check for NULL, then fill with a loop."))
