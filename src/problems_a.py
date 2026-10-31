# Problem bank, part A: Getting started, C basics, bits and bytes, pointers and memory.
# Each test program does  #include "solution.c"  (or .cpp) and then checks the user's code.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Getting started"

add(P("one", S, "Step one", "c", "func",
r"""<p><b>What to write.</b> A function <code>int one(void)</code> that returns the number
<code>1</code>. The word <code>void</code> inside the brackets means the function takes no inputs.</p>
<p><b>How this site works.</b> Every problem asks you to write some code in the editor. When you press
<b>Submit</b>, the site compiles your code together with a hidden test program. The test program calls
your function (usually many times, with different inputs) and compares each answer with the answer of a correct reference solution. If
every answer matches, the problem is solved. If one answer is wrong, you see which call failed, what
your code returned and what was expected.</p>
<h4>Picture</h4>
<pre>  your code (the editor)        hidden test program
  +--------------------+        +------------------------------+
  | int one(void)      | &lt;----- | calls one()                  |
  | {                  |        |                              |
  |     return ...;    | -----&gt; | receives your answer         |
  | }                  |        | compares it with 1           |
  +--------------------+        | reports PASS or FAIL         |
                                +------------------------------+</pre>
<h4>Example</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>one()</code></td><td><code>1</code></td></tr>
</table>
<h4>What to do</h4>
<ol>
<li>Look at the starter code. It returns <code>0</code>, which is wrong.</li>
<li>Change it so that it returns <code>1</code>.</li>
<li>Press <b>Submit</b> and read the result.</li>
</ol>""",
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
r"""<p><b>What to write.</b> A complete C program. Its <code>main</code> function must print
exactly this one line, followed by a newline:</p>
<pre>Hello, world!</pre>
<p><b>How this kind of problem works.</b> Here there is no hidden test that calls a function. The site
compiles your whole program, runs it, and compares everything it prints with the expected text. The
comparison is exact, so every character counts.</p>
<h4>The line, character by character</h4>
<pre>H e l l o ,   w o r l d !  \n
^         ^ ^           ^  ^
|         | |           |  +-- newline: ends the line
|         | |           +----- exclamation mark
|         | +----------------- one space
|         +------------------- comma
+----------------------------- capital H; every other letter is small</pre>
<h4>Things to watch out for</h4>
<ul>
<li>Inside a C string, the newline is written as the two characters <code>\n</code>.</li>
<li>Print nothing else: no extra spaces, no extra lines.</li>
<li><code>main</code> should end with <code>return 0;</code>, which tells the system that the program
finished without an error. The starter code already has it.</li>
</ul>""",
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
r"""<p><b>What to write.</b> A complete C program that prints the numbers 1 to 5. Next to each
number, print its square (the number multiplied by itself). Print one pair per line, with one space
between the two numbers.</p>
<p><b>Why it matters.</b> This is your first loop. Almost every problem on this site uses a loop like
this one.</p>
<h4>The output must be exactly</h4>
<pre>1 1
2 4
3 9
4 16
5 25</pre>
<h4>Where each line comes from</h4>
<table>
<tr><th>Number i</th><th>Square i &times; i</th><th>Printed line</th></tr>
<tr><td>1</td><td>1 &times; 1 = 1</td><td><code>1 1</code></td></tr>
<tr><td>2</td><td>2 &times; 2 = 4</td><td><code>2 4</code></td></tr>
<tr><td>3</td><td>3 &times; 3 = 9</td><td><code>3 9</code></td></tr>
<tr><td>4</td><td>4 &times; 4 = 16</td><td><code>4 16</code></td></tr>
<tr><td>5</td><td>5 &times; 5 = 25</td><td><code>5 25</code></td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>Every line, including the last one, ends with a newline <code>\n</code>.</li>
<li>Exactly one space between the two numbers, and no space at the end of a line.</li>
<li>In <code>printf</code>, <code>%d</code> is the place where an <code>int</code> value is printed.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Which variable changes from line to line? It goes 1, 2, 3, 4, 5.</li>
<li>Write one <code>printf</code> that prints one line for one value of that variable. Then repeat it
with a loop.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int abs_diff(int a, int b)</code>. It returns the
distance between the two numbers: |a &minus; b|. The bars mean "absolute value", so the answer is never
negative.</p>
<p><b>Why it matters.</b> Distances such as "how far is this sample from the target" or "how far apart
are two time stamps" are needed everywhere, and the order of the two inputs must not matter.</p>
<h4>Picture on the number line</h4>
<pre>  -9        -4             0           3                  10
   |---------|             |           |-------------------|
   distance = 5                         distance = 7</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>a &minus; b</th><th>You return</th></tr>
<tr><td><code>abs_diff(3, 10)</code></td><td>&minus;7</td><td>7</td></tr>
<tr><td><code>abs_diff(10, 3)</code></td><td>7</td><td>7</td></tr>
<tr><td><code>abs_diff(-4, -9)</code></td><td>5</td><td>5</td></tr>
<tr><td><code>abs_diff(5, 5)</code></td><td>0</td><td>0</td></tr>
<tr><td><code>abs_diff(-1000000, 1000000)</code></td><td>&minus;2,000,000</td><td>2,000,000</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>a</code> and <code>b</code> are each between &minus;1,000,000 and 1,000,000.</li>
<li>So the answer is at most 2,000,000. That fits easily in an <code>int</code>, whose largest value
is 2,147,483,647.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The distance is always "larger number minus smaller number". Which of the two is larger?</li>
<li>One comparison decides the order. Then one subtraction gives the answer.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int clamp_int(int x, int lo, int hi)</code>. It
keeps <code>x</code> inside the range from <code>lo</code> to <code>hi</code>:</p>
<ul>
<li>if <code>x</code> is below <code>lo</code>, return <code>lo</code>;</li>
<li>if <code>x</code> is above <code>hi</code>, return <code>hi</code>;</li>
<li>otherwise <code>x</code> is already inside the range, so return <code>x</code> unchanged.</li>
</ul>
<p><b>Why it matters.</b> "Clamping" (also called limiting or saturating) is everywhere in audio and
embedded code: a volume must stay between 0 and 100, an array index must stay inside the array, a sample
value must fit the range the hardware accepts.</p>
<h4>Picture on the number line (lo = 0, hi = 10)</h4>
<pre>    x = -5          x = 7           x = 15
      |               |               |
      v               v               v
  ----*----[==========*==========]----*----
           0                     10
      -5 is pulled     7 stays     15 is pulled
      up to 0          as 7        down to 10</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Where x is</th><th>You return</th></tr>
<tr><td><code>clamp_int(-5, 0, 10)</code></td><td>below the range</td><td>0</td></tr>
<tr><td><code>clamp_int(15, 0, 10)</code></td><td>above the range</td><td>10</td></tr>
<tr><td><code>clamp_int(7, 0, 10)</code></td><td>inside</td><td>7</td></tr>
<tr><td><code>clamp_int(10, 0, 10)</code></td><td>exactly on the edge (inside)</td><td>10</td></tr>
<tr><td><code>clamp_int(-50, -20, -10)</code></td><td>below a negative range</td><td>&minus;20</td></tr>
<tr><td><code>clamp_int(7, 7, 7)</code></td><td>range of one number</td><td>7</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li>You can assume <code>lo &lt;= hi</code>. They may be equal.</li>
<li><code>lo</code>, <code>hi</code> and <code>x</code> can be negative.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>There are three regions: below, inside and above. Check the two outside regions first.</li>
<li>If neither "below" nor "above" is true, what is left?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int sign_of(int x)</code> that tells you the
sign of <code>x</code>:</p>
<ul>
<li>return <code>-1</code> if <code>x</code> is negative;</li>
<li>return <code>0</code> if <code>x</code> is zero;</li>
<li>return <code>1</code> if <code>x</code> is positive.</li>
</ul>
<p><b>Why it matters.</b> Sign functions appear in control loops and in adaptive filters (the
"sign-error LMS" update uses only the sign of the error).</p>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>sign_of(5)</code></td><td>1</td></tr>
<tr><td><code>sign_of(-5)</code></td><td>&minus;1</td></tr>
<tr><td><code>sign_of(0)</code></td><td>0</td></tr>
<tr><td><code>sign_of(2147483647)</code> (the largest <code>int</code>, <code>INT_MAX</code>)</td><td>1</td></tr>
<tr><td><code>sign_of(-2147483648)</code> (the smallest <code>int</code>, <code>INT_MIN</code>)</td><td>&minus;1</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>The test uses the extreme values <code>INT_MAX</code> and <code>INT_MIN</code>.</li>
<li>Do not compute <code>-x</code> or <code>x / abs(x)</code>. For <code>INT_MIN</code>, the value
+2,147,483,648 does not fit in an <code>int</code>. That is "signed overflow", which is undefined
behaviour in C, and this site stops the program with a runtime error when it happens.</li>
<li>Comparing <code>x</code> with 0 is always safe.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>A chain of <code>if</code> statements that compare <code>x</code> with 0 is enough.</li>
<li>For a shorter version: in C, a comparison such as <code>(x &gt; 0)</code> is itself a number, 1 if
true and 0 if false. Which two comparisons could you combine with a subtraction?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int round_div(int a, int b)</code>. It divides
<code>a</code> by <code>b</code> and returns the answer rounded to the <b>nearest whole number</b>.</p>
<p><b>Why you need it.</b> When both numbers are <code>int</code>, C's <code>/</code> simply throws the
fraction away. So <code>7 / 2</code> gives 3, not 3.5 and not 4. This is called "rounding towards
zero". Your function must round properly instead.</p>
<h4>The rounding rule</h4>
<ul>
<li>Work out the exact answer, for example 7 &divide; 2 = 3.5.</li>
<li>Fraction part <b>below one half</b>: drop it. 1.33 becomes 1.</li>
<li>Fraction part <b>above one half</b>: go to the next whole number. 1.67 becomes 2.</li>
<li>Fraction part <b>exactly one half</b>: move <b>away from zero</b>. 3.5 becomes 4, and
&minus;3.5 becomes &minus;4.</li>
</ul>
<h4>Picture on the number line</h4>
<pre>  -4    -3.5    -3        0        3     3.5     4
   |&lt;-----*       |        |        |       *-----&gt;|
   -7/2 goes to -4                   7/2 goes to 4
   (a half always moves AWAY from 0, on both sides)</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Exact value</th><th>C's <code>a / b</code></th><th>You return</th></tr>
<tr><td><code>round_div(7, 2)</code></td><td>3.5</td><td>3</td><td>4</td></tr>
<tr><td><code>round_div(-7, 2)</code></td><td>&minus;3.5</td><td>&minus;3</td><td>&minus;4</td></tr>
<tr><td><code>round_div(5, 3)</code></td><td>1.67</td><td>1</td><td>2</td></tr>
<tr><td><code>round_div(4, 3)</code></td><td>1.33</td><td>1</td><td>1</td></tr>
<tr><td><code>round_div(-5, 3)</code></td><td>&minus;1.67</td><td>&minus;1</td><td>&minus;2</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>b</code> is always positive: 1 to 1000.</li>
<li><code>a</code> is between &minus;1,000,000 and 1,000,000, so adding <code>b</code> to it can never
overflow an <code>int</code>.</li>
<li>You do not need floating point. Integer arithmetic is enough.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Solve the case <code>a &ge; 0</code> first. Suppose you add something to <code>a</code> before
dividing. How much would you have to add so that 3.5 lands on 4 but 3.4 stays at 3?</li>
<li>For a negative <code>a</code>, use the mirror image: rounding &minus;3.5 is the same as rounding
3.5 and putting the minus sign back.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>void swap_int(int *a, int *b)</code>.
<code>a</code> and <code>b</code> are <em>pointers</em>: they hold the addresses of two
<code>int</code> variables that belong to the caller. Your function must exchange the values of those
two variables.</p>
<p><b>Why it matters.</b> C passes every argument <em>by value</em>: the function receives a copy. If
you passed the two ints themselves, you would only swap the copies, and the caller would see no change.
Passing their addresses lets the function reach the caller's own variables. This is the standard
interview question about pointers.</p>
<h4>Picture (the caller wrote <code>swap_int(&amp;x, &amp;y)</code>)</h4>
<pre>  caller's variables              inside swap_int
  +--------+                      +--------+
  | x:  3  | &lt;------------------- | a: &amp;x  |   *a is x
  +--------+                      +--------+
  +--------+                      +--------+
  | y:  8  | &lt;------------------- | b: &amp;y  |   *b is y
  +--------+                      +--------+

  after the call:   x = 8,  y = 3</pre>
<h4>Facts you need</h4>
<ul>
<li><code>*a</code> reads the value that <code>a</code> points to.</li>
<li><code>*a = 5;</code> writes 5 into the variable that <code>a</code> points to.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>Before the call</th><th>Call</th><th>After the call</th></tr>
<tr><td><code>x = 3, y = 8</code></td><td><code>swap_int(&amp;x, &amp;y)</code></td><td><code>x = 8, y = 3</code></td></tr>
<tr><td><code>x = -7, y = 0</code></td><td><code>swap_int(&amp;x, &amp;y)</code></td><td><code>x = 0, y = -7</code></td></tr>
<tr><td><code>z = 42</code></td><td><code>swap_int(&amp;z, &amp;z)</code></td><td><code>z = 42</code> (unchanged)</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>The test also calls the function with the <b>same</b> address twice, as in the last example. The
value must stay the same. The well-known "XOR swap" trick without a temporary variable fails here: it
turns the value into 0.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Think of two cups of water. To exchange them you need a third, empty cup.</li>
<li>Once you overwrite <code>*a</code>, its old value is gone. Where must you keep it first?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>long long array_sum(const int *x, int n)</code>. It
adds up the <code>n</code> numbers <code>x[0]</code>, <code>x[1]</code>, &hellip;,
<code>x[n-1]</code> and returns the total.</p>
<p><b>Why it matters.</b> The starter code looks correct, but it has a classic bug: the running total is
an <code>int</code>, and the total can be far too big for an <code>int</code>. Choosing a wide enough
type for an accumulator is a basic skill in DSP code (think of summing many audio samples).</p>
<h4>Facts you need</h4>
<table>
<tr><th>Type</th><th>Size on this site</th><th>Range</th></tr>
<tr><td><code>int</code></td><td>4 bytes</td><td>&minus;2,147,483,648 to 2,147,483,647 (about &plusmn;2.1 billion)</td></tr>
<tr><td><code>long long</code></td><td>8 bytes</td><td>about &plusmn;9.2 &times; 10<sup>18</sup></td></tr>
</table>
<p>Going past the range of a signed type is called <em>signed overflow</em>. In C it is undefined
behaviour. On this site it is caught: the program stops with a runtime error, so you will see it.</p>
<h4>Examples</h4>
<table>
<tr><th>Array</th><th><code>n</code></th><th>You return</th><th>Note</th></tr>
<tr><td><code>{1, 2, 3}</code></td><td>3</td><td>6</td><td></td></tr>
<tr><td>any array</td><td>0</td><td>0</td><td>no numbers: the sum is 0</td></tr>
<tr><td><code>{2000000000, 2000000000}</code></td><td>2</td><td>4,000,000,000</td><td>too big for an <code>int</code></td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>n</code> is 0 to 1000.</li>
<li>Each value is between &minus;2,000,000,000 and 2,000,000,000. One value fits in an
<code>int</code>; the sum of two may not.</li>
<li>The largest possible total, 1000 &times; 2,000,000,000 = 2 &times; 10<sup>12</sup>, fits easily in a
<code>long long</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Which variable in the starter code holds the running total? What is its type?</li>
<li>Each <code>x[i]</code> is an <code>int</code>. If the total is a <code>long long</code>, C converts
<code>x[i]</code> to <code>long long</code> before adding, so the addition happens in the wide type.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int argmax(const int *x, int n)</code>. It returns
the <b>index</b> (the position, counting from 0) of the largest value in the array, not the value itself.
If the largest value appears more than once, return the <b>first</b> (smallest) index.</p>
<p><b>Why it matters.</b> "Where is the peak?" is a common DSP question: the loudest frequency bin of an
FFT, the strongest correlation lag, the best score in a list.</p>
<h4>Picture</h4>
<pre>  index:    0    1    2    3
         +----+----+----+----+
  x:     |  3 |  9 |  2 |  9 |
         +----+----+----+----+
                 ^         ^
                 |         +-- also 9, but it comes later
                 +------------ first largest value: return 1</pre>
<h4>Examples</h4>
<table>
<tr><th>Array</th><th>Largest value</th><th>You return</th></tr>
<tr><td><code>{3, 9, 2, 9}</code></td><td>9</td><td>1</td></tr>
<tr><td><code>{-5, -2, -9}</code></td><td>&minus;2</td><td>1</td></tr>
<tr><td><code>{7}</code></td><td>7</td><td>0</td></tr>
<tr><td><code>{4, 4, 4}</code></td><td>4</td><td>0</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>n</code> is at least 1, so there is always an answer.</li>
<li>Values can be negative. Starting your "best so far" at 0 would be wrong for
<code>{-5, -2, -9}</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Walk through the array once. Remember the index of the best value you have seen so far. A safe
starting choice is index 0.</li>
<li>When you meet a value equal to the best so far, should you move to it or stay? Which comparison,
<code>&gt;</code> or <code>&gt;=</code>, gives the first index?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>void reverse(int *x, int n)</code>. It reverses the
order of the <code>n</code> numbers in the array <b>in place</b>: you change the array you were given and
do not use a second array.</p>
<p><b>Why it matters.</b> In-place algorithms save memory, which matters on small embedded chips. This
is also a frequent first interview question about arrays.</p>
<h4>Picture: swap pairs from the outside in</h4>
<pre>  index:   0   1   2   3   4
  start:  [1] [2] [3] [4] [5]
           ^               ^      swap x[0] and x[4]
  step 1: [5] [2] [3] [4] [1]
               ^       ^          swap x[1] and x[3]
  step 2: [5] [4] [3] [2] [1]
                   ^              the middle one stays: done</pre>
<h4>Examples</h4>
<table>
<tr><th>Before</th><th><code>n</code></th><th>After</th></tr>
<tr><td><code>{1, 2, 3, 4, 5}</code></td><td>5 (odd)</td><td><code>{5, 4, 3, 2, 1}</code></td></tr>
<tr><td><code>{10, 20, 30, 40}</code></td><td>4 (even)</td><td><code>{40, 30, 20, 10}</code></td></tr>
<tr><td><code>{7}</code></td><td>1</td><td><code>{7}</code></td></tr>
<tr><td><code>{}</code></td><td>0</td><td>nothing to do</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>The test uses <code>n</code> from 0 up to 101, both even and odd.</li>
<li>If you keep swapping after you pass the middle, you swap every pair a second time and the array
comes back to its original order.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Use two positions: one starting at the left end, one at the right end.</li>
<li>Swap the two values, then move both positions one step towards the middle.</li>
<li>When must you stop? Think about the odd case (they meet) and the even case (they cross).</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>size_t my_strlen(const char *s)</code> that
returns the length of the string <code>s</code>: the number of characters before the end marker. Do not
call the library function <code>strlen</code>.</p>
<p><b>How C stores a string.</b> A C string is an array of <code>char</code>. After the last real
character there is one extra byte with the value 0, written <code>'\0'</code> (the "null byte" or
"terminator"). Nothing else tells you where the string ends, so you must walk along until you find
it.</p>
<h4>Picture of <code>"hello"</code> in memory</h4>
<pre>  index:    0     1     2     3     4     5
         +-----+-----+-----+-----+-----+-----+
  s:     | 'h' | 'e' | 'l' | 'l' | 'o' | \0  |
         +-----+-----+-----+-----+-----+-----+
          \___________________________/   ^
               5 characters: return 5     the terminator is NOT counted</pre>
<h4>Examples</h4>
<table>
<tr><th>String</th><th>You return</th><th>Note</th></tr>
<tr><td><code>"hello"</code></td><td>5</td><td></td></tr>
<tr><td><code>""</code></td><td>0</td><td>empty string: the first byte is already <code>'\0'</code></td></tr>
<tr><td><code>"Sony audio"</code></td><td>10</td><td>the space is a character too</td></tr>
<tr><td><code>"line\nbreak"</code></td><td>10</td><td><code>\n</code> is ONE character (a newline)</td></tr>
</table>
<h4>Facts you need</h4>
<ul>
<li><code>size_t</code> is an unsigned integer type used for sizes and lengths. On this site it is 4
bytes.</li>
<li><code>s[i]</code> is the character at position <code>i</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep a counter that starts at 0.</li>
<li>Look at the character at the counter's position. If it is not the terminator, count it and move
on. What should happen when it is the terminator?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int count_char(const char *s, char c)</code>. It
returns how many times the character <code>c</code> appears in the string <code>s</code>.</p>
<p><b>Why it matters.</b> Counting characters is the first step of many text tasks: counting commas to
split a CSV line, counting spaces to count words, checking a protocol message.</p>
<h4>Picture: <code>count_char("banana", 'a')</code></h4>
<pre>  index:    0     1     2     3     4     5     6
         +-----+-----+-----+-----+-----+-----+-----+
  s:     | 'b' | 'a' | 'n' | 'a' | 'n' | 'a' | \0  |
         +-----+-----+-----+-----+-----+-----+-----+
  match?   no   YES    no   YES    no   YES   stop
  count:    0     1     1     2     2     3   return 3</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>count_char("banana", 'a')</code></td><td>3</td></tr>
<tr><td><code>count_char("mississippi", 's')</code></td><td>4</td></tr>
<tr><td><code>count_char("C and C++", '+')</code></td><td>2</td></tr>
<tr><td><code>count_char("aaaa", 'a')</code></td><td>4</td></tr>
<tr><td><code>count_char("", 'a')</code></td><td>0 (empty string)</td></tr>
</table>
<h4>Facts you need</h4>
<ul>
<li>A C string ends with the byte <code>'\0'</code> (value 0). Stop there; do not count it.</li>
<li>Characters are compared with <code>==</code>, like numbers. Upper and lower case are different
characters: <code>'A'</code> is not <code>'a'</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Walk through the string one character at a time until you reach the terminator.</li>
<li>At each character ask one question: is it equal to <code>c</code>? If yes, add 1 to a counter.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>void to_upper(char *s)</code>. It changes every
lower-case letter <code>'a'</code> to <code>'z'</code> in the string into the matching capital letter.
It works <b>in place</b>: you change the characters of <code>s</code> directly and return nothing.
Every other character (capitals, digits, spaces, punctuation) stays as it is. Do not use the library
function <code>toupper</code>.</p>
<h4>Facts you need: ASCII codes</h4>
<p>Every character is stored as a number, its ASCII code. The letters are in order, so you can do
arithmetic on them.</p>
<table>
<tr><th>Characters</th><th>Codes</th></tr>
<tr><td><code>'A'</code> &hellip; <code>'Z'</code></td><td>65 &hellip; 90</td></tr>
<tr><td><code>'a'</code> &hellip; <code>'z'</code></td><td>97 &hellip; 122</td></tr>
<tr><td><code>'0'</code> &hellip; <code>'9'</code></td><td>48 &hellip; 57</td></tr>
<tr><td>space</td><td>32</td></tr>
</table>
<pre>  'a' = 97  --- minus 32 ---&gt;  'A' = 65
  'h' = 104 --- minus 32 ---&gt;  'H' = 72
  every small letter is exactly 32 above its capital</pre>
<p>In C you can write <code>'a'</code> instead of 97, so you do not need to remember the numbers. For
example, <code>'h' - 'a'</code> is 7: the letter's position in the alphabet, counting from 0.</p>
<h4>Examples</h4>
<table>
<tr><th>Before</th><th>After</th></tr>
<tr><td><code>"hello"</code></td><td><code>"HELLO"</code></td></tr>
<tr><td><code>"Hello, World!"</code></td><td><code>"HELLO, WORLD!"</code></td></tr>
<tr><td><code>"abc-xyz_123"</code></td><td><code>"ABC-XYZ_123"</code> (the <code>-</code>, <code>_</code>
and digits do not change)</td></tr>
<tr><td><code>"ALREADY"</code></td><td><code>"ALREADY"</code></td></tr>
<tr><td><code>""</code></td><td><code>""</code></td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Walk through the string until the <code>'\0'</code> at the end.</li>
<li>For each character, first ask: is it between <code>'a'</code> and <code>'z'</code>? Only then change
it.</li>
<li>How do you turn a letter's position in the alphabet back into a capital letter?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int parse_int(const char *s)</code>. It reads a
whole number written as text at the start of the string and returns its value. For example the text
<code>"-42"</code> becomes the number &minus;42. Do not use <code>atoi</code>, <code>strtol</code> or
<code>sscanf</code>.</p>
<p><b>Why it matters.</b> Text arrives from a serial port, a file or a command line. Turning characters
into numbers is a classic embedded and interview task.</p>
<h4>The rule, step by step</h4>
<ol>
<li>Skip any space characters (<code>' '</code>) at the start. Only spaces need to be skipped.</li>
<li>Then there may be <b>one</b> sign: <code>'+'</code> or <code>'-'</code>. It is optional.</li>
<li>Then read digits <code>'0'</code>&hellip;<code>'9'</code>. Stop at the first character that is not a
digit (a letter, a space, <code>'\0'</code>, anything).</li>
<li>If there were no digits at all, the answer is 0.</li>
<li>Apply the sign.</li>
</ol>
<h4>Facts you need</h4>
<ul>
<li>The digits have the ASCII codes 48 (<code>'0'</code>) to 57 (<code>'9'</code>), in order. So
<code>c - '0'</code> turns the character <code>c</code> into its digit value: <code>'7' - '0'</code> is 7.</li>
<li>Reading digits from left to right, each new digit means "multiply what you have by 10, then add the
new digit":</li>
</ul>
<pre>  text "305"     value so far
  read '3'   -&gt;  0 * 10 + 3 =   3
  read '0'   -&gt;  3 * 10 + 0 =  30
  read '5'   -&gt; 30 * 10 + 5 = 305</pre>
<h4>Picture: <code>parse_int("  -42dB")</code></h4>
<pre>  ' '  ' '  '-'  '4'  '2'  'd'  'B'  '\0'
  skip skip sign digit digit stop
                 \________/
                  value 42, sign minus: return -42</pre>
<h4>Examples (these are the test's fixed cases)</h4>
<table>
<tr><th>Text</th><th>You return</th><th>Why</th></tr>
<tr><td><code>"  -42dB"</code></td><td>&minus;42</td><td>spaces skipped, stop at <code>d</code></td></tr>
<tr><td><code>"+7"</code></td><td>7</td><td>a plus sign is allowed</td></tr>
<tr><td><code>"123"</code></td><td>123</td><td></td></tr>
<tr><td><code>"0"</code> and <code>"-0"</code></td><td>0</td><td></td></tr>
<tr><td><code>"12 34"</code></td><td>12</td><td>stop at the space after 12</td></tr>
<tr><td><code>"  +88x"</code></td><td>88</td><td></td></tr>
<tr><td><code>"abc"</code></td><td>0</td><td>no digits</td></tr>
<tr><td><code>"   "</code></td><td>0</td><td>only spaces, no digits</td></tr>
<tr><td><code>"--5"</code></td><td>0</td><td>only ONE sign is allowed; the second <code>-</code> is not a digit</td></tr>
<tr><td><code>"2147483647"</code></td><td>2147483647</td><td>the largest <code>int</code></td></tr>
<tr><td><code>"-2147483647"</code></td><td>&minus;2147483647</td><td></td></tr>
</table>
<h4>Limits</h4>
<ul>
<li>The value always fits in an <code>int</code> (&minus;2,147,483,647 to 2,147,483,647 in the
tests).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Move a pointer (or an index) along the string. Each step of the rule above moves it forward.</li>
<li>Remember the sign in a separate variable. Build the value as a positive number.</li>
<li>Apply the sign only once, at the end. If you build a negative number digit by digit instead, the
in-between steps behave differently and are harder to get right.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> The starter code defines a <code>struct</code> called
<code>Point</code> with two <code>int</code> fields, <code>x</code> and <code>y</code>. Write
<code>long long dist2(Point a, Point b)</code> that returns the <b>squared</b> distance between the two
points:</p>
<pre>  dist2 = (a.x - b.x)^2 + (a.y - b.y)^2</pre>
<p>("^2" means "multiplied by itself".) There is no square root: the squared distance is enough to
compare which of two points is nearer, and it stays a whole number.</p>
<p><b>Why it matters.</b> Nearest-point searches, k-means clustering and constellation decoding in
modems all compare squared distances. A <code>struct</code> groups related values, and you read a
field with a dot: <code>a.x</code>.</p>
<h4>Picture: from (0, 0) to (3, 4)</h4>
<pre>  y
  4 |        * b = (3, 4)
  3 |       /|
  2 |      / |  dy = 4
  1 |     /  |
  0 *-----+--+-- x        dx = 3
    a = (0, 0)
    dist2 = 3*3 + 4*4 = 9 + 16 = 25   (the real distance is 5)</pre>
<h4>Examples</h4>
<table>
<tr><th>a</th><th>b</th><th>dx, dy</th><th>You return</th></tr>
<tr><td>(0, 0)</td><td>(3, 4)</td><td>&minus;3, &minus;4</td><td>25</td></tr>
<tr><td>(5, 5)</td><td>(5, 5)</td><td>0, 0</td><td>0</td></tr>
<tr><td>(&minus;1000000, &minus;1000000)</td><td>(1000000, 1000000)</td><td>&minus;2000000, &minus;2000000</td>
<td>8,000,000,000,000</td></tr>
</table>
<h4>Limits and the trap</h4>
<ul>
<li>Each coordinate is between &minus;1,000,000 and 1,000,000.</li>
<li>A difference can be up to 2,000,000. Its square is 4 &times; 10<sup>12</sup>, far above the largest
<code>int</code> (2,147,483,647). In C, <code>int * int</code> is computed as an <code>int</code>, even if
you store the result in a <code>long long</code> afterwards. The overflow happens first. On this site
that stops the program with a runtime error.</li>
<li>A <code>long long</code> (8 bytes, up to about 9.2 &times; 10<sup>18</sup>) holds the answer
easily.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The type of the <em>operands</em> decides the type of the arithmetic, not the type of the variable
you store into.</li>
<li>So at what point must the values become <code>long long</code>: before or after the
multiplication? (Converting before the subtraction is the safest habit.)</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> Four small functions. Each works on bit number <code>n</code>
(0 to 31) of a 32-bit unsigned value <code>x</code> and returns the result:</p>
<pre>uint32_t set_bit(uint32_t x, int n);     // bit n becomes 1
uint32_t clear_bit(uint32_t x, int n);   // bit n becomes 0
uint32_t toggle_bit(uint32_t x, int n);  // bit n flips: 0-&gt;1, 1-&gt;0
int      test_bit(uint32_t x, int n);    // returns 1 if bit n is 1, else 0</pre>
<p>All other bits must stay exactly as they were.</p>
<p><b>Why it matters.</b> Microcontroller registers control hardware one bit at a time: "bit 5 turns
the LED on", "bit 0 enables the timer". These four operations are the everyday tools of embedded
C, and they are asked in almost every embedded interview.</p>
<h4>Facts you need</h4>
<table>
<tr><th>Operator</th><th>Meaning, bit by bit</th></tr>
<tr><td><code>a | b</code> (OR)</td><td>1 if either bit is 1</td></tr>
<tr><td><code>a &amp; b</code> (AND)</td><td>1 only if both bits are 1</td></tr>
<tr><td><code>a ^ b</code> (XOR)</td><td>1 if the two bits are different</td></tr>
<tr><td><code>~a</code> (NOT)</td><td>flips every bit</td></tr>
<tr><td><code>a &lt;&lt; k</code>, <code>a &gt;&gt; k</code></td><td>move all bits k places left (towards
bit 31) or right (towards bit 0)</td></tr>
</table>
<p>A <em>mask</em> is a value with a 1 only in the bit you care about. The mask for bit <code>n</code>
is <code>1u &lt;&lt; n</code>. Bit 0 is the lowest (rightmost) bit.</p>
<pre>  bit number:   7 6 5 4 3 2 1 0
  1u &lt;&lt; 0   =   0 0 0 0 0 0 0 1   = 0x01
  1u &lt;&lt; 5   =   0 0 1 0 0 0 0 0   = 0x20
  x = 0xF0  =   1 1 1 1 0 0 0 0   (bits 8..31 are 0)</pre>
<h4>Examples with x = 0xF0</h4>
<table>
<tr><th>Call</th><th>Bits 7..0 after</th><th>Result</th></tr>
<tr><td><code>set_bit(0xF0, 0)</code></td><td>1111 0001</td><td>0xF1</td></tr>
<tr><td><code>set_bit(0xF0, 4)</code></td><td>1111 0000 (already 1)</td><td>0xF0</td></tr>
<tr><td><code>clear_bit(0xF0, 4)</code></td><td>1110 0000</td><td>0xE0</td></tr>
<tr><td><code>toggle_bit(0xF0, 7)</code></td><td>0111 0000</td><td>0x70</td></tr>
<tr><td><code>test_bit(0xF0, 5)</code></td><td>(unchanged)</td><td>1</td></tr>
<tr><td><code>test_bit(0xF0, 3)</code></td><td>(unchanged)</td><td>0</td></tr>
<tr><td><code>set_bit(0, 31)</code></td><td>only the top bit</td><td>0x80000000</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>The test tries every bit from 0 to 31, including bit 31.</li>
<li>Write the 1 as <code>1u</code> (unsigned). <code>1 &lt;&lt; 31</code> with a signed 1 pushes a 1 into
the sign bit, which is undefined behaviour in C. This site stops the program when that happens.</li>
<li><code>test_bit</code> must return exactly 0 or 1, not 32 or 0x80000000.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Build the mask for bit <code>n</code> first. Then ask, for each function: which operator with the
mask forces the bit to 1? Which flips it? Which keeps all bits except that one?</li>
<li>For <code>test_bit</code>: how can you move bit <code>n</code> down to position 0, and then throw
away all the other bits?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>uint32_t get_field(uint32_t reg, int pos, int width)</code>.
A hardware register packs several small numbers ("fields") into one 32-bit word. Your function returns
the field that is <code>width</code> bits wide and whose lowest bit is bit <code>pos</code>. The result
is moved down so that the field's lowest bit becomes bit 0.</p>
<p><b>Why it matters.</b> Datasheets describe registers like "bits 15:8 = GAIN". Reading such a field
is one of the most common lines of driver code.</p>
<h4>Picture: <code>get_field(0xABCD1234, 8, 8)</code></h4>
<pre>  bits:    31..28 27..24 23..20 19..16 15..12  11..8   7..4   3..0
  hex:        A      B      C      D      1      2      3      4
                                       \____________/
                                       pos = 8, width = 8
                                       bits 15..8 = 0x12

  step 1: shift right by pos=8   0xABCD1234 &gt;&gt; 8 = 0x00ABCD12
  step 2: keep the low 8 bits    0x00ABCD12 &amp; 0xFF = 0x12</pre>
<p>Each hex digit is exactly 4 bits, so a field that starts on a multiple of 4 can be read straight
from the hex digits.</p>
<h4>Facts you need</h4>
<ul>
<li>A mask of <code>w</code> ones in the low bits is 2<sup>w</sup> &minus; 1. For w = 8 that is 255 =
0xFF; for w = 12 it is 4095 = 0xFFF.</li>
<li>In C, shifting a 32-bit value by 32 or more places is undefined behaviour. So
<code>1u &lt;&lt; 32</code> is not allowed, and this site traps it.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Bits taken</th><th>You return</th></tr>
<tr><td><code>get_field(0xABCD1234, 8, 8)</code></td><td>15..8</td><td>0x12</td></tr>
<tr><td><code>get_field(0xABCD1234, 28, 4)</code></td><td>31..28</td><td>0xA</td></tr>
<tr><td><code>get_field(0xABCD1234, 4, 12)</code></td><td>15..4</td><td>0x123</td></tr>
<tr><td><code>get_field(0x80000000, 31, 1)</code></td><td>31 only</td><td>0x1</td></tr>
<tr><td><code>get_field(0xABCD1234, 0, 32)</code></td><td>all 32 bits</td><td>0xABCD1234</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>width</code> is 1 to 32, and <code>pos + width &lt;= 32</code>, so the field always fits inside
the word.</li>
<li><code>width</code> = 32 (with <code>pos</code> = 0) is tested. That is the case where the usual mask
formula needs a shift by 32.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Two steps: move the field down to bit 0, then remove everything above it.</li>
<li>How do you build a mask of <code>width</code> ones? For which <code>width</code> does that recipe
break, and what should the answer be in that case?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function
<code>uint32_t set_field(uint32_t reg, int pos, int width, uint32_t value)</code>. It returns a copy of
<code>reg</code> in which the field of <code>width</code> bits starting at bit <code>pos</code> is
replaced by the low <code>width</code> bits of <code>value</code>. Every bit outside the field keeps its
old value.</p>
<p><b>Why it matters.</b> This is the classic <em>read-modify-write</em> of a hardware register: read
the register, change one field, write it back without disturbing the other fields. Getting the mask
wrong silently breaks some other setting of the chip.</p>
<h4>Picture: <code>set_field(0x12345678, 8, 8, 0xAB)</code></h4>
<pre>  reg               = 0x12345678
  field mask        = 0x0000FF00   (8 ones, moved up to bit 8)
  reg with the field
  cleared to 0      = 0x12340078   (reg AND the inverted mask)
  value moved to
  the field         = 0x0000AB00   (value &lt;&lt; 8, AND the mask)
  combine (OR)      = 0x1234AB78   &lt;-- return this</pre>
<h4>Facts you need</h4>
<ul>
<li>A mask of <code>w</code> ones in the low bits is 2<sup>w</sup> &minus; 1 (for w = 4 that is 0xF,
for w = 8 it is 0xFF). Shift it left by <code>pos</code> to put it over the field.</li>
<li><code>~m</code> flips every bit of <code>m</code>: ones become zeros. ANDing with <code>~m</code>
clears the field and keeps the rest.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th><th>Note</th></tr>
<tr><td><code>set_field(0x12345678, 8, 8, 0xAB)</code></td><td>0x1234AB78</td><td>the picture above</td></tr>
<tr><td><code>set_field(0xFFFFFFFF, 4, 4, 0x0)</code></td><td>0xFFFFFF0F</td><td>bits 7..4 cleared</td></tr>
<tr><td><code>set_field(0x00000000, 8, 4, 0x1F)</code></td><td>0x00000F00</td><td><code>value</code> has 5 bits but
the field has only 4: the extra top bit is ignored</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>width</code> is 1 to 31, and <code>pos + width &lt;= 32</code>.</li>
<li><code>value</code> may have extra high bits set (random 32-bit values in the test). They must not
leak outside the field.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Build one mask that has ones exactly over the field.</li>
<li>Use it twice: once to clear the field in <code>reg</code>, once to cut <code>value</code> (after
shifting) down to the field.</li>
<li>Combine the two parts. Since they never have a 1 in the same place, which operator joins them?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int popcount32(uint32_t x)</code> that returns how
many of the 32 bits of <code>x</code> are 1 ("population count"). Try it without the compiler's
built-in <code>__builtin_popcount</code>.</p>
<p><b>Why it matters.</b> Counting set bits is used for parity checks, error-correcting codes (Hamming
distance = popcount of a XOR b), and counting how many flags in a status register are on.</p>
<h4>Picture: <code>x = 0xF0</code></h4>
<pre>  bit:   7 6 5 4 3 2 1 0      (bits 8..31 are all 0)
  x:     1 1 1 1 0 0 0 0
         ^ ^ ^ ^
         four ones: return 4</pre>
<p>Each hex digit is 4 bits: 0 = 0000, 1 = 0001, 5 = 0101, 8 = 1000, F = 1111.</p>
<h4>Examples</h4>
<table>
<tr><th>x</th><th>Bits</th><th>You return</th></tr>
<tr><td><code>0x00000000</code></td><td>all 0</td><td>0</td></tr>
<tr><td><code>0x00000001</code></td><td>only bit 0</td><td>1</td></tr>
<tr><td><code>0x000000F0</code></td><td>1111 0000</td><td>4</td></tr>
<tr><td><code>0x80000000</code></td><td>only bit 31</td><td>1</td></tr>
<tr><td><code>0x55555555</code></td><td>0101 repeated 8 times</td><td>16</td></tr>
<tr><td><code>0xFFFFFFFF</code></td><td>all 1</td><td>32</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Simple way: look at bit 0 (<code>x &amp; 1</code>), add it to a count, shift <code>x</code> right by
one, and repeat. When can you stop?</li>
<li>Use an unsigned type, so that shifting right always brings in zeros at the top.</li>
<li>Faster way (a common interview follow-up): find an expression that removes only the lowest 1 bit
of <code>x</code>. Then the loop runs once per 1 bit instead of 32 times.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int is_pow2(uint32_t x)</code>. It returns 1 if
<code>x</code> is a power of two (1, 2, 4, 8, 16, &hellip;) and 0 otherwise. <b>Zero is not</b> a power
of two.</p>
<p><b>Why it matters.</b> Buffer sizes and FFT sizes are usually powers of two. For a power of two
<code>N</code>, the slow remainder <code>i % N</code> can be replaced by the fast
<code>i &amp; (N - 1)</code>. Code often checks the size first with exactly this function.</p>
<h4>What powers of two look like in binary</h4>
<table>
<tr><th>x</th><th>Binary</th><th>Power of two?</th></tr>
<tr><td>1</td><td>0000 0001</td><td>yes (2<sup>0</sup>)</td></tr>
<tr><td>2</td><td>0000 0010</td><td>yes</td></tr>
<tr><td>3</td><td>0000 0011</td><td>no</td></tr>
<tr><td>4</td><td>0000 0100</td><td>yes</td></tr>
<tr><td>6</td><td>0000 0110</td><td>no</td></tr>
<tr><td>8</td><td>0000 1000</td><td>yes</td></tr>
<tr><td>0</td><td>0000 0000</td><td><b>no</b></td></tr>
</table>
<p>A power of two has <b>exactly one</b> bit set to 1.</p>
<h4>A useful pattern: subtract 1</h4>
<pre>  x     = 8 = 0000 1000        x     = 6 = 0000 0110
  x - 1 = 7 = 0000 0111        x - 1 = 5 = 0000 0101
  the single 1 becomes 0,      the LOWEST 1 becomes 0, the zeros
  all zeros below become 1     below it become 1, higher 1s stay</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>is_pow2(1)</code></td><td>1</td></tr>
<tr><td><code>is_pow2(1024)</code></td><td>1</td></tr>
<tr><td><code>is_pow2(1023)</code></td><td>0</td></tr>
<tr><td><code>is_pow2(0x80000000)</code> (2<sup>31</sup>, the largest one)</td><td>1</td></tr>
<tr><td><code>is_pow2(0xFFFFFFFF)</code></td><td>0</td></tr>
<tr><td><code>is_pow2(0)</code></td><td>0</td></tr>
</table>
<p>The test treats any non-zero return value as "yes", but returning exactly 1 is cleaner.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Simple way: count the 1 bits (as in the previous problem) and check the count.</li>
<li>Quick way: look at the "subtract 1" pattern. What do <code>x</code> and <code>x - 1</code> have in
common when <code>x</code> is a power of two? What about when it is not?</li>
<li>Check what your method says for 0. (For an unsigned 0, <code>0 - 1</code> wraps around to
0xFFFFFFFF.)</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>uint32_t bswap32(uint32_t x)</code> that reverses
the order of the four bytes of <code>x</code>. The bits inside each byte do not change; only whole bytes
move.</p>
<p><b>Why it matters.</b> <em>Endianness</em> is the order in which a CPU stores the bytes of a number in
memory. A <em>little-endian</em> CPU (x86, most ARM chips, this site) stores the lowest byte first. A
<em>big-endian</em> device or network protocol sends the highest byte first. When the two meet, you must
swap the bytes, or 0x11223344 is read as 0x44332211.</p>
<h4>Picture: <code>bswap32(0x11223344)</code></h4>
<pre>  byte number:   3    2    1    0        (byte 0 = bits 7..0)
  x          = [11] [22] [33] [44]
  result     = [44] [33] [22] [11]  = 0x44332211
                 ^    ^    ^    ^
                 |    |    |    +-- was byte 3 of x
                 |    |    +------- was byte 2 of x
                 |    +------------ was byte 1 of x
                 +----------------- was byte 0 of x</pre>
<table>
<tr><th>Byte of x</th><th>Its bits in x</th><th>Goes to bits</th><th>Moves</th></tr>
<tr><td>byte 0 (0x44)</td><td>7..0</td><td>31..24</td><td>left by 24</td></tr>
<tr><td>byte 1 (0x33)</td><td>15..8</td><td>23..16</td><td>left by 8</td></tr>
<tr><td>byte 2 (0x22)</td><td>23..16</td><td>15..8</td><td>right by 8</td></tr>
<tr><td>byte 3 (0x11)</td><td>31..24</td><td>7..0</td><td>right by 24</td></tr>
</table>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>bswap32(0x11223344)</code></td><td>0x44332211</td></tr>
<tr><td><code>bswap32(0xAABBCCDD)</code></td><td>0xDDCCBBAA</td></tr>
<tr><td><code>bswap32(0x000000FF)</code></td><td>0xFF000000</td></tr>
</table>
<p>Swapping twice gives back the original value.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Treat the four bytes separately. For each one, use the table: shift it to its new place.</li>
<li>After a shift, other bytes may land in the same place too. A mask such as
<code>0x00FF0000</code> keeps only the byte you want.</li>
<li>The four moved bytes do not overlap. How do you join them into one value?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>uint32_t rotl32(uint32_t x, int r)</code> that
<em>rotates</em> <code>x</code> left by <code>r</code> bits. Rotating is like shifting, but the bits that
fall off the top (left) end come back in at the bottom (right) end, so no bit is lost.</p>
<p><b>Why it matters.</b> Rotations are used in hash functions, checksums, random-number generators
and ciphers. Many CPUs have a single instruction for it.</p>
<h4>Picture with 8 bits (your function uses 32), rotate left by 3</h4>
<pre>  before:  1 0 1 1 0 0 1 0
           \___/
           these 3 bits fall off the left end ...
  shift:   1 0 0 1 0 _ _ _
  after:   1 0 0 1 0 1 0 1
                     \___/
                     ... and come back in on the right</pre>
<p>Compare with a plain shift <code>x &lt;&lt; r</code>: there the right end is filled with zeros and
the top bits are lost.</p>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th><th>Note</th></tr>
<tr><td><code>rotl32(0x80000001, 1)</code></td><td>0x00000003</td><td>bit 31 comes back as bit 0</td></tr>
<tr><td><code>rotl32(0x12345678, 4)</code></td><td>0x23456781</td><td>4 bits = one hex digit moves round</td></tr>
<tr><td><code>rotl32(0x12345678, 8)</code></td><td>0x34567812</td><td>one whole byte moves round</td></tr>
<tr><td><code>rotl32(0x12345678, 31)</code></td><td>0x091A2B3C</td><td>same as rotating right by 1</td></tr>
<tr><td><code>rotl32(0x12345678, 0)</code></td><td>0x12345678</td><td>no change</td></tr>
</table>
<h4>Limits and the trap</h4>
<ul>
<li><code>r</code> is 0 to 31. <code>r</code> = 0 is tested.</li>
<li>In C, shifting a 32-bit value by 32 or more places is undefined behaviour, and this site traps
it. Check every shift amount in your formula for <code>r</code> = 0.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Split the result into two parts: the bits that move left and stay inside, and the bits that fall
off and wrap round to the bottom.</li>
<li>The wrapped bits were the top <code>r</code> bits. By how much must you shift right to bring them to
the bottom?</li>
<li>Then join the two parts.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int32_t sign_extend(uint32_t x, int bits)</code>.
The low <code>bits</code> bits of <code>x</code> hold a signed number in <em>two's complement</em>; all
higher bits of <code>x</code> are 0. Return that number as a normal 32-bit signed integer.</p>
<p><b>Why it matters.</b> A 12-bit ADC (analog-to-digital converter) sends each sample in the low 12 bits
of a 32-bit word. The value 0xFFF is not 4095: it means &minus;1. If you use the word directly, every
negative sample becomes a large positive number. Copying the field's top bit into all higher bits is
called <em>sign extension</em>.</p>
<h4>Facts you need: two's complement in a field of <code>bits</code> bits</h4>
<ul>
<li>The top bit of the field (bit <code>bits</code>&minus;1) is the sign bit.</li>
<li>If the sign bit is 0, the value is the field read as a normal positive number.</li>
<li>If the sign bit is 1, the value is (the field read as positive) &minus; 2<sup>bits</sup>.</li>
</ul>
<p>Full table for a 4-bit field (2<sup>4</sup> = 16):</p>
<pre>  field:  0000 0001 ... 0111 | 1000 1001 ... 1110 1111
  as hex:   0    1  ...   7  |   8    9  ...   E    F
  value:    0    1  ...   7  |  -8   -7  ...  -2   -1
            sign bit 0       |  sign bit 1: value = field - 16</pre>
<h4>Picture: 12 bits, <code>x = 0xFF6</code></h4>
<pre>  bit:   11 10 9 8 7 6 5 4 3 2 1 0
          1  1 1 1 1 1 1 1 0 1 1 0     = 0xFF6 = 4086
          ^ sign bit is 1, so the value is 4086 - 4096 = -10</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Sign bit</th><th>You return</th></tr>
<tr><td><code>sign_extend(0x005, 12)</code></td><td>0</td><td>5</td></tr>
<tr><td><code>sign_extend(0x7FF, 12)</code></td><td>0</td><td>2047 (largest 12-bit value)</td></tr>
<tr><td><code>sign_extend(0x800, 12)</code></td><td>1</td><td>&minus;2048 (smallest)</td></tr>
<tr><td><code>sign_extend(0xFF6, 12)</code></td><td>1</td><td>&minus;10</td></tr>
<tr><td><code>sign_extend(0xFFF, 12)</code></td><td>1</td><td>&minus;1</td></tr>
<tr><td><code>sign_extend(0x1, 1)</code></td><td>1</td><td>&minus;1 (a 1-bit field holds only 0 and &minus;1)</td></tr>
<tr><td><code>sign_extend(0xFFFFFFFF, 32)</code></td><td>1</td><td>&minus;1 (the field is the whole word)</td></tr>
</table>
<h4>Limits and traps</h4>
<ul>
<li><code>bits</code> is any width from 1 to 32. Both ends are tested.</li>
<li>For <code>bits</code> = 32, 2<sup>32</sup> does not fit in 32 bits, and <code>1u &lt;&lt; 32</code> is
undefined behaviour (trapped on this site). Use a 64-bit type (<code>int64_t</code>) for the arithmetic,
or handle 32 separately.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>First find out whether the sign bit is set. Which mask has a 1 only at bit <code>bits</code>&minus;1?</li>
<li>If it is set, apply the "minus 2<sup>bits</sup>" rule. Do the subtraction in a type wide enough to
hold 2<sup>bits</sup>.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>uint8_t reverse_bits8(uint8_t x)</code> that
reverses the order of the 8 bits of a byte, like a mirror: bit 0 goes to bit 7, bit 1 goes to bit 6, and
so on, up to bit 7 going to bit 0.</p>
<p><b>Why it matters.</b> The radix-2 FFT reorders its inputs in "bit-reversed order", and some serial
links send the lowest bit first, so the byte arrives mirrored.</p>
<h4>Picture: <code>reverse_bits8(0xB0)</code></h4>
<pre>  bit:      7 6 5 4 3 2 1 0
  x:        1 0 1 1 0 0 0 0     = 0xB0
             mirror: read x from right to left
  result:   0 0 0 0 1 1 0 1     = 0x0D</pre>
<table>
<tr><th>Bit of x</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th></tr>
<tr><td>goes to bit</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td></tr>
</table>
<p>In general bit <code>i</code> goes to bit 7 &minus; <code>i</code>.</p>
<h4>Examples</h4>
<table>
<tr><th>x</th><th>Binary</th><th>Reversed</th><th>You return</th></tr>
<tr><td>0x01</td><td>0000 0001</td><td>1000 0000</td><td>0x80</td></tr>
<tr><td>0xB0</td><td>1011 0000</td><td>0000 1101</td><td>0x0D</td></tr>
<tr><td>0x06</td><td>0000 0110</td><td>0110 0000</td><td>0x60</td></tr>
<tr><td>0xFF</td><td>1111 1111</td><td>1111 1111</td><td>0xFF</td></tr>
<tr><td>0x00</td><td>0000 0000</td><td>0000 0000</td><td>0x00</td></tr>
</table>
<p>The test checks all 256 possible bytes.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Build the result in a new variable that starts at 0. Handle one bit of <code>x</code> per loop
step, 8 steps in total.</li>
<li>Option A: if bit <code>i</code> of <code>x</code> is 1, set bit 7 &minus; <code>i</code> of the
result.</li>
<li>Option B: take bits from the bottom of <code>x</code> one by one, and push each into the result from
the right (shift the result left by 1 first). The bit you pushed first ends up highest.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>uint32_t next_pow2(uint32_t x)</code> that returns
the smallest power of two (1, 2, 4, 8, &hellip;) that is <b>greater than or equal to</b> <code>x</code>.
If <code>x</code> is already a power of two, return <code>x</code> itself.</p>
<p><b>Why it matters.</b> An FFT or a ring buffer usually needs a power-of-two size. If you have 1000
samples, you pick an FFT size of 1024 and fill the rest with zeros.</p>
<h4>Picture on a number line</h4>
<pre>  powers of two:  1   2   4   8   16  ...  512   1024   2048
                        x=5 --^           x=1000 --^      ^-- x=1025
                                          x=1024 --^</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>You return</th></tr>
<tr><td><code>next_pow2(1)</code></td><td>1</td></tr>
<tr><td><code>next_pow2(3)</code></td><td>4</td></tr>
<tr><td><code>next_pow2(5)</code></td><td>8</td></tr>
<tr><td><code>next_pow2(17)</code></td><td>32</td></tr>
<tr><td><code>next_pow2(1000)</code></td><td>1024</td></tr>
<tr><td><code>next_pow2(1024)</code></td><td>1024</td></tr>
<tr><td><code>next_pow2(1025)</code></td><td>2048</td></tr>
<tr><td><code>next_pow2(0x40000001)</code></td><td>0x80000000 (2<sup>31</sup>)</td></tr>
<tr><td><code>next_pow2(0x80000000)</code></td><td>0x80000000</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>x</code> is from 1 to 2<sup>31</sup> (0x80000000). So the answer is at most 2<sup>31</sup>,
which fits in a <code>uint32_t</code>. <code>x</code> = 0 is never passed.</li>
<li>Careful with a doubling loop near the top: if a <code>uint32_t</code> ever doubles past
2<sup>31</sup>, it wraps round to 0.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Simple way: start with 1 and keep doubling while it is smaller than <code>x</code>. With the limits
above this loop runs at most 31 times.</li>
<li>Bit trick (a common interview follow-up): in binary, the answer has one 1 bit, just above the
highest 1 bit of <code>x &minus; 1</code>. If you could turn every bit below the highest 1 of
<code>x &minus; 1</code> into 1 (giving 0&hellip;0111&hellip;1), what would adding 1 give?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function
<code>void *my_memcpy(void *dst, const void *src, size_t n)</code>. It copies <code>n</code> bytes, starting
at address <code>src</code>, to the memory starting at address <code>dst</code>. Then it returns
<code>dst</code> (the same pointer it was given). Write the copy loop yourself; calling the library
<code>memcpy</code> would skip the exercise.</p>
<p><b>Why it matters.</b> Copying blocks of memory (audio frames, packets, structs) is everywhere in
embedded code, and "write your own memcpy" is a classic interview question about pointers.</p>
<h4>Facts you need</h4>
<ul>
<li><code>void *</code> is a pointer "to anything": it holds an address but has no element type. You
cannot read through it or do <code>++</code> on it directly. First convert it to a pointer to bytes:
<code>unsigned char *</code> (1 byte per element).</li>
<li><code>const</code> on <code>src</code> means you only read from it.</li>
<li><code>size_t</code> is an unsigned integer type for sizes; it is 4 bytes on this site.</li>
</ul>
<h4>Picture: <code>my_memcpy(dst, src, 4)</code></h4>
<pre>  src:  [0x41][0x42][0x43][0x44][0x45]...
           |     |     |     |
           v     v     v     v           exactly n = 4 bytes are written
  dst:  [0x41][0x42][0x43][0x44][ ?? ]...  &lt;- this byte is NOT touched
         ^
         return this address (dst)</pre>
<h4>What the test checks</h4>
<table>
<tr><th>Check</th><th>Meaning</th></tr>
<tr><td>return value</td><td>must be exactly the <code>dst</code> pointer you received</td></tr>
<tr><td>copied bytes</td><td>the <code>n</code> bytes at <code>dst</code> equal the <code>n</code> bytes at
<code>src</code></td></tr>
<tr><td>no stray writes</td><td>the bytes just before <code>dst</code> and every byte after
<code>dst + n</code> must keep their old value</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>n</code> is from 0 to 256. For <code>n</code> = 0 copy nothing, but still return
<code>dst</code>.</li>
<li>The two areas never overlap (the next problem handles overlap).</li>
<li>The bytes are random, so any value 0 to 255 can appear, including 0. Do not stop at a zero byte:
this is not a string copy.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Make byte pointers from <code>dst</code> and <code>src</code>. Keep the original <code>dst</code>
somewhere, because you need to return it.</li>
<li>Copy one byte, move both pointers one byte forward, and repeat <code>n</code> times.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function
<code>void *my_memmove(void *dst, const void *src, size_t n)</code>. It copies <code>n</code> bytes from
<code>src</code> to <code>dst</code> and returns <code>dst</code>, like <code>memcpy</code>. The difference:
the two areas <b>may overlap</b>. The result must be as if the <code>n</code> source bytes were first copied
to a safe place and then written to <code>dst</code>. Write the copy loops yourself; calling the library
<code>memmove</code> would skip the exercise.</p>
<p><b>Why it matters.</b> Inside one buffer you often shift data along: "move these samples two places
to the right to make room". Source and destination then overlap, and a plain front-to-back copy
destroys data before it has been read.</p>
<h4>Picture: the problem (shift 4 bytes right by 2)</h4>
<pre>  index:      0 1 2 3 4 5 6 7
  buf:        A B C D E F G H
  call: my_memmove(buf + 2, buf, 4)    copy "ABCD" to positions 2..5

  correct result:                      A B A B C D G H

  front-to-back copy, step by step:
    buf[2] = buf[0]  -&gt;  A B A D E F G H
    buf[3] = buf[1]  -&gt;  A B A B E F G H
    buf[4] = buf[2]  -&gt;  A B A B A F G H   wrong: buf[2] was already
    buf[5] = buf[3]  -&gt;  A B A B A B G H   overwritten, C is lost</pre>
<p>Now copy the same bytes back to front: <code>buf[5] = buf[3]</code>, then <code>buf[4] = buf[2]</code>,
<code>buf[3] = buf[1]</code>, <code>buf[2] = buf[0]</code>. Each byte is read before it is overwritten,
and you get the correct <code>A B A B C D G H</code>.</p>
<h4>Examples (buffer starts as <code>"ABCDEFGH"</code>)</h4>
<table>
<tr><th>Call</th><th>Result</th><th>Note</th></tr>
<tr><td><code>my_memmove(buf + 2, buf, 4)</code></td><td><code>ABABCDGH</code></td><td>dst after src</td></tr>
<tr><td><code>my_memmove(buf, buf + 2, 4)</code></td><td><code>CDEFEFGH</code></td><td>dst before src</td></tr>
<tr><td><code>my_memmove(buf + 3, buf + 3, 4)</code></td><td><code>ABCDEFGH</code></td><td>same place: nothing
changes</td></tr>
<tr><td>any call with <code>n</code> = 0</td><td>unchanged</td><td>still return <code>dst</code></td></tr>
</table>
<h4>Limits</h4>
<ul>
<li>The test picks random start positions 0 to 100 inside a 200-byte buffer and <code>n</code> from 0 to
99, so every case appears: no overlap, overlap from either side, and <code>dst == src</code>.</li>
<li>It compares the whole 200-byte buffer with the real <code>memmove</code>, and checks that you return
<code>dst</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Look at the picture. When <code>dst</code> is after <code>src</code>, which end of the source gets
overwritten first if you copy front to back?</li>
<li>Try the other case, <code>dst</code> before <code>src</code>, on paper. Is front-to-back safe
there?</li>
<li>So the only decision is the direction, and you choose it by comparing the two addresses.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function
<code>const int *find_first_negative(const int *x, int n)</code>. It searches the array <code>x</code> of
<code>n</code> numbers and returns a <b>pointer</b> to the first element that is negative (less than 0).
If no element is negative, it returns <code>NULL</code> (the "points to nothing" value).</p>
<p><b>Why it matters.</b> Many C library functions (<code>strchr</code>, <code>memchr</code>,
<code>bsearch</code>) return a pointer to what they found, or <code>NULL</code> if nothing was found.
The caller must always check for <code>NULL</code> before using the result.</p>
<h4>Picture</h4>
<pre>  index:      0    1    2    3    4
            +----+----+----+----+----+
  x:        |  4 |  7 | -2 |  5 | -9 |
            +----+----+----+----+----+
                        ^
                        first negative: return &amp;x[2]  (which equals x + 2)</pre>
<h4>Facts you need</h4>
<ul>
<li><code>&amp;x[i]</code> is the address of element <code>i</code>. It is the same as
<code>x + i</code>.</li>
<li>The test checks the <b>address</b> you return, not only the value. So return a pointer into the
array you were given, not a pointer to a copy.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>Array</th><th><code>n</code></th><th>You return</th></tr>
<tr><td><code>{4, 7, -2, 5, -9}</code></td><td>5</td><td><code>&amp;x[2]</code></td></tr>
<tr><td><code>{-1, 3}</code></td><td>2</td><td><code>&amp;x[0]</code></td></tr>
<tr><td><code>{1, 2, 3}</code></td><td>3</td><td><code>NULL</code></td></tr>
<tr><td><code>{0, 0}</code></td><td>2</td><td><code>NULL</code> (0 is not negative)</td></tr>
<tr><td>empty</td><td>0</td><td><code>NULL</code></td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>n</code> is 0 to 50. Values are &minus;3 to 30.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Look at the elements in order. As soon as you find one below 0, you are done: return its address
straight away.</li>
<li>If the loop ends without finding one, what must you return?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function</p>
<pre>void transpose(const int *in, int *out, int rows, int cols);</pre>
<p><code>in</code> is a matrix with <code>rows</code> rows and <code>cols</code> columns. Write its
<em>transpose</em> into <code>out</code>: rows become columns and columns become rows. So <code>out</code>
has <code>cols</code> rows and <code>rows</code> columns, and element (r, c) of <code>in</code> becomes
element (c, r) of <code>out</code>.</p>
<p><b>Why it matters.</b> Image, multi-channel audio and matrix code in C usually stores a matrix in
one flat 1-D array and computes the index by hand, because the size is often known only at run time.
Getting that index right is the whole skill.</p>
<h4>How a matrix is stored ("row by row", or row-major)</h4>
<p>Row 0 comes first, then row 1, and so on. So element (r, c) of a matrix with <code>cols</code>
columns is at index <code>r * cols + c</code>.</p>
<pre>  in: 2 rows x 3 cols                 out: 3 rows x 2 cols
      col: 0  1  2                         col: 0  1
  row 0: [ 1  2  3 ]                   row 0: [ 1  4 ]
  row 1: [ 4  5  6 ]                   row 1: [ 2  5 ]
                                       row 2: [ 3  6 ]

  in  in memory:  {1, 2, 3, 4, 5, 6}      (row 0 | row 1)
  out in memory:  {1, 4, 2, 5, 3, 6}      (row 0 | row 1 | row 2)</pre>
<h4>Where each element goes (same example: rows = 2, cols = 3)</h4>
<table>
<tr><th>(r, c) in <code>in</code></th><th>index in <code>in</code> = r&times;3 + c</th><th>value</th>
<th>(c, r) in <code>out</code></th><th>index in <code>out</code> = c&times;2 + r</th></tr>
<tr><td>(0, 0)</td><td>0</td><td>1</td><td>(0, 0)</td><td>0</td></tr>
<tr><td>(0, 1)</td><td>1</td><td>2</td><td>(1, 0)</td><td>2</td></tr>
<tr><td>(0, 2)</td><td>2</td><td>3</td><td>(2, 0)</td><td>4</td></tr>
<tr><td>(1, 0)</td><td>3</td><td>4</td><td>(0, 1)</td><td>1</td></tr>
<tr><td>(1, 1)</td><td>4</td><td>5</td><td>(1, 1)</td><td>3</td></tr>
<tr><td>(1, 2)</td><td>5</td><td>6</td><td>(2, 1)</td><td>5</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li><code>rows</code> and <code>cols</code> are each 1 to 20. Matrices are often not square, and a
1&times;N or N&times;1 shape can appear.</li>
<li><code>in</code> and <code>out</code> are different arrays.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Visit every element of <code>in</code> with two nested loops, one over rows and one over
columns.</li>
<li>For each element, write two index formulas: where it is in <code>in</code>, and where it goes in
<code>out</code>. The row length is different in the two matrices: <code>out</code> has
<code>rows</code> columns.</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> The starter code defines a node of a <em>singly linked list</em>:
each node holds a <code>value</code> and a pointer <code>next</code> to the following node. The last node's
<code>next</code> is <code>NULL</code>. Write two functions:</p>
<pre>// returns how many nodes there are
int list_length(const struct Node *head);

// reverses the links and returns the new first node
struct Node *list_reverse(struct Node *head);</pre>
<p><code>head</code> points to the first node, or is <code>NULL</code> for an empty list.</p>
<p><b>Why it matters.</b> "Reverse a linked list" is one of the most frequently asked interview
questions. It tests whether you can change pointers in the right order without losing part of the
list.</p>
<h4>Picture: before and after <code>list_reverse</code></h4>
<pre>  before:
  head
   |
   v
  +---+---+    +---+---+    +---+---+
  | 1 | *-+---&gt;| 2 | *-+---&gt;| 3 | / |     / = NULL
  +---+---+    +---+---+    +---+---+

  after (the SAME three nodes; only the next pointers changed):
  new head (returned)
   |
   v
  +---+---+    +---+---+    +---+---+
  | 3 | *-+---&gt;| 2 | *-+---&gt;| 1 | / |
  +---+---+    +---+---+    +---+---+
  the node holding 1 was the old head; its next is now NULL</pre>
<h4>The rules</h4>
<ul>
<li><code>list_reverse</code> must <b>reuse the existing nodes</b>. Do not call <code>malloc</code> and do
not change any <code>value</code>. The test checks that the node addresses come back in reverse order.</li>
<li>Return the new first node, which was the old last node. For an empty list, return
<code>NULL</code>.</li>
<li>Use <code>p-&gt;next</code> to read the <code>next</code> field of the node that <code>p</code> points
to.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>List</th><th><code>list_length</code></th><th>After <code>list_reverse</code></th></tr>
<tr><td>1 &rarr; 2 &rarr; 3</td><td>3</td><td>3 &rarr; 2 &rarr; 1, returns the node holding 3</td></tr>
<tr><td>7</td><td>1</td><td>7, returns the same node</td></tr>
<tr><td>empty (<code>head == NULL</code>)</td><td>0</td><td>returns <code>NULL</code></td></tr>
</table>
<p>The test uses lists of 0 up to 39 nodes, including the empty list and a list of one node.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>For the length: follow the <code>next</code> pointers from <code>head</code> until you reach
<code>NULL</code>, counting the nodes.</li>
<li>For the reverse: walk the list once. At each node, its <code>next</code> should point back to the
node you visited just before it. So keep a pointer to that previous node.</li>
<li>Once you overwrite <code>next</code>, the rest of the list is unreachable. What must you save
before you change it?</li>
</ol>
</details>""",
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
r"""<p><b>What to write.</b> A function <code>int *range_alloc(int n)</code>. It asks for memory
for an array of <code>n</code> ints with <code>malloc</code>, fills it with 0, 1, 2, &hellip;,
<code>n</code>&minus;1, and returns the pointer. The caller will release the memory later with
<code>free</code>.</p>
<p><b>Why it matters.</b> A function cannot return a local array: it disappears when the function
returns. Memory from <code>malloc</code> (on the "heap") stays until somebody frees it. In real-time
audio code you allocate like this <em>once</em>, at start-up, never inside the audio callback, because
<code>malloc</code> can take an unpredictable amount of time.</p>
<h4>Facts you need</h4>
<ul>
<li><code>malloc(k)</code> reserves <code>k</code> <b>bytes</b> and returns their address, or
<code>NULL</code> if there is not enough memory. The bytes are not cleared: they contain garbage.</li>
<li>An <code>int</code> is 4 bytes on this site, so <code>n</code> ints need <code>n * 4</code> bytes.
Write <code>sizeof(int)</code> instead of 4, so the code is correct on every machine.</li>
</ul>
<h4>Picture: <code>range_alloc(5)</code></h4>
<pre>  stack (your function)          heap (from malloc: 5 * 4 = 20 bytes)
  +-----------+                  +---+---+---+---+---+
  | p: addr --+-----------------&gt;| 0 | 1 | 2 | 3 | 4 |
  +-----------+                  +---+---+---+---+---+
  p disappears when the          this memory stays until
  function returns, but its      the caller calls free(p)
  value is returned</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Returned array</th><th>Bytes to allocate</th></tr>
<tr><td><code>range_alloc(1)</code></td><td><code>{0}</code></td><td>4</td></tr>
<tr><td><code>range_alloc(5)</code></td><td><code>{0, 1, 2, 3, 4}</code></td><td>20</td></tr>
<tr><td><code>range_alloc(100000)</code></td><td><code>{0, 1, &hellip;, 99999}</code></td><td>400,000</td></tr>
</table>
<h4>Limits</h4>
<ul>
<li>The test calls it with <code>n</code> = 1, 2, 10, 1000 and 100000. For these it expects a
non-<code>NULL</code> pointer with the right contents, and then frees it.</li>
<li>For <code>n</code> = 0 you may return <code>NULL</code> or a valid pointer (this case is not
tested).</li>
<li>If <code>malloc</code> returns <code>NULL</code>, return <code>NULL</code> and do not write through
it.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Work out how many bytes you need, and ask <code>malloc</code> for them.</li>
<li>Check the result before you use it.</li>
<li>Fill the array with a loop, then return the pointer. Do not free it yourself: the caller does
that.</li>
</ol>
</details>""",
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
