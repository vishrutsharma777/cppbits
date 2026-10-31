# Problem bank, part D: predict-the-output questions (the "C output" and "OOP output" MCQs of
# campus OAs such as Qualcomm's HirePro test). Every expected output is checked by tools/grade.mjs
# against a real compile-and-run with the site's own compiler and flags.
from common import Q

PROBLEMS = []
add = PROBLEMS.append

SIZES = ("<p>What does this program print? Sizes on this site: it compiles for 32-bit WebAssembly, so "
         "<code>int</code>, <code>long</code>, <code>size_t</code> and every pointer are 4 bytes, "
         "<code>double</code> is 8, and the machine is little-endian. On a 64-bit PC (what most OA "
         "questions assume) pointers, <code>long</code> and <code>size_t</code> are 8 bytes.</p>")

S = "OA: predict the output (C)"

add(Q("pr_incr", S, "Pre- and post-increment", "c",
r"""#include <stdio.h>

int main(void)
{
    int i = 5;
    int a = i++;
    int b = ++i;
    printf("%d %d %d\n", a, b, i);
    return 0;
}
""",
"5 7 7\n",
r"""<p><code>i++</code> gives the old value (5), then <code>i</code> becomes 6. <code>++i</code> makes it 7
first and gives 7.</p>
<p><b>Trap:</b> <code>i = i++ + ++i;</code> or <code>printf("%d %d", i++, i);</code> change and read
<code>i</code> with no sequence point between them. That is <em>undefined behaviour</em>; in an MCQ the answer is
"undefined / compiler dependent".</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints. Type one line
of answer for each line the program prints. Spaces at the end of a line do not matter. <b>Check</b> compares
your answer with the right one and needs no compiler. <b>Run it</b> really compiles the program and shows
what it prints, so use it after you have tried on paper.</p>
<p><b>What this question tests.</b> The difference between <em>post-increment</em> <code>i++</code> (use
the value, then add 1) and <em>pre-increment</em> <code>++i</code> (add 1, then use the value).</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>What happens, in order</th></tr>
<tr><td><code>x = i++;</code></td><td>1. <code>x</code> gets the <b>current</b> value of <code>i</code>.
2. Then <code>i</code> goes up by 1.</td></tr>
<tr><td><code>x = ++i;</code></td><td>1. <code>i</code> goes up by 1. 2. Then <code>x</code> gets the
<b>new</b> value of <code>i</code>.</td></tr>
<tr><td>Both forms</td><td>Change <code>i</code> by exactly 1. They differ only in which value they hand
over.</td></tr>
<tr><td><code>printf("%d %d %d\n", ...)</code></td><td>Prints three <code>int</code> values with one space
between them, then ends the line.</td></tr>
</table>
<p>Small example with other numbers: if <code>k</code> is 10, then <code>y = k++;</code> gives
<code>y</code> = 10 and leaves <code>k</code> = 11.</p>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a small table with one column for each variable: <code>i</code>, <code>a</code>,
<code>b</code>.</li>
<li>Go line by line. On each line, write the new values in a new row. Use the table above to decide
whether the variable on the left gets the value before or after the +1.</li>
<li>The <code>printf</code> prints the last row of your table, in the order <code>a</code>,
<code>b</code>, <code>i</code>.</li>
</ol>
</details>"""))

add(Q("pr_divmod", S, "Integer division and %", "c",
r"""#include <stdio.h>

int main(void)
{
    printf("%d %d\n", 7 / 2, -7 / 2);
    printf("%d %d %d\n", -7 % 3, 7 % -3, -7 % -3);
    return 0;
}
""",
"3 -3\n-1 1 -1\n",
r"""<p>Since C99, integer division truncates <b>towards zero</b>: 3.5 becomes 3 and &minus;3.5 becomes &minus;3.</p>
<p>The remainder follows from <code>(a / b) * b + a % b == a</code>, so <code>%</code> takes the <b>sign of the
left operand</b>: &minus;7 % 3 = &minus;7 &minus; (&minus;2)(3) = &minus;1, and 7 % &minus;3 = 7 &minus; (&minus;2)(&minus;3) = 1.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How C divides two whole numbers with
<code>/</code>, and what the remainder operator <code>%</code> gives when a number is negative.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>a / b</code> with two <code>int</code>s</td><td>Do the real division, then <b>throw the
fraction away</b>. This is called "rounding towards zero": a positive answer goes down, a negative answer
goes up towards 0. It never rounds to the nearest number.</td></tr>
<tr><td><code>a % b</code></td><td>Defined so that <code>(a / b) * b + a % b</code> equals <code>a</code>.
So <code>a % b = a &minus; (a / b) &times; b</code>, using the rounded-towards-zero <code>a / b</code>.</td></tr>
<tr><td>Sign of <code>a % b</code></td><td>It follows from the formula: the remainder has the sign of the
<b>left</b> number <code>a</code> (or it is 0). The sign of <code>b</code> does not matter.</td></tr>
<tr><td><code>-7 / 2</code></td><td>The minus belongs to the 7: it means <code>(-7) / 2</code>.</td></tr>
</table>
<h4>Worked examples (with other numbers)</h4>
<table>
<tr><th>Expression</th><th>Real division</th><th><code>/</code> gives</th><th><code>%</code> by the formula</th></tr>
<tr><td><code>10 / 4</code>, <code>10 % 4</code></td><td>2.5</td><td>2</td><td>10 &minus; 2&times;4 = 2</td></tr>
<tr><td><code>-10 / 4</code>, <code>-10 % 4</code></td><td>&minus;2.5</td><td>&minus;2 (not &minus;3)</td><td>&minus;10 &minus; (&minus;2)&times;4 = &minus;2</td></tr>
<tr><td><code>10 / -4</code>, <code>10 % -4</code></td><td>&minus;2.5</td><td>&minus;2</td><td>10 &minus; (&minus;2)&times;(&minus;4) = 2</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each <code>/</code>: divide as on a calculator, then cut off everything after the decimal
point. Keep the sign.</li>
<li>For each <code>%</code>: first find <code>a / b</code> the same way, then use
<code>a &minus; (a / b) &times; b</code>. Be careful with the signs when you multiply two negatives.</li>
<li>Check: the sign of every remainder should match the sign of its left number.</li>
</ol>
</details>"""))

add(Q("pr_unsigned", S, "Signed meets unsigned", "c",
r"""#include <stdio.h>

int main(void)
{
    int neg = -1;
    unsigned int one = 1;
    if (neg < one)
        printf("less\n");
    else
        printf("not less\n");
    if (sizeof(int) > neg)
        printf("bigger\n");
    else
        printf("smaller\n");
    return 0;
}
""",
"not less\nsmaller\n",
r"""<p>When an <code>int</code> meets an <code>unsigned int</code>, the <code>int</code> is converted to
<code>unsigned</code>. &minus;1 becomes 4,294,967,295, which is not less than 1.</p>
<p><code>sizeof</code> gives a <code>size_t</code>, which is unsigned too, so <code>neg</code> again becomes
4,294,967,295 and 4 &gt; 4,294,967,295 is false. This is a classic OA trap. <code>-Wextra</code>
(<code>-Wsign-compare</code>) warns about both comparisons.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> What happens when you compare a signed
(can be negative) number with an unsigned (never negative) number. This is a very common OA trap.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>int</code> compared with <code>unsigned int</code></td><td>C first converts the <code>int</code>
to <code>unsigned int</code>, and only then compares. Both sides are now unsigned.</td></tr>
<tr><td>Negative <code>int</code> &rarr; <code>unsigned int</code></td><td>The 32 bits are kept and read as an
unsigned number. The value becomes <i>n</i> + 2<sup>32</sup>, where 2<sup>32</sup> = 4,294,967,296. So
&minus;1 becomes 4,294,967,295 and &minus;2 becomes 4,294,967,294: huge numbers, not small ones.</td></tr>
<tr><td>Type of <code>sizeof(...)</code></td><td><code>size_t</code>, which is an <b>unsigned</b> type. On this
site it is <code>unsigned long</code>, 4 bytes (32 bits, the same as <code>unsigned int</code>); on a 64-bit PC
it is 8 bytes. In both cases it is unsigned and at least as wide as <code>int</code>, so the same rule applies:
the <code>int</code> is converted to this unsigned type first.</td></tr>
<tr><td><code>sizeof(int)</code></td><td>4, on this site and on a normal PC.</td></tr>
</table>
<h4>Picture: the same 32 bits read two ways</h4>
<pre>bits of -1:   1111 1111 1111 1111 1111 1111 1111 1111

read as int:           -1
read as unsigned int:   4,294,967,295   (the largest unsigned int)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each <code>if</code>, write down the type of the left side and of the right side.</li>
<li>If one side is unsigned, convert the other side to unsigned using the rule above.</li>
<li>Now compare the two (possibly very large) numbers normally, and pick the branch.</li>
</ol>
</details>"""))

add(Q("pr_short", S, "Short-circuit evaluation", "c",
r"""#include <stdio.h>

int main(void)
{
    int z = 0;
    int r = (z++ || z++) && z++;
    printf("%d %d\n", r, z);

    int a = 0, b = 0;
    if (a++ && b++)
        printf("yes\n");
    printf("%d %d\n", a, b);
    return 0;
}
""",
"1 3\n1 0\n",
r"""<p><code>||</code> and <code>&amp;&amp;</code> evaluate left to right and stop as soon as the answer is known.
Each one is a sequence point, so the increments here are well defined.</p>
<ul><li>The first <code>z++</code> gives 0 (false), so the second <code>z++</code> runs and gives 1 (true). Then
<code>&amp;&amp; z++</code> runs too and gives 2 (true). <code>r = 1</code>, <code>z = 3</code>.</li>
<li><code>a++</code> gives 0, so <code>&amp;&amp;</code> is already false and <code>b++</code> never runs:
<code>a = 1</code>, <code>b = 0</code>.</li></ul>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> <em>Short-circuit evaluation</em>: the
operators <code>||</code> (OR) and <code>&amp;&amp;</code> (AND) stop early when the answer is already known,
so some parts of the expression may never run.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>What happens</th></tr>
<tr><td><code>A || B</code></td><td>Work out <code>A</code>. If it is true (not 0), the result is 1 and
<code>B</code> is <b>not run at all</b>. Otherwise run <code>B</code>: the result is 1 if <code>B</code> is
not 0, else 0.</td></tr>
<tr><td><code>A &amp;&amp; B</code></td><td>Work out <code>A</code>. If it is false (0), the result is 0 and
<code>B</code> is <b>not run at all</b>. Otherwise run <code>B</code>: the result is 1 if <code>B</code> is
not 0, else 0.</td></tr>
<tr><td>Result value</td><td><code>||</code> and <code>&amp;&amp;</code> always give exactly 0 or 1.</td></tr>
<tr><td><code>z++</code></td><td>Gives the <b>old</b> value of <code>z</code> to the expression, then adds 1
to <code>z</code>.</td></tr>
<tr><td>Order</td><td>The left side, including its <code>++</code>, is completely finished before the right
side starts. So this program is well defined.</td></tr>
<tr><td><code>if (cond)</code></td><td>The body runs only when <code>cond</code> is not 0.</td></tr>
</table>
<p>The brackets in <code>(z++ || z++) &amp;&amp; z++</code> mean: finish the <code>||</code> part first, then
decide about the <code>&amp;&amp;</code> part.</p>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns: "which <code>z++</code>", "value it gives", "<code>z</code> after it".</li>
<li>Go left to right. Before each part, ask: is the answer already known? If yes, that part is skipped
and <code>z</code> does not change.</li>
<li>Do the same for <code>a++ &amp;&amp; b++</code>. A skipped <code>b++</code> leaves <code>b</code>
unchanged.</li>
</ol>
</details>"""))

