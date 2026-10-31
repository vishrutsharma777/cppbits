# Problem bank, part B: fixed point, DSP in C, real-time buffers.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Fixed point (Q15 / Q31)"

add(P("float_to_q15", S, "Float to Q15", "c", "func",
r"""<p><b>What to write.</b> A function <code>int16_t float_to_q15(float x)</code>. It turns a real
number <code>x</code> into its <b>Q15</b> code: a 16-bit integer that stands for that number.</p>
<p><b>Why it matters.</b> Many DSP chips and audio codecs have no floating-point hardware, or only a slow
one. They store samples and filter coefficients as <em>fixed-point</em> integers instead. Q15 is the
most common fixed-point format.</p>
<h4>What Q15 means</h4>
<p>A Q15 number is an ordinary <code>int16_t</code>. You read it as a fraction:
real value = integer &divide; 32768 (32768 = 2<sup>15</sup>). So to go from a real number to Q15, you
multiply by 32768.</p>
<pre> bit:     15    14    13    12   ...    1      0
        [ s ] [ . ] [ . ] [ . ]  ...  [ . ]  [ . ]
 weight:  -1   1/2   1/4   1/8   ...  2^-14  2^-15
          sign bit, then 15 fraction bits</pre>
<table>
<tr><th>Real value</th><th>Q15 integer</th><th>Note</th></tr>
<tr><td>&minus;1.0</td><td>&minus;32768</td><td>the smallest value</td></tr>
<tr><td>&minus;0.5</td><td>&minus;16384</td><td></td></tr>
<tr><td>0.0</td><td>0</td><td></td></tr>
<tr><td>0.000030517578125</td><td>1</td><td>one step (1/32768), the smallest possible change</td></tr>
<tr><td>0.25</td><td>8192</td><td></td></tr>
<tr><td>0.5</td><td>16384</td><td></td></tr>
<tr><td>0.999969482421875</td><td>32767</td><td>the largest value</td></tr>
</table>
<p>+1.0 does not fit. It would need 32768, which is one more than the largest <code>int16_t</code>.</p>
<h4>The rule, step by step</h4>
<ol>
<li>Multiply: v = x &times; 32768.</li>
<li>Round v to the nearest whole number. When the fraction is exactly one half, move <b>away from
zero</b>: 1.5 becomes 2 and &minus;1.5 becomes &minus;2. This is exactly what <code>roundf</code> from
<code>&lt;math.h&gt;</code> does.</li>
<li><b>Saturate</b>: if the result is above 32767, use 32767. If it is below &minus;32768, use
&minus;32768. ("Saturate" means: stick at the nearest end of the range instead of wrapping round.)</li>
<li>Return the result as an <code>int16_t</code>.</li>
</ol>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>x &times; 32768</th><th>After rounding</th><th>You return</th></tr>
<tr><td><code>float_to_q15(0.5f)</code></td><td>16384</td><td>16384</td><td>16384</td></tr>
<tr><td><code>float_to_q15(0.1f)</code></td><td>3276.8</td><td>3277</td><td>3277</td></tr>
<tr><td><code>float_to_q15(-0.5f)</code></td><td>&minus;16384</td><td>&minus;16384</td><td>&minus;16384</td></tr>
<tr><td><code>float_to_q15(3.0f / 65536)</code></td><td>1.5</td><td>2 (a half moves away from 0)</td><td>2</td></tr>
<tr><td><code>float_to_q15(-1.0f / 65536)</code></td><td>&minus;0.5</td><td>&minus;1</td><td>&minus;1</td></tr>
<tr><td><code>float_to_q15(1.0f)</code></td><td>32768</td><td>32768</td><td>32767 (saturated)</td></tr>
<tr><td><code>float_to_q15(-1.5f)</code></td><td>&minus;49152</td><td>&minus;49152</td><td>&minus;32768 (saturated)</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li><code>x</code> is between &minus;2 and 2. So some inputs are outside the Q15 range and must be
saturated.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>A plain cast such as <code>(int16_t)v</code> throws the fraction away (3276.8 becomes 3276). It
does not round.</li>
<li>Converting a float that is outside the range of the target integer type is <b>undefined
behaviour</b> in C: the result can be anything. So compare with 32767 and &minus;32768 while the value
is still a <code>float</code>, and cast only after that.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write the three steps (multiply, round, saturate) in that order.</li>
<li>At which step is the value still a <code>float</code>? Do the range checks there.</li>
<li>Test your idea on 1.0: the multiply gives 32768. What must happen next?</li>
</ol>
</details>""",
r"""#include <stdint.h>
#include <math.h>

int16_t float_to_q15(float x)
{
    return (int16_t)(x * 32768.0f);
}
""",
r"""#include <stdint.h>
#include <math.h>

int16_t float_to_q15(float x)
{
    float v = roundf(x * 32768.0f);
    if (v > 32767.0f) return 32767;
    if (v < -32768.0f) return -32768;
    return (int16_t)v;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(float x)
{
    double v = (double)x * 32768.0;
    v = v < 0 ? -floor(-v + 0.5) : floor(v + 0.5);
    return v > 32767 ? 32767 : (v < -32768 ? -32768 : (int)v);
}
int main(void)
{
    char d[64];
    float f[] = {0.0f, 0.5f, -0.5f, 1.0f, -1.0f, 1.5f, -1.5f, 0.999f, 1.0f / 65536.0f, -1.0f / 65536.0f, 3.0f / 65536.0f};
    for (int i = 0; i < 11; i++) { CK_FMT(d, "float_to_q15(%.9g)", f[i]); ck_int(d, float_to_q15(f[i]), ref(f[i])); }
    for (int i = 0; i < 400; i++) { float x = (float)(ck_unit() * 2.0); CK_FMT(d, "float_to_q15(%.9g)", x); ck_int(d, float_to_q15(x), ref(x)); }
    return ck_done();
}
""",
"roundf(x * 32768.0f), then clamp to the int16 range before converting. Converting an out-of-range float to an integer is undefined behaviour."))

add(P("q15_add_sat", S, "Saturating add", "c", "func",
r"""<p><b>What to write.</b> A function <code>int16_t q15_add_sat(int16_t a, int16_t b)</code>. It
returns a + b, but if the sum does not fit in an <code>int16_t</code>, it returns the nearest value that
does fit: 32767 for a sum that is too big, &minus;32768 for a sum that is too small. This is called a
<b>saturating</b> add.</p>
<p><b>Why it matters.</b> Two Q15 samples can add up to more than the format can hold:
0.75 + 0.75 = 1.5 does not fit. Normal integer arithmetic <em>wraps round</em>, so a loud positive sample
turns into a large negative one. In audio you hear that as a sharp click. Audio code saturates instead:
the sample sticks at full scale, which sounds much softer.</p>
<h4>Picture: wrap versus saturate</h4>
<pre> -32768                    0                    32767
   |-----------------------|-----------------------|
   ^                                               |
   +---------- wrap: 32767 + 1 lands here &lt;--------+

 wrap:      32767 + 1  --&gt;  -32768   (top jumps to the bottom)
 saturate:  32767 + 1  --&gt;   32767   (stays at the top)</pre>
<h4>Examples</h4>
<table>
<tr><th>a</th><th>b</th><th>True sum</th><th>If you wrap</th><th>You return</th></tr>
<tr><td>24576 (0.75)</td><td>24576 (0.75)</td><td>49152</td><td>&minus;16384 (&minus;0.5!)</td><td>32767</td></tr>
<tr><td>32767</td><td>1</td><td>32768</td><td>&minus;32768</td><td>32767</td></tr>
<tr><td>&minus;32768</td><td>&minus;1</td><td>&minus;32769</td><td>32767</td><td>&minus;32768</td></tr>
<tr><td>100</td><td>&minus;200</td><td>&minus;100</td><td>&minus;100</td><td>&minus;100</td></tr>
<tr><td>&minus;32768</td><td>32767</td><td>&minus;1</td><td>&minus;1</td><td>&minus;1</td></tr>
</table>
<h4>Facts you need</h4>
<ul>
<li>The <code>int16_t</code> range is &minus;32768 to 32767.</li>
<li>In C, when you write <code>a + b</code> with two <code>int16_t</code> values, both are first widened
to <code>int</code> (32 bits on this site). This is called <em>integer promotion</em>. So the sum
itself is computed correctly. The damage happens only when you store it back into an
<code>int16_t</code>.</li>
<li>The true sum is always between &minus;65536 and 65534, so it fits easily in an
<code>int32_t</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Where can you keep the full sum so that nothing is lost?</li>
<li>Which two comparisons decide whether you must clamp it?</li>
<li>Only after those checks, convert the result to <code>int16_t</code>.</li>
</ol>
</details>""",
r"""#include <stdint.h>

int16_t q15_add_sat(int16_t a, int16_t b)
{
    return (int16_t)(a + b);
}
""",
r"""#include <stdint.h>

int16_t q15_add_sat(int16_t a, int16_t b)
{
    int32_t s = (int32_t)a + b;
    if (s > 32767) return 32767;
    if (s < -32768) return -32768;
    return (int16_t)s;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int a, int b) { int s = a + b; return s > 32767 ? 32767 : (s < -32768 ? -32768 : s); }
int main(void)
{
    char d[64];
    int f[][2] = {{24576, 24576}, {-32768, -1}, {32767, 1}, {100, -200}, {-32768, 32767}, {0, 0}};
    for (int i = 0; i < 6; i++) { CK_FMT(d, "q15_add_sat(%d, %d)", f[i][0], f[i][1]); ck_int(d, q15_add_sat((int16_t)f[i][0], (int16_t)f[i][1]), ref(f[i][0], f[i][1])); }
    for (int i = 0; i < 400; i++) { int a = ck_range(-32768, 32767), b = ck_range(-32768, 32767); CK_FMT(d, "q15_add_sat(%d, %d)", a, b); ck_int(d, q15_add_sat((int16_t)a, (int16_t)b), ref(a, b)); }
    return ck_done();
}
""",
"Add in int32_t, where the sum always fits, then clamp."))

add(P("q15_mul", S, "Q15 multiply", "c", "func",
r"""<p><b>What to write.</b> A function <code>int16_t q15_mul(int16_t a, int16_t b)</code>. Both inputs
are Q15 numbers (real value = integer &divide; 32768). Return their product, also as a Q15 number.</p>
<p><b>Why it matters.</b> Every gain, filter tap and mixer on a fixed-point DSP is a multiply like this
one. Interviewers often ask you to write it and explain the shift and the rounding.</p>
<h4>The idea</h4>
<p>a stands for a/32768 and b stands for b/32768. Their real product is (a&middot;b)/32768<sup>2</sup>.
To write that as Q15 again, you need (a&middot;b)/32768. So: multiply the two integers, then divide by
32768 once. Dividing by 32768 = 2<sup>15</sup> is a right shift by 15. The integer product a&middot;b has
30 fraction bits, so it is called a <b>Q30</b> number.</p>
<pre> a (16 bits) x b (16 bits) = p (32 bits, a Q30 number)

 p:  bit 31 ................ bit 15 | bit 14 ............ bit 0
     these bits become the 16-bit  | these bits are thrown away
     Q15 answer                    | by the shift &gt;&gt; 15</pre>
<h4>The rule, step by step</h4>
<ol>
<li>Multiply as <code>int32_t</code>: p = a &times; b.</li>
<li>Add 2<sup>14</sup> = 16384. That is half of 2<sup>15</sup>, so the next step rounds to the nearest
value instead of cutting the fraction off.</li>
<li>Shift right by 15.</li>
<li>Saturate to the <code>int16_t</code> range [&minus;32768, 32767].</li>
</ol>
<h4>Facts you need</h4>
<ul>
<li>The product of two <code>int16_t</code> values always fits in an <code>int32_t</code> (its size is at
most 2<sup>30</sup>).</li>
<li>On this site, as on almost every compiler, <code>&gt;&gt;</code> on a negative <code>int</code>
copies the sign bit. That is the same as dividing by 2<sup>15</sup> and rounding <b>down</b> (towards
minus infinity). Together with the +16384, an exact half therefore always rounds <b>up</b>:
1.5 &rarr; 2, &minus;1.5 &rarr; &minus;1, &minus;0.5 &rarr; 0. The test expects exactly this.</li>
<li>Only one input pair overflows: (&minus;1) &times; (&minus;1) = +1.0, which would be 32768. It must
become 32767. The smallest possible result is &minus;32767, so the lower end never overflows.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>a</th><th>b</th><th>Real product</th><th>a&middot;b / 32768 (exact)</th><th>You return</th></tr>
<tr><td>16384</td><td>16384</td><td>0.5 &times; 0.5 = 0.25</td><td>8192</td><td>8192</td></tr>
<tr><td>24576</td><td>16384</td><td>0.75 &times; 0.5 = 0.375</td><td>12288</td><td>12288</td></tr>
<tr><td>16384</td><td>&minus;8192</td><td>0.5 &times; &minus;0.25 = &minus;0.125</td><td>&minus;4096</td><td>&minus;4096</td></tr>
<tr><td>3</td><td>16384</td><td>tiny</td><td>1.5</td><td>2</td></tr>
<tr><td>&minus;3</td><td>16384</td><td>tiny</td><td>&minus;1.5</td><td>&minus;1</td></tr>
<tr><td>&minus;1</td><td>16384</td><td>tiny</td><td>&minus;0.5</td><td>0</td></tr>
<tr><td>32767</td><td>32767</td><td>about 0.99994</td><td>32766.00003</td><td>32766</td></tr>
<tr><td>&minus;32768</td><td>32767</td><td>about &minus;0.99997</td><td>&minus;32767</td><td>&minus;32767</td></tr>
<tr><td>&minus;32768</td><td>&minus;32768</td><td>&minus;1 &times; &minus;1 = +1</td><td>32768</td><td>32767 (saturated)</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>In which type must the multiply happen so that nothing overflows?</li>
<li>Why does adding half of the divisor before a shift turn "cut off" into "round"?</li>
<li>Which single result can be too big, and what do you return then?</li>
</ol>
</details>""",
r"""#include <stdint.h>

int16_t q15_mul(int16_t a, int16_t b)
{
    return 0;
}
""",
r"""#include <stdint.h>

int16_t q15_mul(int16_t a, int16_t b)
{
    int32_t p = ((int32_t)a * b + (1 << 14)) >> 15;
    if (p > 32767) return 32767;
    return (int16_t)p;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int a, int b) { int p = (a * b + 16384) >> 15; return p > 32767 ? 32767 : p; }
int main(void)
{
    char d[64];
    int f[][2] = {{16384, 16384}, {-32768, -32768}, {-32768, 32767}, {32767, 32767}, {1, 1}, {-1, 16384}, {3, 16384}, {-3, 16384}};
    for (int i = 0; i < 8; i++) { CK_FMT(d, "q15_mul(%d, %d)", f[i][0], f[i][1]); ck_int(d, q15_mul((int16_t)f[i][0], (int16_t)f[i][1]), ref(f[i][0], f[i][1])); }
    for (int i = 0; i < 400; i++) { int a = ck_range(-32768, 32767), b = ck_range(-32768, 32767); CK_FMT(d, "q15_mul(%d, %d)", a, b); ck_int(d, q15_mul((int16_t)a, (int16_t)b), ref(a, b)); }
    return ck_done();
}
""",
"((int32_t)a * b + (1 << 14)) >> 15, then saturate. The product of two int16 values always fits in int32."))

