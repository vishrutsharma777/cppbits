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
statement="<p>What does this program print? Type the output exactly, one line per line. Spaces at the "
          "end of a line do not matter. <b>Check</b> needs no compiler; <b>Run it</b> compiles the program "
          "and shows what it really prints.</p>"))

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
left operand</b>: &minus;7 % 3 = &minus;7 &minus; (&minus;2)(3) = &minus;1, and 7 % &minus;3 = 7 &minus; (&minus;2)(&minus;3) = 1.</p>"""))

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
(<code>-Wsign-compare</code>) warns about both comparisons.</p>"""))

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
<code>a = 1</code>, <code>b = 0</code>.</li></ul>"""))

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
behaviour</em>. On this site it stops the program with a runtime error.</p>"""))

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
<p><code>p</code> stays at <code>arr[2]</code>, so <code>p - arr</code> is 2 (elements, not bytes).</p>"""))

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
<code>alloc(int **p)</code> or inserting at the head of a linked list.</p>"""))

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
<code>char *t = "hello"</code> is undefined behaviour.) <code>*s + 1</code> is <code>'j' + 1</code> = <code>'k'</code>.</p>"""))

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
statement=SIZES))

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
statement=SIZES))

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
<code>malloc</code> also leaks memory.</p>"""))

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
(internal linkage).</p>"""))

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
<p>A 2026 Qualcomm interview asked a question of this shape.</p>"""))

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
<code>*pc</code> sees it. <code>const int *const p</code> fixes both the pointer and the value.</p>"""))

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
(the caller frees), or have the caller pass a buffer in.</p>"""))

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
statement=SIZES))

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
<code>static inline</code> function avoids this.</li></ul>"""))

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
<li>i = 3: <code>default</code>: <code>d</code>.</li></ul>"""))

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
prints <code>3</code> and a newline, so the line reads <code>1233</code>.</p>"""))

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
<p>(0, 10): body runs, n = 1. (2, 7): body runs, n = 2. (4, 4): 4 &lt; 4 is false, so the loop stops.</p>"""))

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
<p><code>while (--y)</code> decrements first: the loop sees 2 and 1, stops at 0, and <code>y</code> stays 0.</p>"""))

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
10010: two bits differ. "How many bits must flip to turn a into b?" was a 2026 interview question.</li></ul>"""))

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
instead of bit-fields.</p>"""))

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
<code>a[1][1]</code> = 11.</p>"""))

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
the <code>* 2.0</code>, giving 6.00.</p>"""))

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
everything <em>after</em> it happens on the way back up (1 2 3).</p>"""))

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
two ways to write the same call: 6 + (&minus;1) = 5.</p>"""))

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
<p>An enum is stored as an integer type that can hold every value, normally <code>int</code> (4 bytes).</p>"""))

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
<code>free</code>, or freeing it twice, is undefined behaviour.</p>"""))

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
(<code>~A</code>).</p>"""))

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
<code>Base</code>, so it prints <code>Base</code>.</p>"""))

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
end of the block, <code>b</code> and <code>c</code> die: alive 1.</p>"""))

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
<p>Default arguments fill in from the right: <code>g(1)</code> is <code>g(1, 10)</code>.</p>"""))

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
<p>A reference must be initialised and cannot be re-seated; a pointer can be null and can move.</p>"""))

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
constructor runs, calls go to <code>D::hello</code>. (Destructors work the same way in reverse.)</p>"""))

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
<p>c = 3; <code>d = c++</code> gives 3 and c becomes 4; <code>e = ++c</code> makes c 5 and gives 5.</p>"""))