add(Q("pr_wrap", S, "Small types wrap around", "c",
r"""#include <stdio.h>

int main(void)
{
    unsigned char u = 255;
    signed char s = 127;
    u++;
    s++;
    printf("%d %d\n", u, s);

    unsigned int x = 0;
    x--;
    printf("%u\n", x);
    return 0;
}
""",
"0 -128\n4294967295\n",
r"""<p>Unsigned arithmetic is defined to wrap modulo 2<sup>N</sup>: 255 + 1 in 8 bits is 0, and 0 &minus; 1 in 32 bits
is 4,294,967,295.</p>
<p><code>s++</code> is computed in <code>int</code> (128) and then converted back to <code>signed char</code>.
That conversion is implementation-defined, and every mainstream compiler wraps it to &minus;128.</p>
<p><b>Different case:</b> overflow of an <code>int</code> itself (<code>INT_MAX + 1</code>) is <em>undefined
behaviour</em>. On this site it stops the program with a runtime error.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> What happens when a value goes past the
largest or smallest number its type can hold ("wrap-around").</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Type</th><th>Bits</th><th>Smallest</th><th>Largest</th></tr>
<tr><td><code>unsigned char</code></td><td>8</td><td>0</td><td>2<sup>8</sup> &minus; 1</td></tr>
<tr><td><code>signed char</code></td><td>8</td><td>&minus;2<sup>7</sup></td><td>2<sup>7</sup> &minus; 1</td></tr>
<tr><td><code>unsigned int</code></td><td>32</td><td>0</td><td>2<sup>32</sup> &minus; 1</td></tr>
</table>
<p>Powers you may need: 2<sup>7</sup> = 128, 2<sup>8</sup> = 256, 2<sup>32</sup> = 4,294,967,296.</p>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Unsigned types wrap</td><td>The result is taken modulo 2<sup>N</sup> (N = number of bits). Going above
the largest value starts again at the smallest; going below 0 continues from the largest. Like a clock.</td></tr>
<tr><td><code>s++</code> on a <code>signed char</code></td><td>C does the +1 in <code>int</code>, then stores the
result back into the 8-bit <code>signed char</code>. If it does not fit, clang (and every common compiler) keeps
the low 8 bits: the same as adding or subtracting 256 until the value fits.</td></tr>
<tr><td><code>%d</code> with a <code>char</code></td><td>The char is turned into an <code>int</code> first, so the
<b>number</b> is printed, not a letter.</td></tr>
<tr><td><code>%u</code></td><td>Prints an <code>unsigned int</code> as a normal decimal number.</td></tr>
</table>
<h4>Picture: the same idea with tiny 3-bit numbers</h4>
<pre>bit pattern:      000 001 010 011 100 101 110 111 | 000 ...
3-bit unsigned:    0   1   2   3   4   5   6   7  |  0  ...  (7 + 1 -&gt; 0)
3-bit signed:      0   1   2   3  -4  -3  -2  -1  |  0  ...  (3 + 1 -&gt; -4)

The numbers sit on a circle: after the last one comes the first one.</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each variable, find its type and its range from the table.</li>
<li>Do the <code>++</code> or <code>--</code> as normal school arithmetic.</li>
<li>If the answer is outside the range, move it back into the range by adding or subtracting
2<sup>N</sup> (256 for 8 bits, 2<sup>32</sup> for 32 bits).</li>
</ol>
</details>"""))

add(Q("pr_ptr", S, "*p++, *++p, ++*p", "c",
r"""#include <stdio.h>

int main(void)
{
    int arr[] = {10, 20, 30, 40};
    int *p = arr;
    int x1 = *p++;
    int x2 = *p;
    int x3 = *++p;
    int x4 = ++*p;
    int x5 = (*p)++;
    printf("%d %d %d %d %d\n", x1, x2, x3, x4, x5);
    printf("%d %d\n", arr[2], (int)(p - arr));
    return 0;
}
""",
"10 20 30 31 31\n32 2\n",
r"""<p>Postfix <code>++</code> binds tighter than <code>*</code>; prefix <code>++</code> and <code>*</code> bind
right to left.</p>
<ul><li><code>*p++</code> = <code>*(p++)</code>: read 10, then move to <code>arr[1]</code>.</li>
<li><code>*++p</code>: move to <code>arr[2]</code> first, read 30.</li>
<li><code>++*p</code>: increment the <em>value</em>: <code>arr[2]</code> becomes 31.</li>
<li><code>(*p)++</code>: give 31, then <code>arr[2]</code> becomes 32.</li></ul>
<p><code>p</code> stays at <code>arr[2]</code>, so <code>p - arr</code> is 2 (elements, not bytes).</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Reading pointer expressions where
<code>*</code> (read the value) and <code>++</code> (add 1) are mixed. You must know which one is done first,
and whether the <em>pointer</em> moves or the <em>value</em> changes.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Means</th><th>Does <code>p</code> move?</th><th>Does the array change?</th><th>Value it gives</th></tr>
<tr><td><code>*p++</code></td><td><code>*(p++)</code></td><td>yes, one element forward, <b>after</b> the read</td><td>no</td><td>the element at the <b>old</b> position</td></tr>
<tr><td><code>*++p</code></td><td><code>*(++p)</code></td><td>yes, one element forward, <b>before</b> the read</td><td>no</td><td>the element at the <b>new</b> position</td></tr>
<tr><td><code>++*p</code></td><td><code>++(*p)</code></td><td>no</td><td>yes, the element goes up by 1</td><td>the <b>new</b> value</td></tr>
<tr><td><code>(*p)++</code></td><td>brackets first</td><td>no</td><td>yes, the element goes up by 1</td><td>the <b>old</b> value</td></tr>
</table>
<ul>
<li>"One element forward" for an <code>int *</code> means the next <code>int</code> in the array.</li>
<li><code>p - arr</code> is the distance between two pointers counted in <b>elements</b>, not bytes.</li>
<li>The <code>(int)</code> cast is only there so <code>%d</code> prints the distance correctly.</li>
</ul>
<h4>Picture at the start</h4>
<pre>index:     [0]    [1]    [2]    [3]
arr:     |  10  |  20  |  30  |  40  |
            ^
            p          (p points at arr[0] before the first line)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Copy the picture. After each line, move the arrow and/or change the number in a box, using the
table.</li>
<li>Write down the value each line stores in <code>x1</code> &hellip; <code>x5</code>.</li>
<li>At the end, read <code>arr[2]</code> from your picture and count how many boxes <code>p</code> is from
the start.</li>
</ol>
</details>"""))

add(Q("pr_dptr", S, "Pointer to a pointer", "c",
r"""#include <stdio.h>

int main(void)
{
    int v = 3, w = 8;
    int *q = &v;
    int **pp = &q;
    **pp = 9;
    *pp = &w;
    *q += 1;
    printf("%d %d %d\n", v, w, **pp);
    return 0;
}
""",
"9 9 9\n",
r"""<p><code>**pp = 9</code> writes through <code>q</code> into <code>v</code>. <code>*pp = &amp;w</code> changes
<code>q</code> itself, so <code>q</code> now points at <code>w</code>, and <code>*q += 1</code> makes
<code>w</code> 9.</p>
<p>A double pointer is what you pass when a function must change the caller's <em>pointer</em>, for example
<code>alloc(int **p)</code> or inserting at the head of a linked list.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> A pointer to a pointer
(<code>int **</code>). You must see whether a line changes an <code>int</code>, or changes <em>where a
pointer points</em>.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>&amp;v</code></td><td>The address of <code>v</code>.</td></tr>
<tr><td><code>*q</code></td><td>The variable that <code>q</code> points at.</td></tr>
<tr><td><code>pp</code> holds <code>&amp;q</code></td><td>So <code>*pp</code> <b>is</b> <code>q</code> itself
(the pointer), and <code>**pp</code> is the <code>int</code> that <code>q</code> points at.</td></tr>
<tr><td><code>**pp = 9;</code></td><td>Writes into the <code>int</code> that <code>q</code> points at right now.</td></tr>
<tr><td><code>*pp = &amp;w;</code></td><td>Writes into <code>q</code>: <code>q</code> now points somewhere else.</td></tr>
<tr><td><code>*q += 1;</code></td><td>Adds 1 to whatever <code>q</code> points at <b>at that moment</b>.</td></tr>
</table>
<h4>Picture at the start</h4>
<pre>   pp              q               v
 [ &amp;q ] ------&gt; [ &amp;v ] ------&gt; [ 3 ]

                                   w
                                 [ 8 ]</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Copy the picture.</li>
<li>For each line, follow the arrows: one <code>*</code> = follow one arrow. Then change the box you land
on (a number, or the arrow inside <code>q</code>).</li>
<li>For the <code>printf</code>, read <code>v</code>, <code>w</code>, and follow two arrows from
<code>pp</code>.</li>
</ol>
</details>"""))

add(Q("pr_strlit", S, "String literals are arrays", "c",
r"""#include <stdio.h>

int main(void)
{
    printf("%c %s\n", *("abcd" + 2), "abcd" + 1);
    printf("%c\n", 3["hello"]);
    char s[] = "hello";
    s[0] = 'j';
    printf("%s %c\n", s, *s + 1);
    return 0;
}
""",
"c bcd\nl\njello k\n",
r"""<p>A string literal is a <code>char</code> array, and in an expression it becomes a pointer to its first
character. <code>"abcd" + 2</code> points at <code>'c'</code>; <code>"abcd" + 1</code> is the string
<code>"bcd"</code>.</p>
<p><code>a[i]</code> means <code>*(a + i)</code>, and addition commutes, so <code>3["hello"]</code> is
<code>"hello"[3]</code> = <code>'l'</code>.</p>
<p><code>char s[] = "hello"</code> copies the literal into a writable array. (Writing into a literal through
<code>char *t = "hello"</code> is undefined behaviour.) <code>*s + 1</code> is <code>'j' + 1</code> = <code>'k'</code>.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> That a string in double quotes is an array
of <code>char</code>, and that indexing and pointer arithmetic work on it like on any other array.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>"abcd"</code></td><td>An array of 5 chars: the 4 letters and a hidden <code>'\0'</code> at the
end. Used in an expression, it becomes a pointer to its first letter.</td></tr>
<tr><td><code>pointer + n</code></td><td>Points <code>n</code> chars further on.</td></tr>
<tr><td><code>a[i]</code></td><td>Is defined as <code>*(a + i)</code>. Because <code>a + i</code> equals
<code>i + a</code>, writing <code>i[a]</code> means exactly the same thing.</td></tr>
<tr><td><code>%c</code></td><td>Prints one character.</td></tr>
<tr><td><code>%s</code></td><td>Takes a pointer and prints characters from there until the
<code>'\0'</code>.</td></tr>
<tr><td><code>char s[] = "hello";</code></td><td>Makes a new array <code>s</code> with its own copy of the
letters. You may change this copy.</td></tr>
<tr><td><code>*s + 1</code></td><td><code>*</code> is done before <code>+</code>, so this is
<code>(*s) + 1</code>: the code of the first char, plus 1.</td></tr>
<tr><td>Letter codes (ASCII)</td><td>Small letters have codes that follow each other: <code>'a'</code> = 97,
<code>'b'</code> = 98, &hellip;, <code>'z'</code> = 122. So the code + 1 is the next letter of the
alphabet.</td></tr>
</table>
<h4>Picture of the two literals</h4>
<pre>"abcd":   index:   0     1     2     3     4
                 'a'   'b'   'c'   'd'   '\0'

"hello":  index:   0     1     2     3     4     5
                 'h'   'e'   'l'   'l'   'o'   '\0'</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Turn every pointer expression into "start at index n" using the picture.</li>
<li>For <code>%c</code>, print the one letter at that index. For <code>%s</code>, print from that index up to
(not including) the <code>'\0'</code>.</li>
<li>For the array <code>s</code>, first apply the change <code>s[0] = 'j'</code> to your picture.</li>
</ol>
</details>"""))