add(P("q31_mul", S, "Q31 multiply", "c", "func",
r"""<p><b>What to write.</b> A function <code>int32_t q31_mul(int32_t a, int32_t b)</code> that
multiplies two <b>Q31</b> numbers and returns a Q31 result.</p>
<p><b>Why it matters.</b> Q31 is the same idea as Q15, but in 32 bits. Its steps are 65536 times finer
than Q15 steps, so it is used where 16 bits are not precise enough, for example in filter coefficients and
in high-quality audio paths.</p>
<h4>What Q31 means</h4>
<p>A Q31 number is an <code>int32_t</code>. Real value = integer &divide; 2<sup>31</sup>
(2<sup>31</sup> = 2147483648).</p>
<table>
<tr><th>Real value</th><th>Q31 integer</th></tr>
<tr><td>&minus;1.0</td><td>&minus;2147483648 (<code>INT32_MIN</code>), the smallest value</td></tr>
<tr><td>&minus;0.25</td><td>&minus;536870912 = &minus;2<sup>29</sup></td></tr>
<tr><td>0.25</td><td>536870912 = 2<sup>29</sup></td></tr>
<tr><td>0.5</td><td>1073741824 = 2<sup>30</sup></td></tr>
<tr><td>0.9999999995</td><td>2147483647 (<code>INT32_MAX</code>), the largest value</td></tr>
</table>
<h4>The rule, step by step (same recipe as Q15, one size bigger)</h4>
<ol>
<li>Multiply in <code>int64_t</code>: p = a &times; b. This product has 62 fraction bits (a Q62 number)
and needs up to 63 bits, so 32 bits are not enough.</li>
<li>Add 2<sup>30</sup> (half of 2<sup>31</sup>) so that the shift rounds.</li>
<li>Shift right by 31.</li>
<li>Saturate to the <code>int32_t</code> range: above 2147483647 becomes 2147483647.</li>
</ol>
<h4>Examples</h4>
<table>
<tr><th>a</th><th>b</th><th>Real product</th><th>You return</th></tr>
<tr><td>2<sup>30</sup> (0.5)</td><td>2<sup>30</sup> (0.5)</td><td>0.25</td><td>536870912</td></tr>
<tr><td>2<sup>30</sup> (0.5)</td><td>&minus;2<sup>29</sup> (&minus;0.25)</td><td>&minus;0.125</td><td>&minus;268435456</td></tr>
<tr><td>&minus;1</td><td>1</td><td>about &minus;2&times;10<sup>&minus;19</sup></td><td>0 (rounds to zero)</td></tr>
<tr><td><code>INT32_MAX</code></td><td><code>INT32_MAX</code></td><td>just under 1</td><td>2147483646</td></tr>
<tr><td><code>INT32_MIN</code></td><td><code>INT32_MAX</code></td><td>just above &minus;1</td><td>&minus;2147483647</td></tr>
<tr><td><code>INT32_MIN</code></td><td><code>INT32_MIN</code></td><td>&minus;1 &times; &minus;1 = +1</td><td>2147483647 (saturated)</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>Convert <b>before</b> multiplying: <code>(int64_t)a * b</code>. If you write <code>a * b</code>, the
multiply happens in 32 bits and overflows, which is undefined behaviour in C.</li>
<li>Like in Q15, <code>&gt;&gt;</code> on a negative number rounds down, so an exact half rounds up.</li>
<li><code>INT32_MAX</code> and <code>INT32_MIN</code> come from <code>&lt;stdint.h&gt;</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Take your Q15 multiply and replace every size: 16 &rarr; 32 bits, 32 &rarr; 64 bits, shift 15
&rarr; 31, rounding constant 2<sup>14</sup> &rarr; 2<sup>30</sup>.</li>
<li>Which one input pair gives a result that is too big?</li>
</ol>
</details>""",
r"""#include <stdint.h>

int32_t q31_mul(int32_t a, int32_t b)
{
    return 0;
}
""",
r"""#include <stdint.h>

int32_t q31_mul(int32_t a, int32_t b)
{
    int64_t p = ((int64_t)a * b + ((int64_t)1 << 30)) >> 31;
    if (p > INT32_MAX) return INT32_MAX;
    return (int32_t)p;
}
""",
r"""#include "check.h"
#include "solution.c"
static int64_t ref(int64_t a, int64_t b) { int64_t p = (a * b + ((int64_t)1 << 30)) >> 31; return p > 2147483647 ? 2147483647 : p; }
int main(void)
{
    char d[96];
    int32_t f[][2] = {{INT32_MIN, INT32_MIN}, {1 << 30, 1 << 30}, {INT32_MAX, INT32_MAX}, {-1, 1}, {INT32_MIN, INT32_MAX}};
    for (int i = 0; i < 5; i++) { CK_FMT(d, "q31_mul(%d, %d)", f[i][0], f[i][1]); ck_int(d, q31_mul(f[i][0], f[i][1]), ref(f[i][0], f[i][1])); }
    for (int i = 0; i < 400; i++) { int32_t a = (int32_t)ck_rand(), b = (int32_t)ck_rand(); CK_FMT(d, "q31_mul(%d, %d)", a, b); ck_int(d, q31_mul(a, b), ref(a, b)); }
    return ck_done();
}
""",
"Same recipe as Q15, one size up: int64_t product, + (1LL << 30), >> 31, saturate."))

add(P("q15_dot", S, "Q15 dot product", "c", "func",
r"""<p><b>What to write.</b> A function
<code>int16_t q15_dot(const int16_t *a, const int16_t *b, int n)</code>. It returns the dot product
a[0]&middot;b[0] + a[1]&middot;b[1] + &hellip; + a[n&minus;1]&middot;b[n&minus;1] of two Q15 arrays, as a
Q15 number.</p>
<p><b>Why it matters.</b> The output of an FIR filter is a dot product of the filter taps and the most
recent samples. DSP chips have a <b>multiply-accumulate</b> (MAC) instruction and a wide accumulator
register made for exactly this loop.</p>
<h4>Picture</h4>
<pre> a:  [a0]  [a1]  [a2]  ...  [a(n-1)]
      *     *     *            *
 b:  [b0]  [b1]  [b2]  ...  [b(n-1)]
      |     |     |            |
      +-----+-----+--- ... ----+--&gt; acc   (int64_t, a Q30 sum)
                                     |
                       (acc + 2^14) &gt;&gt; 15     round ONCE, at the end
                                     |
                       saturate to [-32768, 32767] --&gt; result</pre>
<h4>The rule, step by step</h4>
<ol>
<li>Start an <code>int64_t</code> accumulator at 0.</li>
<li>Add every product a[i]&middot;b[i] to it. Each product is a Q30 number. Do not round yet.</li>
<li>After the loop, convert to Q15 once: add 2<sup>14</sup> (= 16384), then shift right by 15.</li>
<li>Saturate to [&minus;32768, 32767].</li>
</ol>
<h4>Why 64 bits, and why round only once</h4>
<ul>
<li>One product can be as big as 2<sup>30</sup>, and an <code>int32_t</code> only goes up to about
2<sup>31</sup>. So two or three big products can already overflow 32 bits. With n up to 64, the sum can
reach 2<sup>36</sup>, which needs a 64-bit accumulator.</li>
<li>Rounding every product loses a little each time, and the losses add up. Example: a = {1, 1, 1},
b = {16384, 16384, 16384}. Each product is exactly half a Q15 step. Rounding each one gives
1 + 1 + 1 = <b>3</b>. The exact sum is 1.5 steps, and rounding once gives <b>2</b>. The test expects
2.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>a</th><th>b</th><th>Accumulator (Q30)</th><th>You return</th></tr>
<tr><td>{16384, 16384, &minus;8192}</td><td>{16384, 8192, 16384}</td><td>268435456</td><td>8192 (0.25)</td></tr>
<tr><td>{1, 1, 1}</td><td>{16384, 16384, 16384}</td><td>49152</td><td>2</td></tr>
<tr><td>{32767, 32767}</td><td>{32767, 32767}</td><td>2147352578</td><td>32767 (saturated; the real sum is about 2.0)</td></tr>
<tr><td>{} (n = 0)</td><td>{}</td><td>0</td><td>0</td></tr>
</table>
<p>First row in real numbers: 0.5&middot;0.5 + 0.5&middot;0.25 + (&minus;0.25)&middot;0.5 =
0.25 + 0.125 &minus; 0.125 = 0.25.</p>
<h4>Inputs and limits</h4>
<ul>
<li><code>n</code> is 0 to 64. The values can be anywhere in the <code>int16_t</code> range.</li>
<li>Rounding works as in <code>q15_mul</code>: <code>&gt;&gt;</code> on a negative number rounds down,
so an exact half rounds up.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Inside the loop, only multiply and add. What type must the product have before you add it?</li>
<li>After the loop, use the same "add half, shift, clamp" steps as in <code>q15_mul</code>, but with
both an upper and a lower clamp (a sum can be very negative).</li>
</ol>
</details>""",
r"""#include <stdint.h>

int16_t q15_dot(const int16_t *a, const int16_t *b, int n)
{
    return 0;
}
""",
r"""#include <stdint.h>

int16_t q15_dot(const int16_t *a, const int16_t *b, int n)
{
    int64_t acc = 0;
    for (int i = 0; i < n; i++)
        acc += (int32_t)a[i] * b[i];
    acc = (acc + (1 << 14)) >> 15;
    if (acc > 32767) return 32767;
    if (acc < -32768) return -32768;
    return (int16_t)acc;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const int16_t *a, const int16_t *b, int n)
{
    int64_t acc = 0;
    for (int i = 0; i < n; i++) acc += (int64_t)a[i] * b[i];
    acc = (acc + 16384) >> 15;
    return acc > 32767 ? 32767 : (acc < -32768 ? -32768 : (int)acc);
}
int main(void)
{
    int16_t a[64], b[64];
    char d[64];
    for (int t = 0; t < 200; t++) {
        int n = ck_range(0, 64), big = t % 3 == 0;
        for (int i = 0; i < n; i++) {
            a[i] = (int16_t)(big ? ck_range(-32768, 32767) : ck_range(-3000, 3000));
            b[i] = (int16_t)(big ? ck_range(-32768, 32767) : ck_range(-3000, 3000));
        }
        CK_FMT(d, "q15_dot(random a, b, n=%d)", n);
        ck_int(d, q15_dot(a, b, n), ref(a, b, n));
    }
    return ck_done();
}
""",
"One int64_t accumulator, one rounding step after the loop, then saturate."))

