# Problem bank, part B: fixed point, DSP in C, real-time buffers.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Fixed point (Q15 / Q31)"

add(P("float_to_q15", S, "Float to Q15", "c", "func",
r"""<p><b>Q15</b> stores a number between &minus;1 and just under +1 in an <code>int16_t</code>:
the integer value is the number times 32768. So 0.5 is 16384 and &minus;1.0 is &minus;32768.
+1.0 does not fit; the largest value is 32767 (0.99997).</p>
<p>Write <code>int16_t float_to_q15(float x)</code>: multiply by 32768, round to the nearest
integer (halves away from zero, like <code>roundf</code>), and <b>saturate</b> to
[&minus;32768, 32767]. Inputs are between &minus;2 and 2.</p>
<pre>float_to_q15(0.5f)  -> 16384
float_to_q15(1.0f)  -> 32767   (saturated)
float_to_q15(-1.5f) -> -32768  (saturated)</pre>""",
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
r"""<p>Adding two Q15 numbers can overflow: 0.75 + 0.75 = 1.5 does not fit. Wrapping round would
turn a loud sample into a large negative one, which sounds like a click. Audio code
<b>saturates</b> instead.</p>
<p>Write <code>int16_t q15_add_sat(int16_t a, int16_t b)</code> that returns a + b clamped to
[&minus;32768, 32767].</p>""",
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
r"""<p>Multiplying two Q15 numbers gives a Q30 result in 32 bits. To get back to Q15:</p>
<ol><li>multiply as <code>int32_t</code>;</li>
<li>add 2<sup>14</sup> (= 16384) to round;</li>
<li>shift right by 15;</li>
<li>saturate to the int16 range.</li></ol>
<p>Write <code>int16_t q15_mul(int16_t a, int16_t b)</code>.
Only one input pair actually overflows: (&minus;1) &times; (&minus;1) = +1.</p>
<pre>q15_mul(16384, 16384)   -> 8192    (0.5 * 0.5 = 0.25)
q15_mul(-32768, -32768) -> 32767   (saturated)</pre>""",
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
r"""<p>Q31 is the same idea in 32 bits: the integer is the value times 2<sup>31</sup>. Write
<code>int32_t q31_mul(int32_t a, int32_t b)</code>: multiply in <code>int64_t</code>, add
2<sup>30</sup>, shift right by 31, saturate to the int32 range.</p>""",
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
r"""<p>FIR filters are dot products. Write
<code>int16_t q15_dot(const int16_t *a, const int16_t *b, int n)</code>:</p>
<ol><li>add up all products a[i]&middot;b[i] in an <code>int64_t</code> accumulator (Q30);</li>
<li>at the end only, round and convert to Q15: add 2<sup>14</sup>, shift right by 15;</li>
<li>saturate to the int16 range.</li></ol>
<p>Rounding once at the end (not after every product) is how DSP chips with wide
accumulators keep precision. <code>n</code> is 0 to 64.</p>""",
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
r"""<p>Write <code>void apply_gain_q15(int16_t *x, int n, int16_t gain)</code> that multiplies
every sample in place by a Q15 gain, rounding and saturating like <code>q15_mul</code>:
x[i] = sat16((x[i]&middot;gain + 2<sup>14</sup>) &gt;&gt; 15).</p>
<p>A gain of 16384 halves the volume (&minus;6 dB); &minus;32768 inverts the polarity.</p>""",
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
r"""<p>Audio levels are given in decibels. For amplitudes, linear = 10<sup>dB/20</sup> and
dB = 20&middot;log<sub>10</sub>(linear). Write both:</p>
<pre>float db_to_lin(float db);   // db_to_lin(-6.0206f) is about 0.5
float lin_to_db(float x);    // x > 0;  lin_to_db(0.1f) is about -20</pre>""",
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
r"""<p>Write <code>float rms(const float *x, int n)</code> that returns the root-mean-square
level &radic;(&Sigma;x&sup2;/n). <code>n</code> is at least 1. A full-scale sine has an RMS of
1/&radic;2 &asymp; 0.707.</p>""",
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
r"""<p>Write <code>int zero_crossings(const float *x, int n)</code> that counts the places where
the signal changes sign between neighbouring samples. Treat 0 as positive: count index
<code>i</code> (1 &le; i &lt; n) when <code>(x[i-1] &lt; 0) != (x[i] &lt; 0)</code>.</p>
<p>A sine at f Hz has about 2f crossings per second; this is a cheap pitch estimate.</p>""",
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
r"""<p>Write <code>void moving_average(const float *x, float *y, int n, int L)</code> where
y[i] is the mean of the last <code>L</code> inputs x[i&minus;L+1] ... x[i], counting samples
before the start as 0. So y[i] = (x[i&minus;L+1] + ... + x[i]) / L.</p>
<p>Try to make it O(n) with a running sum, instead of O(n&middot;L).</p>""",
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
r"""<p>Write the direct-form FIR filter</p>
<pre>void fir(const float *h, int M, const float *x, float *y, int n);</pre>
<p>with y[i] = &Sigma;<sub>k=0</sub><sup>M&minus;1</sup> h[k]&middot;x[i&minus;k], where inputs
before the start are 0. <code>M</code> is 1 to 64.</p>""",
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
r"""<p>In real time, samples arrive one at a time, so the filter must remember its past inputs.
The starter code defines the state. Write:</p>
<pre>void  fir_init(Fir *f, const float *h, int M); // copy the taps, clear the history
float fir_process(Fir *f, float x);            // one sample in, one sample out</pre>
<p>Use <code>z</code> as a circular buffer with write index <code>pos</code>, so each sample costs
O(M) and nothing is shifted. The output must equal the block FIR from the previous problem.</p>""",
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
r"""<p>The biquad is the workhorse of audio EQ. With a<sub>0</sub> = 1:</p>
<pre>y[n] = b0 x[n] + b1 x[n-1] + b2 x[n-2] - a1 y[n-1] - a2 y[n-2]</pre>
<p>Direct Form I keeps the last two inputs and the last two outputs. Write</p>
<pre>void  bq1_init(BiquadDF1 *q, float b0, float b1, float b2, float a1, float a2); // state = 0
float bq1_process(BiquadDF1 *q, float x);</pre>""",
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
r"""<p>Transposed Direct Form II computes the same filter with only two state variables, and is
the usual choice in floating point:</p>
<pre>y  = b0 x + s1
s1 = b1 x - a1 y + s2
s2 = b2 x - a2 y</pre>
<p>Write <code>bq2_init</code> and <code>bq2_process</code> for the struct in the starter code.</p>""",
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
r"""<p>The one-pole low-pass y[n] = y[n&minus;1] + a&middot;(x[n] &minus; y[n&minus;1]) smooths
control values such as a volume knob, so that the volume changes without clicks. Write</p>
<pre>float onepole(float *state, float a, float x);</pre>
<p>which updates <code>*state</code> (the previous output) and returns the new output.
<code>a</code> is between 0 and 1.</p>""",
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
r"""<p>A microphone signal often has a small constant offset (DC). The DC blocker
y[n] = x[n] &minus; x[n&minus;1] + R&middot;y[n&minus;1], with R close to 1 (e.g. 0.995), removes
it. Write</p>
<pre>void  dc_init(DcBlock *b, float R);  // store R, clear the state
float dc_process(DcBlock *b, float x);</pre>""",
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
r"""<p>Chorus, flanger and pitch effects read a delay line <em>between</em> samples. Write</p>
<pre>float frac_read(const float *buf, int len, float pos);</pre>
<p>that returns the linearly interpolated value at position <code>pos</code>
(0 &le; pos &lt; len). The buffer is circular, so after index <code>len&minus;1</code> comes 0:</p>
<pre>i = floor(pos), frac = pos - i
value = buf[i] * (1 - frac) + buf[(i + 1) % len] * frac</pre>""",
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
r"""<p>Write <code>int decimate2(const float *x, int n, float *y)</code> that halves the sample
rate with the simplest anti-alias filter, a 2-point average:
y[k] = 0.5&middot;(x[2k] + x[2k+1]). Return the number of outputs, n/2 (a last odd sample is
dropped).</p>""",
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
r"""<p>The Goertzel algorithm measures the power at one DFT bin <code>k</code> with a tiny
recursive filter. Phones use it to detect DTMF key tones. Write
<code>float goertzel_power(const float *x, int N, int k)</code>:</p>
<pre>coeff = 2 cos(2 pi k / N)
s1 = s2 = 0
for each sample:  s = x[i] + coeff*s1 - s2;  s2 = s1;  s1 = s
power = s1*s1 + s2*s2 - coeff*s1*s2</pre>
<p>The result equals |X[k]|&sup2; of the N-point DFT.</p>""",
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
r"""<p>The normalised LMS update, the heart of echo cancellers and noise cancellers, is</p>
<pre>w[k] += mu * e * x[k] / (eps + sum of x[j]^2)</pre>
<p>where x is the current input vector (newest sample first), e = d &minus; y is the error,
and eps avoids division by zero. Write</p>
<pre>void nlms_update(float *w, const float *x, int M, float e, float mu, float eps);</pre>""",
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
r"""<p>Now the whole adaptive filter. The hidden test passes white noise through an unknown
8-tap FIR system. Your filter must learn it. Write</p>
<pre>void  nlms_init(Nlms *s, int M, float mu);   // zero weights and history
float nlms_step(Nlms *s, float x, float d);   // returns the error e = d - y</pre>
<p>Each step: push <code>x</code> into the history (newest first), compute
y = &Sigma; w[k]&middot;h[k], e = d &minus; y, then do the NLMS update with eps = 1e-6.
The test checks every error value and that the weights end up close to the true system.</p>""",
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
r"""<p>Audio programmers switch between samples and time all the time. Write</p>
<pre>double samples_to_ms(int n, int fs);    // 256 samples at 48000 Hz -> 5.3333 ms
int    ms_to_samples(double ms, int fs); // rounded to the nearest sample; 10 ms at 44100 -> 441</pre>
<p><code>ms</code> is never negative.</p>""",
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
r"""<p>Sound cards usually deliver stereo <em>interleaved</em>: L0 R0 L1 R1 ... DSP code often
prefers separate channels. Write both directions for <code>frames</code> stereo frames:</p>
<pre>void deinterleave(const float *in, float *left, float *right, int frames);
void interleave(const float *left, const float *right, float *out, int frames);</pre>""",
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
r"""<p>Write the two conversions every audio driver needs:</p>
<pre>void s16_to_f32(const int16_t *in, float *out, int n);  // out = in / 32768
void f32_to_s16(const float *in, int16_t *out, int n);  // round(in * 32768), clipped</pre>
<p>For <code>f32_to_s16</code>, round to nearest (halves away from zero) and clip to
[&minus;32768, 32767], exactly like <code>float_to_q15</code>.</p>""",
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
r"""<p>24-bit audio is often packed in 3 bytes per sample, little-endian (lowest byte first).
Write <code>int32_t s24le_to_s32(const uint8_t *p)</code> that reads one sample from
<code>p[0..2]</code> and returns it as a sign-extended 32-bit integer
(range &minus;8,388,608 to 8,388,607).</p>
<pre>{0xFF, 0xFF, 0x7F} -> 8388607
{0x00, 0x00, 0x80} -> -8388608
{0xFF, 0xFF, 0xFF} -> -1</pre>""",
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
r"""<p>The ring buffer (FIFO) passes audio between threads, for example from the audio callback to
a recording thread. Use two <b>free-running</b> unsigned counters: <code>head</code> counts
pushes, <code>tail</code> counts pops. Then</p>
<ul><li>number of items = <code>head - tail</code> (unsigned arithmetic wraps correctly);</li>
<li>slot of an index = <code>index &amp; (RING_CAP - 1)</code>, because RING_CAP is a power of two;</li>
<li>the buffer holds up to RING_CAP items.</li></ul>
<pre>void     ring_init(Ring *r);
int      ring_push(Ring *r, float v);   // 1 on success, 0 if full
int      ring_pop(Ring *r, float *v);   // 1 on success, 0 if empty
unsigned ring_count(const Ring *r);</pre>
<p>(With one producer thread and one consumer thread, this design needs no lock; real code adds
atomic loads and stores for <code>head</code> and <code>tail</code>.)</p>""",
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
r"""<p>If you change the volume from one block to the next in a single jump, you hear a click.
Real-time code <em>ramps</em> the gain instead. Write a processor that, when given a new target,
moves its gain in a straight line to the target over exactly <code>ramp_len</code> samples, and
works the same however the audio is split into blocks:</p>
<pre>void gr_init(GainRamp *g, float gain, int ramp_len); // start at gain, not ramping
void gr_set_target(GainRamp *g, float target);       // start a new ramp from the current gain
void gr_process(GainRamp *g, float *x, int n);       // multiply x in place</pre>
<p>During a ramp, sample k (k = 1 ... ramp_len, counting from the first sample after
<code>gr_set_target</code>) uses gain = start + (target &minus; start)&middot;k/ramp_len. After that,
the gain stays at the target.</p>""",
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
r"""<p>To convert from <code>fs_in</code> to <code>fs_out</code>, a polyphase resampler upsamples by
U and downsamples by D, where U/D = fs_out/fs_in in lowest terms. Write</p>
<pre>void src_ratio(int fs_in, int fs_out, int *up, int *down);</pre>
<pre>44100 -> 48000 : up = 160, down = 147
48000 -> 16000 : up = 1,   down = 3</pre>""",
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