add(Q("pr_sizeof", S, "sizeof vs strlen", "c",
r"""#include <stdio.h>
#include <string.h>

int main(void)
{
    char s[] = "Qualcomm";
    char *t = "Qualcomm";
    printf("%d %d %d %d\n", (int)sizeof(s), (int)strlen(s), (int)sizeof(t), (int)strlen(t));
    char u[20] = "SoC";
    printf("%d %d\n", (int)sizeof(u), (int)strlen(u));
    return 0;
}
""",
"9 8 4 8\n20 3\n",
r"""<p><code>sizeof</code> of an array counts every byte, including the terminating <code>'\0'</code>: 8
letters + 1 = 9. <code>strlen</code> counts characters up to the <code>'\0'</code>: 8.</p>
<p><code>sizeof(t)</code> is the size of a <em>pointer</em>: 4 here, <b>8 on a 64-bit PC</b> (the usual OA
answer is <code>9 8 8 8</code>).</p>
<p><code>u</code> has 20 bytes whatever it holds, and the unused ones are zero.</p>""",
statement=r"""<p><b>What to do.</b> Read the program and write down exactly what it prints. Work it out on
paper first, then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Whether you can tell an <em>array</em> from a <em>pointer</em>, and
the difference between <code>sizeof</code> (bytes of storage) and <code>strlen</code> (letters before the end
marker).</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Thing</th><th>What it means</th></tr>
<tr><td><code>sizeof(x)</code></td><td>How many bytes the variable <code>x</code> takes in memory. The compiler
works it out from the type. It does not look at what is stored inside.</td></tr>
<tr><td><code>strlen(s)</code></td><td>Starts at <code>s</code> and counts characters until it reaches the
<code>'\0'</code> byte. The <code>'\0'</code> itself is not counted.</td></tr>
<tr><td><code>"abc"</code></td><td>Every string in double quotes gets a hidden <code>'\0'</code> added at the end,
so <code>"abc"</code> uses 4 bytes.</td></tr>
<tr><td>Sizes on this site</td><td><code>char</code> = 1 byte. Any pointer = 4 bytes, because the site compiles for
32-bit WebAssembly. On a 64-bit PC, which most OA papers assume, a pointer is 8 bytes.</td></tr>
</table>
<h4>Picture of the three variables</h4>
<pre>char s[] = "...";   s is an ARRAY: its boxes hold the letters
                    themselves, and it is made just big enough
                    for them, '\0' included

char *t = "...";    t is a POINTER: one box holding an address
   t: [ address ] ---&gt; [ letters ... | \0 ]
                        (the letters live somewhere else)

char u[20] = "..."; u is an ARRAY of exactly 20 boxes: letters
                    first, then '\0', the rest are zero</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each <code>sizeof</code>, first decide: array or pointer? For an array, count its boxes. For a pointer,
the answer is the size of one pointer.</li>
<li>For each <code>strlen</code>, count the letters up to the first <code>'\0'</code>.</li>
<li>The casts to <code>(int)</code> are only there so that <code>%d</code> prints the values correctly.</li>
</ol>
</details>"""))

add(Q("pr_decay", S, "Arrays decay in function calls", "c",
r"""#include <stdio.h>

void f(int a[10])
{
    printf("%d\n", (int)sizeof(a));
}

int main(void)
{
    int a[10];
    printf("%d %d\n", (int)sizeof(a), (int)(sizeof(a) / sizeof(a[0])));
    f(a);
    return 0;
}
""",
"40 10\n4\n",
r"""<p>In <code>main</code>, <code>a</code> is a real array: 10 &times; 4 = 40 bytes, and
<code>sizeof(a) / sizeof(a[0])</code> is the usual element-count idiom.</p>
<p>A parameter written <code>int a[10]</code> is really <code>int *a</code>: the array <em>decays</em> to a
pointer, and the 10 is ignored. So <code>sizeof(a)</code> inside <code>f</code> is the pointer size (4 here, 8 on
a 64-bit PC). Clang even warns: "sizeof on array function parameter will return size of 'int *'". That is
why C functions take the length as a separate argument.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> That an array passed to a function arrives
as a <em>pointer</em> to its first element. This is called "array decay". Inside the function,
<code>sizeof</code> then measures the pointer, not the array.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Sizes on this site</td><td><code>int</code> = 4 bytes. Every pointer = 4 bytes, because the site
compiles for 32-bit WebAssembly. On a 64-bit PC, which most OA papers assume, a pointer is 8 bytes.</td></tr>
<tr><td><code>sizeof</code> of a real array</td><td>Number of elements &times; size of one element.</td></tr>
<tr><td><code>sizeof(a) / sizeof(a[0])</code></td><td>Whole array &divide; one element = the number of
elements.</td></tr>
<tr><td>Parameter written <code>int a[10]</code></td><td>The compiler treats it as <code>int *a</code>. The
10 is ignored. The function only receives the address of the first element.</td></tr>
<tr><td><code>(int)</code> casts</td><td>Only there so that <code>%d</code> prints the values correctly.</td></tr>
</table>
<h4>Picture</h4>
<pre>in main:  a = [ int | int | int | int | int | int | int | int | int | int ]
              (the real array: 10 boxes, each 4 bytes)

in f:     a = [ address ] ---&gt; points at main's first box
              (one pointer, whatever the [10] in the parameter says)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>There are two different variables called <code>a</code>. For each <code>sizeof</code>, decide which
one it sees.</li>
<li>For the real array, multiply. For the parameter, use the pointer size of this site.</li>
</ol>
</details>"""))

add(Q("pr_swap", S, "Pass by value, even for pointers", "c",
r"""#include <stdio.h>

void swap_bad(int *p, int *q)  { int *t = p; p = q; q = t; }
void swap_good(int *p, int *q) { int t = *p; *p = *q; *q = t; }
void set_bad(int *p)           { static int seven = 7; p = &seven; }

int main(void)
{
    int m = 1, n = 2;
    swap_bad(&m, &n);
    printf("%d %d\n", m, n);
    swap_good(&m, &n);
    printf("%d %d\n", m, n);
    int *h = NULL;
    set_bad(h);
    printf("%s\n", h ? "set" : "NULL");
    return 0;
}
""",
"1 2\n2 1\nNULL\n",
r"""<p>C passes <em>everything</em> by value. <code>swap_bad</code> swaps its own copies of the two addresses, which
changes nothing outside. <code>swap_good</code> swaps the values the addresses point at.</p>
<p><code>set_bad</code> changes its copy of <code>h</code>. To change the caller's pointer, pass its address:
<code>void set_good(int **p) { *p = &amp;seven; }</code> and call <code>set_good(&amp;h)</code>. The same bug with
<code>malloc</code> also leaks memory.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> That C passes every argument <em>by
value</em> (as a copy), even pointers. A function can change the caller's variable only by writing
<em>through</em> a pointer, not by changing the pointer itself.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Arguments are copies</td><td>A function gets its own copy of each argument. Changing the copy does
not change the caller's variable.</td></tr>
<tr><td>Pointer argument</td><td>The function gets a copy of the <b>address</b>. <code>p = q;</code> only
changes the copy (where this copy points). <code>*p = ...;</code> writes into the variable at that address,
which is the caller's variable.</td></tr>
<tr><td><code>static int seven</code></td><td>Lives for the whole program, so <code>&amp;seven</code> is a valid
address. (This does not change the rule above.)</td></tr>
<tr><td><code>h ? "set" : "NULL"</code></td><td>A pointer used as a condition is false if it is
<code>NULL</code> and true otherwise. The whole expression picks one of the two strings.</td></tr>
</table>
<h4>Picture of the call <code>swap_bad(&amp;m, &amp;n)</code></h4>
<pre>main:        m [ 1 ]        n [ 2 ]
                 ^              ^
                 |              |
swap_bad:    p [ &amp;m ]       q [ &amp;n ]     &lt;- copies of the two addresses,
                                            they disappear when it returns</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each function, look at every assignment. Does it assign to <code>p</code> (the copy of the address)
or to <code>*p</code> (the caller's variable)?</li>
<li>Only assignments of the second kind are still visible in <code>main</code> after the call.</li>
<li>Keep a running note of <code>m</code>, <code>n</code> and <code>h</code> in <code>main</code>.</li>
</ol>
</details>"""))

add(Q("pr_static", S, "static locals", "c",
r"""#include <stdio.h>

int counter(void) { static int n = 0; n++; return n; }
int plain(void)   { int n = 0; n++; return n; }

int main(void)
{
    counter();
    counter();
    plain();
    plain();
    printf("%d %d\n", counter(), plain());
    return 0;
}
""",
"3 1\n",
r"""<p>A <code>static</code> local is created once, before the program starts (in <code>.bss</code> or
<code>.data</code>, not on the stack), and keeps its value between calls. Its initialiser runs only once.
<code>plain</code>'s <code>n</code> is a new stack variable on every call.</p>
<p>At file scope, <code>static</code> means something else: the name is private to that <code>.c</code> file
(internal linkage).</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> The difference between an ordinary local
variable and a <code>static</code> local variable.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Kind</th><th>Behaviour</th></tr>
<tr><td>Ordinary local (<code>int n = 0;</code>)</td><td>Made new on the stack every time the function is
called. The <code>= 0</code> runs on every call. It disappears when the function returns.</td></tr>
<tr><td><code>static</code> local (<code>static int n = 0;</code>)</td><td>Made only once, before
<code>main</code> starts. The <code>= 0</code> is applied only that one time. It keeps its value from one call
to the next.</td></tr>
<tr><td>Ignoring a return value</td><td><code>counter();</code> on its own line still runs the whole body,
so <code>n++</code> still happens. Only the returned number is thrown away.</td></tr>
<tr><td>Calls inside <code>printf(...)</code></td><td>Both calls run before anything is printed. The two
functions share no data, so their order does not matter here.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Count how many times <code>counter</code> is called in total, including the one inside
<code>printf</code>. Its <code>n</code> keeps growing across these calls.</li>
<li>For <code>plain</code>, each call starts again from scratch. Only the last call's return value is
printed.</li>
</ol>
</details>"""))

add(Q("pr_main_rec", S, "Recursion hidden in main", "c",
r"""#include <stdio.h>

int main(void)
{
    static int calls = 3;
    if (calls-- > 0) {
        printf("%d ", calls);
        main();
    }
    printf("x");
    return 0;
}
""",
"2 1 0 xxxx\n",
r"""<p>C allows <code>main</code> to call itself (C++ does not). All the calls share the one <code>static</code>
<code>calls</code>. Draw the stack:</p>
<ul><li>Call 1: 3 &gt; 0, <code>calls</code> becomes 2, prints <code>2 </code>, calls main.</li>
<li>Call 2: prints <code>1 </code>; call 3: prints <code>0 </code>.</li>
<li>Call 4: 0 &gt; 0 is false (<code>calls</code> becomes &minus;1), prints <code>x</code> and returns.</li>
<li>Calls 3, 2 and 1 each print their own <code>x</code> on the way out: four in all.</li></ul>
<p>A 2026 Qualcomm interview asked a question of this shape.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Recursion (a function calling itself) when
the function is <code>main</code>, together with a <code>static</code> variable shared by all the calls. You
must trace the calls going down <em>and</em> the returns coming back up.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>main</code> calling itself</td><td>Allowed in C (not in C++). It behaves like any other
recursive function.</td></tr>
<tr><td><code>static int calls = 3;</code></td><td>One single variable shared by every call of
<code>main</code>. It is set to 3 only once, before the program starts.</td></tr>
<tr><td><code>calls-- &gt; 0</code></td><td>Compares the <b>old</b> value with 0, then subtracts 1. The
subtraction happens whether the comparison is true or false.</td></tr>
<tr><td><code>printf("%d ", calls)</code></td><td>Runs after the subtraction, so it prints the value
<b>after</b> the <code>--</code>, followed by one space.</td></tr>
<tr><td>Returning from a call</td><td>The caller continues with the next line after the call. Here that is
<code>printf("x")</code>.</td></tr>
<tr><td>Newlines</td><td>The program never prints <code>\n</code>, so everything is on one line.</td></tr>
</table>
<h4>Picture of the call stack</h4>
<pre>main #1  --calls--&gt;  main #2  --calls--&gt;  main #3  --calls--&gt;  ...
   ^                    |  ^                 |  ^
   +----returns---------+  +----returns------+  +--- ...

Going DOWN: each call prints (maybe) a number and calls the next one.
Coming UP:  each call that is still waiting finishes its own last line.</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with one row per call: "value of <code>calls</code> tested", "test true?", "value after
<code>--</code>", "what this call prints before calling".</li>
<li>Stop adding rows at the first call whose test is false.</li>
<li>Then go back up the table: every call (including the last one) prints <code>x</code> once before it
returns. Count how many.</li>
</ol>
</details>"""))