add(P("apply_gain_q15", S, "Apply a Q15 gain", "c", "func",
r"""<p><b>What to write.</b> A function
<code>void apply_gain_q15(int16_t *x, int n, int16_t gain)</code>. It multiplies every one of the
<code>n</code> samples in <code>x</code> by a Q15 <code>gain</code> and writes the result back into the
same array ("in place").</p>
<p><b>Why it matters.</b> This is a volume control on a fixed-point audio chip.</p>
<h4>The rule</h4>
<p>For every i from 0 to n&minus;1, do exactly what <code>q15_mul</code> does:</p>
<pre>x[i] = saturate( (x[i] * gain + 2^14) &gt;&gt; 15 )

saturate(v) = 32767 if v &gt; 32767, -32768 if v &lt; -32768, otherwise v</pre>
<h4>What different gains mean</h4>
<p>The gain is a Q15 number (real value = gain &divide; 32768). In decibels, gain in dB =
20&middot;log<sub>10</sub>(|gain| / 32768).</p>
<table>
<tr><th>gain</th><th>Real value</th><th>Effect</th></tr>
<tr><td>32767</td><td>0.99997</td><td>almost unchanged (about 0 dB)</td></tr>
<tr><td>23170</td><td>0.7071</td><td>&minus;3 dB: half the power</td></tr>
<tr><td>16384</td><td>0.5</td><td>&minus;6 dB: half the amplitude</td></tr>
<tr><td>0</td><td>0</td><td>silence</td></tr>
<tr><td>&minus;16384</td><td>&minus;0.5</td><td>half the amplitude and the polarity inverted</td></tr>
<tr><td>&minus;32768</td><td>&minus;1.0</td><td>polarity inverted: every sample changes sign</td></tr>
</table>
<h4>Examples (x = {1000, &minus;1000, 32767, &minus;32768})</h4>
<table>
<tr><th>gain</th><th>x after the call</th></tr>
<tr><td>16384</td><td>{500, &minus;500, 16384, &minus;16384}</td></tr>
<tr><td>23170</td><td>{707, &minus;707, 23169, &minus;23170}</td></tr>
<tr><td>&minus;32768</td><td>{&minus;1000, 1000, &minus;32767, 32767}</td></tr>
</table>
<p>Look at the last value of the last row: &minus;32768 &times; &minus;1.0 = +32768, which does not fit,
so it saturates to 32767.</p>
<pre> before:  x = [ 1000 | -1000 | 32767 | -32768 ]    gain = 16384 (0.5)
 after:   x = [  500 |  -500 | 16384 | -16384 ]    same array, overwritten</pre>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>You already wrote the multiply for one pair of values in <code>q15_mul</code>. What changes when
you do it for a whole array?</li>
<li>Remember that the gain can be negative, so a result can be too big at either end. Clamp at both
ends.</li>
</ol>
</details>""",
r"""#include <stdint.h>

void apply_gain_q15(int16_t *x, int n, int16_t gain)
{
}
""",
r"""#include <stdint.h>

void apply_gain_q15(int16_t *x, int n, int16_t gain)
{
    for (int i = 0; i < n; i++) {
        int32_t p = ((int32_t)x[i] * gain + (1 << 14)) >> 15;
        if (p > 32767) p = 32767;
        if (p < -32768) p = -32768;
        x[i] = (int16_t)p;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    int16_t x[256], y[256];
    char d[96];
    int gains[] = {32767, 16384, 0, -32768, -16384, 1, 23170};
    for (int g = 0; g < 7; g++) {
        int n = 256;
        for (int i = 0; i < n; i++) x[i] = y[i] = (int16_t)ck_range(-32768, 32767);
        x[0] = y[0] = -32768;
        apply_gain_q15(x, n, (int16_t)gains[g]);
        int bad = -1;
        for (int i = 0; i < n; i++) {
            int p = (y[i] * gains[g] + 16384) >> 15;
            p = p > 32767 ? 32767 : (p < -32768 ? -32768 : p);
            if (x[i] != p) { bad = i; break; }
        }
        CK_FMT(d, "apply_gain_q15 with gain %d (first wrong index %d)", gains[g], bad);
        ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Reuse your q15_mul recipe inside a loop."))

# ---------------------------------------------------------------------------
S = "DSP in C"

add(P("db_lin", S, "Decibels", "c", "func",
r"""<p><b>What to write.</b> Two functions that convert between decibels (dB) and plain
("linear") amplitude:</p>
<pre>float db_to_lin(float db);   // decibels -&gt; linear amplitude
float lin_to_db(float x);    // linear amplitude -&gt; decibels (x &gt; 0)</pre>
<p><b>Why it matters.</b> Volume knobs, meters and gain settings in audio are given in dB, but the code
multiplies samples by a linear number. You convert between the two all the time.</p>
<h4>The formulas (for amplitudes, such as sample values or voltages)</h4>
<pre>linear = 10^(dB / 20)
dB     = 20 * log10(linear)</pre>
<table>
<tr><th>dB</th><th>linear</th><th>Meaning</th></tr>
<tr><td>+20</td><td>10</td><td>ten times louder in amplitude</td></tr>
<tr><td>+6</td><td>1.995 (about 2)</td><td>about double</td></tr>
<tr><td>0</td><td>1</td><td>unchanged</td></tr>
<tr><td>&minus;3.0103</td><td>0.7071</td><td>half the power</td></tr>
<tr><td>&minus;6.0206</td><td>0.5</td><td>half the amplitude</td></tr>
<tr><td>&minus;20</td><td>0.1</td><td>one tenth</td></tr>
<tr><td>&minus;60</td><td>0.001</td><td>one thousandth</td></tr>
</table>
<p>Rule of thumb: every &minus;20 dB divides by 10, and every &minus;6 dB roughly halves.</p>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Result</th></tr>
<tr><td><code>db_to_lin(-6.0206f)</code></td><td>about 0.5</td></tr>
<tr><td><code>db_to_lin(20.0f)</code></td><td>10</td></tr>
<tr><td><code>db_to_lin(0.0f)</code></td><td>1</td></tr>
<tr><td><code>lin_to_db(0.1f)</code></td><td>about &minus;20</td></tr>
<tr><td><code>lin_to_db(2.0f)</code></td><td>about 6.0206</td></tr>
<tr><td><code>lin_to_db(1.0f)</code></td><td>0</td></tr>
</table>
<h4>Facts you need</h4>
<ul>
<li><code>powf(b, e)</code> from <code>&lt;math.h&gt;</code> returns b<sup>e</sup> for floats.</li>
<li><code>log10f(x)</code> returns the base-10 logarithm of x.</li>
<li>In C, <code>^</code> is <b>not</b> "to the power of". It is bitwise XOR: <code>10 ^ 2</code> is 8.</li>
</ul>
<h4>Inputs and limits</h4>
<ul>
<li><code>db</code> is between &minus;80 and +80.</li>
<li><code>x</code> is between 0.0001 and 10000, so it is always above 0 (the log of 0 does not
exist).</li>
<li>The answers must be right to about 5 significant digits.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Each function is one formula. Which <code>&lt;math.h&gt;</code> function does each formula need?</li>
<li>Check that <code>db / 20</code> is a float division (it is, because <code>db</code> is a
<code>float</code>).</li>
</ol>
</details>""",
r"""#include <math.h>

float db_to_lin(float db) { return 0.0f; }
float lin_to_db(float x)  { return 0.0f; }
""",
r"""#include <math.h>

float db_to_lin(float db) { return powf(10.0f, db / 20.0f); }
float lin_to_db(float x)  { return 20.0f * log10f(x); }
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[64];
    for (int i = 0; i < 100; i++) {
        double db = ck_unit() * 80.0;
        CK_FMT(d, "db_to_lin(%.4f)", db); ck_dbl(d, db_to_lin((float)db), pow(10.0, (double)(float)db / 20.0), 1e-5);
        double x = pow(10.0, ck_unit() * 4.0);
        CK_FMT(d, "lin_to_db(%.6g)", x); ck_dbl(d, lin_to_db((float)x), 20.0 * log10((double)(float)x), 1e-5);
    }
    return ck_done();
}
""",
"powf(10.0f, db / 20.0f) and 20.0f * log10f(x)."))

add(P("rms", S, "RMS level", "c", "func",
r"""<p><b>What to write.</b> A function <code>float rms(const float *x, int n)</code> that returns the
<b>root-mean-square</b> (RMS) level of the <code>n</code> samples in <code>x</code>.</p>
<p><b>Why it matters.</b> RMS is the usual measure of "how loud" a block of audio is. Level meters,
automatic gain control and compressors all use it.</p>
<h4>The formula</h4>
<pre>rms = sqrt( (x[0]^2 + x[1]^2 + ... + x[n-1]^2) / n )</pre>
<p>Read the name backwards and you get the steps: <b>S</b>quare every sample, take the <b>M</b>ean
(add them up and divide by n), then take the square <b>R</b>oot.</p>
<h4>Examples</h4>
<table>
<tr><th>x</th><th>Squares</th><th>Sum</th><th>Mean</th><th>RMS</th></tr>
<tr><td>{3, 4}</td><td>9, 16</td><td>25</td><td>12.5</td><td>3.5355</td></tr>
<tr><td>{1, &minus;1, 1, &minus;1}</td><td>1, 1, 1, 1</td><td>4</td><td>1</td><td>1</td></tr>
<tr><td>{0.5} (n = 1)</td><td>0.25</td><td>0.25</td><td>0.25</td><td>0.5</td></tr>
<tr><td>full-scale sine (peak 1)</td><td></td><td></td><td>0.5</td><td>0.7071 (= 1/&radic;2)</td></tr>
</table>
<p>Notice that negative samples count just as much as positive ones, because squaring removes the
sign.</p>
<h4>Inputs and limits</h4>
<ul>
<li><code>n</code> is at least 1 (the test uses up to 4800 samples). Samples are between &minus;1 and 1.</li>
<li>The answer must be right to about 4 significant digits.</li>
<li><code>sqrt</code> (double) and <code>sqrtf</code> (float) are in <code>&lt;math.h&gt;</code>.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>A <code>float</code> keeps only about 7 significant digits. When you add thousands of small
numbers to a big float sum, the low digits get lost. A <code>double</code> sum is safer.</li>
<li>Divide by <code>n</code> (not n&minus;1), and square the samples (do not take the absolute
value).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>One loop builds the sum of squares.</li>
<li>After the loop: divide, take the root, return it as a <code>float</code>.</li>
</ol>
</details>""",
r"""#include <math.h>

float rms(const float *x, int n)
{
    return 0.0f;
}
""",
r"""#include <math.h>

float rms(const float *x, int n)
{
    double s = 0.0;
    for (int i = 0; i < n; i++)
        s += (double)x[i] * x[i];
    return (float)sqrt(s / n);
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float x[4800];
    char d[64];
    for (int i = 0; i < 4800; i++) x[i] = (float)sin(2.0 * 3.141592653589793 * 1000.0 * i / 48000.0);
    ck_dbl("rms(full-scale 1 kHz sine, 4800 samples)", rms(x, 4800), sqrt(0.5), 1e-4);
    for (int t = 0; t < 30; t++) {
        int n = ck_range(1, 4800);
        double s = 0;
        for (int i = 0; i < n; i++) { x[i] = (float)ck_unit(); s += (double)x[i] * x[i]; }
        CK_FMT(d, "rms(random noise, n=%d)", n); ck_dbl(d, rms(x, n), sqrt(s / n), 1e-4);
    }
    return ck_done();
}
""",
"Sum the squares (a double accumulator is safest), divide by n, take the square root."))

add(P("zero_crossings", S, "Zero crossings", "c", "func",
r"""<p><b>What to write.</b> A function <code>int zero_crossings(const float *x, int n)</code>. It
counts how many times the signal changes from one side of zero to the other, between neighbouring
samples.</p>
<p><b>Why it matters.</b> A sine wave of f Hz crosses zero about 2f times per second (a 1 kHz tone
sampled at 48 kHz gives about 2000 crossings in one second). So the crossing rate is a very cheap
pitch estimate. Speech codecs also use it to tell voiced sounds (low rate) from hissing sounds (high
rate).</p>
<h4>The rule</h4>
<ul>
<li>A sample is on the <b>negative</b> side if <code>x &lt; 0</code>. Everything else is on the positive
side. So <b>0 counts as positive</b>.</li>
<li>For each i from 1 to n&minus;1, compare sample i&minus;1 with sample i. Count it when they are on
different sides: <code>(x[i-1] &lt; 0) != (x[i] &lt; 0)</code>.</li>
</ul>
<h4>Picture</h4>
<pre> index:    0     1     2     3     4     5     6
 x:       0.5   0.2  -0.1  -0.4   0.3   0.6  -0.2
 side:     +     +     -     -     +     +     -
 change?         no    YES   no    YES   no    YES    --&gt; 3 crossings</pre>
<h4>Examples</h4>
<table>
<tr><th>x</th><th>Sides</th><th>Counted at i</th><th>Result</th></tr>
<tr><td>{0.5, 0.2, &minus;0.1, &minus;0.4, 0.3, 0.6, &minus;0.2}</td><td>+ + &minus; &minus; + + &minus;</td><td>2, 4, 6</td><td>3</td></tr>
<tr><td>{0, 0, &minus;1, 0, 1}</td><td>+ + &minus; + +</td><td>2, 3</td><td>2</td></tr>
<tr><td>{0.7} (n = 1)</td><td>+</td><td>none (no pairs)</td><td>0</td></tr>
</table>
<p>In the second row, the step from 0 to 1 is <b>not</b> a crossing, because 0 already counts as
positive.</p>
<h4>Inputs and limits</h4>
<ul><li><code>n</code> is 1 to 2000.</li></ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Which indices i have a neighbour on the left? Start your loop there.</li>
<li>For each pair, work out a true/false "is negative" for both samples and compare the two.</li>
</ol>
</details>""",
r"""int zero_crossings(const float *x, int n)
{
    return 0;
}
""",
r"""int zero_crossings(const float *x, int n)
{
    int c = 0;
    for (int i = 1; i < n; i++)
        if ((x[i - 1] < 0.0f) != (x[i] < 0.0f))
            c++;
    return c;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const float *x, int n) { int c = 0; for (int i = 1; i < n; i++) c += (x[i - 1] < 0) != (x[i] < 0); return c; }
int main(void)
{
    static float x[2000];
    char d[64];
    float z[] = {0.0f, 0.0f, -1.0f, 0.0f, 1.0f};
    ck_int("zero_crossings({0, 0, -1, 0, 1}, 5)", zero_crossings(z, 5), 2);
    for (int t = 0; t < 30; t++) {
        int n = ck_range(1, 2000);
        for (int i = 0; i < n; i++) x[i] = (float)ck_unit();
        CK_FMT(d, "zero_crossings(noise, n=%d)", n); ck_int(d, zero_crossings(x, n), ref(x, n));
    }
    return ck_done();
}
""",
"Compare the sign test of each sample with the one before it."))

add(P("moving_average", S, "Moving average", "c", "func",
r"""<p><b>What to write.</b> A function
<code>void moving_average(const float *x, float *y, int n, int L)</code>. For every position i, it writes
into y[i] the average of the last <code>L</code> inputs, x[i&minus;L+1] up to x[i].</p>
<p><b>Why it matters.</b> The moving average is the simplest smoothing filter. It is used to clean up
sensor readings and to estimate slowly changing levels.</p>
<h4>The formula</h4>
<pre>y[i] = ( x[i-L+1] + x[i-L+2] + ... + x[i] ) / L</pre>
<ul>
<li>Samples before the start of the array (negative index) count as 0.</li>
<li>Always divide by <code>L</code>, even at the start where fewer than L real samples exist.</li>
</ul>
<h4>Picture: a window of L samples slides along x</h4>
<pre> x:   [ 3 ][ 6 ][ 9 ][12 ][15 ]          L = 3
       \___________/
        y[2] = (3 + 6 + 9) / 3 = 6
            \___________/
             y[3] = (6 + 9 + 12) / 3 = 9</pre>
<h4>Worked example with a running sum (x = {3, 6, 9, 12, 15}, L = 3)</h4>
<p>Instead of adding L numbers for every output, keep a running sum. Each step adds the new sample and,
once the window is full, removes the sample that just left the window (x[i&minus;L]).</p>
<table>
<tr><th>i</th><th>x[i]</th><th>Add</th><th>Remove x[i&minus;L]</th><th>Sum</th><th>y[i] = sum / 3</th></tr>
<tr><td>0</td><td>3</td><td>+3</td><td>(nothing, i &lt; L)</td><td>3</td><td>1</td></tr>
<tr><td>1</td><td>6</td><td>+6</td><td>(nothing)</td><td>9</td><td>3</td></tr>
<tr><td>2</td><td>9</td><td>+9</td><td>(nothing)</td><td>18</td><td>6</td></tr>
<tr><td>3</td><td>12</td><td>+12</td><td>&minus;3 (x[0])</td><td>27</td><td>9</td></tr>
<tr><td>4</td><td>15</td><td>+15</td><td>&minus;6 (x[1])</td><td>36</td><td>12</td></tr>
</table>
<h4>More examples</h4>
<ul>
<li>L = 1: y is a copy of x.</li>
<li>L larger than n: x = {4, 8}, L = 4 gives y = {1, 3} (4/4 and 12/4).</li>
</ul>
<h4>Inputs and limits</h4>
<ul>
<li><code>n</code> is 1 to 3000 and <code>L</code> is 1 to 64. L may be bigger than n.</li>
<li>Answers must be right to about 0.0001. A <code>double</code> running sum keeps it accurate.</li>
<li>Try to make it O(n), meaning the work grows with n only. Two nested loops (n outputs &times; L
inputs each) would be O(n&middot;L).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>When you move from y[i&minus;1] to y[i], which one sample enters the window and which one leaves
it?</li>
<li>From which i onwards does a sample leave the window?</li>
</ol>
</details>""",
r"""void moving_average(const float *x, float *y, int n, int L)
{
}
""",
r"""void moving_average(const float *x, float *y, int n, int L)
{
    double s = 0.0;
    for (int i = 0; i < n; i++) {
        s += x[i];
        if (i >= L)
            s -= x[i - L];
        y[i] = (float)(s / L);
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float x[3000], y[3000];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int n = ck_range(1, 3000), L = ck_range(1, 64);
        for (int i = 0; i < n; i++) x[i] = (float)ck_unit();
        moving_average(x, y, n, L);
        int bad = -1;
        for (int i = 0; i < n && bad < 0; i++) {
            double s = 0; for (int k = 0; k < L; k++) if (i - k >= 0) s += x[i - k];
            if (fabs(y[i] - s / L) > 1e-4) bad = i;
        }
        CK_FMT(d, "moving_average(n=%d, L=%d): first wrong y index %d", n, L, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Keep a running sum: add x[i], and once i >= L subtract x[i - L]."))

add(P("fir", S, "FIR filter (block)", "c", "func",
r"""<p><b>What to write.</b> The direct-form <b>FIR filter</b> (finite impulse response filter) for a
whole block of samples:</p>
<pre>void fir(const float *h, int M, const float *x, float *y, int n);</pre>
<p><code>h</code> holds the <code>M</code> filter coefficients (called <em>taps</em>), <code>x</code>
holds <code>n</code> input samples, and you write <code>n</code> output samples into
<code>y</code>.</p>
<p><b>Why it matters.</b> FIR filters are everywhere in DSP: equalisers, anti-alias filters, channel
filters in modems. This loop is the classic DSP interview question.</p>
<h4>The formula</h4>
<pre>y[i] = h[0]*x[i] + h[1]*x[i-1] + h[2]*x[i-2] + ... + h[M-1]*x[i-M+1]</pre>
<p>Inputs before the start of the array (negative index) count as 0. Each output mixes the current
input with the M&minus;1 inputs before it.</p>
<h4>Picture: a tapped delay line</h4>
<pre> x[i] ---+--[z^-1]--+--[z^-1]--+-- ... --[z^-1]--+
         |   x[i-1] |   x[i-2]  |                 | x[i-M+1]
       *h[0]      *h[1]       *h[2]            *h[M-1]
         |          |           |                 |
         +---------(+)---------(+)---- ... ------(+)----&gt; y[i]

 [z^-1] means "one sample of delay"</pre>
<h4>Worked examples</h4>
<p>Example 1: h = {0.5, 0.25}, x = {1, 0, 0, 2}.</p>
<table>
<tr><th>i</th><th>Sum</th><th>y[i]</th></tr>
<tr><td>0</td><td>0.5&middot;x[0] + 0.25&middot;x[&minus;1] = 0.5&middot;1 + 0.25&middot;0</td><td>0.5</td></tr>
<tr><td>1</td><td>0.5&middot;0 + 0.25&middot;1</td><td>0.25</td></tr>
<tr><td>2</td><td>0.5&middot;0 + 0.25&middot;0</td><td>0</td></tr>
<tr><td>3</td><td>0.5&middot;2 + 0.25&middot;0</td><td>1.0</td></tr>
</table>
<p>Example 2: h = {1, 1, 1} (a sum of the last 3 inputs), x = {1, 2, 3, 4} gives
y = {1, 3, 6, 9}.</p>
<p>Useful self-test: if x is an impulse {1, 0, 0, &hellip;}, the output is the taps themselves,
y = {h[0], h[1], h[2], &hellip;}.</p>
<h4>Inputs and limits</h4>
<ul>
<li><code>M</code> is 1 to 64, <code>n</code> is 1 to 1000.</li>
<li>Answers must be right to about 0.0001.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>For the first outputs, i&minus;k can be negative. Reading <code>x[-1]</code> reads memory outside
the array. Skip those terms (they are 0).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>You need two loops: one over the outputs i, and one over the taps k.</li>
<li>For a given i, which values of k give a valid index i&minus;k?</li>
</ol>
</details>""",
r"""void fir(const float *h, int M, const float *x, float *y, int n)
{
}
""",
r"""void fir(const float *h, int M, const float *x, float *y, int n)
{
    for (int i = 0; i < n; i++) {
        float acc = 0.0f;
        for (int k = 0; k < M && k <= i; k++)
            acc += h[k] * x[i - k];
        y[i] = acc;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float h[64], x[1000], y[1000];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int M = ck_range(1, 64), n = ck_range(1, 1000);
        for (int k = 0; k < M; k++) h[k] = (float)ck_unit() / 8.0f;
        for (int i = 0; i < n; i++) x[i] = (float)ck_unit();
        fir(h, M, x, y, n);
        int bad = -1;
        for (int i = 0; i < n && bad < 0; i++) {
            double s = 0; for (int k = 0; k < M && k <= i; k++) s += (double)h[k] * x[i - k];
            if (fabs(y[i] - s) > 1e-4) bad = i;
        }
        CK_FMT(d, "fir(M=%d, n=%d): first wrong y index %d", M, n, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Two loops: over output samples i, and over taps k with k <= i (so you never read x[-1])."))

add(P("fir_state", S, "FIR filter with a circular buffer", "c", "func",
r"""<p><b>What to write.</b> The same FIR filter as the previous problem, but for <b>real time</b>:
samples arrive one at a time, and you return one output for each one. The starter code defines the
state structure <code>Fir</code>. Write:</p>
<pre>// copy the taps and clear the history
void  fir_init(Fir *f, const float *h, int M);

// one sample in, one sample out
float fir_process(Fir *f, float x);</pre>
<p><b>Why it matters.</b> An audio driver hands you the signal sample by sample (or in small blocks).
To compute y = h[0]&middot;x[n] + h[1]&middot;x[n&minus;1] + &hellip;, the filter must remember its last M
inputs between calls.</p>
<h4>The idea: a circular buffer</h4>
<p>The array <code>z</code> holds the last <code>M</code> inputs. You could shift all of them by one
place for every new sample, but that is slow. Instead, write the new sample over the <b>oldest</b> one
and move an index. <code>pos</code> is the slot where the next input goes.</p>
<h4>The rule, step by step (one call of fir_process)</h4>
<ol>
<li>Store the new input: z[pos] = x. It replaces the oldest input.</li>
<li>Compute the output. h[0] goes with the newest input (slot pos), h[1] with the slot before it,
and so on, going <b>backwards</b> through z. Going back from slot 0 wraps to slot M&minus;1.</li>
<li>Move <code>pos</code> one slot forward, wrapping from M&minus;1 to 0.</li>
</ol>
<h4>Picture (M = 3, while computing the output for the 4th input, x = 4)</h4>
<pre> slot:     0       1       2
 z:     [  4  ] [  2  ] [  3  ]
           ^
          pos = 0 (the 4 was just written here, over the oldest input, 1)

 read order:  slot 0 (newest, * h[0]) -&gt; slot 2 (* h[1]) -&gt; slot 1 (* h[2])
              going left, and jumping from slot 0 round to slot 2</pre>
<h4>Worked example: h = {0.5, 0.3, 0.2}, M = 3, inputs 1, 2, 3, 4, 5</h4>
<table>
<tr><th>Input</th><th>Slot written</th><th>z after writing</th><th>Slots read for h[0], h[1], h[2]</th><th>Output</th></tr>
<tr><td>1</td><td>0</td><td>[1, 0, 0]</td><td>0, 2, 1</td><td>0.5</td></tr>
<tr><td>2</td><td>1</td><td>[1, 2, 0]</td><td>1, 0, 2</td><td>1.3</td></tr>
<tr><td>3</td><td>2</td><td>[1, 2, 3]</td><td>2, 1, 0</td><td>2.3</td></tr>
<tr><td>4</td><td>0</td><td>[4, 2, 3]</td><td>0, 2, 1</td><td>3.3</td></tr>
<tr><td>5</td><td>1</td><td>[4, 5, 3]</td><td>1, 0, 2</td><td>4.3</td></tr>
</table>
<p>Check the 4th row: 0.5&middot;4 + 0.3&middot;3 + 0.2&middot;2 = 2 + 0.9 + 0.4 = 3.3. The outputs are
exactly what the block FIR would give for x = {1, 2, 3, 4, 5}.</p>
<h4>Requirements</h4>
<ul>
<li>The output must equal the block FIR from the previous problem (to about 0.0001).</li>
<li><code>fir_init</code> must set <b>everything</b> it uses: M, the taps, the history (all 0) and
<code>pos</code>. The test fills the structure with garbage before calling it.</li>
<li>Each call should cost O(M): a loop over the taps, with nothing shifted.</li>
<li><code>M</code> is 1 to 64. With M = 1 there is only one slot, and <code>pos</code> stays 0.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Use two indices in the loop: k goes forwards through h, and a slot index j goes backwards through
z.</li>
<li>How do you step j backwards so that after 0 it becomes M&minus;1?</li>
<li>When must <code>pos</code> move: before or after the output is computed?</li>
</ol>
</details>""",
r"""#define FIR_MAX 64

typedef struct {
    float h[FIR_MAX];   // taps
    float z[FIR_MAX];   // past inputs (circular)
    int M;              // number of taps
    int pos;            // where the next input goes
} Fir;

void fir_init(Fir *f, const float *h, int M)
{
}

float fir_process(Fir *f, float x)
{
    return 0.0f;
}
""",
r"""#define FIR_MAX 64

typedef struct {
    float h[FIR_MAX];
    float z[FIR_MAX];
    int M;
    int pos;
} Fir;

void fir_init(Fir *f, const float *h, int M)
{
    f->M = M;
    f->pos = 0;
    for (int k = 0; k < M; k++) {
        f->h[k] = h[k];
        f->z[k] = 0.0f;
    }
}

float fir_process(Fir *f, float x)
{
    f->z[f->pos] = x;
    float acc = 0.0f;
    int j = f->pos;
    for (int k = 0; k < f->M; k++) {
        acc += f->h[k] * f->z[j];
        j = (j == 0) ? f->M - 1 : j - 1;
    }
    f->pos = (f->pos + 1) % f->M;
    return acc;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float h[64], x[1000];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int M = ck_range(1, 64), n = ck_range(1, 1000);
        for (int k = 0; k < M; k++) h[k] = (float)ck_unit() / 8.0f;
        for (int i = 0; i < n; i++) x[i] = (float)ck_unit();
        Fir f;
        memset(&f, 0x7F, sizeof f);   /* garbage: fir_init must reset everything */
        fir_init(&f, h, M);
        int bad = -1;
        for (int i = 0; i < n; i++) {
            float y = fir_process(&f, x[i]);
            double s = 0; for (int k = 0; k < M && k <= i; k++) s += (double)h[k] * x[i - k];
            if (bad < 0 && fabs(y - s) > 1e-4) bad = i;
        }
        CK_FMT(d, "fir_process(M=%d, %d samples): first wrong output %d", M, n, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Write x at z[pos]. Then walk backwards from pos (wrapping from 0 to M-1) while stepping forwards through h. Finally advance pos modulo M."))

add(P("biquad_df1", S, "Biquad, Direct Form I", "c", "func",
r"""<p><b>What to write.</b> A <b>biquad</b> filter in "Direct Form I". The starter code defines the
structure <code>BiquadDF1</code>. Write:</p>
<pre>// store the five coefficients and set the state to 0
void  bq1_init(BiquadDF1 *q, float b0, float b1, float b2,
               float a1, float a2);

// one sample in, one sample out
float bq1_process(BiquadDF1 *q, float x);</pre>
<p><b>Why it matters.</b> A biquad is a second-order <b>IIR</b> filter: it uses past outputs as well as
past inputs ("infinite impulse response"). Low-pass, high-pass, band-pass, notch and EQ filters are all
biquads; only the five coefficients change. Longer filters are built as chains of biquads. It is the
workhorse of audio EQ.</p>
<h4>The formula (with a<sub>0</sub> = 1)</h4>
<pre>y[n] = b0*x[n] + b1*x[n-1] + b2*x[n-2] - a1*y[n-1] - a2*y[n-2]</pre>
<p>Note the <b>minus</b> signs in front of a1 and a2. x[n&minus;1] means "the input one sample ago",
y[n&minus;2] means "the output two samples ago", and so on.</p>
<h4>Picture (signal flow)</h4>
<pre> x[n] --+--&gt;(*b0)--&gt;(+)--------------------+--&gt; y[n]
        |            ^                     |
      [z^-1]         |                   [z^-1]
        | x[n-1]     |                     | y[n-1]
        +--&gt;(*b1)--&gt;(+)&lt;-----(*-a1)&lt;-------+
        |            ^                     |
      [z^-1]         |                   [z^-1]
        | x[n-2]     |                     | y[n-2]
        +--&gt;(*b2)--&gt;(+)&lt;-----(*-a2)&lt;-------+

 [z^-1] = one sample of delay</pre>
<h4>The state</h4>
<p>Direct Form I remembers the last two inputs and the last two outputs:
<code>x1</code> = x[n&minus;1], <code>x2</code> = x[n&minus;2], <code>y1</code> = y[n&minus;1],
<code>y2</code> = y[n&minus;2]. After computing y, move the history along by one: the old x1 becomes x2,
the current input becomes x1, and the same for y.</p>
<h4>Worked example</h4>
<p>Coefficients b0 = 0.25, b1 = 0.5, b2 = 0.25, a1 = &minus;0.5, a2 = 0.25. Input: an impulse
1, 0, 0, 0, 0, 0. (Because a1 is negative, &minus;a1&middot;y1 = +0.5&middot;y1.)</p>
<table>
<tr><th>n</th><th>x</th><th>x1</th><th>x2</th><th>y1</th><th>y2</th><th>y</th></tr>
<tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0.25</td></tr>
<tr><td>1</td><td>0</td><td>1</td><td>0</td><td>0.25</td><td>0</td><td>0.625</td></tr>
<tr><td>2</td><td>0</td><td>0</td><td>1</td><td>0.625</td><td>0.25</td><td>0.5</td></tr>
<tr><td>3</td><td>0</td><td>0</td><td>0</td><td>0.5</td><td>0.625</td><td>0.09375</td></tr>
<tr><td>4</td><td>0</td><td>0</td><td>0</td><td>0.09375</td><td>0.5</td><td>&minus;0.078125</td></tr>
<tr><td>5</td><td>0</td><td>0</td><td>0</td><td>&minus;0.078125</td><td>0.09375</td><td>&minus;0.0625</td></tr>
</table>
<p>Check row 2: 0.25&middot;1 + 0.5&middot;0.625 &minus; 0.25&middot;0.25 = 0.25 + 0.3125 &minus;
0.0625 = 0.5. The output keeps going after the input has stopped: that is the "infinite" response.</p>
<h4>Requirements</h4>
<ul>
<li><code>bq1_init</code> stores the five coefficients and sets x1, x2, y1, y2 to 0. The test fills the
structure with garbage first, so every field must be set.</li>
<li>The test runs low-pass filters (100 Hz to 12 kHz at 48 kHz) on noise. Outputs must match the
formula to about 0.001.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Compute y from the formula using the state as it is <b>before</b> this sample.</li>
<li>Then update the history. In which order must you copy the values so that nothing is overwritten
before it has been moved?</li>
</ol>
</details>""",
r"""typedef struct {
    float b0, b1, b2, a1, a2;   // coefficients
    float x1, x2, y1, y2;       // state
} BiquadDF1;

void bq1_init(BiquadDF1 *q, float b0, float b1, float b2, float a1, float a2)
{
}

float bq1_process(BiquadDF1 *q, float x)
{
    return x;
}
""",
r"""typedef struct {
    float b0, b1, b2, a1, a2;
    float x1, x2, y1, y2;
} BiquadDF1;

void bq1_init(BiquadDF1 *q, float b0, float b1, float b2, float a1, float a2)
{
    q->b0 = b0; q->b1 = b1; q->b2 = b2; q->a1 = a1; q->a2 = a2;
    q->x1 = q->x2 = q->y1 = q->y2 = 0.0f;
}

float bq1_process(BiquadDF1 *q, float x)
{
    float y = q->b0 * x + q->b1 * q->x1 + q->b2 * q->x2 - q->a1 * q->y1 - q->a2 * q->y2;
    q->x2 = q->x1; q->x1 = x;
    q->y2 = q->y1; q->y1 = y;
    return y;
}
""",
r"""#include "check.h"
#include "solution.c"
static void coeffs(double fs, double f0, double Q, double c[5])
{
    double w = 2 * 3.141592653589793 * f0 / fs, al = sin(w) / (2 * Q), cs = cos(w), a0 = 1 + al;
    c[0] = (1 - cs) / 2 / a0; c[1] = (1 - cs) / a0; c[2] = (1 - cs) / 2 / a0; c[3] = -2 * cs / a0; c[4] = (1 - al) / a0;
}
int main(void)
{
    char d[96];
    double fcs[] = {100, 1000, 5000, 12000};
    for (int t = 0; t < 4; t++) {
        double c[5]; coeffs(48000, fcs[t], 0.707, c);
        BiquadDF1 q; memset(&q, 0x7F, sizeof q);
        bq1_init(&q, (float)c[0], (float)c[1], (float)c[2], (float)c[3], (float)c[4]);
        double x1 = 0, x2 = 0, y1 = 0, y2 = 0; int bad = -1;
        for (int i = 0; i < 2000; i++) {
            float x = (float)ck_unit();
            double y = (float)c[0] * (double)x + (float)c[1] * x1 + (float)c[2] * x2 - (float)c[3] * y1 - (float)c[4] * y2;
            x2 = x1; x1 = x; y2 = y1; y1 = y;
            float g = bq1_process(&q, x);
            if (bad < 0 && fabs(g - y) > 1e-3) bad = i;
        }
        CK_FMT(d, "low-pass at %.0f Hz on noise: first wrong output %d", fcs[t], bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Compute y from the formula, then shift the history: x2 = x1, x1 = x, y2 = y1, y1 = y. bq1_init must zero the state."))

add(P("biquad_tdf2", S, "Biquad, Transposed Direct Form II", "c", "func",
r"""<p><b>What to write.</b> The same biquad filter in <b>Transposed Direct Form II</b> (TDF2), for
the structure <code>BiquadTDF2</code> in the starter code: <code>bq2_init</code> (store the coefficients,
set the state to 0) and <code>bq2_process</code> (one sample in, one sample out).</p>
<p><b>Why it matters.</b> TDF2 computes exactly the same filter as Direct Form I, but it needs only
<b>two</b> state variables instead of four, and it behaves well in floating point. That makes it the
usual choice for float audio code.</p>
<h4>The three lines (run them in this order for every sample)</h4>
<pre>y  = b0*x + s1
s1 = b1*x - a1*y + s2
s2 = b2*x - a2*y</pre>
<p><code>s1</code> and <code>s2</code> are partial sums that were prepared during earlier samples.
<code>y</code> must be computed first, because the new s1 and s2 both need it. The new s1 uses the
<b>old</b> s2, which is why s1 is updated before s2.</p>
<h4>Picture (signal flow)</h4>
<pre> x[n] -----+---------------+---------------+
           |               |               |
         (*b0)           (*b1)           (*b2)
           |               |               |
           v               v               v
 y[n] &lt;---(+)&lt;--[z^-1]----(+)&lt;--[z^-1]----(+)
           |      s1       ^      s2       ^
           |               |               |
           +-----------&gt;(*-a1)             |
           |                               |
           +---------------------------&gt;(*-a2)

 [z^-1] = one sample of delay (this is where s1 and s2 are stored)</pre>
<h4>Worked example (same filter as the Direct Form I problem)</h4>
<p>b0 = 0.25, b1 = 0.5, b2 = 0.25, a1 = &minus;0.5, a2 = 0.25. Input: 1, 0, 0, 0, &hellip;</p>
<table>
<tr><th>n</th><th>x</th><th>s1 before</th><th>s2 before</th><th>y</th><th>new s1</th><th>new s2</th></tr>
<tr><td>0</td><td>1</td><td>0</td><td>0</td><td>0.25</td><td>0.625</td><td>0.1875</td></tr>
<tr><td>1</td><td>0</td><td>0.625</td><td>0.1875</td><td>0.625</td><td>0.5</td><td>&minus;0.15625</td></tr>
<tr><td>2</td><td>0</td><td>0.5</td><td>&minus;0.15625</td><td>0.5</td><td>0.09375</td><td>&minus;0.125</td></tr>
<tr><td>3</td><td>0</td><td>0.09375</td><td>&minus;0.125</td><td>0.09375</td><td>&minus;0.078125</td><td>&minus;0.0234375</td></tr>
</table>
<p>Check row 0: new s1 = 0.5&middot;1 &minus; (&minus;0.5)&middot;0.25 + 0 = 0.625, and new s2 =
0.25&middot;1 &minus; 0.25&middot;0.25 = 0.1875. The outputs 0.25, 0.625, 0.5, 0.09375 are the same as in
Direct Form I.</p>
<h4>Requirements</h4>
<ul>
<li><code>bq2_init</code> must set all five coefficients and both state values. The test fills the
structure with garbage first.</li>
<li>The test runs high-pass filters (80 Hz to 15 kHz at 48 kHz) on noise and compares with the
Direct Form I formula, to about 0.001.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Copy the three lines into your function, reading and writing the state through the pointer
<code>q</code>.</li>
<li>Ask yourself for each line: does it need the old value of a state variable, or the new one?</li>
</ol>
</details>""",
r"""typedef struct {
    float b0, b1, b2, a1, a2;
    float s1, s2;
} BiquadTDF2;

void bq2_init(BiquadTDF2 *q, float b0, float b1, float b2, float a1, float a2)
{
}

float bq2_process(BiquadTDF2 *q, float x)
{
    return x;
}
""",
r"""typedef struct {
    float b0, b1, b2, a1, a2;
    float s1, s2;
} BiquadTDF2;

void bq2_init(BiquadTDF2 *q, float b0, float b1, float b2, float a1, float a2)
{
    q->b0 = b0; q->b1 = b1; q->b2 = b2; q->a1 = a1; q->a2 = a2;
    q->s1 = q->s2 = 0.0f;
}

float bq2_process(BiquadTDF2 *q, float x)
{
    float y = q->b0 * x + q->s1;
    q->s1 = q->b1 * x - q->a1 * y + q->s2;
    q->s2 = q->b2 * x - q->a2 * y;
    return y;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    double fcs[] = {80, 800, 4000, 15000};
    for (int t = 0; t < 4; t++) {
        double w = 2 * 3.141592653589793 * fcs[t] / 48000, al = sin(w) / (2 * 0.9), cs = cos(w), a0 = 1 + al;
        float c[5] = {(float)((1 + cs) / 2 / a0), (float)(-(1 + cs) / a0), (float)((1 + cs) / 2 / a0), (float)(-2 * cs / a0), (float)((1 - al) / a0)};
        BiquadTDF2 q; memset(&q, 0x7F, sizeof q);
        bq2_init(&q, c[0], c[1], c[2], c[3], c[4]);
        double x1 = 0, x2 = 0, y1 = 0, y2 = 0; int bad = -1;
        for (int i = 0; i < 2000; i++) {
            float x = (float)ck_unit();
            double y = c[0] * (double)x + c[1] * x1 + c[2] * x2 - c[3] * y1 - c[4] * y2;
            x2 = x1; x1 = x; y2 = y1; y1 = y;
            float g = bq2_process(&q, x);
            if (bad < 0 && fabs(g - y) > 1e-3) bad = i;
        }
        CK_FMT(d, "high-pass at %.0f Hz on noise: first wrong output %d", fcs[t], bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Use the three lines in order. Compute y first, because s1 and s2 need it."))

add(P("onepole", S, "One-pole smoother", "c", "func",
r"""<p><b>What to write.</b> A function <code>float onepole(float *state, float a, float x)</code>.
<code>*state</code> holds the previous output. The function computes the new output, stores it in
<code>*state</code>, and returns it.</p>
<p><b>Why it matters.</b> This one-pole low-pass filter smooths control values such as a volume knob.
If the volume jumps straight from one value to another, you hear a click. Smoothed, it glides there in
a few milliseconds.</p>
<h4>The formula</h4>
<pre>y[n] = y[n-1] + a * (x[n] - y[n-1])</pre>
<p>In words: (x[n] &minus; y[n&minus;1]) is the gap between where the output is and where the input
wants it to be. Each sample, the output moves the fraction <code>a</code> of that gap.</p>
<h4>Picture (a = 0.5, input jumps from 0 to 1 and stays there)</h4>
<pre> y:  0 -----&gt; 0.5 -----&gt; 0.75 -----&gt; 0.875 -----&gt; 0.9375 ... --&gt; 1
       half of    half of     half of      half of
       the gap    the gap     the gap      the gap</pre>
<h4>Examples (the state starts at 0)</h4>
<table>
<tr><th>a</th><th>Inputs</th><th>Outputs</th><th>Note</th></tr>
<tr><td>0.5</td><td>1, 1, 1, 1</td><td>0.5, 0.75, 0.875, 0.9375</td><td></td></tr>
<tr><td>0.1</td><td>1, 1, 1, 1</td><td>0.1, 0.19, 0.271, 0.3439</td><td>smaller a: slower, smoother</td></tr>
<tr><td>0.5</td><td>1, 1, 0, 0</td><td>0.5, 0.75, 0.375, 0.1875</td><td>falls the same way</td></tr>
<tr><td>1.0</td><td>1, 0.3</td><td>1, 0.3</td><td>a = 1: output = input, no smoothing</td></tr>
</table>
<p>With a = 0 the output would never change.</p>
<h4>Facts you need</h4>
<ul>
<li>The function has no structure of its own. The caller keeps the state variable and passes its
address. Writing through the pointer (<code>*state = &hellip;</code>) is what makes the value survive
until the next call.</li>
<li>After each call, <code>*state</code> must equal the value you return. The test checks this.</li>
<li><code>a</code> is between 0 and 1 (the test uses 0.01 to 0.5).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Which variable holds y[n&minus;1]? Read it through the pointer.</li>
<li>Compute the new value, write it back through the pointer, and return the same value.</li>
</ol>
</details>""",
r"""float onepole(float *state, float a, float x)
{
    return x;
}
""",
r"""float onepole(float *state, float a, float x)
{
    *state += a * (x - *state);
    return *state;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    for (int t = 0; t < 10; t++) {
        float a = (float)(0.01 + 0.49 * (ck_unit() + 1) / 2), s = 0.0f;
        float r = 0; int bad = -1;
        for (int i = 0; i < 1000; i++) {
            float x = i < 500 ? 1.0f : (float)ck_unit();
            r += a * (x - r);
            float y = onepole(&s, a, x);
            if (bad < 0 && (fabs(y - r) > 1e-4 || s != y)) bad = i;
        }
        CK_FMT(d, "onepole with a=%.4f: first wrong output %d", a, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"*state += a * (x - *state); return *state;"))

add(P("dc_blocker", S, "DC blocker", "c", "func",
r"""<p><b>What to write.</b> A <b>DC blocker</b>: a filter that removes a constant offset from a
signal. The starter code defines the structure <code>DcBlock</code>. Write:</p>
<pre>void  dc_init(DcBlock *b, float R);  // store R, clear the state
float dc_process(DcBlock *b, float x);</pre>
<p><b>Why it matters.</b> A microphone or an ADC often adds a small constant value (an offset) to the
signal. A constant is a 0 Hz signal, also called <b>DC</b> ("direct current"). It wastes headroom and
causes clicks when the sound starts or stops. The DC blocker removes it and keeps the sound.</p>
<h4>The formula</h4>
<pre>y[n] = x[n] - x[n-1] + R * y[n-1]        R is close to 1, for example 0.995</pre>
<ul>
<li>x[n] &minus; x[n&minus;1] is the change from the last sample. A constant does not change, so this
part removes it.</li>
<li>The term R&middot;y[n&minus;1] feeds back part of the old output. It gives back the low
frequencies that the difference alone would weaken, except 0 Hz itself.</li>
<li>The closer R is to 1, the fewer low frequencies are lost, but the slower the offset dies away.</li>
</ul>
<h4>Picture (signal flow)</h4>
<pre> x[n] --+------------------&gt;(+)--------------+--&gt; y[n]
        |                   ^ ^              |
      [z^-1]                | |            [z^-1]
        | x[n-1]            | |              | y[n-1]
        +-----&gt;(*-1)--------+ +-----(*R)&lt;----+</pre>
<h4>Examples (state starts at 0, input is a constant 1)</h4>
<table>
<tr><th>R</th><th>Outputs</th></tr>
<tr><td>0.5</td><td>1, 0.5, 0.25, 0.125, 0.0625 (halves every sample, towards 0)</td></tr>
<tr><td>0.995</td><td>1, 0.995, 0.990025, 0.985075 (falls by 0.5 % per sample)</td></tr>
</table>
<p>With R = 0.995 and a constant input of 0.25, the output is about 0.152 after 100 samples, 0.025
after 460 samples and 0.0017 after 1000 samples. The offset is gone.</p>
<h4>Requirements</h4>
<ul>
<li>The state is <code>x1</code> (previous input) and <code>y1</code> (previous output).
<code>dc_init</code> stores R and sets both to 0. The test fills the structure with garbage first.</li>
<li>The test feeds 0.25 + a 440 Hz sine (48 kHz, 20000 samples) with R = 0.995. Every output must match
the formula (to about 0.0001), and at the end the offset must be removed (|y| &lt; 0.15).</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>It is the same pattern as the biquad: compute y from the current state, then update the state.</li>
<li>Which two values must you remember for the next call?</li>
</ol>
</details>""",
r"""typedef struct {
    float R;
    float x1;   // previous input
    float y1;   // previous output
} DcBlock;

void dc_init(DcBlock *b, float R)
{
}

float dc_process(DcBlock *b, float x)
{
    return x;
}
""",
r"""typedef struct {
    float R;
    float x1;
    float y1;
} DcBlock;

void dc_init(DcBlock *b, float R)
{
    b->R = R;
    b->x1 = 0.0f;
    b->y1 = 0.0f;
}

float dc_process(DcBlock *b, float x)
{
    float y = x - b->x1 + b->R * b->y1;
    b->x1 = x;
    b->y1 = y;
    return y;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    DcBlock b; memset(&b, 0x7F, sizeof b);
    dc_init(&b, 0.995f);
    float x1 = 0, y1 = 0; int bad = -1; float last = 0;
    for (int i = 0; i < 20000; i++) {
        float x = 0.25f + 0.1f * (float)sin(2 * 3.14159265 * 440.0 * i / 48000.0);
        float y = x - x1 + 0.995f * y1; x1 = x; y1 = y;
        last = dc_process(&b, x);
        if (bad < 0 && fabs(last - y) > 1e-4) bad = i;
    }
    char d[96];
    CK_FMT(d, "dc_process on 0.25 + sine: first wrong output %d", bad); ck_true(d, bad < 0);
    ck_true("the 0.25 offset is removed after 20000 samples (|y| < 0.15)", fabs(last) < 0.15);
    return ck_done();
}
""",
"Same pattern as the biquad: compute y, then remember x and y for the next call."))

add(P("frac_delay", S, "Fractional delay read", "c", "func",
r"""<p><b>What to write.</b> A function
<code>float frac_read(const float *buf, int len, float pos)</code>. It reads the circular buffer
<code>buf</code> (of <code>len</code> samples) at a position <code>pos</code> that may lie
<b>between</b> two samples, using straight-line (linear) interpolation.</p>
<p><b>Why it matters.</b> Chorus, flanger, vibrato and pitch-shift effects read a delay line at a time
that changes smoothly. That time is usually not a whole number of samples, so the value between two
samples has to be estimated.</p>
<h4>The rule, step by step</h4>
<ol>
<li>i = the whole part of pos (for example 1.25 &rarr; 1).</li>
<li>frac = pos &minus; i, the part after the point (0.25). It is between 0 and 1.</li>
<li>j = the next index, i + 1. But the buffer is circular: after index len&minus;1 comes index 0. So
if i + 1 equals len, use j = 0.</li>
<li>value = buf[i]&middot;(1 &minus; frac) + buf[j]&middot;frac. When frac is 0 you get buf[i]; as frac
grows towards 1, the value moves in a straight line towards buf[j].</li>
</ol>
<h4>Picture (len = 4)</h4>
<pre> index:     0       1       2       3     (after 3 comes 0 again)
 buf:    [ 10 ]  [ 20 ]  [ 30 ]  [ 40 ]

 pos = 1.25: between index 1 and index 2, a quarter of the way
     pos:  1.0    1.25                   2.0
            |-------*----------------------|
   value:  20     22.5                   30

 pos = 3.5: between index 3 and index 0 (wrapped round), halfway
     pos:  3.0            3.5            4.0 = index 0
            |--------------*--------------|
   value:  40             25             10</pre>
<h4>Examples (buf = {10, 20, 30, 40}, len = 4)</h4>
<table>
<tr><th>pos</th><th>i</th><th>frac</th><th>j</th><th>Value</th></tr>
<tr><td>1.25</td><td>1</td><td>0.25</td><td>2</td><td>20&middot;0.75 + 30&middot;0.25 = 22.5</td></tr>
<tr><td>0.75</td><td>0</td><td>0.75</td><td>1</td><td>10&middot;0.25 + 20&middot;0.75 = 17.5</td></tr>
<tr><td>2.0</td><td>2</td><td>0</td><td>3</td><td>30</td></tr>
<tr><td>3.5</td><td>3</td><td>0.5</td><td>0 (wrapped)</td><td>40&middot;0.5 + 10&middot;0.5 = 25</td></tr>
<tr><td>0.0</td><td>0</td><td>0</td><td>1</td><td>10</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li>0 &le; pos &lt; len, and <code>len</code> is 2 to 64.</li>
<li>For a value that is not negative, the cast <code>(int)pos</code> gives the whole part.</li>
<li>The answer must be right to about 0.00001.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Find i and frac first.</li>
<li>Which i is the dangerous one, where i + 1 would point past the end of the buffer?</li>
</ol>
</details>""",
r"""float frac_read(const float *buf, int len, float pos)
{
    return 0.0f;
}
""",
r"""float frac_read(const float *buf, int len, float pos)
{
    int i = (int)pos;
    float frac = pos - (float)i;
    int j = i + 1 == len ? 0 : i + 1;
    return buf[i] * (1.0f - frac) + buf[j] * frac;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    float buf[64];
    char d[96];
    for (int i = 0; i < 64; i++) buf[i] = (float)ck_unit();
    for (int t = 0; t < 300; t++) {
        int len = ck_range(2, 64);
        float pos = (float)((ck_unit() + 1) / 2 * len);
        if (pos >= (float)len) pos = 0;
        int i = (int)pos; double fr = pos - i; int j = (i + 1) % len;
        double want = buf[i] * (1 - fr) + buf[j] * fr;
        CK_FMT(d, "frac_read(buf, %d, %.5f)", len, pos); ck_dbl(d, frac_read(buf, len, pos), want, 1e-5);
    }
    ck_dbl("frac_read(buf, 4, 3.5) wraps to buf[0]", frac_read(buf, 4, 3.5f), 0.5 * buf[3] + 0.5 * buf[0], 1e-6);
    return ck_done();
}
""",
"(int)pos gives floor for non-negative pos. Remember to wrap the second index to 0."))

add(P("decimate2", S, "Decimate by 2", "c", "func",
r"""<p><b>What to write.</b> A function <code>int decimate2(const float *x, int n, float *y)</code>.
It halves the sample rate: every pair of input samples becomes one output sample, the average of the
pair. It returns the number of outputs written.</p>
<p><b>Why it matters.</b> Lowering the sample rate (for example from 48 kHz to 24 kHz) halves the work
for all later processing. But you cannot just throw every second sample away: frequencies that are too
high for the new rate would fold back and appear as false low tones (this is called <b>aliasing</b>).
So you first filter out the high frequencies. Averaging two neighbours is the simplest such filter.</p>
<h4>The rule</h4>
<pre>y[k] = 0.5 * (x[2k] + x[2k+1])      for k = 0, 1, ..., n/2 - 1
return n / 2                         (integer division)</pre>
<p>If <code>n</code> is odd, the last sample has no partner and is dropped.</p>
<h4>Picture</h4>
<pre> x:  [ 1 ][ 3 ]  [ 2 ][ 6 ]  [ 5 ]        n = 5
     \_______/   \_______/     |
         |           |       dropped (no partner)
 y:    [ 2 ]       [ 4 ]                  return 2</pre>
<h4>Examples</h4>
<table>
<tr><th>x</th><th>n</th><th>y</th><th>Return</th></tr>
<tr><td>{1, 3, 2, 6, 5}</td><td>5</td><td>{2, 4}</td><td>2</td></tr>
<tr><td>{4, 0, &minus;1, 1}</td><td>4</td><td>{2, 0}</td><td>2</td></tr>
<tr><td>{7}</td><td>1</td><td>nothing written</td><td>0</td></tr>
<tr><td>{} (empty)</td><td>0</td><td>nothing written</td><td>0</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul><li><code>n</code> is 0 to 1001.</li></ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>How many outputs are there? Loop over the outputs k, not over the inputs.</li>
<li>Which two input indices belong to output k?</li>
</ol>
</details>""",
r"""int decimate2(const float *x, int n, float *y)
{
    return 0;
}
""",
r"""int decimate2(const float *x, int n, float *y)
{
    int m = n / 2;
    for (int k = 0; k < m; k++)
        y[k] = 0.5f * (x[2 * k] + x[2 * k + 1]);
    return m;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float x[1001], y[600];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int n = ck_range(0, 1001);
        for (int i = 0; i < n; i++) x[i] = (float)ck_unit();
        int m = decimate2(x, n, y);
        CK_FMT(d, "decimate2 with n=%d returns n/2", n); ck_int(d, m, n / 2);
        int bad = -1;
        for (int k = 0; k < n / 2 && bad < 0; k++) if (fabs(y[k] - 0.5 * (x[2 * k] + x[2 * k + 1])) > 1e-6) bad = k;
        CK_FMT(d, "decimate2 with n=%d: first wrong output %d", n, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Loop k from 0 to n/2 - 1."))

add(P("goertzel", S, "Goertzel tone detector", "c", "func",
r"""<p><b>What to write.</b> A function
<code>float goertzel_power(const float *x, int N, int k)</code>. It measures how strong one frequency is
in the block of <code>N</code> samples <code>x</code>, using the <b>Goertzel algorithm</b>.</p>
<p><b>Why it matters.</b> When you press a key on a phone, it sends two tones at once (DTMF). The
receiver only needs to know which of 8 known frequencies are present. A full FFT computes all N
frequencies; Goertzel computes just one, with one multiply per sample and two state variables. It is a
favourite DSP interview topic.</p>
<h4>What is being measured</h4>
<p>The N-point DFT splits a block into N frequency "bins". Bin <code>k</code> is the frequency
k&middot;fs/N (fs = sample rate). Its value is X[k] = &Sigma; x[i]&middot;e<sup>&minus;j2&pi;ki/N</sup>,
and its power is |X[k]|<sup>2</sup>. Your function returns this power, but computed the cheap way.</p>
<h4>The algorithm</h4>
<pre>coeff = 2 * cos(2 * pi * k / N)
s1 = 0, s2 = 0
for each sample x[i], i = 0 .. N-1:
    s  = x[i] + coeff*s1 - s2
    s2 = s1
    s1 = s
power = s1*s1 + s2*s2 - coeff*s1*s2</pre>
<p>s1 is the last value of s, and s2 the one before it. So the loop is a small recursive filter that
"rings" at frequency k.</p>
<pre> x[i] ----&gt;(+)------------+-----&gt; s   (stored as the new s1)
           ^ ^            |
           | |          [z^-1]
           | |            | s1
           | +--(*coeff)--+
           |              |
           |            [z^-1]
           |              | s2
           +----(*-1)-----+</pre>
<h4>Worked example: N = 8, k = 1, x[i] = cos(2&pi;i/8)</h4>
<p>This input is a cosine of amplitude 1 that fits exactly one cycle in the block, so it sits exactly
on bin 1. coeff = 2&middot;cos(&pi;/4) = 1.41421. Values rounded to 4 decimals:</p>
<table>
<tr><th>i</th><th>x[i]</th><th>s = x + coeff&middot;s1 &minus; s2</th><th>s1 after</th><th>s2 after</th></tr>
<tr><td>0</td><td>1</td><td>1 + 0 &minus; 0 = 1</td><td>1</td><td>0</td></tr>
<tr><td>1</td><td>0.7071</td><td>0.7071 + 1.4142 &minus; 0 = 2.1213</td><td>2.1213</td><td>1</td></tr>
<tr><td>2</td><td>0</td><td>0 + 3 &minus; 1 = 2</td><td>2</td><td>2.1213</td></tr>
<tr><td>3</td><td>&minus;0.7071</td><td>&minus;0.7071 + 2.8284 &minus; 2.1213 = 0</td><td>0</td><td>2</td></tr>
<tr><td>4</td><td>&minus;1</td><td>&minus;1 + 0 &minus; 2 = &minus;3</td><td>&minus;3</td><td>0</td></tr>
<tr><td>5</td><td>&minus;0.7071</td><td>&minus;0.7071 &minus; 4.2426 &minus; 0 = &minus;4.9497</td><td>&minus;4.9497</td><td>&minus;3</td></tr>
<tr><td>6</td><td>0</td><td>0 &minus; 7 + 3 = &minus;4</td><td>&minus;4</td><td>&minus;4.9497</td></tr>
<tr><td>7</td><td>0.7071</td><td>0.7071 &minus; 5.6569 + 4.9497 = 0</td><td>0</td><td>&minus;4</td></tr>
</table>
<p>power = 0&sup2; + (&minus;4)&sup2; &minus; 1.4142&middot;0&middot;(&minus;4) = <b>16</b>. That is
(N/2)&sup2;, the DFT power of a cosine of amplitude 1 sitting exactly on the bin.</p>
<h4>More results</h4>
<table>
<tr><th>Input (N = 8)</th><th>k</th><th>Power</th></tr>
<tr><td>the same cosine (on bin 1)</td><td>2</td><td>0 (up to rounding): the tone is not at bin 2</td></tr>
<tr><td>all ones (a constant, 0 Hz)</td><td>1</td><td>0 (up to rounding)</td></tr>
<tr><td>sin(2&pi;&middot;2i/8) (on bin 2)</td><td>2</td><td>16</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li><code>N</code> is 32 to 256, and <code>k</code> is 1 to N/2 &minus; 1.</li>
<li>The result must match |X[k]|&sup2; to about 0.5 %.</li>
<li><code>cosf</code> is in <code>&lt;math.h&gt;</code>. <code>M_PI</code> is not part of standard C,
so write &pi; as a number: 3.14159265358979.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Compute coeff once, before the loop.</li>
<li>Inside the loop, follow the three lines exactly. What would go wrong if you set s1 = s before
s2 = s1?</li>
<li>After the loop, s1 and s2 are all you need for the power.</li>
</ol>
</details>""",
r"""#include <math.h>

float goertzel_power(const float *x, int N, int k)
{
    return 0.0f;
}
""",
r"""#include <math.h>

float goertzel_power(const float *x, int N, int k)
{
    float coeff = 2.0f * cosf(2.0f * 3.14159265358979f * (float)k / (float)N);
    float s1 = 0.0f, s2 = 0.0f;
    for (int i = 0; i < N; i++) {
        float s = x[i] + coeff * s1 - s2;
        s2 = s1;
        s1 = s;
    }
    return s1 * s1 + s2 * s2 - coeff * s1 * s2;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float x[256];
    char d[96];
    for (int t = 0; t < 20; t++) {
        int N = ck_range(32, 256), k = ck_range(1, N / 2 - 1);
        for (int i = 0; i < N; i++) x[i] = (float)(0.6 * sin(2 * 3.141592653589793 * (k + 0.3 * ck_unit()) * i / N) + 0.2 * ck_unit());
        double re = 0, im = 0;
        for (int i = 0; i < N; i++) { re += x[i] * cos(2 * 3.141592653589793 * k * i / N); im -= x[i] * sin(2 * 3.141592653589793 * k * i / N); }
        CK_FMT(d, "goertzel_power(N=%d, k=%d) vs |DFT|^2", N, k);
        ck_dbl(d, goertzel_power(x, N, k), re * re + im * im, 5e-3);
    }
    return ck_done();
}
""",
"Follow the pseudo-code exactly; the order s2 = s1; s1 = s matters."))

add(P("nlms_update", S, "NLMS weight update", "c", "func",
r"""<p><b>What to write.</b> One weight update of the <b>NLMS</b> (normalised least mean squares)
adaptive filter:</p>
<pre>void nlms_update(float *w, const float *x, int M,
                 float e, float mu, float eps);</pre>
<p><b>Why it matters.</b> An adaptive filter changes its own coefficients while it runs, to make its
output match a target signal. NLMS is the heart of echo cancellers (in phones and conference systems)
and of active noise cancellation.</p>
<h4>The setting</h4>
<pre>                 +-------------------+
 x (inputs) --+-&gt;| filter, weights w |--&gt; y --&gt;(-)--&gt; e = d - y
              |  +-------------------+          ^
              |            ^                    |
              |            | nudge w            d (the target)
              +------------+---- using x and e</pre>
<ul>
<li><code>w[0..M-1]</code>: the filter weights (coefficients). You change them in place.</li>
<li><code>x[0..M-1]</code>: the current input vector, <b>newest sample first</b> (x[0] is the newest,
x[1] the one before, and so on).</li>
<li><code>e</code>: the error, e = d &minus; y, already computed by the caller (y = &Sigma; w[k]&middot;x[k]
was the filter output and d the target).</li>
<li><code>mu</code>: the step size (how big a correction to make), and <code>eps</code>: a tiny number
that stops a division by zero when the input is silent.</li>
</ul>
<h4>The formula</h4>
<pre>norm = eps + x[0]^2 + x[1]^2 + ... + x[M-1]^2
w[k] = w[k] + mu * e * x[k] / norm          for every k = 0 .. M-1</pre>
<p>"Normalised" means the correction is divided by the input energy <code>norm</code>. Then the size
of the step does not depend on how loud the input is.</p>
<h4>Examples</h4>
<table>
<tr><th>w before</th><th>x</th><th>e</th><th>mu</th><th>eps</th><th>norm</th><th>mu&middot;e/norm</th><th>w after</th></tr>
<tr><td>{0, 0}</td><td>{1, 2}</td><td>0.5</td><td>1</td><td>0</td><td>5</td><td>0.1</td><td>{0.1, 0.2}</td></tr>
<tr><td>{1, &minus;1}</td><td>{2, &minus;1}</td><td>1</td><td>0.5</td><td>0</td><td>5</td><td>0.1</td><td>{1.2, &minus;1.1}</td></tr>
<tr><td>{0, 0}</td><td>{0, 0}</td><td>0.3</td><td>0.5</td><td>10<sup>&minus;6</sup></td><td>10<sup>&minus;6</sup></td><td>150000</td><td>{0, 0} (every x[k] is 0)</td></tr>
</table>
<p>A check on the first row: with the new weights, the same input gives
y = 0.1&middot;1 + 0.2&middot;2 = 0.5, which is exactly the old error. With mu = 1, one step removes the
whole error for this input. A smaller mu makes smaller, safer steps.</p>
<h4>Inputs and limits</h4>
<ul>
<li><code>M</code> is 1 to 64; <code>mu</code> is 0.1 to 1; the test uses eps = 10<sup>&minus;6</sup>.</li>
<li>Weights must be right to about 0.0001.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The norm is the same for every weight. Compute it once, in its own loop.</li>
<li>The factor mu&middot;e/norm is also the same for every weight. Then one more loop updates all
weights.</li>
</ol>
</details>""",
r"""void nlms_update(float *w, const float *x, int M, float e, float mu, float eps)
{
}
""",
r"""void nlms_update(float *w, const float *x, int M, float e, float mu, float eps)
{
    float norm = eps;
    for (int k = 0; k < M; k++)
        norm += x[k] * x[k];
    float g = mu * e / norm;
    for (int k = 0; k < M; k++)
        w[k] += g * x[k];
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    float w[64], x[64], r[64];
    char d[96];
    for (int t = 0; t < 30; t++) {
        int M = ck_range(1, 64);
        float e = (float)ck_unit(), mu = (float)(0.1 + 0.9 * (ck_unit() + 1) / 2), eps = 1e-6f;
        double nrm = eps;
        for (int k = 0; k < M; k++) { w[k] = r[k] = (float)ck_unit(); x[k] = (float)ck_unit(); nrm += (double)x[k] * x[k]; }
        for (int k = 0; k < M; k++) r[k] = (float)(r[k] + mu * e * x[k] / nrm);
        nlms_update(w, x, M, e, mu, eps);
        int bad = -1;
        for (int k = 0; k < M && bad < 0; k++) if (fabs(w[k] - r[k]) > 1e-4) bad = k;
        CK_FMT(d, "nlms_update(M=%d): first wrong weight %d", M, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Compute the norm once, then one loop to update all weights."))

add(P("nlms_sysid", S, "NLMS system identification", "c", "func",
r"""<p><b>What to write.</b> A complete NLMS adaptive filter that runs sample by sample. The starter
code defines the structure <code>Nlms</code>. Write:</p>
<pre>// zero the weights and the history
void  nlms_init(Nlms *s, int M, float mu);

// one sample in; returns the error e = d - y
float nlms_step(Nlms *s, float x, float d);</pre>
<p><b>Why it matters.</b> This is <b>system identification</b>: the filter learns an unknown system by
watching its input and output. An echo canceller does exactly this to learn the echo path of a
room.</p>
<h4>The setting used by the test</h4>
<pre>                  +---------------------+
          +------&gt;|  unknown system     |------- d[n] -----+
          |       |  (an 8-tap FIR)     |                  |
          |       +---------------------+                  v
 x[n] ----+                                               (+)--&gt; e[n]
 (white   |       +---------------------+                  ^
  noise)  |       |  your filter w      |                  | (minus)
          +------&gt;|                     |------- y[n] -----+
                  +---------------------+
                            ^
                            | NLMS update, using the history and e[n]</pre>
<p>The test sends 4000 random samples (between &minus;1 and 1) through the system
{0.5, &minus;0.3, 0.2, 0.1, &minus;0.05, 0.03, 0, &minus;0.01} to get d, and calls your
<code>nlms_step(s, x, d)</code> for each sample, with M = 8 and mu = 0.5.</p>
<h4>The structure</h4>
<ul>
<li><code>w[k]</code>: the weights. <code>h[k]</code>: the input history, <b>h[0] = newest</b>,
h[1] = the one before, and so on. <code>M</code>: number of taps. <code>mu</code>: step size.</li>
</ul>
<h4>The rule, step by step (one call of nlms_step)</h4>
<ol>
<li>Push x into the history: every value moves one place towards the end (the oldest, h[M&minus;1],
falls out), and x goes into h[0].</li>
<li>Filter output with the <b>current</b> weights: y = &Sigma; w[k]&middot;h[k], for k = 0 .. M&minus;1.</li>
<li>Error: e = d &minus; y.</li>
<li>NLMS update, as in the previous problem, with eps = 10<sup>&minus;6</sup>:
norm = 10<sup>&minus;6</sup> + &Sigma; h[k]&sup2;, then w[k] += mu&middot;e&middot;h[k] / norm.</li>
<li>Return e.</li>
</ol>
<h4>Worked example (small version: M = 2, mu = 0.5, unknown system {0.5, &minus;0.3})</h4>
<p>Values are rounded to 6 decimals.</p>
<table>
<tr><th>n</th><th>x</th><th>h after push</th><th>d</th><th>y</th><th>e (returned)</th><th>w after update</th></tr>
<tr><td>0</td><td>1</td><td>{1, 0}</td><td>0.5</td><td>0</td><td>0.5</td><td>{0.25, 0}</td></tr>
<tr><td>1</td><td>&minus;1</td><td>{&minus;1, 1}</td><td>&minus;0.8</td><td>&minus;0.25</td><td>&minus;0.55</td><td>{0.3875, &minus;0.1375}</td></tr>
<tr><td>2</td><td>0.5</td><td>{0.5, &minus;1}</td><td>0.55</td><td>0.33125</td><td>0.21875</td><td>{0.43125, &minus;0.225}</td></tr>
<tr><td>3</td><td>1</td><td>{1, 0.5}</td><td>0.35</td><td>0.31875</td><td>0.03125</td><td>{0.44375, &minus;0.21875}</td></tr>
</table>
<p>The weights move towards the true system {0.5, &minus;0.3}, and the error gets smaller.</p>
<h4>What the test checks</h4>
<ul>
<li>Every returned error matches a reference filter (to about 0.001). So the order of the steps above
matters.</li>
<li>After 4000 samples, the weights are very close to the true system: the sum of
(w[k] &minus; true[k])&sup2; must be below 10<sup>&minus;6</sup>.</li>
<li><code>nlms_init</code> must set M, mu, and all weights and history values to 0. The test fills the
structure with garbage first.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>When you shift the history, which end must you start from so that you do not overwrite a value
before it has been copied?</li>
<li>Is y computed with the weights from before or after this sample's update?</li>
<li>Your <code>nlms_update</code> from the previous problem already does step 4.</li>
</ol>
</details>""",
r"""#define NLMS_MAX 32

typedef struct {
    float w[NLMS_MAX];   // weights
    float h[NLMS_MAX];   // input history, h[0] = newest
    int M;
    float mu;
} Nlms;

void nlms_init(Nlms *s, int M, float mu)
{
}

float nlms_step(Nlms *s, float x, float d)
{
    return d;
}
""",
r"""#define NLMS_MAX 32

typedef struct {
    float w[NLMS_MAX];
    float h[NLMS_MAX];
    int M;
    float mu;
} Nlms;

void nlms_init(Nlms *s, int M, float mu)
{
    s->M = M;
    s->mu = mu;
    for (int k = 0; k < NLMS_MAX; k++)
        s->w[k] = s->h[k] = 0.0f;
}

float nlms_step(Nlms *s, float x, float d)
{
    for (int k = s->M - 1; k > 0; k--)
        s->h[k] = s->h[k - 1];
    s->h[0] = x;
    float y = 0.0f, norm = 1e-6f;
    for (int k = 0; k < s->M; k++) {
        y += s->w[k] * s->h[k];
        norm += s->h[k] * s->h[k];
    }
    float e = d - y;
    float g = s->mu * e / norm;
    for (int k = 0; k < s->M; k++)
        s->w[k] += g * s->h[k];
    return e;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    const float sys[8] = {0.5f, -0.3f, 0.2f, 0.1f, -0.05f, 0.03f, 0.0f, -0.01f};
    float xh[8] = {0}, rw[8] = {0}, rh[8] = {0};
    Nlms s; memset(&s, 0x7F, sizeof s);
    nlms_init(&s, 8, 0.5f);
    int bad = -1; char d[96];
    for (int n = 0; n < 4000; n++) {
        float x = (float)ck_unit();
        for (int k = 7; k > 0; k--) xh[k] = xh[k - 1];
        xh[0] = x;
        float dd = 0; for (int k = 0; k < 8; k++) dd += sys[k] * xh[k];
        for (int k = 7; k > 0; k--) rh[k] = rh[k - 1];
        rh[0] = x;
        float y = 0, nrm = 1e-6f; for (int k = 0; k < 8; k++) { y += rw[k] * rh[k]; nrm += rh[k] * rh[k]; }
        float re = dd - y, g = 0.5f * re / nrm;
        for (int k = 0; k < 8; k++) rw[k] += g * rh[k];
        float e = nlms_step(&s, x, dd);
        if (bad < 0 && fabs(e - re) > 1e-3) bad = n;
    }
    CK_FMT(d, "error sequence matches the reference (first wrong step %d)", bad); ck_true(d, bad < 0);
    double mis = 0; for (int k = 0; k < 8; k++) mis += (s.w[k] - sys[k]) * (s.w[k] - sys[k]);
    CK_FMT(d, "weights converge to the true system (squared error %.2e < 1e-6)", mis); ck_true(d, mis < 1e-6);
    return ck_done();
}
""",
"Shift the history down by one and put x in h[0]. Then the filter output, the error, and your nlms_update from the previous problem."))

# ---------------------------------------------------------------------------
S = "Real-time and buffers"

add(P("latency", S, "Samples and milliseconds", "c", "func",
r"""<p><b>What to write.</b> Two conversions between a number of samples and a time in
milliseconds (ms), for a sample rate <code>fs</code> in samples per second (Hz):</p>
<pre>// how long do n samples last?
double samples_to_ms(int n, int fs);

// how many samples fit in ms milliseconds? (rounded)
int    ms_to_samples(double ms, int fs);</pre>
<p><b>Why it matters.</b> Audio programmers switch between samples and time all the time. "A buffer of
256 samples at 48 kHz" means 5.33 ms of delay (latency) for every buffer in the chain.</p>
<h4>The formulas</h4>
<pre>ms      = 1000 * n / fs
samples = ms * fs / 1000      then round to the nearest whole sample</pre>
<pre> fs = 48000 samples per second, so one sample lasts 1/48000 s = 0.02083 ms

 |&lt;------------- 256 samples = 5.333 ms ------------&gt;|
 |s|s|s|s|s|s|s|s|s|s|s|s|s|s|s|s|s|s| ... |s|s|s|s|s|</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Working</th><th>Result</th></tr>
<tr><td><code>samples_to_ms(256, 48000)</code></td><td>256000 / 48000</td><td>5.3333&hellip;</td></tr>
<tr><td><code>samples_to_ms(480, 48000)</code></td><td>480000 / 48000</td><td>10.0</td></tr>
<tr><td><code>samples_to_ms(64, 44100)</code></td><td>64000 / 44100</td><td>1.45125&hellip;</td></tr>
<tr><td><code>samples_to_ms(0, 8000)</code></td><td></td><td>0.0</td></tr>
<tr><td><code>ms_to_samples(10, 44100)</code></td><td>441.0</td><td>441</td></tr>
<tr><td><code>ms_to_samples(1, 44100)</code></td><td>44.1</td><td>44</td></tr>
<tr><td><code>ms_to_samples(2.7, 48000)</code></td><td>129.6</td><td>130</td></tr>
<tr><td><code>ms_to_samples(0.0625, 8000)</code></td><td>0.5 (exactly half)</td><td>1 (a half rounds up)</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li><code>ms</code> is never negative (the test uses 0 to 500 ms). So rounding to nearest can be done
by adding 0.5 and then cutting the fraction off with a cast to <code>int</code>.</li>
<li><code>n</code> is 0 to 100000; <code>fs</code> is a normal audio rate (8000 to 192000).</li>
<li><code>samples_to_ms</code> must be accurate to about 9 significant digits, so use
<code>double</code>.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>Integer division throws the fraction away: <code>256 * 1000 / 48000</code> in <code>int</code> is
5, not 5.333. Make sure the division happens in <code>double</code>, for example by writing
<code>1000.0</code>.</li>
<li>For <code>ms_to_samples</code>, compute <code>ms * fs / 1000.0</code> in that order, then
round.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Check the units: samples &divide; (samples per second) gives seconds; times 1000 gives ms.</li>
<li>For the other direction, turn the formula round, and then decide how to round the result.</li>
</ol>
</details>""",
r"""double samples_to_ms(int n, int fs)
{
    return 0.0;
}

int ms_to_samples(double ms, int fs)
{
    return 0;
}
""",
r"""double samples_to_ms(int n, int fs)
{
    return 1000.0 * n / fs;
}

int ms_to_samples(double ms, int fs)
{
    return (int)(ms * fs / 1000.0 + 0.5);
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[64];
    ck_dbl("samples_to_ms(256, 48000)", samples_to_ms(256, 48000), 256000.0 / 48000, 1e-9);
    ck_int("ms_to_samples(10, 44100)", ms_to_samples(10, 44100), 441);
    int rates[] = {8000, 16000, 22050, 44100, 48000, 96000, 192000};
    for (int i = 0; i < 100; i++) {
        int fs = rates[ck_range(0, 6)], n = ck_range(0, 100000);
        CK_FMT(d, "samples_to_ms(%d, %d)", n, fs); ck_dbl(d, samples_to_ms(n, fs), 1000.0 * n / fs, 1e-9);
        double ms = ck_range(0, 500000) / 1000.0;
        CK_FMT(d, "ms_to_samples(%.3f, %d)", ms, fs); ck_int(d, ms_to_samples(ms, fs), (long long)floor(ms * fs / 1000.0 + 0.5));
    }
    return ck_done();
}
""",
"Do the arithmetic in double (1000.0 * n / fs), not int: 256 * 1000 / 48000 in int is 5."))

add(P("interleave", S, "Interleave stereo", "c", "func",
r"""<p><b>What to write.</b> Two functions that convert stereo audio between the
<em>interleaved</em> layout and two separate channel arrays. <code>frames</code> is the number of stereo
frames.</p>
<pre>void deinterleave(const float *in, float *left, float *right,
                  int frames);
void interleave(const float *left, const float *right, float *out,
                int frames);</pre>
<p><b>Why it matters.</b> Sound cards and WAV files usually store stereo interleaved: left, right,
left, right, &hellip; DSP code often prefers one array per channel. Every audio driver converts
between the two.</p>
<h4>Picture</h4>
<p>A <b>frame</b> is one left sample and one right sample taken at the same moment.</p>
<pre> interleaved (in for deinterleave, out for interleave), frames = 3:
 index:    0    1    2    3    4    5
        [ L0 | R0 | L1 | R1 | L2 | R2 ]
          \____/    \____/    \____/
          frame 0   frame 1   frame 2

 separate channels:
 left:  [ L0 | L1 | L2 ]      index 0, 1, 2
 right: [ R0 | R1 | R2 ]      index 0, 1, 2</pre>
<table>
<tr><th>Frame i</th><th>Left sample is at</th><th>Right sample is at</th></tr>
<tr><td>0</td><td>in[0]</td><td>in[1]</td></tr>
<tr><td>1</td><td>in[2]</td><td>in[3]</td></tr>
<tr><td>2</td><td>in[4]</td><td>in[5]</td></tr>
</table>
<h4>Example</h4>
<p>in = {1, &minus;1, 2, &minus;2, 3, &minus;3} with frames = 3:</p>
<ul>
<li><code>deinterleave</code> gives left = {1, 2, 3} and right = {&minus;1, &minus;2, &minus;3}.</li>
<li><code>interleave</code> of that left and right gives back {1, &minus;1, 2, &minus;2, 3, &minus;3}.</li>
</ul>
<h4>Inputs and limits</h4>
<ul>
<li><code>frames</code> is 1 to 512. The interleaved array has 2 &times; frames values.</li>
<li>The test checks that interleaving the result of deinterleaving gives back exactly the original
array.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Loop over the frames, not over the interleaved array.</li>
<li>Look at the table: what formula gives the left index and the right index from i?</li>
</ol>
</details>""",
r"""void deinterleave(const float *in, float *left, float *right, int frames)
{
}

void interleave(const float *left, const float *right, float *out, int frames)
{
}
""",
r"""void deinterleave(const float *in, float *left, float *right, int frames)
{
    for (int i = 0; i < frames; i++) {
        left[i] = in[2 * i];
        right[i] = in[2 * i + 1];
    }
}

void interleave(const float *left, const float *right, float *out, int frames)
{
    for (int i = 0; i < frames; i++) {
        out[2 * i] = left[i];
        out[2 * i + 1] = right[i];
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float in[1024], L[512], R[512], out[1024];
    char d[96];
    for (int t = 0; t < 10; t++) {
        int fr = ck_range(1, 512);
        for (int i = 0; i < 2 * fr; i++) in[i] = (float)ck_unit();
        deinterleave(in, L, R, fr);
        int ok = 1; for (int i = 0; i < fr; i++) if (L[i] != in[2 * i] || R[i] != in[2 * i + 1]) ok = 0;
        CK_FMT(d, "deinterleave(%d frames)", fr); ck_true(d, ok);
        interleave(L, R, out, fr);
        CK_FMT(d, "interleave(deinterleave(x)) == x for %d frames", fr); ck_true(d, memcmp(out, in, sizeof(float) * 2 * fr) == 0);
    }
    return ck_done();
}
""",
"Frame i lives at in[2*i] (left) and in[2*i + 1] (right)."))

add(P("pcm_convert", S, "int16 to float and back", "c", "func",
r"""<p><b>What to write.</b> The two conversions every audio driver needs, between 16-bit integer
samples (PCM) and float samples:</p>
<pre>// out[i] = in[i] / 32768
void s16_to_f32(const int16_t *in, float *out, int n);

// out[i] = round(in[i] * 32768), clipped to the int16_t range
void f32_to_s16(const float *in, int16_t *out, int n);</pre>
<p><b>Why it matters.</b> Sound cards and WAV files use 16-bit integers. DSP code often prefers floats
between &minus;1 and +1, where "full scale" is 1.0. You convert on the way in and on the way out.</p>
<h4>The rules</h4>
<ul>
<li><b>s16_to_f32</b>: divide each sample by 32768.0. This is the same scale as Q15.</li>
<li><b>f32_to_s16</b>: multiply by 32768, round to nearest (an exact half moves <b>away from zero</b>,
like <code>roundf</code>), and clip to [&minus;32768, 32767]. Exactly the same steps as
<code>float_to_q15</code>.</li>
</ul>
<h4>Examples</h4>
<table>
<tr><th>int16 in</th><th>float out</th></tr>
<tr><td>16384</td><td>0.5</td></tr>
<tr><td>&minus;32768</td><td>&minus;1.0</td></tr>
<tr><td>32767</td><td>0.999969482421875</td></tr>
<tr><td>1</td><td>0.000030517578125</td></tr>
<tr><td>0</td><td>0.0</td></tr>
</table>
<table>
<tr><th>float in</th><th>in &times; 32768</th><th>int16 out</th></tr>
<tr><td>0.5</td><td>16384</td><td>16384</td></tr>
<tr><td>&minus;0.25</td><td>&minus;8192</td><td>&minus;8192</td></tr>
<tr><td>1.5/32768</td><td>1.5</td><td>2 (a half moves away from 0)</td></tr>
<tr><td>&minus;1.5/32768</td><td>&minus;1.5</td><td>&minus;2</td></tr>
<tr><td>1.0</td><td>32768</td><td>32767 (clipped)</td></tr>
<tr><td>&minus;1.2</td><td>&minus;39321.6</td><td>&minus;32768 (clipped)</td></tr>
</table>
<h4>What the test checks</h4>
<ul>
<li><code>s16_to_f32</code> gives exactly <code>in[i] / 32768.0f</code>.</li>
<li>Converting int16 &rarr; float &rarr; int16 gives back exactly the original samples.</li>
<li><code>f32_to_s16</code> rounds and clips correctly for floats between &minus;1.3 and 1.3.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>Divide by 32768, not 32767. With 32767 the round trip would fail (16384 would come back as
16385).</li>
<li><code>in[i] / 32768</code> with an integer 32768 is <b>integer</b> division and gives 0 for most
samples. Write <code>32768.0f</code>.</li>
<li>Converting an out-of-range float to an integer type is undefined behaviour in C. Clip while the
value is still a float, then cast.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The first function is one division per sample.</li>
<li>For the second function, reuse your <code>float_to_q15</code> steps inside a loop.</li>
</ol>
</details>""",
r"""#include <stdint.h>
#include <math.h>

void s16_to_f32(const int16_t *in, float *out, int n)
{
}

void f32_to_s16(const float *in, int16_t *out, int n)
{
}
""",
r"""#include <stdint.h>
#include <math.h>

void s16_to_f32(const int16_t *in, float *out, int n)
{
    for (int i = 0; i < n; i++)
        out[i] = in[i] / 32768.0f;
}

void f32_to_s16(const float *in, int16_t *out, int n)
{
    for (int i = 0; i < n; i++) {
        float v = roundf(in[i] * 32768.0f);
        if (v > 32767.0f) v = 32767.0f;
        if (v < -32768.0f) v = -32768.0f;
        out[i] = (int16_t)v;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static int16_t s[1000], s2[1000];
    static float f[1000];
    char d[96];
    for (int i = 0; i < 1000; i++) s[i] = (int16_t)ck_range(-32768, 32767);
    s[0] = -32768; s[1] = 32767;
    s16_to_f32(s, f, 1000);
    int bad = -1; for (int i = 0; i < 1000 && bad < 0; i++) if (f[i] != s[i] / 32768.0f) bad = i;
    CK_FMT(d, "s16_to_f32: first wrong sample %d", bad); ck_true(d, bad < 0);
    f32_to_s16(f, s2, 1000);
    ck_true("f32_to_s16(s16_to_f32(x)) == x", memcmp(s, s2, sizeof s) == 0);
    for (int i = 0; i < 1000; i++) f[i] = (float)(ck_unit() * 1.3);
    f32_to_s16(f, s2, 1000);
    bad = -1;
    for (int i = 0; i < 1000 && bad < 0; i++) {
        double v = (double)f[i] * 32768.0; v = v < 0 ? -floor(-v + 0.5) : floor(v + 0.5);
        int w = v > 32767 ? 32767 : (v < -32768 ? -32768 : (int)v);
        if (s2[i] != w) bad = i;
    }
    CK_FMT(d, "f32_to_s16 rounds and clips (first wrong sample %d)", bad); ck_true(d, bad < 0);
    return ck_done();
}
""",
"Divide by 32768.0f one way. The other way: roundf, clamp, then cast."))

add(P("s24_unpack", S, "Unpack 24-bit samples", "c", "func",
r"""<p><b>What to write.</b> A function <code>int32_t s24le_to_s32(const uint8_t *p)</code>. It
reads one 24-bit audio sample stored in the 3 bytes <code>p[0]</code>, <code>p[1]</code>,
<code>p[2]</code> and returns it as a normal 32-bit signed integer.</p>
<p><b>Why it matters.</b> 24-bit audio (studio recordings, many audio codecs and I2S links) is often
packed into 3 bytes per sample to save space. Before you can use a sample, you must unpack it into an
<code>int32_t</code>.</p>
<h4>The layout</h4>
<p>The bytes are <b>little-endian</b>: the lowest byte comes first in memory.</p>
<pre> memory:      p[0]          p[1]          p[2]
          [ low byte  ] [ middle byte ] [ high byte ]

 the 24-bit value:
  bit:   23 ....... 16 | 15 ........ 8 | 7 ......... 0
        [    p[2]      |     p[1]      |     p[0]     ]
         ^
         bit 23 is the sign bit: 1 means the sample is negative</pre>
<h4>The rule, step by step</h4>
<ol>
<li>Put the bytes together: u = p[0] + p[1]&middot;2<sup>8</sup> + p[2]&middot;2<sup>16</sup> (with
shifts and OR). This gives a number from 0 to 16777215 (0xFFFFFF).</li>
<li>The 24 bits are in <b>two's complement</b>. If bit 23 is 1 (u &ge; 0x800000 = 8388608), the real
value is negative: value = u &minus; 2<sup>24</sup> = u &minus; 16777216. Otherwise value = u.</li>
</ol>
<p>This is called <b>sign extension</b>: in 32 bits, the top 8 bits must become copies of bit 23.
Without it, 0xFFFFFF would read as +16777215 instead of &minus;1.</p>
<h4>Examples</h4>
<table>
<tr><th>p[0], p[1], p[2]</th><th>24 bits (hex)</th><th>As unsigned</th><th>You return</th></tr>
<tr><td>0x56, 0x34, 0x12</td><td>0x123456</td><td>1193046</td><td>1193046</td></tr>
<tr><td>0x01, 0x00, 0x00</td><td>0x000001</td><td>1</td><td>1</td></tr>
<tr><td>0x00, 0x00, 0x00</td><td>0x000000</td><td>0</td><td>0</td></tr>
<tr><td>0xFF, 0xFF, 0x7F</td><td>0x7FFFFF</td><td>8388607</td><td>8388607 (the largest)</td></tr>
<tr><td>0x00, 0x00, 0x80</td><td>0x800000</td><td>8388608</td><td>&minus;8388608 (the smallest)</td></tr>
<tr><td>0xFF, 0xFF, 0xFF</td><td>0xFFFFFF</td><td>16777215</td><td>&minus;1</td></tr>
<tr><td>0x00, 0xFF, 0xFF</td><td>0xFFFF00</td><td>16776960</td><td>&minus;256</td></tr>
</table>
<p>The range of the result is &minus;8,388,608 to 8,388,607.</p>
<h4>Things to watch out for</h4>
<ul>
<li>Notice that p[0] is the <em>low</em> byte, even though it is written first.</li>
<li>Do the shifts on unsigned values (for example cast each byte to <code>uint32_t</code>). Shifting a
1 into the sign bit of a signed <code>int</code> is not allowed in C.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>How far must each byte be shifted to land in its place in the picture?</li>
<li>How do you test whether bit 23 is set?</li>
<li>What do you subtract to turn the unsigned 24-bit value into the signed one?</li>
</ol>
</details>""",
r"""#include <stdint.h>

int32_t s24le_to_s32(const uint8_t *p)
{
    return 0;
}
""",
r"""#include <stdint.h>

int32_t s24le_to_s32(const uint8_t *p)
{
    int32_t v = (int32_t)((uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16));
    if (v & 0x800000)
        v -= 0x1000000;
    return v;
}
""",
r"""#include "check.h"
#include "solution.c"
static int32_t ref(const uint8_t *p) { int32_t v = p[0] | (p[1] << 8) | (p[2] << 16); return v >= 0x800000 ? v - 0x1000000 : v; }
int main(void)
{
    uint8_t b[3];
    char d[96];
    uint8_t f[][3] = {{0xFF, 0xFF, 0x7F}, {0x00, 0x00, 0x80}, {0xFF, 0xFF, 0xFF}, {0, 0, 0}, {0x01, 0x00, 0x00}};
    for (int i = 0; i < 5; i++) { CK_FMT(d, "s24le_to_s32({0x%02X, 0x%02X, 0x%02X})", f[i][0], f[i][1], f[i][2]); ck_int(d, s24le_to_s32(f[i]), ref(f[i])); }
    for (int i = 0; i < 300; i++) {
        unsigned r = ck_rand(); b[0] = (uint8_t)r; b[1] = (uint8_t)(r >> 8); b[2] = (uint8_t)(r >> 16);
        CK_FMT(d, "s24le_to_s32({0x%02X, 0x%02X, 0x%02X})", b[0], b[1], b[2]); ck_int(d, s24le_to_s32(b), ref(b));
    }
    return ck_done();
}
""",
"Assemble the 24 bits with shifts, then sign-extend: if bit 23 is set, subtract 2^24."))

add(P("ring_buffer", S, "Lock-free ring buffer", "c", "func",
r"""<p><b>What to write.</b> A ring buffer (a FIFO queue: first in, first out) of
<code>float</code> values with a fixed capacity <code>RING_CAP</code> = 8. The starter code defines the
structure <code>Ring</code>. Write:</p>
<pre>void     ring_init(Ring *r);
int      ring_push(Ring *r, float v);   // 1 on success, 0 if full
int      ring_pop(Ring *r, float *v);   // 1 on success, 0 if empty
unsigned ring_count(const Ring *r);     // how many items are stored now</pre>
<p><b>Why it matters.</b> A ring buffer passes audio between threads, for example from the audio
callback to a recording thread. It never allocates memory and never moves data, so it is safe in real
time.</p>
<h4>The idea: two counters that only go up</h4>
<ul>
<li><code>head</code> counts all pushes so far. <code>tail</code> counts all pops so far. Neither is
ever reset (except by <code>ring_init</code>, which sets both to 0).</li>
<li>Number of items stored = <code>head - tail</code>.</li>
<li>The slot used by a counter value c is <code>c &amp; (RING_CAP - 1)</code>. Because RING_CAP = 8 is
a power of two, <code>c &amp; 7</code> keeps only the lowest 3 bits, which is the same as c % 8.</li>
<li>Empty: head == tail. Full: head &minus; tail == RING_CAP. All 8 slots can be used.</li>
<li><code>ring_push</code> on a full buffer and <code>ring_pop</code> on an empty buffer change
nothing and return 0. A successful pop writes the oldest value into <code>*v</code>.</li>
</ul>
<h4>Picture (head = 11 pushes so far, tail = 6 pops so far)</h4>
<p>v0, v1, &hellip; are the values in the order they were pushed. v0 to v5 have been popped.</p>
<pre> slot:     0     1     2     3     4     5     6     7
        [ v8  | v9  | v10 |  -  |  -  |  -  | v6  | v7  ]

 next pop  reads slot  tail &amp; 7 = 6 &amp; 7  = 6   (v6, the oldest)
 next push writes slot head &amp; 7 = 11 &amp; 7 = 3
 items stored = head - tail = 11 - 6 = 5         (v6, v7, v8, v9, v10)</pre>
<h4>Example sequence (after ring_init)</h4>
<table>
<tr><th>Call</th><th>Returns</th><th>head</th><th>tail</th><th>count</th></tr>
<tr><td><code>ring_push(r, 1.5f)</code></td><td>1</td><td>1</td><td>0</td><td>1</td></tr>
<tr><td><code>ring_push(r, 2.5f)</code></td><td>1</td><td>2</td><td>0</td><td>2</td></tr>
<tr><td><code>ring_pop(r, &amp;v)</code></td><td>1, v = 1.5</td><td>2</td><td>1</td><td>1</td></tr>
<tr><td><code>ring_pop(r, &amp;v)</code></td><td>1, v = 2.5</td><td>2</td><td>2</td><td>0</td></tr>
<tr><td><code>ring_pop(r, &amp;v)</code></td><td>0 (empty)</td><td>2</td><td>2</td><td>0</td></tr>
<tr><td>8 more pushes</td><td>1 each</td><td>10</td><td>2</td><td>8 (full)</td></tr>
<tr><td>a 9th push</td><td>0 (full)</td><td>10</td><td>2</td><td>8</td></tr>
</table>
<h4>When the counters wrap round</h4>
<p>An <code>unsigned</code> is 32 bits, so after 4294967295 it wraps to 0. Unsigned arithmetic in C is
done modulo 2<sup>32</sup>, so <code>head - tail</code> is still right. Example: tail = 4294967294
(0xFFFFFFFE) and head = 2 (it has wrapped). Then head &minus; tail = 4 in unsigned arithmetic, which is
correct: 4 pushes happened since then. The slots used by the counter values 0xFFFFFFFE, 0xFFFFFFFF, 0,
1 are 6, 7, 0, 1, which continue smoothly. The test moves both counters to 0xFFFFFFF0 halfway through,
so this case is checked.</p>
<h4>Requirements</h4>
<ul>
<li>Values come out in the same order they went in.</li>
<li><code>ring_init</code> must set both counters; the test fills the structure with garbage first.</li>
</ul>
<p>(With one producer thread and one consumer thread, this design needs no lock. Real code also uses
atomic loads and stores for <code>head</code> and <code>tail</code>.)</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write <code>ring_count</code> first; push and pop can use the same expression to test for full and
empty.</li>
<li>In push: which slot do you write, and which counter moves? In pop: which slot do you read, and
which counter moves?</li>
<li>Why must you never reset the counters to 0 when the buffer becomes empty?</li>
</ol>
</details>""",
r"""#define RING_CAP 8u   // must be a power of two

typedef struct {
    float buf[RING_CAP];
    unsigned head;   // total number of pushes
    unsigned tail;   // total number of pops
} Ring;

void ring_init(Ring *r)
{
}

int ring_push(Ring *r, float v)
{
    return 0;
}

int ring_pop(Ring *r, float *v)
{
    return 0;
}

unsigned ring_count(const Ring *r)
{
    return 0;
}
""",
r"""#define RING_CAP 8u

typedef struct {
    float buf[RING_CAP];
    unsigned head;
    unsigned tail;
} Ring;

void ring_init(Ring *r)
{
    r->head = 0;
    r->tail = 0;
}

int ring_push(Ring *r, float v)
{
    if (r->head - r->tail == RING_CAP)
        return 0;
    r->buf[r->head & (RING_CAP - 1)] = v;
    r->head++;
    return 1;
}

int ring_pop(Ring *r, float *v)
{
    if (r->head == r->tail)
        return 0;
    *v = r->buf[r->tail & (RING_CAP - 1)];
    r->tail++;
    return 1;
}

unsigned ring_count(const Ring *r)
{
    return r->head - r->tail;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    Ring r; memset(&r, 0x5A, sizeof r);
    ring_init(&r);
    float q[64]; int qh = 0, qt = 0;   /* reference FIFO */
    char d[128];
    for (int step = 0; step < 3000; step++) {
        if (step == 1500) {   /* empty both, then move the counters close to wrapping */
            float t; for (int i = 0; i < 100 && ring_pop(&r, &t); i++) {}
            qh = qt = 0; r.head = r.tail = 0xFFFFFFF0u;
        }
        if (ck_rand() % 2) {
            float v = (float)step;
            int ok = ring_push(&r, v), want = (qh - qt) < (int)RING_CAP;
            if (want) q[qh++ % 64] = v;
            CK_FMT(d, "step %d: ring_push with %d items stored returns %d", step, qh - qt - (want ? 1 : 0), want); ck_int(d, ok, want);
        } else {
            float v = -1;
            int ok = ring_pop(&r, &v), want = qh > qt;
            CK_FMT(d, "step %d: ring_pop returns %d", step, want); ck_int(d, ok, want);
            if (want) { CK_FMT(d, "step %d: ring_pop value (FIFO order)", step); ck_dbl(d, v, q[qt++ % 64], 0); }
        }
        CK_FMT(d, "step %d: ring_count", step); ck_int(d, (long long)ring_count(&r), qh - qt);
    }
    return ck_done();
}
""",
"Full means head - tail == RING_CAP; empty means head == tail. Never reset the counters; just mask them when indexing."))

add(P("gain_ramp", S, "Click-free gain changes", "c", "func",
r"""<p><b>What to write.</b> A gain (volume) processor that never jumps. When it gets a new target
gain, it moves the gain in a straight line to the target over exactly <code>ramp_len</code> samples.
The starter code defines the structure <code>GainRamp</code>. Write:</p>
<pre>// start at gain, not ramping
void gr_init(GainRamp *g, float gain, int ramp_len);

// start a new ramp from the current gain to target
void gr_set_target(GainRamp *g, float target);

// multiply the n samples of x in place
void gr_process(GainRamp *g, float *x, int n);</pre>
<p><b>Why it matters.</b> If you change the volume from one block to the next in a single jump, the
waveform gets a sudden step, and you hear a click. Real-time audio code <em>ramps</em> the gain
instead.</p>
<h4>The rule</h4>
<ul>
<li>After <code>gr_init</code>, every sample is multiplied by the starting gain.</li>
<li><code>gr_set_target</code> starts a ramp from the current gain ("start") to the target.</li>
<li>Count the samples processed after that call: k = 1, 2, &hellip;, ramp_len. Sample k is multiplied by
<pre>gain = start + (target - start) * k / ramp_len</pre></li>
<li>So the last ramp sample (k = ramp_len) uses exactly the target, and every sample after it uses the
target too.</li>
<li><code>gr_process</code> multiplies the <code>n</code> samples of <code>x</code> in place.</li>
</ul>
<h4>Picture (gain 1.0, then gr_set_target(&amp;g, 0.0) with ramp_len = 4)</h4>
<pre> sample:   0     1     2     3  |  4     5     6     7     8     9
 gain:    1.0   1.0   1.0   1.0 | 0.75  0.50  0.25  0.0   0.0   0.0
                                |
              gr_set_target is called here
 k:                                1     2     3     4   (ramp done)</pre>
<h4>The output must not depend on the block sizes</h4>
<p>The caller may hand you the audio in blocks of any size, and a ramp may continue across several calls
of <code>gr_process</code>. The samples after the call above must get the same gains however they are
split:</p>
<pre> one block of 6:     [0.75 0.50 0.25 0.00 0.00 0.00]
 blocks of 2, 1, 3:  [0.75 0.50] [0.25] [0.00 0.00 0.00]
 blocks of 1:        [0.75] [0.50] [0.25] [0.00] [0.00] [0.00]</pre>
<h4>More examples</h4>
<table>
<tr><th>Start</th><th>Target</th><th>ramp_len</th><th>Gains for k = 1, 2, &hellip;</th></tr>
<tr><td>1.0</td><td>0.0</td><td>4</td><td>0.75, 0.5, 0.25, 0.0</td></tr>
<tr><td>0.0</td><td>1.0</td><td>4</td><td>0.25, 0.5, 0.75, 1.0</td></tr>
<tr><td>1.0</td><td>0.25</td><td>5</td><td>0.85, 0.70, 0.55, 0.40, 0.25</td></tr>
</table>
<h4>What the test does</h4>
<ul>
<li>It fills the structure with garbage, calls <code>gr_init(&amp;g, 1.0f, R)</code> with R between 16
and 600, then processes 6000 samples of 1.0 in random block sizes (1 to 300).</li>
<li>It sets the targets 0.25, 0.8, 0.0 and 1.0 at samples 1000, 2000, 3000 and 4000.</li>
<li>Every output must match the rule to about 0.0001.</li>
</ul>
<h4>Things to watch out for</h4>
<ul>
<li>If you add a float step again and again, small errors pile up (in the last row above, float steps
give 0.40000007 instead of 0.4). Set the gain to exactly the target on the last ramp sample.</li>
<li>Anything that must survive until the next call (the step, how many ramp samples are left) must be
kept in the structure, not in local variables.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>What should <code>gr_set_target</code> store so that <code>gr_process</code> knows how much to
change the gain per sample, and for how many more samples?</li>
<li>In <code>gr_process</code>, for each sample: first update the gain if a ramp is running, then
multiply. Check this order against the picture: the first sample after the call must already use
0.75.</li>
</ol>
</details>""",
r"""typedef struct {
    float gain;      // current gain
    float target;
    float step;      // change per sample while ramping
    int remaining;   // samples left in the ramp
    int ramp_len;
} GainRamp;

void gr_init(GainRamp *g, float gain, int ramp_len)
{
}

void gr_set_target(GainRamp *g, float target)
{
}

void gr_process(GainRamp *g, float *x, int n)
{
}
""",
r"""typedef struct {
    float gain;
    float target;
    float step;
    int remaining;
    int ramp_len;
} GainRamp;

void gr_init(GainRamp *g, float gain, int ramp_len)
{
    g->gain = g->target = gain;
    g->step = 0.0f;
    g->remaining = 0;
    g->ramp_len = ramp_len;
}

void gr_set_target(GainRamp *g, float target)
{
    g->target = target;
    g->step = (target - g->gain) / (float)g->ramp_len;
    g->remaining = g->ramp_len;
}

void gr_process(GainRamp *g, float *x, int n)
{
    for (int i = 0; i < n; i++) {
        if (g->remaining > 0) {
            g->remaining--;
            g->gain = g->remaining == 0 ? g->target : g->gain + g->step;
        }
        x[i] *= g->gain;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static float x[6000], y[6000];
    char d[128];
    for (int t = 0; t < 6; t++) {
        int R = ck_range(16, 600);
        GainRamp g; memset(&g, 0x7F, sizeof g);
        gr_init(&g, 1.0f, R);
        for (int i = 0; i < 6000; i++) x[i] = y[i] = 1.0f;
        /* reference gains in double */
        double cur = 1.0, start = 1.0, tgt = 1.0; int k = 0, ramping = 0;
        int pos = 0, bad = -1;
        float targets[] = {0.25f, 0.8f, 0.0f, 1.0f};
        int nt = 0;
        while (pos < 6000) {
            if (pos >= 1000 * (nt + 1) && nt < 4) { gr_set_target(&g, targets[nt]); start = cur; tgt = targets[nt]; k = 0; ramping = 1; nt++; }
            int blk = ck_range(1, 300); if (pos + blk > 6000) blk = 6000 - pos;
            if (nt < 4 && pos + blk > 1000 * (nt + 1)) blk = 1000 * (nt + 1) - pos;
            gr_process(&g, x + pos, blk);
            for (int i = 0; i < blk; i++) {
                if (ramping) { k++; cur = k >= R ? tgt : start + (tgt - start) * k / R; if (k >= R) ramping = 0; }
                if (bad < 0 && fabs(x[pos + i] - cur * y[pos + i]) > 1e-4) bad = pos + i;
            }
            pos += blk;
        }
        CK_FMT(d, "ramp_len=%d, random block sizes: first wrong sample %d", R, bad); ck_true(d, bad < 0);
    }
    return ck_done();
}
""",
"Keep the ramp in the state (step and samples remaining), not in local variables, so it continues across calls. On the last ramp sample, set gain = target exactly."))

add(P("src_ratio", S, "Resampling ratio", "c", "func",
r"""<p><b>What to write.</b> A function
<code>void src_ratio(int fs_in, int fs_out, int *up, int *down)</code>. It finds the smallest whole
numbers U and D with U/D = fs_out/fs_in, and stores them in <code>*up</code> and <code>*down</code>.</p>
<p><b>Why it matters.</b> A sample-rate converter (for example 44.1 kHz music to a 48 kHz sound card)
often works in two stages: first it raises the rate by a whole number U (upsampling), then it lowers it
by a whole number D (downsampling). The smaller U and D are, the less work and memory it needs.</p>
<pre> fs_in --&gt; [ up by U ] --&gt; [ low-pass filter ] --&gt; [ down by D ] --&gt; fs_out

 44100 Hz --&gt; x160 = 7056000 Hz --&gt; filter --&gt; /147 --&gt; 48000 Hz</pre>
<h4>The rule</h4>
<ol>
<li>g = the greatest common divisor (GCD) of fs_in and fs_out: the largest number that divides both
exactly.</li>
<li>up = fs_out / g and down = fs_in / g. (Careful with the order: <b>up</b> comes from the
<b>output</b> rate.)</li>
</ol>
<h4>Euclid's algorithm for the GCD</h4>
<p>Replace the pair (a, b) by (b, a % b) until b becomes 0. Then a is the GCD. Example for
gcd(44100, 48000):</p>
<table>
<tr><th>a</th><th>b</th><th>a % b</th></tr>
<tr><td>44100</td><td>48000</td><td>44100</td></tr>
<tr><td>48000</td><td>44100</td><td>3900</td></tr>
<tr><td>44100</td><td>3900</td><td>1200</td></tr>
<tr><td>3900</td><td>1200</td><td>300</td></tr>
<tr><td>1200</td><td>300</td><td>0 &rarr; stop, the GCD is 300</td></tr>
</table>
<p>So up = 48000 / 300 = 160 and down = 44100 / 300 = 147.</p>
<h4>Examples</h4>
<table>
<tr><th>fs_in</th><th>fs_out</th><th>GCD</th><th>up</th><th>down</th></tr>
<tr><td>44100</td><td>48000</td><td>300</td><td>160</td><td>147</td></tr>
<tr><td>48000</td><td>44100</td><td>300</td><td>147</td><td>160</td></tr>
<tr><td>48000</td><td>16000</td><td>16000</td><td>1</td><td>3</td></tr>
<tr><td>22050</td><td>32000</td><td>50</td><td>640</td><td>441</td></tr>
<tr><td>96000</td><td>44100</td><td>300</td><td>147</td><td>320</td></tr>
<tr><td>8000</td><td>8000</td><td>8000</td><td>1</td><td>1</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li>The test tries every pair (including equal pairs) of the rates 8000, 11025, 16000, 22050, 24000,
32000, 44100, 48000, 88200, 96000, 176400 and 192000.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a small helper function for the GCD first and test it on the table above.</li>
<li>Then two divisions give the answer.</li>
</ol>
</details>""",
r"""void src_ratio(int fs_in, int fs_out, int *up, int *down)
{
    *up = fs_out;
    *down = fs_in;
}
""",
r"""static int gcd_int(int a, int b)
{
    while (b) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

void src_ratio(int fs_in, int fs_out, int *up, int *down)
{
    int g = gcd_int(fs_in, fs_out);
    *up = fs_out / g;
    *down = fs_in / g;
}
""",
r"""#include "check.h"
#include "solution.c"
static int g_(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
int main(void)
{
    int rates[] = {8000, 11025, 16000, 22050, 24000, 32000, 44100, 48000, 88200, 96000, 176400, 192000};
    char d[96];
    for (int i = 0; i < 12; i++) for (int j = 0; j < 12; j++) {
        int u = -1, dn = -1, g = g_(rates[i], rates[j]);
        src_ratio(rates[i], rates[j], &u, &dn);
        CK_FMT(d, "src_ratio(%d, %d) up", rates[i], rates[j]); ck_int(d, u, rates[j] / g);
        CK_FMT(d, "src_ratio(%d, %d) down", rates[i], rates[j]); ck_int(d, dn, rates[i] / g);
    }
    return ck_done();
}
""",
"Divide both rates by their greatest common divisor (Euclid's algorithm)."))