add(Q("pr_const", S, "const pointer or pointer to const?", "c",
r"""#include <stdio.h>

int main(void)
{
    int c1 = 1, c2 = 2;
    const int *pc = &c1;   /* pointer to const int */
    pc = &c2;
    int *const cp = &c1;   /* const pointer to int */
    *cp = 5;
    c2 = 7;
    printf("%d %d %d\n", *pc, *cp, c1);
    return 0;
}
""",
"7 5 5\n",
r"""<p>Read declarations right to left. <code>const int *pc</code> is a "pointer to a const int": the pointer may
move, but <code>*pc = 5</code> would not compile. <code>int *const cp</code> is a "const pointer to an int":
<code>*cp = 5</code> is fine, but <code>cp = &amp;c2</code> would not compile.</p>
<p><code>const</code> only stops changes <em>through that name</em>: <code>c2 = 7</code> is fine, and
<code>*pc</code> sees it. <code>const int *const p</code> fixes both the pointer and the value.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> The difference between a "pointer to a
<code>const</code> int" and a "<code>const</code> pointer to an int", and what <code>const</code> really
protects.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Declaration</th><th>Read it right to left</th><th>Allowed</th><th>Not allowed</th></tr>
<tr><td><code>const int *pc</code></td><td>pc is a pointer to an int that is const</td><td>move it:
<code>pc = &amp;c2;</code></td><td>write through it: <code>*pc = 5;</code></td></tr>
<tr><td><code>int *const cp</code></td><td>cp is a const pointer to an int</td><td>write through it:
<code>*cp = 5;</code></td><td>move it: <code>cp = &amp;c2;</code></td></tr>
</table>
<ul>
<li><code>const</code> only limits what you can do <b>through that name</b>. The variables <code>c1</code> and
<code>c2</code> are not const: they can still be changed directly, and every pointer to them sees the new
value.</li>
<li>This program only does allowed things, so it compiles and runs.</li>
</ul>
<h4>Picture at the start</h4>
<pre>c1 [ 1 ]        c2 [ 2 ]

pc --&gt; ?        cp --&gt; ?      (fill in the arrows as you trace)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Go line by line. When a line sets a pointer, draw (or move) its arrow. When a line writes a number,
change the box it lands in.</li>
<li>For the <code>printf</code>, follow each arrow to its box and read <code>c1</code> directly.</li>
</ol>
</details>"""))

add(Q("pr_ret_static", S, "Returning a pointer from a function", "c",
r"""#include <stdio.h>

int *next_id(void)
{
    static int id = 100;   /* without "static" this would be a dangling pointer */
    id++;
    return &id;
}

int main(void)
{
    int *a = next_id();
    int *b = next_id();
    (*a)++;
    printf("%d %d %d\n", *a, *b, a == b);
    return 0;
}
""",
"103 103 1\n",
r"""<p>Both calls return the address of the same <code>static</code> variable, so <code>a == b</code>. After the
two calls <code>id</code> is 102, and <code>(*a)++</code> makes it 103. Both pointers see 103.</p>
<p><b>Interview version:</b> if <code>id</code> were an ordinary local, it would die when the function returns,
and <code>a</code> would be a <em>dangling pointer</em>. Using it is undefined behaviour: it might still show the
old value, or garbage once another call reuses that stack space. Fixes: <code>static</code>, <code>malloc</code>
(the caller frees), or have the caller pass a buffer in.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Returning the address of a
<code>static</code> local variable, and what it means when two pointers hold the same address.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>static int id = 100;</code></td><td>One variable that lives for the whole program. It is set to
100 only once. Every call of <code>next_id</code> uses this same variable.</td></tr>
<tr><td><code>return &amp;id;</code></td><td>Returns the address of that one variable. The address is still
valid after the function returns, because the variable is static.</td></tr>
<tr><td><code>(*a)++</code></td><td>Adds 1 to the variable <code>a</code> points at.</td></tr>
<tr><td><code>a == b</code></td><td>Compares the two <b>addresses</b>. Gives 1 if they are the same, 0 if not.</td></tr>
<tr><td>Inside <code>printf</code></td><td>All the values are read when <code>printf</code> is called, after
every line above it has run.</td></tr>
</table>
<h4>Picture</h4>
<pre>static memory (made before main starts):   id [ 100 ]

main's stack:   a [ ? ]    b [ ? ]     (each will hold an address)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Ask first: how many variables called <code>id</code> exist? Then which address does each call
return?</li>
<li>Track the value of <code>id</code> through both calls and the <code>(*a)++</code>.</li>
<li><code>*a</code> and <code>*b</code> both read the box their pointer holds.</li>
</ol>
</details>"""))

add(Q("pr_struct", S, "Struct padding and unions", "c",
r"""#include <stdio.h>

struct S1 { char c; int i; char d; };
struct S2 { int i; char c; char d; };
struct S3 { char c; double x; };
union U   { int i; char c[4]; };

int main(void)
{
    printf("%d %d %d %d\n", (int)sizeof(struct S1), (int)sizeof(struct S2),
           (int)sizeof(struct S3), (int)sizeof(union U));
    union U u;
    u.i = 0x01020304;
    printf("%d %d\n", u.c[0], u.c[3]);
    return 0;
}
""",
"12 8 16 4\n4 1\n",
r"""<p>Each member sits at a multiple of its own alignment, and the struct's size is rounded up to a multiple of
its largest alignment.</p>
<ul><li><code>S1</code>: c (1) + 3 padding + i (4) + d (1) + 3 padding = 12.</li>
<li><code>S2</code>: i (4) + c + d (2) + 2 padding = 8. Largest members first wastes the least space.</li>
<li><code>S3</code>: c (1) + 7 padding + x (8) = 16.</li>
<li>A union's members share memory, so its size is that of its largest member: 4.</li></ul>
<p>On a <b>little-endian</b> machine (x86, Arm, this site) the lowest address holds the least significant byte,
so <code>c[0]</code> is 4 and <code>c[3]</code> is 1. Big-endian would give 1 and 4. This is the standard
"detect endianness" trick.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How the compiler lays out a
<code>struct</code> in memory (with <em>padding</em> bytes), how big a <code>union</code> is, and the byte
order of the machine (<em>endianness</em>).</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Type (on this site)</th><th>Size in bytes</th><th>Alignment</th></tr>
<tr><td><code>char</code></td><td>1</td><td>1 (any address)</td></tr>
<tr><td><code>short</code></td><td>2</td><td>2 (address a multiple of 2)</td></tr>
<tr><td><code>int</code></td><td>4</td><td>4 (address a multiple of 4)</td></tr>
<tr><td><code>double</code></td><td>8</td><td>8 (address a multiple of 8)</td></tr>
</table>
<ol>
<li><b>Order:</b> members are stored in the order they are written.</li>
<li><b>Each member</b> starts at the next offset that is a multiple of its alignment. Skipped bytes are
<em>padding</em> (unused).</li>
<li><b>The end:</b> the total size is rounded up to a multiple of the <b>largest</b> alignment in the struct,
so that in an array of these structs every member stays aligned.</li>
<li><b>A union:</b> all members start at offset 0 and share the same bytes. Its size is the size of its largest
member (rounded up the same way).</li>
<li><b>Little-endian</b> (this site, x86, Arm): an <code>int</code> is stored with its <b>least significant</b>
byte at the lowest address.</li>
<li><code>%d</code> with a <code>char</code> prints the char's number. In hex, each pair of digits is one byte:
<code>0x11223344</code> has the bytes 0x11, 0x22, 0x33, 0x44 (most significant first).</li>
</ol>
<h4>Worked example (a different struct)</h4>
<pre>struct X { char a; short b; };

offset:   0     1     2     3
        [ a  | pad |  b  |  b  ]   a at 0; b needs an even offset,
                                   so byte 1 is padding;
                                   size = 4 (already a multiple of 2)

int 0x11223344 on a little-endian machine:
address:  +0    +1    +2    +3
        [ 44 | 33  | 22  | 11  ]   (lowest address = least significant)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each struct, draw a row of byte boxes numbered 0, 1, 2, &hellip; and place the members one by one
using rules 1&ndash;2.</li>
<li>Then apply rule 3 to the total.</li>
<li>For the union, <code>c[0]</code> is the byte at address +0 of <code>i</code> and <code>c[3]</code> the byte
at +3. Write <code>0x01020304</code> into four boxes the little-endian way.</li>
</ol>
</details>"""))

add(Q("pr_macro", S, "Macros are text substitution", "c",
r"""#include <stdio.h>

#define SQ(x)     x * x
#define SQ2(x)    ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int main(void)
{
    printf("%d %d\n", SQ(2 + 3), SQ2(2 + 3));
    printf("%d\n", 100 / SQ(5));
    int i = 3;
    int m = MAX(i++, 2);
    printf("%d %d\n", m, i);
    return 0;
}
""",
"11 25\n100\n4 5\n",
r"""<p>The preprocessor pastes text before the compiler sees it.</p>
<ul><li><code>SQ(2 + 3)</code> becomes <code>2 + 3 * 2 + 3</code> = 11. With brackets, <code>SQ2</code> gives 25.</li>
<li><code>100 / SQ(5)</code> becomes <code>100 / 5 * 5</code> = 100: you need brackets around the
<em>whole</em> body too.</li>
<li><code>MAX(i++, 2)</code> becomes <code>((i++) &gt; (2) ? (i++) : (2))</code>: the test reads 3 (i becomes 4),
then the chosen branch reads 4 (i becomes 5). An argument with a side effect is evaluated twice. A
<code>static inline</code> function avoids this.</li></ul>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> That a <code>#define</code> macro is pure
<em>text replacement</em>, done before the compiler sees the code. Missing brackets and arguments with
<code>++</code> give surprising results.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Macro expansion</td><td>Every use like <code>SQ(something)</code> is replaced by the macro body, with
<code>x</code> replaced by <b>exactly the text you wrote</b>. No brackets are added for you.</td></tr>
<tr><td>Then normal C rules</td><td><code>*</code> and <code>/</code> are done before <code>+</code> and
<code>-</code>. <code>*</code> and <code>/</code> have the same rank and go left to right.</td></tr>
<tr><td><code>c ? a : b</code></td><td>Work out <code>c</code>. If true, work out only <code>a</code>; otherwise
only <code>b</code>.</td></tr>
<tr><td><code>i++</code></td><td>Gives the old value, then adds 1. If the text <code>i++</code> appears twice
after expansion and both copies run, <code>i</code> goes up twice.</td></tr>
</table>
<h4>Worked example (a different macro)</h4>
<pre>#define DBL(x) x + x

3 * DBL(4)   becomes   3 * 4 + 4   =  12 + 4  =  16      (not 3 * 8 = 24)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each macro use, write out the replaced text on paper, character by character.</li>
<li>Only then calculate, using the normal order of operations.</li>
<li>For <code>MAX(i++, 2)</code>, count how many copies of <code>i++</code> actually run, and what value each
copy gives.</li>
</ol>
</details>"""))

add(Q("pr_switch", S, "switch fall-through", "c",
r"""#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 4; i++) {
        switch (i) {
        case 0: printf("a");
        case 1: printf("b"); break;
        case 2: printf("c");
        default: printf("d");
        }
    }
    printf("\n");
    return 0;
}
""",
"abbcdd\n",
r"""<p>Without <code>break</code>, execution falls through into the next case.</p>
<ul><li>i = 0: prints <code>a</code>, falls into case 1, prints <code>b</code>, then breaks.</li>
<li>i = 1: <code>b</code>.</li>
<li>i = 2: <code>c</code>, then falls into <code>default</code>: <code>d</code>.</li>
<li>i = 3: <code>default</code>: <code>d</code>.</li></ul>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> <em>Fall-through</em> in a
<code>switch</code>: without <code>break</code>, execution continues into the next case.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Where it starts</td><td><code>switch (i)</code> jumps to the <code>case</code> whose value equals
<code>i</code>. If no case matches, it jumps to <code>default</code>.</td></tr>
<tr><td>Where it stops</td><td>From there it runs every statement below, <b>across later case labels</b>, until
it reaches a <code>break</code> or the closing <code>}</code> of the switch. Case labels are only entry points,
not walls.</td></tr>
<tr><td><code>break</code></td><td>Leaves the <code>switch</code> only. The <code>for</code> loop goes on to the
next <code>i</code>.</td></tr>
<tr><td>No newlines</td><td><code>printf("a")</code> etc. print no newline, so everything is on one line until
the final <code>printf("\n")</code>.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>The loop runs for <code>i</code> = 0, 1, 2, 3. Take each value in turn.</li>
<li>Find the label where execution enters. Put your finger there and move down, writing each letter printed,
until you hit <code>break</code> or the end of the switch.</li>
<li>Join all the letters together in order.</li>
</ol>
</details>"""))

add(Q("pr_printf", S, "printf returns a number", "c",
r"""#include <stdio.h>

int main(void)
{
    int n = printf("Qualcomm\n");
    printf("%d\n", n);
    printf("%d\n", printf("%d", 123));
    return 0;
}
""",
"Qualcomm\n9\n1233\n",
r"""<p><code>printf</code> returns how many characters it printed. <code>"Qualcomm\n"</code> is 8 letters + the newline = 9.</p>
<p>On the last line the inner call runs first: it prints <code>123</code> and returns 3. Then the outer call
prints <code>3</code> and a newline, so the line reads <code>1233</code>.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> That <code>printf</code> is a function
that returns a number, and in which order nested calls print.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Return value</td><td><code>printf</code> returns an <code>int</code>: how many characters it printed.
The newline <code>\n</code> counts as one character.</td></tr>
<tr><td>Example</td><td><code>printf("Hi\n")</code> prints <code>Hi</code> and a newline, and returns 3.</td></tr>
<tr><td>Nested calls</td><td>Before a function can be called, all its arguments must be worked out. So in
<code>printf("%d\n", printf(...))</code> the <b>inner</b> <code>printf</code> runs (and prints) first.</td></tr>
<tr><td><code>printf("%d", 123)</code></td><td>Prints the digits with no newline after them.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Write the screen as a list of characters, adding to it in the order things are printed.</li>
<li>For each <code>printf</code> whose result is used, count the characters it printed (letters, digits and
<code>\n</code>).</li>
<li>On the last line, the inner call's characters come first, then the outer call's. Nothing separates
them.</li>
</ol>
</details>"""))

add(Q("pr_comma", S, "The comma operator in a for loop", "c",
r"""#include <stdio.h>

int main(void)
{
    int i, j, n = 0;
    for (i = 0, j = 10; i < j; i += 2, j -= 3)
        n++;
    printf("%d %d %d\n", i, j, n);
    return 0;
}
""",
"4 4 2\n",
r"""<p>The comma operator evaluates the left side, then the right side, and gives the right side's value. Here
it updates two variables in one step.</p>
<p>(0, 10): body runs, n = 1. (2, 7): body runs, n = 2. (4, 4): 4 &lt; 4 is false, so the loop stops.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How a <code>for</code> loop runs step by
step, with two variables changed at once using the <em>comma operator</em>.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>for (init; test; step) body</code></td><td>1. Run <code>init</code> once. 2. Check
<code>test</code>; if false, the loop ends. 3. Run <code>body</code>. 4. Run <code>step</code>. 5. Go back to
2.</td></tr>
<tr><td>Comma operator <code>x, y</code></td><td>Does <code>x</code> first, then <code>y</code>. Here it lets
<code>init</code> and <code>step</code> change two variables.</td></tr>
<tr><td><code>i += 2</code>, <code>j -= 3</code></td><td>Add 2 to <code>i</code>; subtract 3 from
<code>j</code>.</td></tr>
<tr><td>After the loop</td><td><code>i</code> and <code>j</code> keep the values they had when the test
failed.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns <code>i</code>, <code>j</code>, "<code>i &lt; j</code>?", <code>n</code>.</li>
<li>Start with the <code>init</code> values. In each row: test; if true add 1 to <code>n</code>, then apply the
step to get the next row.</li>
<li>Stop at the first row where the test is false. That row has the final <code>i</code> and
<code>j</code>.</li>
</ol>
</details>"""))

add(Q("pr_while", S, "while (x--) and while (--x)", "c",
r"""#include <stdio.h>

int main(void)
{
    int x = 3;
    while (x--)
        printf("%d ", x);
    printf("| %d\n", x);

    int y = 3;
    while (--y)
        printf("%d ", y);
    printf("| %d\n", y);
    return 0;
}
""",
"2 1 0 | -1\n2 1 | 0\n",
r"""<p><code>while (x--)</code> tests the <em>old</em> value, then decrements. Tests 3, 2, 1 pass and print 2, 1, 0.
The test of 0 fails, but the decrement still happens, so <code>x</code> ends at &minus;1.</p>
<p><code>while (--y)</code> decrements first: the loop sees 2 and 1, stops at 0, and <code>y</code> stays 0.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> The difference between
<code>while (x--)</code> and <code>while (--x)</code>: which value is tested, and what the variable holds
when the loop ends.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>while (cond) body</code></td><td>Work out <code>cond</code>. If it is not 0, run the body and
repeat. If it is 0, stop.</td></tr>
<tr><td><code>while (x--)</code></td><td>Tests the <b>old</b> value of <code>x</code>, then subtracts 1. The
subtraction also happens on the last test, the one that fails.</td></tr>
<tr><td><code>while (--y)</code></td><td>Subtracts 1 first, then tests the <b>new</b> value.</td></tr>
<tr><td>Inside the body</td><td><code>printf("%d ", x)</code> prints the value after the subtraction,
followed by a space.</td></tr>
<tr><td><code>"| %d\n"</code></td><td>Prints a bar, a space, the number, then ends the line.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns: "value tested", "test passes?", "value after the <code>--</code>", "printed
by the body".</li>
<li>Fill one row per test, including the test that fails.</li>
<li>The number after the bar is the variable's value after the last row.</li>
</ol>
</details>"""))

add(Q("pr_bits", S, "Bitwise operators", "c",
r"""#include <stdio.h>

int main(void)
{
    printf("%d %d %d\n", 1 << 4, 0x0F & 0x3C, 5 ^ 3);
    printf("%d %d %d\n", 0x0F | 0x30, ~5, -8 >> 1);
    printf("%u %x\n", ~0u, 0xF0u >> 4);
    unsigned a = 29, b = 15, d = a ^ b, c = 0;
    while (d) {
        d &= d - 1;
        c++;
    }
    printf("%u\n", c);
    return 0;
}
""",
"16 12 6\n63 -6 -4\n4294967295 f\n2\n",
r"""<ul><li><code>0x0F &amp; 0x3C</code> = 0000 1111 &amp; 0011 1100 = 0000 1100 = 12. <code>5 ^ 3</code> = 101 ^ 011 = 110 = 6.</li>
<li><code>~x</code> = &minus;x &minus; 1 in two's complement, so <code>~5</code> = &minus;6.</li>
<li>Right-shifting a negative number is implementation-defined; compilers do an arithmetic shift (copy the sign
bit), so &minus;8 &gt;&gt; 1 = &minus;4.</li>
<li><code>d &amp;= d - 1</code> clears the lowest set bit, so the loop counts the 1s. 29 ^ 15 = 11101 ^ 01111 =
10010: two bits differ. "How many bits must flip to turn a into b?" was a 2026 interview question.</li></ul>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> The bitwise operators <code>&lt;&lt;</code>,
<code>&gt;&gt;</code>, <code>&amp;</code>, <code>|</code>, <code>^</code>, <code>~</code>, hex numbers, and a
classic loop that counts 1-bits.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Operator</th><th>Meaning</th></tr>
<tr><td><code>a &lt;&lt; n</code></td><td>Shift the bits left by <code>n</code> places, filling with 0s. For small
positive numbers this is <code>a &times; 2<sup>n</sup></code>.</td></tr>
<tr><td><code>a &gt;&gt; n</code></td><td>Shift right by <code>n</code> places. For an unsigned number, 0s come in
from the left. For a <b>negative</b> <code>int</code>, clang copies the sign bit in from the left (arithmetic
shift). That equals dividing by 2<sup>n</sup> and rounding <b>down</b> (towards minus infinity).</td></tr>
<tr><td><code>a &amp; b</code></td><td>AND: a result bit is 1 only where <b>both</b> bits are 1.</td></tr>
<tr><td><code>a | b</code></td><td>OR: 1 where <b>at least one</b> bit is 1.</td></tr>
<tr><td><code>a ^ b</code></td><td>XOR: 1 where the two bits are <b>different</b>.</td></tr>
<tr><td><code>~a</code></td><td>NOT: flips every bit. For a signed <code>int</code> (two's complement),
<code>~a</code> equals <code>&minus;a &minus; 1</code>.</td></tr>
<tr><td><code>0u</code>, <code>0xF0u</code></td><td>The <code>u</code> makes the number an <code>unsigned int</code>
(32 bits). <code>~0u</code> has all 32 bits set to 1. Note 2<sup>32</sup> = 4,294,967,296.</td></tr>
<tr><td><code>%u</code> / <code>%x</code></td><td><code>%u</code> prints an unsigned int in decimal. <code>%x</code>
prints it in hex, with small letters, no <code>0x</code> and no leading zeros.</td></tr>
<tr><td><code>d &amp;= d - 1</code></td><td>Clears the lowest 1-bit of <code>d</code>. Example: 12 = 1100, 11 =
1011, 1100 &amp; 1011 = 1000.</td></tr>
</table>
<h4>Data: hex digits and powers of 2</h4>
<pre>hex:   0    1    2    3    4    5    6    7
bin:  0000 0001 0010 0011 0100 0101 0110 0111
hex:   8    9    A    B    C    D    E    F
bin:  1000 1001 1010 1011 1100 1101 1110 1111   (A=10 B=11 ... F=15)

A two-digit hex number 0xHL = H*16 + L.   Example: 0x2B = 2*16 + 11 = 43

bit:    7    6    5    4    3    2    1    0
value: 128   64   32   16    8    4    2    1</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Write each number in binary (use 8 bits for the small ones), one under the other so the bits line up.</li>
<li>Apply the operator column by column, then turn the binary result back into decimal (or hex for
<code>%x</code>).</li>
<li>For the last part, first find <code>a ^ b</code> in binary. Then each pass of the loop removes one 1-bit,
and <code>c</code> counts the passes.</li>
</ol>
</details>"""))

add(Q("pr_bitfield", S, "Bit-fields", "c",
r"""#include <stdio.h>

struct Reg {
    unsigned en   : 1;
    unsigned mode : 3;
    unsigned div  : 4;
};

int main(void)
{
    struct Reg r = {0};
    unsigned v1 = 3, v2 = 9, v3 = 15;
    r.en = v1;
    r.mode = v2;
    r.div = v3;
    printf("%u %u %u %d\n", r.en, r.mode, r.div, (int)sizeof r);
    return 0;
}
""",
"1 1 15 4\n",
r"""<p>A bit-field keeps only its low bits: 3 = 11<sub>2</sub> in 1 bit gives 1; 9 = 1001<sub>2</sub> in 3 bits gives
001 = 1; 15 fits in 4 bits.</p>
<p>The 8 bits are packed into one <code>unsigned int</code>, so the struct is 4 bytes. The bit order inside the
word is implementation-defined, which is why driver code for hardware registers usually uses masks and shifts
instead of bit-fields.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> <em>Bit-fields</em>: struct members that
are only a few bits wide, as used for hardware registers. What happens to a value that is too big for its
field, and how big the struct is.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>unsigned mode : 3;</code></td><td>A field that is 3 bits wide. An N-bit unsigned field holds 0 to
2<sup>N</sup> &minus; 1.</td></tr>
<tr><td>Storing a value that is too big</td><td>Only the <b>lowest N bits</b> are kept; the higher bits are thrown
away (the same as <code>value % 2<sup>N</sup></code>). There is no error at run time.</td></tr>
<tr><td><code>struct Reg r = {0};</code></td><td>Starts every field at 0.</td></tr>
<tr><td>Packing on this site</td><td>clang puts consecutive <code>unsigned</code> bit-fields into one
<code>unsigned int</code> (32 bits = 4 bytes) as long as they fit. The size of the struct is a whole number of
these 4-byte units.</td></tr>
<tr><td>Example</td><td>A 2-bit field given 6: 6 = 110 in binary, the low 2 bits are 10, so the field holds
2.</td></tr>
</table>
<h4>Picture of the storage unit (bit order as clang uses it here)</h4>
<pre>bit:  31 ................... 8   7  6  5  4   3  2  1   0
     [   not used               |    div     |  mode   | en ]
                                   (4 bits)    (3 bits)  (1)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Write each value (<code>v1</code>, <code>v2</code>, <code>v3</code>) in binary.</li>
<li>Keep only as many low bits as its field is wide, and turn them back into decimal.</li>
<li>For <code>sizeof r</code>, add up the widths and decide how many 32-bit units are needed.</li>
</ol>
</details>"""))

add(Q("pr_2d", S, "2-D arrays and pointer arithmetic", "c",
r"""#include <stdio.h>

int main(void)
{
    int a[3][4];
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 4; j++)
            a[i][j] = 10 * i + j;
    printf("%d %d %d\n", (int)sizeof a, (int)sizeof a[0], (int)sizeof a[0][0]);
    printf("%d %d %d\n", *(*(a + 1) + 2), *(a[2] + 3), **a);
    int *p = &a[0][0];
    printf("%d\n", p[5]);
    return 0;
}
""",
"48 16 4\n12 23 0\n11\n",
r"""<p><code>a</code> is 3 rows of 4 ints: 48 bytes; one row is 16; one element is 4.</p>
<p><code>a + 1</code> points to row 1, <code>*(a + 1)</code> is that row (decays to <code>&amp;a[1][0]</code>),
and <code>+ 2</code> moves 2 ints: <code>a[1][2]</code> = 12. <code>*(a[2] + 3)</code> = <code>a[2][3]</code>
= 23. <code>**a</code> = <code>a[0][0]</code> = 0.</p>
<p>Rows are stored one after another (row-major), so the 6th int from the start, <code>p[5]</code>, is
<code>a[1][1]</code> = 11.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How a 2-D array is stored, what
<code>sizeof</code> gives for the whole array, one row and one element, and how pointer expressions like
<code>*(*(a + 1) + 2)</code> pick an element.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>int a[3][4]</code></td><td>3 rows; each row is an array of 4 <code>int</code>s. An
<code>int</code> is 4 bytes on this site.</td></tr>
<tr><td><code>sizeof</code></td><td><code>sizeof a</code> = whole array, <code>sizeof a[0]</code> = one row,
<code>sizeof a[0][0]</code> = one <code>int</code>.</td></tr>
<tr><td>Row-major storage</td><td>In memory the rows lie one after another in a single line: all of row 0, then
all of row 1, then row 2.</td></tr>
<tr><td><code>a + 1</code></td><td><code>a</code> becomes a pointer to row 0; <code>+ 1</code> moves one whole
<b>row</b>.</td></tr>
<tr><td><code>*(a + 1)</code></td><td>That row. It becomes a pointer to the row's first <code>int</code>, so
<code>+ 2</code> then moves 2 <b>ints</b>.</td></tr>
<tr><td><code>a[2]</code>, <code>**a</code></td><td><code>a[2]</code> is row 2 (a pointer to
<code>a[2][0]</code>). <code>**a</code> is the very first element.</td></tr>
<tr><td><code>p[5]</code></td><td>Means <code>*(p + 5)</code>: 5 ints after where <code>p</code> points.</td></tr>
</table>
<h4>Picture</h4>
<pre>as a grid:         col 0     col 1     col 2     col 3
          row 0   a[0][0]   a[0][1]   a[0][2]   a[0][3]
          row 1   a[1][0]   a[1][1]   a[1][2]   a[1][3]
          row 2   a[2][0]   a[2][1]   a[2][2]   a[2][3]

in memory (one line):
  position:  0         1         2         3         4      ...
            a[0][0]   a[0][1]   a[0][2]   a[0][3]   a[1][0]  ...</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>First fill the grid with numbers using the formula in the program's loop.</li>
<li>For the sizes, count boxes and multiply by 4.</li>
<li>Rewrite each pointer expression as <code>a[row][col]</code> (or as a position in the memory line) and read
the grid.</li>
</ol>
</details>"""))

add(Q("pr_float", S, "float vs double", "c",
r"""#include <stdio.h>

int main(void)
{
    float f = 0.1;
    if (f == 0.1)
        printf("equal\n");
    else
        printf("not equal\n");
    float g = 0.5;
    if (g == 0.5)
        printf("equal\n");
    else
        printf("not equal\n");
    printf("%d %.2f\n", (int)3.99, 7 / 2 * 2.0);
    return 0;
}
""",
"not equal\nequal\n3 6.00\n",
r"""<p>0.1 has no exact binary form. <code>f</code> holds 0.1 rounded to 24 bits; the literal <code>0.1</code> is a
<code>double</code> rounded to 53 bits. In <code>f == 0.1</code>, <code>f</code> is widened to double, and the two
roundings differ. 0.5 = 2<sup>&minus;1</sup> is exact in both, so they compare equal.</p>
<p>Casting to <code>int</code> truncates (3.99 &rarr; 3). <code>7 / 2</code> is integer division (3) before
the <code>* 2.0</code>, giving 6.00.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Why comparing a <code>float</code> with a
decimal number can fail, how a cast to <code>int</code> works, and integer division hiding inside a
floating-point expression.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>float</code> / <code>double</code></td><td><code>float</code>: 4 bytes, about 24 significant
binary digits. <code>double</code>: 8 bytes, 53 significant binary digits.</td></tr>
<tr><td>Literal type</td><td>A number like <code>0.1</code> with no letter after it is a <code>double</code>.
<code>float f = 0.1;</code> rounds it to the nearest <code>float</code>.</td></tr>
<tr><td>Exact or not?</td><td>Only fractions whose bottom is a power of 2 (1/2, 1/4, 3/8, &hellip;) are stored
exactly in binary. Others, like 1/10, have a binary form that never ends, so they are rounded. A
<code>float</code> and a <code>double</code> round at different places, so they keep different values.</td></tr>
<tr><td><code>f == 0.1</code></td><td><code>f</code> is first widened to <code>double</code> (this keeps its
value exactly), then compared with the <code>double</code> value of the literal.</td></tr>
<tr><td><code>(int)</code> of a decimal</td><td>Throws away the fraction (rounds towards zero). It does not round
to the nearest.</td></tr>
<tr><td><code>7 / 2 * 2.0</code></td><td><code>/</code> and <code>*</code> have the same rank and go left to right.
<code>7 / 2</code> has two <code>int</code>s, so it is integer division (fraction thrown away). Then
<code>int * double</code> gives a <code>double</code>.</td></tr>
<tr><td><code>%.2f</code></td><td>Prints a <code>double</code> with exactly 2 digits after the decimal point.</td></tr>
</table>
<p>Example of a number with an endless binary form: 1/10 = 0.000110011001100110011&hellip; (binary, the
pattern 0011 repeats forever).</p>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each comparison, ask: can this number be written exactly in binary? If yes, rounding to
<code>float</code> loses nothing.</li>
<li>For the last line, do the operations one at a time from left to right and note the type after each
step.</li>
</ol>
</details>"""))

add(Q("pr_recursion", S, "Recursion", "c",
r"""#include <stdio.h>

int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }

void up(int i, int n)
{
    if (i > n)
        return;
    printf("%d ", i);
    up(i + 1, n);
}

void down_up(int n)
{
    if (n == 0)
        return;
    printf("%d ", n);
    down_up(n - 1);
    printf("%d ", n);
}

int main(void)
{
    printf("%d\n", fact(5));
    up(1, 5);
    printf("\n");
    down_up(3);
    printf("\n");
    return 0;
}
""",
"120\n1 2 3 4 5\n3 2 1 1 2 3\n",
r"""<p><code>up</code> prints 1 to n with no loop, a 2026 interview question.</p>
<p>In <code>down_up</code>, everything <em>before</em> the recursive call happens on the way down (3 2 1), and
everything <em>after</em> it happens on the way back up (1 2 3).</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Tracing recursive functions: what happens
before the recursive call (on the way down) and what happens after it (on the way back up).</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>c ? x : y</code></td><td>If <code>c</code> is true the result is <code>x</code>, else
<code>y</code>.</td></tr>
<tr><td>A call waits</td><td>When a function calls itself, the caller stops at that line and waits until the
inner call has completely finished. Then it continues with its next line.</td></tr>
<tr><td>Own copies</td><td>Every call has its own copy of its parameters (<code>n</code>, <code>i</code>).
Changing one call's <code>n</code> does not change another's.</td></tr>
<tr><td><code>fact</code></td><td><code>fact(n) = n &times; fact(n &minus; 1)</code>, and <code>fact(1) = 1</code>.</td></tr>
<tr><td>Spaces</td><td><code>"%d "</code> prints a number and one space. Each <code>printf("\n")</code> in
<code>main</code> ends a line.</td></tr>
</table>
<h4>Picture: the shape of <code>down_up(n)</code></h4>
<pre>down_up(n):
    1. print n          &lt;- happens on the way DOWN
    2. down_up(n - 1)   &lt;- wait here until it has completely finished
    3. print n          &lt;- happens on the way back UP
    (stops at once when n == 0)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For <code>fact(5)</code>, expand: 5 &times; fact(4) = 5 &times; 4 &times; fact(3) &hellip; until
<code>fact(1)</code>.</li>
<li>For <code>up</code>, list the calls <code>up(1,5)</code>, <code>up(2,5)</code>, &hellip; and what each prints
before calling the next.</li>
<li>For <code>down_up(3)</code>, draw the calls as an indented list (each inner call one step to the right).
Write step 1 above the inner call and step 3 below it, then read the list from top to bottom.</li>
</ol>
</details>"""))

add(Q("pr_funcptr", S, "Function pointers", "c",
r"""#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

int main(void)
{
    int (*ops[3])(int, int) = {add, sub, mul};
    int acc = 2;
    for (int i = 0; i < 3; i++)
        acc = ops[i](acc, 3);
    printf("%d\n", acc);
    int (*op)(int, int) = sub;
    printf("%d\n", op(10, 4) + (*op)(1, 2));
    return 0;
}
""",
"6\n5\n",
r"""<p><code>int (*ops[3])(int, int)</code> is an array of 3 pointers to functions taking two ints and returning
an int. That is how interrupt vector tables, callbacks and command dispatchers are built.</p>
<p>acc: 2 + 3 = 5, 5 &minus; 3 = 2, 2 &times; 3 = 6. Then <code>op(10, 4)</code> and <code>(*op)(1, 2)</code> are
two ways to write the same call: 6 + (&minus;1) = 5.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Function pointers: storing functions in
an array and calling them through a pointer, as done in callback tables and interrupt vector tables.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>int (*op)(int, int)</code></td><td><code>op</code> is a pointer to a function that takes two
<code>int</code>s and returns an <code>int</code>.</td></tr>
<tr><td><code>int (*ops[3])(int, int)</code></td><td><code>ops</code> is an array of 3 such pointers.</td></tr>
<tr><td><code>= {add, sub, mul}</code></td><td>A function name without <code>()</code> gives a pointer to it.
<code>ops[0]</code> = <code>add</code>, <code>ops[1]</code> = <code>sub</code>, <code>ops[2]</code> =
<code>mul</code>.</td></tr>
<tr><td><code>op(x, y)</code> and <code>(*op)(x, y)</code></td><td>Two ways of writing the same call.</td></tr>
<tr><td><code>acc = ops[i](acc, 3);</code></td><td>Calls function number <code>i</code> with the current
<code>acc</code> and 3. The result becomes the new <code>acc</code> for the next turn of the loop.</td></tr>
</table>
<h4>Picture</h4>
<pre>ops:  [0] ---&gt; add(a, b) = a + b
      [1] ---&gt; sub(a, b) = a - b
      [2] ---&gt; mul(a, b) = a * b

op  ---&gt; sub</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns <code>i</code>, "function called", "<code>acc</code> before", "<code>acc</code>
after".</li>
<li>For the second <code>printf</code>, work out the two calls separately (watch the order of the arguments
in a subtraction), then add the results.</li>
</ol>
</details>"""))

add(Q("pr_enum", S, "enum values", "c",
r"""#include <stdio.h>

enum Color { RED, GREEN = 5, BLUE, ALPHA = 2, BETA };

int main(void)
{
    printf("%d %d %d %d\n", RED, BLUE, BETA, (int)sizeof(enum Color));
    return 0;
}
""",
"0 6 3 4\n",
r"""<p>Enumerators start at 0, and each one without an <code>=</code> is the previous one + 1. RED = 0, GREEN = 5,
BLUE = 6, ALPHA = 2, BETA = 3. Repeating values is allowed.</p>
<p>An enum is stored as an integer type that can hold every value, normally <code>int</code> (4 bytes).</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How C gives numbers to the names in an
<code>enum</code>, and how big an enum is.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>First name</td><td>Gets 0 if it has no <code>=</code>.</td></tr>
<tr><td>Name with <code>= value</code></td><td>Gets exactly that value.</td></tr>
<tr><td>Name without <code>=</code></td><td>Gets the value of the name just before it, plus 1. Counting goes on
from the last value given, even if that value is smaller.</td></tr>
<tr><td>Repeats</td><td>Two names may have the same value. That is allowed.</td></tr>
<tr><td>Size</td><td>On this site an enum whose values all fit in an <code>int</code> is stored in a 4-byte
integer (the same size as an <code>int</code>).</td></tr>
</table>
<h4>Worked examples (different enums)</h4>
<pre>enum { P = 4, Q, R = 9, S };     P = 4, Q = 5, R = 9, S = 10
enum { X, Y };                   X = 0, Y = 1</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Write the names of <code>enum Color</code> in a column.</li>
<li>Go down the column: copy a given value, or take the value above and add 1.</li>
<li>Read off the three names that are printed, then the size.</li>
</ol>
</details>"""))

add(Q("pr_calloc", S, "calloc, pointers and free", "c",
r"""#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *a = calloc(4, sizeof *a);
    if (a == NULL)
        return 1;
    int *b = a;
    a[1] = 7;
    b++;
    printf("%d %d %d\n", a[3], *b, (int)(b - a));
    free(a);
    a = NULL;
    b = NULL;
    printf("%s\n", a == NULL ? "freed" : "dangling");
    return 0;
}
""",
"0 7 1\nfreed\n",
r"""<p><code>calloc</code> zero-fills, so <code>a[3]</code> is 0. (<code>malloc</code> does not: its memory holds
whatever was there.) <code>b</code> is a second pointer into the same block, moved to <code>a[1]</code>.</p>
<p>After <code>free(a)</code>, <b>both</b> <code>a</code> and <code>b</code> are dangling: they still hold the
old address. Setting them to <code>NULL</code> makes a later mistake easy to spot. Using memory after
<code>free</code>, or freeing it twice, is undefined behaviour.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Heap memory with <code>calloc</code> and
<code>free</code>, two pointers to the same block, and pointer subtraction.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>calloc(n, size)</code></td><td>Gets a block of <code>n &times; size</code> bytes on the heap and
sets <b>every byte to 0</b>. Returns <code>NULL</code> if it fails. (<code>malloc</code> does not clear the
memory.)</td></tr>
<tr><td><code>sizeof *a</code></td><td>The size of one <code>int</code>, so the block holds 4 ints:
<code>a[0]</code> to <code>a[3]</code>.</td></tr>
<tr><td><code>int *b = a;</code></td><td>Copies the <b>address</b> only. Both pointers now point at the same block;
a change made through one is seen through the other.</td></tr>
<tr><td><code>b++</code></td><td>Moves <code>b</code> forward by one <code>int</code>.</td></tr>
<tr><td><code>b - a</code></td><td>The distance in <b>elements</b> (ints), not bytes.</td></tr>
<tr><td><code>free(a)</code></td><td>Gives the block back. The pointers still hold the old address until you
change them.</td></tr>
<tr><td><code>x ? "freed" : "dangling"</code></td><td>Picks the first string if <code>x</code> is true, else the
second.</td></tr>
</table>
<h4>Picture after <code>calloc</code> and <code>int *b = a;</code></h4>
<pre>heap block:   [0]    [1]    [2]    [3]
            |  ?   |  ?   |  ?   |  ?   |    (fill in what calloc puts here)
               ^
               a
               b   (same address as a)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Copy the picture and fill in the boxes. Then apply <code>a[1] = 7</code> and move the arrow for
<code>b++</code>.</li>
<li>Read <code>a[3]</code> and <code>*b</code> from the picture; count the boxes between the two arrows.</li>
<li>For the last line, look at the value <code>a</code> holds just before the <code>printf</code>.</li>
</ol>
</details>"""))

# ---------------------------------------------------------------------------
S = "OA: predict the output (C++)"

add(Q("pr_ctor_order", S, "Constructor and destructor order", "cpp",
r"""#include <cstdio>

struct A { A() { std::printf("A "); } ~A() { std::printf("~A "); } };
struct B : A { B() { std::printf("B "); } ~B() { std::printf("~B "); } };
struct C {
    A a;
    B b;
    C() { std::printf("C "); }
    ~C() { std::printf("~C "); }
};

int main()
{
    {
        C c;
    }
    std::printf("\n");
}
""",
"A A B C ~C ~B ~A ~A\n",
r"""<p>Construction order: base classes first, then members <em>in declaration order</em>, then the constructor
body. <code>a</code> prints <code>A</code>; <code>b</code> builds its base (<code>A</code>), then itself
(<code>B</code>); then <code>C</code>.</p>
<p>Destruction is the exact reverse: <code>~C</code>, then <code>b</code> (<code>~B ~A</code>), then <code>a</code>
(<code>~A</code>).</p>""",
statement=r"""<p><b>What to do.</b> Read the C++ program below and write down exactly what it
prints. Type one line of answer for each line the program prints. Spaces at the end of a line do not matter.
<b>Check</b> compares your answer with the right one and needs no compiler. <b>Run it</b> really compiles the
program and shows what it prints, so use it after you have tried on paper. (<code>std::printf</code> is the
same <code>printf</code> as in C.)</p>
<p><b>What this question tests.</b> The order in which C++ builds an object (constructors) and takes it apart
again (destructors), when the object has members and one member has a base class.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>struct B : A</code></td><td><code>B</code> is derived from <code>A</code>: every <code>B</code> object
has an <code>A</code> part inside it (the <em>base</em>).</td></tr>
<tr><td>Building an object</td><td>1. Build its base-class part first. 2. Then build its data members, in the
order they are <b>declared</b> in the class. 3. Last, run the body of its own constructor. Steps 1 and 2 use
the same rule again for each part (it is recursive).</td></tr>
<tr><td>Destroying an object</td><td>Exactly the reverse: 1. run its own destructor body, 2. destroy the members
in reverse declaration order, 3. destroy the base part.</td></tr>
<tr><td><code>{ C c; }</code></td><td><code>c</code> is built at its declaration and destroyed at the closing
<code>}</code> of that block, before the <code>printf("\n")</code>.</td></tr>
<tr><td>Printing</td><td>Each constructor and destructor prints a word and a space; there is no newline until
the end.</td></tr>
</table>
<h4>Picture of a <code>C</code> object</h4>
<pre>c : C
+-------------------------------+
|  a : A                        |   member 1
|  b : B                        |   member 2
|      +-- A part (B's base)    |
|      +-- B's own part         |
+-------------------------------+</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Write the picture as a tree. For building, each node prints <b>after</b> all the nodes inside it, going
top to bottom (base before members, members in declaration order).</li>
<li>For destruction, each node prints <b>before</b> the nodes inside it, and the inside nodes go in reverse
order.</li>
<li>Write the building words first, then the destroying words, on one line.</li>
</ol>
</details>"""))

add(Q("pr_virtual", S, "virtual vs non-virtual, and slicing", "cpp",
r"""#include <cstdio>

struct Base {
    virtual const char *name() const { return "Base"; }
    const char *kind() const { return "base-kind"; }
    virtual ~Base() = default;
};
struct Derived : Base {
    const char *name() const override { return "Derived"; }
    const char *kind() const { return "derived-kind"; }
};

int main()
{
    Derived d;
    Base &r = d;
    Base *p = &d;
    Base b = d;
    std::printf("%s %s\n", r.name(), r.kind());
    std::printf("%s %s\n", p->name(), d.kind());
    std::printf("%s\n", b.name());
}
""",
"Derived base-kind\nDerived derived-kind\nBase\n",
r"""<p>A <code>virtual</code> call through a reference or pointer uses the object's real type (looked up in its
vtable at run time): <code>Derived</code>. A non-virtual call uses the <em>static</em> type of the expression:
through <code>Base&amp;</code> it is <code>Base::kind</code>.</p>
<p><code>Base b = d</code> copies only the <code>Base</code> part (<b>object slicing</b>); <code>b</code> really is a
<code>Base</code>, so it prints <code>Base</code>.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> When a call goes to the <code>Base</code>
version of a function and when to the <code>Derived</code> version: <code>virtual</code> versus non-virtual
functions, and <em>object slicing</em>.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Term / rule</th><th>Meaning</th></tr>
<tr><td>Static type</td><td>The type written in the code for the name you call through. For
<code>Base &amp;r</code> and <code>Base *p</code> it is <code>Base</code>.</td></tr>
<tr><td>Dynamic type</td><td>The type of the object that really sits in memory. <code>r</code> and
<code>p</code> both refer to <code>d</code>, which is a <code>Derived</code>.</td></tr>
<tr><td>Virtual function, called through a reference or pointer</td><td>Uses the <b>dynamic</b> type. Decided
at run time, using the object's hidden table of virtual functions (<em>vtable</em>).</td></tr>
<tr><td>Non-virtual function</td><td>Uses the <b>static</b> type. Decided at compile time.</td></tr>
<tr><td>Called directly on an object variable (<code>d.f()</code>, <code>b.f()</code>)</td><td>Static and dynamic
type are the same: the variable's own type.</td></tr>
<tr><td><code>override</code></td><td><code>Derived::name</code> replaces the virtual <code>Base::name</code>.
<code>Derived::kind</code> is a separate, non-virtual function that only <em>hides</em>
<code>Base::kind</code>.</td></tr>
<tr><td><code>Base b = d;</code></td><td>Makes a <b>new</b> <code>Base</code> object by copying only the
<code>Base</code> part of <code>d</code>. This is <em>slicing</em>. <code>b</code> is a plain <code>Base</code>
and knows nothing about <code>Derived</code>.</td></tr>
</table>
<h4>Picture</h4>
<pre>d : Derived                        b : Base  (a separate copy)
+----------------------------+     +----------------------------+
| vptr --&gt; Derived's vtable  |     | vptr --&gt; Base's vtable     |
| Base part                  |     | Base part                  |
| Derived part               |     +----------------------------+
+----------------------------+
      ^           ^
      r           p      (r and p both lead to d)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each call, write two things: is the function virtual? Is it called through a reference/pointer or
directly on an object?</li>
<li>Virtual through a reference/pointer: follow the arrow to the real object and use its type. Otherwise: use
the type written in the code.</li>
</ol>
</details>"""))

add(Q("pr_static_member", S, "Static members and copies", "cpp",
r"""#include <cstdio>

struct Obj {
    static int alive, made;
    Obj() { alive++; made++; }
    Obj(const Obj &) { alive++; made++; }
    ~Obj() { alive--; }
};
int Obj::alive = 0, Obj::made = 0;

void by_value(Obj) {}
void by_ref(const Obj &) {}

int main()
{
    Obj a;
    {
        Obj b, c;
        by_value(a);
        by_ref(b);
        std::printf("%d %d\n", Obj::alive, Obj::made);
    }
    std::printf("%d %d\n", Obj::alive, Obj::made);
}
""",
"3 4\n1 4\n",
r"""<p>A <code>static</code> data member is shared by all objects of the class.</p>
<p><code>a</code>, <code>b</code>, <code>c</code>: 3 made. <code>by_value(a)</code> copy-constructs a parameter
(made 4, alive 4), which is destroyed when the call returns (alive 3). <code>by_ref</code> makes no copy. At the
end of the block, <code>b</code> and <code>c</code> die: alive 1.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> <code>static</code> data members
(one counter shared by the whole class), and which lines create or destroy objects, including the hidden
copy made when you pass an object by value.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td><code>static int alive, made;</code></td><td>One <code>alive</code> and one <code>made</code> for the
whole class, shared by all objects. Both start at 0.</td></tr>
<tr><td><code>Obj()</code></td><td>The normal constructor. Runs once for each object made with
<code>Obj x;</code>. <code>Obj b, c;</code> makes two objects.</td></tr>
<tr><td><code>Obj(const Obj &amp;)</code></td><td>The <em>copy constructor</em>. Runs whenever a new object is
made as a copy of another one.</td></tr>
<tr><td>Pass by value: <code>by_value(Obj)</code></td><td>The parameter is a <b>new object</b>, copied from the
argument. It is destroyed when the call is finished, before the next statement runs.</td></tr>
<tr><td>Pass by reference: <code>by_ref(const Obj &amp;)</code></td><td>No new object; the function uses the
caller's object.</td></tr>
<tr><td>End of a block <code>}</code></td><td>Every object declared inside that block is destroyed there
(<code>~Obj</code> runs once for each).</td></tr>
<tr><td><code>a</code></td><td>Declared in <code>main</code>'s outer block, so it lives until <code>main</code>
ends, after the last <code>printf</code>.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns "line", "objects made", "objects destroyed", <code>alive</code>,
<code>made</code>.</li>
<li>For each line, ask: does it make a new object (normal or copy)? Does any object die here?</li>
<li>Remember that <code>made</code> never goes down, while <code>alive</code> goes down in each destructor.</li>
</ol>
</details>"""))

add(Q("pr_overload", S, "Overload resolution and default arguments", "cpp",
r"""#include <cstdio>

void f(int)          { std::printf("int "); }
void f(double)       { std::printf("double "); }
void f(const char *) { std::printf("string "); }
void g(int a, int b = 10) { std::printf("%d ", a + b); }

int main()
{
    f(1);
    f(1.5);
    f('a');
    f("a");
    f(2.5f);
    g(1);
    g(1, 2);
    std::printf("\n");
}
""",
"int double int string double 11 3\n",
r"""<p>An exact match wins; next comes a <em>promotion</em> (<code>char</code> &rarr; <code>int</code>,
<code>float</code> &rarr; <code>double</code>); then other conversions. So <code>f('a')</code> calls the
<code>int</code> version and <code>f(2.5f)</code> the <code>double</code> one. <code>"a"</code> is a
<code>const char[2]</code>, which decays to <code>const char *</code>.</p>
<p>Default arguments fill in from the right: <code>g(1)</code> is <code>g(1, 10)</code>.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> How C++ chooses between functions with the
same name (<em>overload resolution</em>), and default arguments.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Literal</th><th>Its type in C++</th></tr>
<tr><td><code>1</code></td><td><code>int</code></td></tr>
<tr><td><code>1.5</code>, <code>2.5</code></td><td><code>double</code></td></tr>
<tr><td><code>2.5f</code></td><td><code>float</code> (the <code>f</code> makes it a float)</td></tr>
<tr><td><code>'a'</code></td><td><code>char</code> (in C++; in C it would be an <code>int</code>)</td></tr>
<tr><td><code>"a"</code></td><td>array of 2 <code>const char</code>, which turns into <code>const char *</code></td></tr>
</table>
<table>
<tr><th>Rank (best first)</th><th>Kind of match</th></tr>
<tr><td>1. Exact match</td><td>Same type (array to pointer also counts as exact).</td></tr>
<tr><td>2. Promotion</td><td>Only these: <code>char</code>, <code>short</code>, <code>bool</code> &rarr;
<code>int</code>; and <code>float</code> &rarr; <code>double</code>.</td></tr>
<tr><td>3. Conversion</td><td>Other number changes, for example <code>int</code> &rarr; <code>double</code> or
<code>double</code> &rarr; <code>int</code>.</td></tr>
<tr><td>Not possible</td><td>A string cannot become a number, and a number cannot become a
<code>const char *</code>.</td></tr>
</table>
<p>The version with the best rank is called. <b>Default argument:</b> in <code>g(int a, int b = 10)</code>, a
call that leaves out <code>b</code> uses 10 for it. Every <code>printf</code> here adds one space and there is
one newline at the end.</p>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>For each call of <code>f</code>, write the type of the argument.</li>
<li>For each of the three versions of <code>f</code>, write the rank of the match (exact, promotion,
conversion or impossible). Pick the best.</li>
<li>For <code>g</code>, fill in the missing argument, then add.</li>
</ol>
</details>"""))

add(Q("pr_refs", S, "Value, reference, pointer", "cpp",
r"""#include <cstdio>

void inc_val(int x) { x++; }
void inc_ref(int &x) { x++; }
void inc_ptr(int *x) { (*x)++; }

int main()
{
    int a = 1;
    inc_val(a);
    inc_ref(a);
    inc_ptr(&a);
    int &r = a;
    r += 10;
    int b = r;
    b++;
    std::printf("%d %d\n", a, b);
}
""",
"13 14\n",
r"""<p><code>inc_val</code> changes a copy. <code>inc_ref</code> and <code>inc_ptr</code> change <code>a</code>: 3.
<code>r</code> is another name for <code>a</code>, so <code>r += 10</code> makes <code>a</code> 13.
<code>int b = r</code> copies the value; changing <code>b</code> does not touch <code>a</code>.</p>
<p>A reference must be initialised and cannot be re-seated; a pointer can be null and can move.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> The three ways of passing a variable to a
function in C++ (value, reference, pointer), and what a reference variable is.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>void f(int x)</code></td><td>By value: <code>x</code> is a copy. Changing it does not change the
caller's variable.</td></tr>
<tr><td><code>void f(int &amp;x)</code></td><td>By reference: <code>x</code> is another name for the caller's
variable. Changing <code>x</code> changes it.</td></tr>
<tr><td><code>void f(int *x)</code></td><td>By pointer: <code>x</code> is a copy of the address;
<code>(*x)++</code> changes the caller's variable.</td></tr>
<tr><td><code>int &amp;r = a;</code></td><td>From now on <code>r</code> is another name for <code>a</code>.
Anything done to <code>r</code> is done to <code>a</code>. A reference can never be moved to another
variable.</td></tr>
<tr><td><code>int b = r;</code></td><td>Makes a <b>new</b>, separate <code>int</code> holding a copy of the
value. Changing <code>b</code> later does not touch <code>a</code>.</td></tr>
</table>
<h4>Picture after <code>int &amp;r = a;</code> and <code>int b = r;</code></h4>
<pre>a [ ? ]   &lt;-- r      (r is a second name for the same box)

b [ ? ]              (its own box, filled with a copy)</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Keep the value of <code>a</code> in a running note. For each function call, decide whether it changes
<code>a</code> or only a copy.</li>
<li>From the line <code>int &amp;r = a;</code> on, treat every <code>r</code> as <code>a</code>.</li>
<li><code>b</code> starts as a copy and then changes on its own.</li>
</ol>
</details>"""))

add(Q("pr_ctor_virtual", S, "Virtual calls inside a constructor", "cpp",
r"""#include <cstdio>

struct Base {
    Base() { hello(); }
    virtual void hello() { std::printf("Base "); }
    virtual ~Base() {}
};
struct D : Base {
    D() { hello(); }
    void hello() override { std::printf("D "); }
};

int main()
{
    D d;
    Base &b = d;
    b.hello();
    std::printf("\n");
}
""",
"Base D D\n",
r"""<p>While the <code>Base</code> constructor runs, the <code>D</code> part does not exist yet, so the object is
treated as a <code>Base</code> and the virtual call goes to <code>Base::hello</code>. Once <code>D</code>'s
constructor runs, calls go to <code>D::hello</code>. (Destructors work the same way in reverse.)</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> What a <code>virtual</code> call does
when it is made from inside a constructor, while the object is still being built.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Rule</th><th>Meaning</th></tr>
<tr><td>Building <code>D d;</code></td><td>First the <code>Base</code> constructor runs completely, then the
body of the <code>D</code> constructor.</td></tr>
<tr><td>During <code>Base()</code></td><td>The <code>D</code> part does not exist yet. The object counts as a
<code>Base</code>, so a virtual call made here goes to <code>Base</code>'s version.</td></tr>
<tr><td>During <code>D()</code> and after</td><td>The object counts as a <code>D</code>, so virtual calls go to
<code>D</code>'s version.</td></tr>
<tr><td>Virtual call through <code>Base &amp;b</code></td><td>Uses the real type of the finished object.</td></tr>
<tr><td>Printing</td><td>Each <code>hello</code> prints a word and a space; one newline at the end.</td></tr>
</table>
<h4>Picture: what the object "is" over time</h4>
<pre>time ---&gt;
| Base() body runs | D() body runs | after construction (main goes on) |
| object acts as:  | acts as:      | acts as:                          |
|      Base        |      D        |      D                            |</pre>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>List every call of <code>hello()</code> in the order it happens: one in each constructor, one in
<code>main</code>.</li>
<li>For each, look at the picture to see what the object acts as at that moment, and pick that version.</li>
</ol>
</details>"""))

add(Q("pr_operators", S, "Prefix and postfix operator++", "cpp",
r"""#include <cstdio>

struct V {
    int x;
    V operator+(const V &o) const { return {x + o.x}; }
    V &operator++() { ++x; return *this; }               // prefix
    V operator++(int) { V t = *this; ++x; return t; }    // postfix
};

int main()
{
    V a{1}, b{2};
    V c = a + b;
    V d = c++;
    V e = ++c;
    std::printf("%d %d %d\n", c.x, d.x, e.x);
}
""",
"5 3 5\n",
r"""<p>The postfix form is the one with the dummy <code>int</code> parameter. It saves a copy, increments, and
returns the <em>old</em> copy (by value). Prefix increments and returns the object itself (by reference), which
is why <code>++it</code> is preferred for iterators.</p>
<p>c = 3; <code>d = c++</code> gives 3 and c becomes 4; <code>e = ++c</code> makes c 5 and gives 5.</p>""",
statement=r"""<p><b>What to do.</b> Read the program below and write down exactly what it prints (one line of your
answer for each printed line; spaces at the end of a line do not matter). Then press <b>Check</b>.</p>
<p><b>What this question tests.</b> Writing your own <code>+</code> and
<code>++</code> for a class, and the difference between the prefix (<code>++c</code>) and postfix
(<code>c++</code>) versions.</p>
<h4>Facts you need (given here, so you do not have to remember them)</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>V a{1}</code></td><td>Makes a <code>V</code> with <code>a.x = 1</code>. <code>return {x + o.x};</code>
makes a <code>V</code> the same way.</td></tr>
<tr><td><code>a + b</code></td><td>Calls <code>a.operator+(b)</code>: returns a new <code>V</code> whose
<code>x</code> is <code>a.x + b.x</code>. <code>a</code> and <code>b</code> do not change.</td></tr>
<tr><td><code>++c</code></td><td>Calls <code>operator++()</code> (no parameter): adds 1 to <code>c.x</code>, then
returns <code>c</code> itself (the <b>new</b> value).</td></tr>
<tr><td><code>c++</code></td><td>Calls <code>operator++(int)</code>. The <code>int</code> is only a marker that
means "postfix". It saves a copy <code>t</code>, adds 1 to <code>c.x</code>, and returns the saved copy (the
<b>old</b> value).</td></tr>
<tr><td><code>V d = c++;</code></td><td><code>d</code> becomes whatever the operator returns.</td></tr>
</table>
<details><summary>How to work it out (open if you are stuck)</summary>
<ol>
<li>Make a table with columns <code>c.x</code>, <code>d.x</code>, <code>e.x</code>, one row per line of
<code>main</code>.</li>
<li>For each <code>++</code>, decide: which operator runs, how <code>c.x</code> changes, and which value is
handed to the new variable.</li>
</ol>
</details>"""))
