# Problem bank, part E: embedded C, OS and architecture, sorting, interview classics.
# Topics follow the Qualcomm hardware-engineer study guide (OA programming section and the
# embedded / OS / C questions reported from interviews).
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Embedded C"

add(P("uart_frame", S, "UART: build a frame", "c", "func",
r"""<p><b>What to write.</b> A function
<code>int uart_frame(uint8_t byte, int parity, int stop_bits, uint8_t bits[12])</code>. It writes, one entry
per bit time, the level (0 or 1) that a UART puts on the wire to send <code>byte</code>. It returns how many
entries it wrote (the frame length).</p>
<p><b>Why it matters.</b> A UART (serial port) is on almost every microcontroller. It has no clock wire, so
each byte travels inside a fixed pattern called a <em>frame</em>. The receiver uses the pattern to find where
a byte starts and ends. OA papers often ask how many bits a frame has or how many bytes per second a baud rate
gives.</p>
<h4>The frame, in the order the bits are sent</h4>
<table>
<tr><th>Part</th><th>Bits</th><th>Level</th></tr>
<tr><td>Idle line (before and after; not part of the frame)</td><td>&ndash;</td><td>1</td></tr>
<tr><td>Start bit</td><td>1</td><td>always 0</td></tr>
<tr><td>Data bits, <b>least significant bit first</b>: bit 0 of the byte, then bit 1, ..., bit 7</td><td>8</td><td>the bits of <code>byte</code></td></tr>
<tr><td>Parity bit (only if <code>parity</code> is 1 or 2)</td><td>0 or 1</td><td>see below</td></tr>
<tr><td>Stop bits (<code>stop_bits</code> is 1 or 2)</td><td>1 or 2</td><td>always 1</td></tr>
</table>
<p>So the length is 10, 11 or 12, and the array has room for 12 entries.</p>
<h4>The parity rule</h4>
<ul>
<li><code>parity</code> = 0: <b>no parity bit</b> at all.</li>
<li><code>parity</code> = 1: <b>odd</b> parity. Choose the parity bit so that the number of 1s in
(8 data bits + parity bit) is <b>odd</b>.</li>
<li><code>parity</code> = 2: <b>even</b> parity. Choose it so that this number of 1s is <b>even</b>.</li>
</ul>
<p>Example: 0x41 has two 1s. Even parity adds a 0 (the count stays 2, even). Odd parity adds a 1 (the count
becomes 3, odd).</p>
<h4>Picture: 'A' = 0x41 = 0100 0001 in binary, sent as 8N1</h4>
<p>"8N1" means 8 data bits, No parity, 1 stop bit. Read the bits of 0x41 from bit 0 upwards:
1, 0, 0, 0, 0, 0, 1, 0.</p>
<pre>______       _____                               _____       ___________
      |_____|     |_____________________________|     |_____|
 idle start   b0    b1    b2    b3    b4    b5    b6    b7   stop  idle
  1     0     1     0     0     0     0     0     1     0     1     1

bits[] = 0 1 0 0 0 0 0 1 0 1          (the idle 1s are NOT stored)</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Returns</th><th><code>bits[]</code></th><th>Why</th></tr>
<tr><td><code>uart_frame(0x41, 0, 1, bits)</code></td><td>10</td><td>0 1 0 0 0 0 0 1 0 1</td><td>8N1: start, data, stop</td></tr>
<tr><td><code>uart_frame(0x41, 2, 1, bits)</code></td><td>11</td><td>0 1 0 0 0 0 0 1 0 0 1</td><td>8E1: two 1s, so parity 0</td></tr>
<tr><td><code>uart_frame(0x41, 1, 2, bits)</code></td><td>12</td><td>0 1 0 0 0 0 0 1 0 1 1 1</td><td>8O2: parity 1, then two stop bits</td></tr>
<tr><td><code>uart_frame(0x00, 1, 1, bits)</code></td><td>11</td><td>0 0 0 0 0 0 0 0 0 1 1</td><td>zero 1s, so odd parity needs a 1</td></tr>
<tr><td><code>uart_frame(0xFF, 2, 1, bits)</code></td><td>11</td><td>0 1 1 1 1 1 1 1 1 0 1</td><td>eight 1s is already even, parity 0</td></tr>
</table>
<h4>Worth knowing for the OA</h4>
<p>Baud rate = bit times per second. With 8N1 every byte costs 10 bit times, so 115,200 baud carries
115,200 / 10 = 11,520 bytes per second. With 8E1 (11 bit times) it is about 10,473 bytes per second.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep a counter <code>n</code> of how many entries you have written so far. Every entry you add goes to
<code>bits[n]</code> and then <code>n</code> grows by one. At the end, <code>n</code> is the answer.</li>
<li>How do you get bit number <i>i</i> of a byte as 0 or 1? (Shift right, then keep only the lowest bit.)</li>
<li>While you write the 8 data bits, also count the 1s. The parity bit only depends on whether that count is
odd or even.</li>
</ol>
</details>""",
r"""#include <stdint.h>

int uart_frame(uint8_t byte, int parity, int stop_bits, uint8_t bits[12])
{
    return 0;
}
""",
r"""#include <stdint.h>

int uart_frame(uint8_t byte, int parity, int stop_bits, uint8_t bits[12])
{
    int n = 0, ones = 0;
    bits[n++] = 0;                          /* start bit */
    for (int i = 0; i < 8; i++) {
        int b = (byte >> i) & 1;            /* LSB first */
        bits[n++] = (uint8_t)b;
        ones += b;
    }
    if (parity == 1)
        bits[n++] = (uint8_t)!(ones & 1);   /* odd: make the count of 1s odd */
    else if (parity == 2)
        bits[n++] = (uint8_t)(ones & 1);    /* even: make it even */
    for (int i = 0; i < stop_bits; i++)
        bits[n++] = 1;
    return n;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(uint8_t byte, int parity, int stop, uint8_t *b)
{
    int n = 0, ones = 0;
    b[n++] = 0;
    for (int i = 0; i < 8; i++) { b[n] = (byte >> i) & 1; ones += b[n++]; }
    if (parity) b[n++] = (uint8_t)((ones & 1) ^ (parity == 1));
    for (int i = 0; i < stop; i++) b[n++] = 1;
    return n;
}
int main(void)
{
    char d[160];
    static const char *pn[] = {"none", "odd", "even"};
    for (int byte = 0; byte < 256; byte++)
        for (int par = 0; par < 3; par++)
            for (int stop = 1; stop <= 2; stop++) {
                uint8_t got[12], want[12];
                memset(got, 7, sizeof got);
                int ng = uart_frame((uint8_t)byte, par, stop, got), nw = ref((uint8_t)byte, par, stop, want);
                CK_FMT(d, "uart_frame(0x%02X, parity %s, %d stop) length", byte, pn[par], stop);
                ck_int(d, ng, nw);
                if (ng == nw) {
                    int k = 0;
                    while (k < nw && got[k] == want[k]) k++;
                    CK_FMT(d, "uart_frame(0x%02X, parity %s, %d stop) bit %d", byte, pn[par], stop, k);
                    if (k < nw) ck_int(d, got[k], want[k]); else ck_true(d, 1);
                }
            }
    return ck_done();
}
""",
"Start with bits[n++] = 0, then a loop over i = 0..7 writing (byte >> i) & 1 and counting the 1s. Even parity bit = count & 1; odd parity = the opposite."))

add(P("uart_decode", S, "UART: receive bytes", "c", "func",
r"""<p><b>What to write.</b> The receiving side of a UART:
<code>int uart_decode(const uint8_t *line, int n, uint8_t *out, int *framing_errors)</code>.
<code>line[0..n-1]</code> holds the level of the wire (0 or 1) at each bit time, one sample per bit. Find the
8N1 frames in it, store each good byte in <code>out</code>, count the bad frames in
<code>*framing_errors</code>, and return how many good bytes you stored.</p>
<p><b>Why it matters.</b> This is what the UART hardware in a microcontroller does for you. Writing it once
shows you why a wrong baud rate or a noisy wire gives "framing errors".</p>
<h4>An 8N1 frame (10 bit times)</h4>
<pre>index:   i    i+1  i+2  i+3  i+4  i+5  i+6  i+7  i+8  i+9
       start  b0   b1   b2   b3   b4   b5   b6   b7  stop
       (=0)   (data, least significant bit first)    (should be 1)</pre>
<p>The byte is b0 + 2&middot;b1 + 4&middot;b2 + ... + 128&middot;b7: the sample at <code>i+1+k</code> is bit
<i>k</i> of the byte.</p>
<h4>The rules, step by step</h4>
<ol>
<li><b>Searching.</b> Start at index 0. A 1 is the idle line: skip it. A 0 is a start bit at index
<i>i</i>.</li>
<li><b>Too short?</b> If the frame would need samples past the end (that is, <code>i + 9</code> is not a valid
index, <code>i + 9 &ge; n</code>), ignore it and stop: nothing more can be decoded.</li>
<li>Read the 8 data bits at <code>i+1 .. i+8</code>, then look at the stop bit at <code>i+9</code>.</li>
<li><b>Stop bit is 1</b>: a good frame. Store the byte in <code>out</code> (in order) and continue
searching at <code>i + 10</code>, right after the stop bit.</li>
<li><b>Stop bit is 0</b>: a <b>framing error</b>. Add 1 to <code>*framing_errors</code> and drop the byte.
Then move to <code>i + 10</code> and skip every 0 there until you see a 1 (or reach the end). Only then
search again. (A long run of 0s is a "break" condition, not new start bits.)</li>
</ol>
<p>Set <code>*framing_errors</code> to 0 at the start of every call.</p>
<h4>Example 1: one good byte (n = 13)</h4>
<pre>index:   0  1  2  3  4  5  6  7  8  9 10 11 12
line:    1  1  0  1  0  0  0  0  0  1  0  1  1
part:   id id St b0 b1 b2 b3 b4 b5 b6 b7 Sp id
        (id = idle, St = start bit, Sp = stop bit)

data bits b0..b7 = 1 0 0 0 0 0 1 0  -&gt;  byte 0x41 ('A')
result: returns 1, out = {0x41}, framing errors 0</pre>
<h4>Example 2: a framing error, then a good byte (n = 25)</h4>
<pre>line = 1 0 1 0 1 0 1 0 1 0 0 0 0 1 0 1 1 1 1 0 0 0 0 1 1</pre>
<table>
<tr><th>Index</th><th>Samples</th><th>What the decoder does</th></tr>
<tr><td>0</td><td>1</td><td>idle: skip</td></tr>
<tr><td>1</td><td>0</td><td>start bit found</td></tr>
<tr><td>2..9</td><td>1 0 1 0 1 0 1 0</td><td>data bits b0..b7 = 0x55</td></tr>
<tr><td>10</td><td>0</td><td>stop bit is 0: <b>framing error</b>, 0x55 is dropped</td></tr>
<tr><td>11..12</td><td>0 0</td><td>skipped while waiting for a 1 (not start bits!)</td></tr>
<tr><td>13</td><td>1</td><td>line is idle again: start searching</td></tr>
<tr><td>14</td><td>0</td><td>start bit found</td></tr>
<tr><td>15..22</td><td>1 1 1 1 0 0 0 0</td><td>data bits b0..b7 = 0x0F</td></tr>
<tr><td>23</td><td>1</td><td>stop bit is 1: store 0x0F</td></tr>
<tr><td>24</td><td>1</td><td>idle: skip</td></tr>
</table>
<p>Result: returns 1, <code>out</code> = {0x0F}, framing errors 1.</p>
<h4>Example 3: a frame cut off at the end (n = 8)</h4>
<pre>line: 1 1 0 1 1 0 0 1     start bit at index 2, but 2 + 9 = 11 &ge; 8
result: returns 0, framing errors 0
        (the cut frame is ignored; it is not an error)</pre>
<h4>Things to watch out for</h4>
<ul>
<li>Two frames can follow each other with no idle bit between them: the next start bit can be at
<code>i + 10</code>.</li>
<li>The test feeds long streams (up to about 3,000 samples, up to a few hundred bytes), some with random
noise.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Use one index <code>i</code> that walks through <code>line</code>. Each time round the loop, decide which
case you are in: idle 1, start bit with too few samples left, or a full frame.</li>
<li>To build the byte, sample <code>i+1+k</code> must land on bit position <i>k</i>.</li>
<li>After a frame, by how much must <code>i</code> move? After a framing error, what extra skipping is
needed before you look for a start bit again?</li>
</ol>
</details>""",
r"""#include <stdint.h>

int uart_decode(const uint8_t *line, int n, uint8_t *out, int *framing_errors)
{
    *framing_errors = 0;
    return 0;
}
""",
r"""#include <stdint.h>

int uart_decode(const uint8_t *line, int n, uint8_t *out, int *framing_errors)
{
    int i = 0, count = 0;
    *framing_errors = 0;
    while (i < n) {
        if (line[i]) {                /* idle */
            i++;
            continue;
        }
        if (i + 9 >= n)               /* frame would run past the end */
            break;
        uint8_t b = 0;
        for (int k = 0; k < 8; k++)
            b |= (uint8_t)(line[i + 1 + k] << k);
        if (line[i + 9]) {
            out[count++] = b;
            i += 10;
        } else {
            (*framing_errors)++;
            i += 10;
            while (i < n && line[i] == 0)   /* wait for the line to go idle */
                i++;
        }
    }
    return count;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const uint8_t *line, int n, uint8_t *out, int *fe)
{
    int i = 0, c = 0; *fe = 0;
    while (i < n) {
        if (line[i]) { i++; continue; }
        if (i + 9 > n - 1) break;
        int b = 0;
        for (int k = 0; k < 8; k++) b |= line[i + 1 + k] << k;
        if (line[i + 9]) out[c++] = (uint8_t)b; else { ++*fe; i += 10; while (i < n && !line[i]) i++; continue; }
        i += 10;
    }
    return c;
}
static uint8_t line[4000];
int main(void)
{
    char d[128];
    uint8_t ex[] = {1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1}, o[8];
    int fe = -1;
    ck_int("example: byte count", uart_decode(ex, 13, o, &fe), 1);
    ck_hex("example: byte", o[0], 0x41);
    ck_int("example: framing errors", fe, 0);
    for (int t = 0; t < 300; t++) {
        int n = 0;
        while (n < 3000) {
            int gap = ck_range(0, 3);
            for (int g = 0; g < gap; g++) line[n++] = 1;
            int kind = ck_range(0, 9), byte = ck_range(0, 255);
            if (t % 3 == 2) { line[n++] = (uint8_t)(ck_rand() & 1); continue; }   /* random noise */
            line[n++] = 0;
            for (int k = 0; k < 8; k++) line[n++] = (byte >> k) & 1;
            if (kind == 0) { line[n++] = 0; int br = ck_range(0, 12); for (int g = 0; g < br; g++) line[n++] = 0; }
            else line[n++] = 1;
        }
        n -= ck_range(0, 9);                                      /* maybe cut the last frame */
        uint8_t got[400], want[400];
        memset(got, 0xEE, sizeof got);
        int fg = -1, fw = 0;
        int cg = uart_decode(line, n, got, &fg), cw = ref(line, n, want, &fw);
        CK_FMT(d, "stream %d (%d samples): byte count", t, n); ck_int(d, cg, cw);
        CK_FMT(d, "stream %d: framing errors", t); ck_int(d, fg, fw);
        if (cg == cw) {
            int k = 0;
            while (k < cw && got[k] == want[k]) k++;
            CK_FMT(d, "stream %d: byte %d", t, k);
            if (k < cw) ck_hex(d, got[k], want[k]); else ck_true(d, 1);
        }
    }
    return ck_done();
}
""",
"Keep an index i. If line[i] is 1, move on. Otherwise check i + 9 < n, read the 8 data bits at i+1..i+8 (bit k goes to position k), look at the stop bit at i+9, then jump to i + 10."))

add(P("i2c_decode", S, "I2C: a tiny logic analyser", "c", "func",
r"""<p><b>What to write.</b> A tiny logic analyser for I2C:
<code>int i2c_decode(const uint8_t *scl, const uint8_t *sda, int n, char *out)</code>. You get
<code>n</code> samples of each of the two I2C wires. Write a string of events into <code>out</code>: a
character <code>'0'</code> or <code>'1'</code> for each data bit, <code>'S'</code> for a START and
<code>'P'</code> for a STOP. End the string with <code>'\0'</code> and return its length.</p>
<p><b>Why it matters.</b> I2C connects sensors, EEPROMs and power chips to a processor. Knowing how START and
STOP are signalled is a common interview question.</p>
<h4>How I2C works (the facts you need)</h4>
<ul>
<li>Two wires: <b>SCL</b> (the clock) and <b>SDA</b> (the data). When nobody drives them, both rest at 1.</li>
<li>Normal data: SDA may change only while SCL is 0. The receiver reads SDA at the moment SCL goes from 0 to 1
(the <em>rising edge</em>).</li>
<li>Two special patterns break that rule on purpose, so they can never be confused with data:
<ul>
<li><b>START</b>: SDA goes 1 &rarr; 0 while SCL stays 1.</li>
<li><b>STOP</b>: SDA goes 0 &rarr; 1 while SCL stays 1.</li>
</ul></li>
</ul>
<h4>The rules (check them in this order)</h4>
<p>Compare each sample with the one before it: for every <code>i</code> from 1 to <code>n &minus; 1</code>,</p>
<ol>
<li>If SCL rose (<code>scl[i-1] == 0</code> and <code>scl[i] == 1</code>): append <code>'0'</code> or
<code>'1'</code>, the value of <code>sda[i]</code>.</li>
<li>Otherwise, if SCL was 1 in both samples and SDA fell (1 then 0): append <code>'S'</code>.</li>
<li>Otherwise, if SCL was 1 in both samples and SDA rose (0 then 1): append <code>'P'</code>.</li>
<li>Otherwise nothing happens at this <code>i</code>.</li>
</ol>
<h4>Example 1 (n = 9): result "S100P", returns 5</h4>
<pre>SCL ________     ___     ___     _______
            |___|   |___|   |___|
SDA ____         _______             ___
        |_______|       |___________|
i:   0   1   2   3   4   5   6   7   8</pre>
<table>
<tr><th>i</th><th>scl[i-1] &rarr; scl[i]</th><th>sda[i-1] &rarr; sda[i]</th><th>Rule</th><th>Append</th></tr>
<tr><td>1</td><td>1 &rarr; 1</td><td>1 &rarr; 0</td><td>SCL high, SDA fell</td><td>S</td></tr>
<tr><td>2</td><td>1 &rarr; 0</td><td>0 &rarr; 0</td><td>SCL fell: nothing</td><td></td></tr>
<tr><td>3</td><td>0 &rarr; 1</td><td>0 &rarr; 1</td><td>SCL rose, sda[3] = 1</td><td>1</td></tr>
<tr><td>4</td><td>1 &rarr; 0</td><td>1 &rarr; 1</td><td>nothing</td><td></td></tr>
<tr><td>5</td><td>0 &rarr; 1</td><td>1 &rarr; 0</td><td>SCL rose, sda[5] = 0</td><td>0</td></tr>
<tr><td>6</td><td>1 &rarr; 0</td><td>0 &rarr; 0</td><td>nothing</td><td></td></tr>
<tr><td>7</td><td>0 &rarr; 1</td><td>0 &rarr; 0</td><td>SCL rose, sda[7] = 0</td><td>0</td></tr>
<tr><td>8</td><td>1 &rarr; 1</td><td>0 &rarr; 1</td><td>SCL high, SDA rose</td><td>P</td></tr>
</table>
<h4>Example 2 (n = 8): a "repeated START"</h4>
<pre>scl: 1 1 0 1 1 0 1 1
sda: 1 0 0 1 0 0 0 1      -&gt; "S1S0P", returns 5</pre>
<p>At <code>i</code> = 4, SCL stays 1 and SDA falls, so it is a second START without a STOP before it. Real
masters do this to switch from writing to reading.</p>
<h4>Good to know (not needed for this function)</h4>
<p>These simple rules also report the clock pulse just before a STOP as a bit (the last <code>'0'</code> in
example 1). A real decoder knows the frame layout and drops it. In a real transfer the bytes are sent
<b>most significant bit first</b>; the first byte after START is the 7-bit address shifted left by one, with
the R/W bit in bit 0 (0 = write); and every byte is followed by an ACK bit (0 = acknowledged):</p>
<pre>START | A6 A5 A4 A3 A2 A1 A0 R/W | ACK | D7 ... D0 | ACK | ... | STOP</pre>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Every rule looks at a pair of neighbouring samples, <code>i-1</code> and <code>i</code>. So one loop
starting at <code>i = 1</code> is enough.</li>
<li>The order of the rules matters: test "SCL rose" first, and only then the two "SCL stayed high" cases.</li>
<li>Keep a separate counter for where the next character goes in <code>out</code>. Do not forget the
<code>'\0'</code> at the end, even when there are no events.</li>
</ol>
</details>""",
r"""#include <stdint.h>

int i2c_decode(const uint8_t *scl, const uint8_t *sda, int n, char *out)
{
    out[0] = '\0';
    return 0;
}
""",
r"""#include <stdint.h>

int i2c_decode(const uint8_t *scl, const uint8_t *sda, int n, char *out)
{
    int k = 0;
    for (int i = 1; i < n; i++) {
        if (!scl[i - 1] && scl[i])
            out[k++] = (char)('0' + sda[i]);         /* data bit, sampled on the rising edge */
        else if (scl[i - 1] && scl[i] && sda[i - 1] && !sda[i])
            out[k++] = 'S';
        else if (scl[i - 1] && scl[i] && !sda[i - 1] && sda[i])
            out[k++] = 'P';
    }
    out[k] = '\0';
    return k;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const uint8_t *c, const uint8_t *s, int n, char *o)
{
    int k = 0;
    for (int i = 1; i < n; i++) {
        if (!c[i - 1] && c[i]) o[k++] = (char)('0' + s[i]);
        else if (c[i - 1] && c[i] && s[i - 1] != s[i]) o[k++] = s[i] ? 'P' : 'S';
    }
    o[k] = 0;
    return k;
}
static uint8_t C[3000], D[3000];
static int n;
static void put(int c, int s) { C[n] = (uint8_t)c; D[n] = (uint8_t)s; n++; }
static void bit(int b) { put(0, D[n - 1]); put(0, b); put(1, b); put(1, b); }
static void byte(int v) { for (int k = 7; k >= 0; k--) bit((v >> k) & 1); bit(ck_range(0, 1)); }
int main(void)
{
    char d[96], got[3000], want[3000];
    uint8_t c0[] = {1, 1, 0, 1, 0, 1, 0, 1, 1}, s0[] = {1, 0, 0, 1, 1, 0, 0, 0, 1};
    ck_int("example: length", i2c_decode(c0, s0, 9, got), 5);
    ck_str("example", got, "S100P");
    for (int t = 0; t < 200; t++) {
        n = 0;
        put(1, 1); put(1, 1);
        if (t % 4 == 3) {
            while (n < 2000) put((int)(ck_rand() & 1), (int)(ck_rand() & 1));   /* random wires */
        } else {
            int frames = ck_range(1, 6);
            for (int f = 0; f < frames; f++) {
                put(1, 1); put(1, 0);                                     /* START */
                byte(ck_range(0, 127) << 1 | ck_range(0, 1));            /* address + R/W */
                int nb = ck_range(0, 5);
                for (int b = 0; b < nb; b++) byte(ck_range(0, 255));
                put(0, 0); put(1, 0); put(1, 1);                          /* STOP */
            }
        }
        memset(got, 'x', sizeof got);
        int lg = i2c_decode(C, D, n, got), lw = ref(C, D, n, want);
        got[sizeof got - 1] = 0;
        CK_FMT(d, "capture %d (%d samples): length", t, n); ck_int(d, lg, lw);
        int k = 0;
        while (want[k] && got[k] == want[k]) k++;
        CK_FMT(d, "capture %d: event %d", t, k);
        if (want[k] || got[k]) ck_true(d, 0); else ck_true(d, 1);
    }
    return ck_done();
}
""",
"Loop i from 1 to n-1 with an if / else if / else if chain. Rising SCL first; otherwise SCL high in both samples, and compare sda[i-1] with sda[i]."))

add(P("crc16", S, "CRC-16/CCITT", "c", "func",
r"""<p><b>What to write.</b> <code>uint16_t crc16_ccitt(const uint8_t *data, int n)</code>. It computes the
16-bit CRC of the <code>n</code> bytes at <code>data</code>, using the variant called
<b>CRC-16/CCITT-FALSE</b>.</p>
<p><b>Why it matters.</b> A CRC (cyclic redundancy check) is a short checksum added to a packet, a flash image
or a radio frame. The receiver computes it again; if the two values differ, the data was damaged. In maths it
is the remainder of a division of polynomials over bits, but you only need the shift-and-XOR recipe below.</p>
<h4>The settings of this CRC variant</h4>
<table>
<tr><th>Setting</th><th>Value</th><th>Meaning</th></tr>
<tr><td>Width</td><td>16 bits</td><td>keep the CRC in a <code>uint16_t</code></td></tr>
<tr><td>Polynomial</td><td>0x1021</td><td>x<sup>16</sup> + x<sup>12</sup> + x<sup>5</sup> + 1; the x<sup>16</sup>
term is not written, so 0x1021 = 0001 0000 0010 0001</td></tr>
<tr><td>Initial value</td><td>0xFFFF</td><td>the CRC before any byte is processed</td></tr>
<tr><td>Bit order</td><td>MSB first</td><td>no "reflection": bit 7 of each byte goes in first</td></tr>
<tr><td>Final XOR</td><td>none</td><td>return the register as it is</td></tr>
</table>
<h4>The recipe, step by step</h4>
<ol>
<li>Start with <code>crc = 0xFFFF</code>.</li>
<li>For each byte: XOR the byte into the <b>top 8 bits</b> of <code>crc</code> (bits 15..8).</li>
<li>Then repeat 8 times: look at bit 15 (the top bit).
<ul><li>If it is 1: shift <code>crc</code> left by one, then XOR with 0x1021.</li>
<li>If it is 0: only shift left by one.</li></ul>
The bit that falls off the top is thrown away, so <code>crc</code> stays 16 bits.</li>
<li>After the last byte, <code>crc</code> is the answer.</li>
</ol>
<h4>Picture of one shift step</h4>
<pre>bit:  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
crc: [ t  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . ]
      |
      +-- top bit t.  Shift everything one place left (a 0 enters at bit 0).
          If t was 1, also XOR with 0x1021 = 0001 0000 0010 0001.</pre>
<h4>Worked example: one byte, 'A' = 0x41</h4>
<table>
<tr><th>Step</th><th>Top bit before</th><th><code>crc</code> after</th></tr>
<tr><td>start</td><td></td><td>0xFFFF</td></tr>
<tr><td>XOR 0x41 into bits 15..8 (0xFFFF ^ 0x4100)</td><td></td><td>0xBEFF</td></tr>
<tr><td>shift 1</td><td>1</td><td>0x6DDF</td></tr>
<tr><td>shift 2</td><td>0</td><td>0xDBBE</td></tr>
<tr><td>shift 3</td><td>1</td><td>0xA75D</td></tr>
<tr><td>shift 4</td><td>1</td><td>0x5E9B</td></tr>
<tr><td>shift 5</td><td>0</td><td>0xBD36</td></tr>
<tr><td>shift 6</td><td>1</td><td>0x6A4D</td></tr>
<tr><td>shift 7</td><td>0</td><td>0xD49A</td></tr>
<tr><td>shift 8</td><td>1</td><td>0xB915</td></tr>
</table>
<p>So <code>crc16_ccitt("A", 1)</code> returns 0xB915.</p>
<h4>More examples</h4>
<table>
<tr><th>Call</th><th>Returns</th><th>Note</th></tr>
<tr><td><code>crc16_ccitt("123456789", 9)</code></td><td>0x29B1</td><td>the standard "check value" of this variant</td></tr>
<tr><td><code>crc16_ccitt(anything, 0)</code></td><td>0xFFFF</td><td>no bytes: the initial value</td></tr>
<tr><td><code>crc16_ccitt(buf, 1)</code> with <code>buf[0] = 0x00</code></td><td>0xE1F0</td><td>one zero byte</td></tr>
</table>
<p>The tests also use random buffers of 1 to 300 bytes.</p>
<h4>Things to watch out for</h4>
<ul>
<li>In C, <code>crc &lt;&lt; 1</code> on a <code>uint16_t</code> is computed as an <code>int</code>, so the
result can have a 17th bit. Cut it back to 16 bits (store into a <code>uint16_t</code>, or use
<code>&amp; 0xFFFF</code>) before you test the top bit again.</li>
<li>Test the top bit <b>before</b> you shift, not after.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>How do you move a byte into bits 15..8? (Shift it left by 8.)</li>
<li>Which mask tells you whether bit 15 is 1? (0x8000.)</li>
<li>Check your code with the 'A' table above: print <code>crc</code> after each shift and compare.</li>
</ol>
</details>""",
r"""#include <stdint.h>

uint16_t crc16_ccitt(const uint8_t *data, int n)
{
    return 0;
}
""",
r"""#include <stdint.h>

uint16_t crc16_ccitt(const uint8_t *data, int n)
{
    uint16_t crc = 0xFFFF;
    for (int i = 0; i < n; i++) {
        crc ^= (uint16_t)(data[i] << 8);
        for (int k = 0; k < 8; k++)
            crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021) : (uint16_t)(crc << 1);
    }
    return crc;
}
""",
r"""#include "check.h"
#include "solution.c"
static uint16_t ref(const uint8_t *p, int n)
{
    unsigned c = 0xFFFF;
    for (int i = 0; i < n; i++) {
        c ^= (unsigned)p[i] << 8;
        for (int k = 0; k < 8; k++) c = (c & 0x8000) ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF;
    }
    return (uint16_t)c;
}
int main(void)
{
    char d[96];
    ck_hex("crc16_ccitt(\"123456789\")", crc16_ccitt((const uint8_t *)"123456789", 9), 0x29B1);
    ck_hex("crc16_ccitt(empty)", crc16_ccitt((const uint8_t *)"", 0), 0xFFFF);
    uint8_t buf[300];
    for (int t = 0; t < 200; t++) {
        int n = ck_range(1, 300);
        for (int i = 0; i < n; i++) buf[i] = (uint8_t)ck_rand();
        CK_FMT(d, "crc16_ccitt(random %d bytes, case %d)", n, t);
        ck_hex(d, crc16_ccitt(buf, n), ref(buf, n));
    }
    return ck_done();
}
""",
"crc ^= data[i] << 8; then 8 times: crc = (crc & 0x8000) ? (crc << 1) ^ 0x1021 : crc << 1, keeping it 16 bits."))

add(P("hamming74", S, "Hamming (7,4): correct a flipped bit", "c", "func",
r"""<p><b>What to write.</b> Two functions for the Hamming (7,4) error-correcting code:</p>
<pre>uint8_t ham_encode(uint8_t nibble);              // 4 data bits -&gt; codeword
uint8_t ham_decode(uint8_t cw, int *fixed_pos);  // codeword -&gt; 4 data bits</pre>
<p><code>ham_decode</code> returns the 4 data bits (corrected if one bit was flipped) and sets
<code>*fixed_pos</code> to the position it corrected, or 0 if there was no error.</p>
<p><b>Why it matters.</b> ECC memory corrects single flipped bits (the "EDAC" interview question: Error
Detection And Correction). Hamming (7,4) is the smallest example: 4 data bits plus 3 parity bits, and any one
flipped bit can be found and fixed.</p>
<h4>Where each bit goes</h4>
<p>Number the 7 codeword positions 1 to 7. Position <i>k</i> is stored in bit <i>k</i>&minus;1 of the
byte. The data bits d1..d4 are bits 0..3 of <code>nibble</code>.</p>
<pre>position:     7    6    5    4    3    2    1
byte bit:     6    5    4    3    2    1    0
holds:       d4   d3   d2   p4   d1   p2   p1
            (d1 = nibble bit 0, d2 = bit 1, d3 = bit 2, d4 = bit 3)</pre>
<p>Parity bits sit at the positions that are powers of two (1, 2, 4). Data bits fill the others (3, 5, 6,
7).</p>
<h4>Which positions each parity bit covers</h4>
<p>Parity bit <i>p</i> covers every position whose number, written in binary, has bit <i>p</i> set. It is
chosen so that its group has an <b>even</b> number of 1s.</p>
<table>
<tr><th>Parity bit</th><th>Covers positions</th><th>So it equals</th></tr>
<tr><td>p1 (position 1 = 001)</td><td>1, 3, 5, 7</td><td>d1 ^ d2 ^ d4</td></tr>
<tr><td>p2 (position 2 = 010)</td><td>2, 3, 6, 7</td><td>d1 ^ d3 ^ d4</td></tr>
<tr><td>p4 (position 4 = 100)</td><td>4, 5, 6, 7</td><td>d2 ^ d3 ^ d4</td></tr>
</table>
<h4>Encoding example: <code>ham_encode(0xB)</code> = 0x55</h4>
<pre>0xB = 1011  -&gt;  d1 = 1, d2 = 1, d3 = 0, d4 = 1
p1 = d1^d2^d4 = 1      p2 = d1^d3^d4 = 0      p4 = d2^d3^d4 = 0

position:  7  6  5  4  3  2  1
holds:    d4 d3 d2 p4 d1 p2 p1
value:     1  0  1  0  1  0  1    = 101 0101 binary = 0x55</pre>
<h4>Decoding: the syndrome</h4>
<p>XOR together the <b>position numbers</b> of all the bits that are 1. The result is called the
<b>syndrome</b>.</p>
<ul>
<li>Syndrome 0: no error.</li>
<li>Syndrome <i>s</i> (1 to 7): the bit at position <i>s</i> is wrong. Flip it (byte bit <i>s</i>&minus;1),
then read the data from positions 3, 5, 6, 7.</li>
</ul>
<table>
<tr><th>Received</th><th>Positions holding a 1</th><th>Syndrome</th><th>Returns</th><th><code>*fixed_pos</code></th></tr>
<tr><td>0x55 = 1010101</td><td>1, 3, 5, 7</td><td>1^3^5^7 = 0</td><td>0xB</td><td>0</td></tr>
<tr><td>0x75 = 1110101 (position 6 flipped)</td><td>1, 3, 5, 6, 7</td><td>1^3^5^6^7 = 6</td><td>0xB</td><td>6</td></tr>
<tr><td>0x54 = 1010100 (position 1 flipped)</td><td>3, 5, 7</td><td>3^5^7 = 1</td><td>0xB</td><td>1</td></tr>
</table>
<p>The tests try all 16 nibbles, each with no flip and with each of the 7 positions flipped.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Encode: pull out d1..d4 with shifts and <code>&amp; 1</code>, compute p1, p2, p4 with XOR, then shift
each of the 7 bits to its byte bit (position minus 1) and OR them together.</li>
<li>Decode: loop over positions 1..7. If byte bit (pos &minus; 1) is 1, XOR <code>pos</code> into the
syndrome.</li>
<li>If the syndrome is not 0, flip that bit first. Then collect the data bits from byte bits 2, 4, 5, 6 back
into bits 0..3.</li>
</ol>
</details>""",
r"""#include <stdint.h>

uint8_t ham_encode(uint8_t nibble)
{
    return 0;
}

uint8_t ham_decode(uint8_t cw, int *fixed_pos)
{
    *fixed_pos = 0;
    return 0;
}
""",
r"""#include <stdint.h>

#define BIT(x, k) (((x) >> (k)) & 1)

uint8_t ham_encode(uint8_t nibble)
{
    int d1 = BIT(nibble, 0), d2 = BIT(nibble, 1), d3 = BIT(nibble, 2), d4 = BIT(nibble, 3);
    int p1 = d1 ^ d2 ^ d4;          /* positions 3, 5, 7 */
    int p2 = d1 ^ d3 ^ d4;          /* positions 3, 6, 7 */
    int p4 = d2 ^ d3 ^ d4;          /* positions 5, 6, 7 */
    return (uint8_t)(p1 | p2 << 1 | d1 << 2 | p4 << 3 | d2 << 4 | d3 << 5 | d4 << 6);
}

uint8_t ham_decode(uint8_t cw, int *fixed_pos)
{
    int s = 0;
    for (int pos = 1; pos <= 7; pos++)
        if (BIT(cw, pos - 1))
            s ^= pos;               /* syndrome = XOR of the positions holding a 1 */
    if (s)
        cw ^= (uint8_t)(1 << (s - 1));
    *fixed_pos = s;
    return (uint8_t)(BIT(cw, 2) | BIT(cw, 4) << 1 | BIT(cw, 5) << 2 | BIT(cw, 6) << 3);
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref_enc(int v)
{
    int cw = 0, dpos[4] = {3, 5, 6, 7};
    for (int k = 0; k < 4; k++) if ((v >> k) & 1) cw |= 1 << (dpos[k] - 1);
    for (int p = 1; p <= 4; p <<= 1) {
        int par = 0;
        for (int pos = 1; pos <= 7; pos++) if ((pos & p) && pos != p) par ^= (cw >> (pos - 1)) & 1;
        cw |= par << (p - 1);
    }
    return cw;
}
int main(void)
{
    char d[96];
    ck_hex("ham_encode(0xB)", ham_encode(0xB), 0x55);
    for (int v = 0; v < 16; v++) {
        CK_FMT(d, "ham_encode(0x%X)", v); ck_hex(d, ham_encode((uint8_t)v), (unsigned)ref_enc(v));
        int cw = ref_enc(v);
        for (int flip = 0; flip <= 7; flip++) {
            int bad = flip ? cw ^ (1 << (flip - 1)) : cw, fp = -1;
            int got = ham_decode((uint8_t)bad, &fp);
            CK_FMT(d, "ham_decode(0x%02X) (nibble 0x%X, bit position %d flipped)", bad, v, flip);
            ck_hex(d, (unsigned)got, (unsigned)v);
            CK_FMT(d, "ham_decode(0x%02X) fixed_pos", bad);
            ck_int(d, fp, flip);
        }
    }
    return ck_done();
}
""",
"Encode: compute p1 = d1^d2^d4, p2 = d1^d3^d4, p4 = d2^d3^d4 and place all seven bits. Decode: s = 0; for pos = 1..7, if bit pos-1 is set, s ^= pos. If s != 0, flip bit s-1. Then read back positions 3, 5, 6, 7."))

add(P("debounce", S, "Debounce a push button", "c", "func",
r"""<p><b>What to write.</b> A software debouncer for a push button, kept in a small struct:</p>
<pre>struct Debounce { int state; int count; };
void debounce_init(struct Debounce *d, int initial);
     // sets state = initial, count = 0
int  debounce_step(struct Debounce *d, int raw, int n);
     // takes one raw sample, returns the debounced state</pre>
<p>Firmware calls <code>debounce_step</code> once per sample (for example every millisecond) with the raw
pin level <code>raw</code> (0 or 1). It returns the cleaned-up level.</p>
<p><b>Why it matters.</b> When you press a mechanical button, the metal contacts bounce for a few
milliseconds, so the pin flips between 0 and 1 many times. Without debouncing, one press looks like many
presses. The fix: accept a new level only after it has stayed the same for <code>n</code> samples in a
row.</p>
<h4>The rule for each sample</h4>
<ol>
<li>If <code>raw</code> equals <code>state</code>: nothing is changing. Set <code>count</code> to 0.</li>
<li>Otherwise (<code>raw</code> differs from <code>state</code>): add 1 to <code>count</code>. If
<code>count</code> has reached <code>n</code>, accept the new level: <code>state = raw</code> and
<code>count = 0</code>.</li>
<li>Return <code>state</code>.</li>
</ol>
<h4>Example: n = 3, starting state 0</h4>
<table>
<tr><th>Sample</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th></tr>
<tr><td><code>raw</code></td><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr>
<tr><td><code>count</code> after</td><td>1</td><td>0</td><td>1</td><td>2</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>returned <code>state</code></td><td>0</td><td>0</td><td>0</td><td>0</td><td><b>1</b></td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr>
</table>
<ul>
<li>Sample 0: a single 1 (a bounce). <code>count</code> becomes 1, but sample 1 is back to 0, so
<code>count</code> resets.</li>
<li>Samples 2, 3, 4: three 1s in a row. On the third one <code>count</code> reaches 3, so the state
becomes 1.</li>
<li>Samples 5, 6: only two 0s, then a 1. Not enough, so the state stays 1.</li>
</ul>
<h4>Edge case: n = 1</h4>
<p>With <code>n</code> = 1 the first differing sample is accepted at once: raw 1, 0, 0, 1 from state 0 gives
1, 0, 0, 1.</p>
<p>The tests use <code>n</code> from 1 to 6, both starting states, and long random bouncy inputs.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li><code>debounce_init</code> only fills in the two fields.</li>
<li>In <code>debounce_step</code> there are only two cases: <code>raw</code> equals the state, or it does
not. Write the rule above as an <code>if</code> / <code>else</code>.</li>
<li>Check yourself against the table: after each sample, are your <code>count</code> and
<code>state</code> the same as the table's?</li>
</ol>
</details>""",
r"""struct Debounce {
    int state;
    int count;
};

void debounce_init(struct Debounce *d, int initial)
{
}

int debounce_step(struct Debounce *d, int raw, int n)
{
    return raw;
}
""",
r"""struct Debounce {
    int state;
    int count;
};

void debounce_init(struct Debounce *d, int initial)
{
    d->state = initial;
    d->count = 0;
}

int debounce_step(struct Debounce *d, int raw, int n)
{
    if (raw == d->state) {
        d->count = 0;
    } else if (++d->count >= n) {
        d->state = raw;
        d->count = 0;
    }
    return d->state;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    int ex[] = {1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1}, exo[] = {0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1};
    struct Debounce db;
    debounce_init(&db, 0);
    for (int i = 0; i < 11; i++) { CK_FMT(d, "example sample %d", i); ck_int(d, debounce_step(&db, ex[i], 3), exo[i]); }
    for (int t = 0; t < 100; t++) {
        int n = ck_range(1, 6), init = ck_range(0, 1), st = init, cnt = 0, level = init;
        debounce_init(&db, init);
        for (int i = 0; i < 300; i++) {
            if (ck_range(0, 30) == 0) level ^= 1;
            int raw = ck_range(0, 3) == 0 ? (int)(ck_rand() & 1) : level;     /* bounces */
            if (raw == st) cnt = 0; else if (++cnt >= n) { st = raw; cnt = 0; }
            CK_FMT(d, "run %d (n = %d), sample %d", t, n, i);
            ck_int(d, debounce_step(&db, raw, n), st);
        }
    }
    return ck_done();
}
""",
"if (raw == d->state) d->count = 0; else if (++d->count >= n) { d->state = raw; d->count = 0; }"))

add(P("watchdog", S, "Windowed watchdog", "c", "func",
r"""<p><b>What to write.</b>
<code>int wdt_first_reset(const int *kicks, int nk, int timeout, int window, int end)</code>. It simulates a
windowed watchdog timer and returns the time of the first chip reset, or &minus;1 if there is no reset up to
time <code>end</code>.</p>
<p><b>Why it matters.</b> A watchdog timer resets the chip unless the software "kicks" (restarts) it in
time. If the program hangs, the kicks stop and the chip recovers by itself. A <em>windowed</em> watchdog also
resets the chip if a kick comes <b>too early</b>. That catches code stuck in a tight loop that keeps kicking.
(This was asked in both 2026 Qualcomm interview rounds.)</p>
<h4>The inputs</h4>
<ul>
<li><code>kicks[0..nk-1]</code>: the times when the software kicks, in strictly increasing order.
<code>nk</code> can be 0.</li>
<li><code>timeout</code>: the longest allowed gap between two kicks.</li>
<li><code>window</code>: the shortest allowed gap. 0 means "no window" (any early kick is fine).</li>
<li><code>end</code>: the time the simulation stops.</li>
</ul>
<h4>The rules, step by step</h4>
<ol>
<li>Time 0 counts as the last kick: <code>last = 0</code>.</li>
<li>For each kick time <code>t</code>, in order:
<ul>
<li>If <code>t &minus; last &ge; timeout</code>: the kick came too late. The chip already reset at
<code>last + timeout</code>. Return that.</li>
<li>Otherwise, if <code>t &minus; last &lt; window</code>: the kick is too early. The chip resets at
<code>t</code>. Return <code>t</code>.</li>
<li>Otherwise the kick is good: <code>last = t</code>.</li>
</ul></li>
<li>After the last kick, the timer runs out at <code>last + timeout</code>. If that is &le;
<code>end</code>, return it. Otherwise return &minus;1.</li>
</ol>
<p>Note the exact borders: a gap of exactly <code>timeout</code> is already too late, and a gap of exactly
<code>window</code> is fine.</p>
<h4>Picture: example 1 (timeout 100, window 0)</h4>
<pre>time:   0        50            120          220     250
        |---------|--------------|-------------X------|
       start    kick ok        kick ok      RESET   kick (too late,
       last=0   gap 50         gap 70       120+100  gap 130 &ge; 100)</pre>
<h4>Picture: example 2 (timeout 100, window 30)</h4>
<pre>time:   0        50   60
        |---------|----X
       start    kick  kick only 10 after the last one: 10 &lt; 30,
                ok    too early, RESET at 60</pre>
<h4>Examples</h4>
<table>
<tr><th>timeout</th><th>window</th><th>kicks</th><th>end</th><th>Returns</th><th>Why</th></tr>
<tr><td>100</td><td>0</td><td>50 120 250</td><td>1000</td><td>220</td><td>gap 120 &rarr; 250 is 130 &ge; 100</td></tr>
<tr><td>100</td><td>30</td><td>50 60</td><td>1000</td><td>60</td><td>gap 10 &lt; 30: too early</td></tr>
<tr><td>100</td><td>30</td><td>50 90</td><td>150</td><td>&minus;1</td><td>gaps 50 and 40 are fine; 90 + 100 = 190 &gt; 150</td></tr>
<tr><td>100</td><td>0</td><td>50 150</td><td>1000</td><td>150</td><td>gap exactly 100 counts as too late: reset at 50 + 100</td></tr>
<tr><td>10</td><td>0</td><td>(none)</td><td>10</td><td>10</td><td>no kicks: 0 + 10 = 10 &le; 10</td></tr>
<tr><td>10</td><td>0</td><td>(none)</td><td>9</td><td>&minus;1</td><td>10 &gt; 9: the run ends first</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>You only need one variable besides the loop counter: the time of the last good kick.</li>
<li>Inside the loop, check "too late" first, then "too early". Each failing check ends the function at
once.</li>
<li>If the loop finishes, one more check against <code>end</code> decides between a reset and &minus;1.</li>
</ol>
</details>""",
r"""int wdt_first_reset(const int *kicks, int nk, int timeout, int window, int end)
{
    return -1;
}
""",
r"""int wdt_first_reset(const int *kicks, int nk, int timeout, int window, int end)
{
    int last = 0;
    for (int i = 0; i < nk; i++) {
        int t = kicks[i];
        if (t - last >= timeout)
            return last + timeout;      /* nobody kicked in time */
        if (t - last < window)
            return t;                   /* kicked too early */
        last = t;
    }
    return last + timeout <= end ? last + timeout : -1;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const int *k, int nk, int to, int w, int end)
{
    int last = 0;
    for (int i = 0; i < nk; i++) {
        if (k[i] - last >= to) return last + to;
        if (k[i] - last < w) return k[i];
        last = k[i];
    }
    return last + to <= end ? last + to : -1;
}
int main(void)
{
    char d[96];
    int k1[] = {50, 120, 250}, k2[] = {50, 60}, k3[] = {50, 90};
    ck_int("example 1", wdt_first_reset(k1, 3, 100, 0, 1000), 220);
    ck_int("example 2", wdt_first_reset(k2, 2, 100, 30, 1000), 60);
    ck_int("example 3", wdt_first_reset(k3, 2, 100, 30, 150), -1);
    ck_int("no kicks, timeout 10, end 9", wdt_first_reset(k1, 0, 10, 0, 9), -1);
    ck_int("no kicks, timeout 10, end 10", wdt_first_reset(k1, 0, 10, 0, 10), 10);
    for (int t = 0; t < 400; t++) {
        int to = ck_range(5, 50), w = ck_range(0, 1) ? 0 : ck_range(1, to - 1), nk = ck_range(0, 30), ks[30], last = 0;
        for (int i = 0; i < nk; i++) { last += ck_range(1, to + 3); ks[i] = last; }
        int end = last + ck_range(0, to + 5);
        CK_FMT(d, "case %d: timeout %d, window %d, %d kicks", t, to, w, nk);
        ck_int(d, wdt_first_reset(ks, nk, to, w, end), ref(ks, nk, to, w, end));
    }
    return ck_done();
}
""",
"Keep last = 0. For each kick: check the timeout first, then the window, then set last = t. After the loop, compare last + timeout with end."))

add(P("irq_dispatch", S, "Interrupt dispatch with a vector table", "c", "func",
r"""<p><b>What to write.</b> The interrupt dispatcher of a small firmware:</p>
<pre>typedef void (*isr_t)(int irq);   // a handler: takes the IRQ number

void irq_register(int irq, isr_t handler);
     // NULL removes a handler
int  irq_dispatch(volatile uint32_t *pending);
     // returns how many handlers were called</pre>
<p><b>Why it matters.</b> This is how an interrupt controller and its driver work on a real chip. It also
practises function pointers and bit tricks, which interviews like to combine.</p>
<h4>The data</h4>
<ul>
<li>The <b>pending register</b> is a 32-bit value. Bit <i>k</i> = 1 means IRQ (interrupt request) number
<i>k</i> is waiting to be handled. IRQ numbers are 0 to 31.</li>
<li>The <b>vector table</b> is an array of 32 function pointers, one per IRQ (the starter code already
declares <code>vector_table[32]</code>). Entry <i>k</i> is the handler for IRQ <i>k</i>, or
<code>NULL</code> if there is none.</li>
</ul>
<pre>pending = 0x00000029
bit:   31 30 ... 6  5  4  3  2  1  0
value:  0  0 ... 0  1  0  1  0  0  1     -&gt; IRQs 0, 3 and 5 are waiting</pre>
<h4>The rules</h4>
<ul>
<li><code>irq_register(irq, handler)</code> stores <code>handler</code> in the table entry for
<code>irq</code>.</li>
<li><code>irq_dispatch</code> repeats these steps until <code>*pending</code> is 0:
<ol>
<li>Read <code>*pending</code> and find its <b>lowest</b> set bit <i>k</i>. Lower number = higher
priority.</li>
<li>Clear bit <i>k</i> in <code>*pending</code>. Do this <b>before</b> calling the handler.</li>
<li>If entry <i>k</i> has a handler, call it with <i>k</i> and count the call. If it is
<code>NULL</code>, the interrupt is "spurious": it is only cleared, and not counted.</li>
</ol></li>
</ul>
<h4>Example 1: handlers for IRQ 0 and IRQ 5 only, pending = 0x29</h4>
<table>
<tr><th>Round</th><th><code>*pending</code> read</th><th>Lowest bit</th><th>After clearing</th><th>Action</th><th>Calls so far</th></tr>
<tr><td>1</td><td>0x29</td><td>0</td><td>0x28</td><td>call handler 0</td><td>1</td></tr>
<tr><td>2</td><td>0x28</td><td>3</td><td>0x20</td><td>no handler: only cleared</td><td>1</td></tr>
<tr><td>3</td><td>0x20</td><td>5</td><td>0x00</td><td>call handler 5</td><td>2</td></tr>
</table>
<p>Returns 2, and <code>*pending</code> ends at 0.</p>
<h4>Example 2: a handler that raises a new interrupt</h4>
<p>Handlers for IRQ 1 and IRQ 5. Pending = 0x22 (IRQs 1 and 5). The handler for IRQ 5 sets bit 1 again.</p>
<table>
<tr><th>Round</th><th>Read</th><th>Lowest bit</th><th>After clearing</th><th>Action</th></tr>
<tr><td>1</td><td>0x22</td><td>1</td><td>0x20</td><td>call handler 1</td></tr>
<tr><td>2</td><td>0x20</td><td>5</td><td>0x00</td><td>call handler 5, which makes pending 0x02</td></tr>
<tr><td>3</td><td>0x02</td><td>1</td><td>0x00</td><td>call handler 1 again</td></tr>
</table>
<p>Returns 3. This is why you must read <code>*pending</code> again every round, and why the register is
<code>volatile</code> (it can change behind the compiler's back).</p>
<div class="note">Clear the bit <b>before</b> calling the handler. A handler may raise its own IRQ again. If
you cleared after the call, you would wipe out that new request.</div>
<p>The tests use random tables and random pending values; the handlers that raise IRQs stop after a few
raises, so the loop always ends.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>How do you find the lowest set bit of a value? (Test bit 0, bit 1, ... until one is 1.)</li>
<li>How do you clear bit <i>k</i> and keep all the others? (AND with a mask that has a 0 only at bit
<i>k</i>; use <code>1u</code> so that bit 31 works.)</li>
<li>Calling through a function pointer looks like an ordinary call: <code>table_entry(k)</code>.</li>
</ol>
</details>""",
r"""#include <stdint.h>
#include <stddef.h>

typedef void (*isr_t)(int irq);

static isr_t vector_table[32];

void irq_register(int irq, isr_t handler)
{
}

int irq_dispatch(volatile uint32_t *pending)
{
    return 0;
}
""",
r"""#include <stdint.h>
#include <stddef.h>

typedef void (*isr_t)(int irq);

static isr_t vector_table[32];

void irq_register(int irq, isr_t handler)
{
    vector_table[irq] = handler;
}

int irq_dispatch(volatile uint32_t *pending)
{
    int calls = 0;
    uint32_t p;
    while ((p = *pending) != 0) {
        int k = 0;
        while (!((p >> k) & 1))          /* lowest set bit = highest priority */
            k++;
        *pending &= ~(1u << k);          /* clear before calling: the handler may raise it again */
        if (vector_table[k]) {
            vector_table[k](k);
            calls++;
        }
    }
    return calls;
}
""",
r"""#include "check.h"
#include "solution.c"
static int lg[256], nl;
static volatile uint32_t *cur;
static int raise_left;
static void h_log(int irq) { if (nl < 256) lg[nl++] = irq; }
static void h_raise(int irq) { if (nl < 256) lg[nl++] = 100 + irq; if (raise_left > 0) { raise_left--; *cur |= 1u << (irq % 3); *cur |= 1u << 31; } }
static isr_t rv[32];
static int ref_dispatch(volatile uint32_t *p)
{
    int c = 0;
    while (*p) { int k = __builtin_ctz(*p); *p &= ~(1u << k); if (rv[k]) { rv[k](k); c++; } }
    return c;
}
int main(void)
{
    char d[96];
    for (int t = 0; t < 300; t++) {
        for (int k = 0; k < 32; k++) {
            int r = ck_range(0, 5);
            rv[k] = r == 0 ? NULL : (r == 1 ? h_raise : h_log);
            irq_register(k, rv[k]);
        }
        uint32_t init = ck_rand() & ck_rand();
        int raises = ck_range(0, 3);
        volatile uint32_t pend = init;
        cur = &pend; nl = 0; raise_left = raises;
        int cg = irq_dispatch(&pend);
        int lgot[256], ngot = nl; memcpy(lgot, lg, sizeof lg);
        uint32_t left = pend;
        pend = init; nl = 0; raise_left = raises;
        int cw = ref_dispatch(&pend);
        CK_FMT(d, "case %d (pending 0x%08X): handlers called", t, (unsigned)init); ck_int(d, cg, cw);
        CK_FMT(d, "case %d: pending register at the end", t); ck_hex(d, left, 0);
        int k = 0;
        while (k < nl && k < ngot && lgot[k] == lg[k]) k++;
        CK_FMT(d, "case %d: call %d (100+k = a handler that raises IRQs)", t, k);
        if (k < nl || k < ngot) ck_int(d, k < ngot ? lgot[k] : -1, k < nl ? lg[k] : -1); else ck_true(d, 1);
    }
    return ck_done();
}
""",
"irq_register just stores the pointer. In irq_dispatch: while ((p = *pending) != 0) { find the lowest set bit k; *pending &= ~(1u << k); if (vector_table[k]) call it and count. }"))

add(P("mem_pool", S, "Fixed-block memory pool", "c", "func",
r"""<p><b>What to write.</b> A fixed-block memory pool, a small replacement for <code>malloc</code>:</p>
<pre>#define BLOCK_SIZE 32
#define NUM_BLOCKS 16
void  pool_init(void);         // make every block free
void *pool_alloc(void);        // one free block, or NULL if all 16 are used
void  pool_free(void *p);      // take back a block from pool_alloc</pre>
<p><b>Why it matters.</b> Embedded and real-time code avoids <code>malloc</code>: it can be slow, it
fragments the heap (leaves small unusable gaps), and it can fail at the worst moment. A pool of equal-sized
blocks has none of these problems, and both allocation and free take O(1) time (the same short time, however
many blocks there are).</p>
<h4>The idea: a free list stored inside the free blocks</h4>
<p>Keep the memory in one static array of 16 blocks of 32 bytes (no <code>malloc</code>). A free block is not
used by anybody, so you may store something in it: a pointer to the next free block. The free blocks then form
a linked list, and one variable <code>free_list</code> points to its first block.</p>
<pre>after pool_init (all 16 blocks free):

free_list
    |
    v
+---------+     +---------+     +---------+           +---------+
| next ---+----&gt;| next ---+----&gt;| next ---+--&gt; ... --&gt;|  NULL   |
| (free)  |     | (free)  |     | (free)  |           | (free)  |
+---------+     +---------+     +---------+           +---------+
  block 0         block 1         block 2               block 15</pre>
<h4>The operations</h4>
<ul>
<li><b>alloc</b>: take the first block of the list. <code>free_list</code> moves to that block's
<code>next</code>. If the list is empty, return <code>NULL</code>.</li>
<li><b>free</b>: put the block back at the front: its <code>next</code> becomes the old
<code>free_list</code>, and <code>free_list</code> points to it.</li>
</ul>
<h4>Example sequence (if <code>pool_init</code> links the blocks in order 0, 1, 2, ...)</h4>
<table>
<tr><th>Call</th><th>Returns</th><th>Free list afterwards</th></tr>
<tr><td><code>pool_init()</code></td><td></td><td>0 &rarr; 1 &rarr; 2 &rarr; ... &rarr; 15</td></tr>
<tr><td><code>a = pool_alloc()</code></td><td>block 0</td><td>1 &rarr; 2 &rarr; ... &rarr; 15</td></tr>
<tr><td><code>b = pool_alloc()</code></td><td>block 1</td><td>2 &rarr; 3 &rarr; ... &rarr; 15</td></tr>
<tr><td><code>pool_free(a)</code></td><td></td><td>0 &rarr; 2 &rarr; 3 &rarr; ... &rarr; 15</td></tr>
<tr><td><code>c = pool_alloc()</code></td><td>block 0 again</td><td>2 &rarr; 3 &rarr; ... &rarr; 15</td></tr>
</table>
<p>Any order of blocks is fine. The tests do not care which free block you hand out.</p>
<h4>What the tests check (three rounds, each starting with <code>pool_init</code>)</h4>
<ul>
<li>16 calls to <code>pool_alloc</code> all succeed, and the 17th returns <code>NULL</code>.</li>
<li>The 16 blocks are at least 32 bytes apart. The test writes all 32 bytes of every block and checks that
no other block changed.</li>
<li>After freeing a random half, the blocks still in use are unchanged. Allocating again gives back exactly
the freed blocks, and then the pool is empty again.</li>
</ul>
<div class="note">A pointer is 4 bytes on this site (8 on a 64-bit PC), so it fits easily inside a 32-byte
block. A <code>union</code> of "pointer to next block" and "32 bytes" describes such a block neatly. You may
only use the inside of a block for <code>next</code> while it is free.</div>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Draw the list on paper. What does <code>pool_init</code> have to do so that every block is in it, and the
last one ends with <code>NULL</code>?</li>
<li><code>pool_alloc</code> is "remove the first node of a linked list". <code>pool_free</code> is "insert a
node at the front".</li>
<li><code>pool_init</code> is called again at the start of each round. Make sure it rebuilds the whole list
from scratch.</li>
</ol>
</details>""",
r"""#include <stddef.h>

#define BLOCK_SIZE 32
#define NUM_BLOCKS 16

void pool_init(void)
{
}

void *pool_alloc(void)
{
    return NULL;
}

void pool_free(void *p)
{
}
""",
r"""#include <stddef.h>

#define BLOCK_SIZE 32
#define NUM_BLOCKS 16

typedef union Block {
    union Block *next;                  /* used while the block is free */
    unsigned char bytes[BLOCK_SIZE];    /* used while it is allocated */
} Block;

static Block pool[NUM_BLOCKS];
static Block *free_list;

void pool_init(void)
{
    free_list = NULL;
    for (int i = NUM_BLOCKS - 1; i >= 0; i--) {
        pool[i].next = free_list;
        free_list = &pool[i];
    }
}

void *pool_alloc(void)
{
    Block *b = free_list;
    if (b)
        free_list = b->next;
    return b;
}

void pool_free(void *p)
{
    Block *b = p;
    b->next = free_list;
    free_list = b;
}
""",
r"""#include "check.h"
#include "solution.c"
#include <stdint.h>
static unsigned char *ptr[16];
static void fill(int i, int tag) { memset(ptr[i], tag, 32); }
static int intact(int i, int tag) { for (int k = 0; k < 32; k++) if (ptr[i][k] != (unsigned char)tag) return 0; return 1; }
int main(void)
{
    char d[96];
    for (int round = 0; round < 3; round++) {
        pool_init();
        int ok = 1;
        for (int i = 0; i < 16; i++) { ptr[i] = pool_alloc(); if (!ptr[i]) ok = 0; }
        CK_FMT(d, "round %d: 16 allocations succeed", round); ck_true(d, ok);
        if (!ok) break;
        CK_FMT(d, "round %d: the 17th allocation returns NULL", round); ck_true(d, pool_alloc() == NULL);
        int distinct = 1;
        for (int i = 0; i < 16; i++) for (int j = i + 1; j < 16; j++) {
            intptr_t gap = (intptr_t)ptr[i] - (intptr_t)ptr[j];
            if (gap < 0) gap = -gap;
            if (gap < 32) distinct = 0;
        }
        CK_FMT(d, "round %d: blocks are at least 32 bytes apart", round); ck_true(d, distinct);
        for (int i = 0; i < 16; i++) fill(i, i + 1);
        int all = 1;
        for (int i = 0; i < 16; i++) all &= intact(i, i + 1);
        CK_FMT(d, "round %d: writing 32 bytes into each block corrupts no other block", round); ck_true(d, all);
        /* free a random half, check the others are untouched, then reallocate */
        int freed[16] = {0}, nf = 0;
        for (int i = 0; i < 16; i++) if (ck_rand() & 1) { pool_free(ptr[i]); freed[i] = 1; nf++; }
        all = 1;
        for (int i = 0; i < 16; i++) if (!freed[i]) all &= intact(i, i + 1);
        CK_FMT(d, "round %d: freeing blocks leaves the allocated ones intact", round); ck_true(d, all);
        int back = 1;
        for (int k = 0; k < nf; k++) {
            unsigned char *p = pool_alloc();
            int found = 0;
            for (int i = 0; i < 16; i++) if (freed[i] && p == ptr[i]) { freed[i] = 0; found = 1; }
            back &= found;
        }
        CK_FMT(d, "round %d: allocating %d times again returns exactly the freed blocks", round, nf); ck_true(d, back);
        CK_FMT(d, "round %d: then the pool is empty", round); ck_true(d, pool_alloc() == NULL);
    }
    return ck_done();
}
""",
"Make each block a union of 'pointer to next block' and 32 bytes. pool_init links all blocks into a list; alloc pops the head; free pushes the block back on the head."))

add(P("gray_code", S, "Gray code (async FIFO pointers)", "c", "func",
r"""<p><b>What to write.</b> Two conversions between ordinary binary numbers and Gray code:</p>
<pre>uint32_t bin_to_gray(uint32_t b);    // 5 (101) -&gt; 7 (111)
uint32_t gray_to_bin(uint32_t g);    // 7 (111) -&gt; 5 (101)</pre>
<p><b>Why it matters.</b> In Gray code, two numbers that follow each other differ in <b>exactly one bit</b>.
An async FIFO (a buffer between two clock domains) sends its read and write pointers across the clock
boundary in Gray code. If the other side samples a pointer while it is changing, only one bit can be caught
"in the middle", so it reads either the old value or the new one, never a random mix.</p>
<h4>Table for 3 bits</h4>
<table>
<tr><th>Number</th><th>Binary</th><th>Gray</th><th>Gray as a number</th></tr>
<tr><td>0</td><td>000</td><td>000</td><td>0</td></tr>
<tr><td>1</td><td>001</td><td>001</td><td>1</td></tr>
<tr><td>2</td><td>010</td><td>011</td><td>3</td></tr>
<tr><td>3</td><td>011</td><td>010</td><td>2</td></tr>
<tr><td>4</td><td>100</td><td>110</td><td>6</td></tr>
<tr><td>5</td><td>101</td><td>111</td><td>7</td></tr>
<tr><td>6</td><td>110</td><td>101</td><td>5</td></tr>
<tr><td>7</td><td>111</td><td>100</td><td>4</td></tr>
</table>
<p>Look down the Gray column: each row differs from the one above it in one bit only.</p>
<h4>Binary to Gray</h4>
<p>Each Gray bit is the XOR of the binary bit at the same place and the binary bit just above it (the top
bit has nothing above, so it is copied). In other words: XOR the number with itself shifted right by one.</p>
<pre>binary b      = 1 0 1 1 0 0    (0x2C = 44)
b shifted &gt;&gt;1 = 0 1 0 1 1 0
XOR           = 1 1 1 0 1 0    (0x3A = 58)  = bin_to_gray(44)</pre>
<h4>Gray to binary</h4>
<p>Go from the top bit down. Each binary bit is the XOR of <b>all</b> the Gray bits at or above its
position. Equivalently: binary bit = (binary bit above it) XOR (Gray bit here).</p>
<pre>Gray g = 1 1 1                      (7)
bit 2: b2 = g2           = 1
bit 1: b1 = b2 ^ g1 = 1^1 = 0
bit 0: b0 = b1 ^ g0 = 0^1 = 1       -&gt; binary 101 = 5</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Returns</th></tr>
<tr><td><code>bin_to_gray(5)</code></td><td>7</td></tr>
<tr><td><code>gray_to_bin(7)</code></td><td>5</td></tr>
<tr><td><code>bin_to_gray(0x2C)</code></td><td>0x3A</td></tr>
<tr><td><code>gray_to_bin(0x3A)</code></td><td>0x2C</td></tr>
<tr><td><code>gray_to_bin(0x80000000)</code></td><td>0xFFFFFFFF (the top 1 flows down into every bit)</td></tr>
</table>
<p>The tests use values of all sizes up to 32 bits, so <code>gray_to_bin</code> must handle all 32 bits.
They also check that <code>bin_to_gray(b)</code> and <code>bin_to_gray(b + 1)</code> differ in exactly one
bit.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li><code>bin_to_gray</code> is one expression with a shift and an XOR.</li>
<li>For <code>gray_to_bin</code>, a loop from bit 31 down to bit 0 works: keep a running XOR of the Gray bits
seen so far, and that running value is the binary bit at the current position.</li>
<li>Faster idea: XOR <code>g</code> with <code>g</code> shifted right by 1, 2, 3, ... (all positions). Can you
get the same with only five shifts, by 16, 8, 4, 2 and 1?</li>
</ol>
</details>""",
r"""#include <stdint.h>

uint32_t bin_to_gray(uint32_t b)
{
    return b;
}

uint32_t gray_to_bin(uint32_t g)
{
    return g;
}
""",
r"""#include <stdint.h>

uint32_t bin_to_gray(uint32_t b)
{
    return b ^ (b >> 1);
}

uint32_t gray_to_bin(uint32_t g)
{
    g ^= g >> 16;       /* prefix XOR from the top, in 5 steps */
    g ^= g >> 8;
    g ^= g >> 4;
    g ^= g >> 2;
    g ^= g >> 1;
    return g;
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t ref_g2b(uint32_t g) { uint32_t b = 0, bit = 0; for (int k = 31; k >= 0; k--) { bit ^= (g >> k) & 1u; b |= bit << k; } return b; }
int main(void)
{
    char d[96];
    ck_hex("bin_to_gray(5)", bin_to_gray(5), 7);
    ck_hex("gray_to_bin(7)", gray_to_bin(7), 5);
    int onebit = 1;
    for (uint32_t b = 0; b < 4096; b++) {
        uint32_t x = bin_to_gray(b) ^ bin_to_gray(b + 1);
        if (x == 0 || (x & (x - 1))) onebit = 0;
    }
    ck_true("bin_to_gray(b) and bin_to_gray(b + 1) differ in exactly one bit for b < 4096", onebit);
    for (int t = 0; t < 300; t++) {
        uint32_t b = ck_rand() >> ck_range(0, 31);
        CK_FMT(d, "bin_to_gray(0x%X)", (unsigned)b); ck_hex(d, bin_to_gray(b), b ^ (b >> 1));
        uint32_t g = ck_rand() >> ck_range(0, 31);
        CK_FMT(d, "gray_to_bin(0x%X)", (unsigned)g); ck_hex(d, gray_to_bin(g), ref_g2b(g));
    }
    return ck_done();
}
""",
"bin_to_gray: b ^ (b >> 1). gray_to_bin: start with b = g and repeatedly do b ^= b >> s for s = 1, 2, 4, 8, 16 (or loop: b ^= g >> k for every k)."))

# ---------------------------------------------------------------------------
S = "OS and architecture in C"

add(P("cache_bits", S, "Cache address split", "c", "func",
r"""<p><b>What to write.</b></p>
<pre>void cache_bits(int addr_bits, int cache_bytes, int line_bytes, int ways,
                int *tag, int *index, int *offset);</pre>
<p>Given the address width in bits and the cache shape, store in <code>*tag</code>, <code>*index</code> and
<code>*offset</code> how many address bits each of the three fields uses.</p>
<p><b>Why it matters.</b> "How many tag bits does this cache need?" is one of the most common computer
architecture questions in OA papers.</p>
<h4>How a cache cuts an address</h4>
<pre>  most significant bit                          least significant bit
 +-----------------------------+-----------------+-----------------+
 |             TAG             |      INDEX      |     OFFSET      |
 +-----------------------------+-----------------+-----------------+
  the rest of the bits          picks the set     picks the byte
  (stored to check for a hit)                     inside the line</pre>
<h4>The formulas</h4>
<ul>
<li>A <b>line</b> (block) is the unit the cache copies from memory. Number of lines =
<code>cache_bytes / line_bytes</code>.</li>
<li>Lines are grouped into <b>sets</b> of <code>ways</code> lines each. Number of sets =
lines / <code>ways</code>.</li>
<li>offset bits = log<sub>2</sub>(<code>line_bytes</code>)</li>
<li>index bits = log<sub>2</sub>(number of sets)</li>
<li>tag bits = <code>addr_bits</code> &minus; index bits &minus; offset bits</li>
</ul>
<p>All sizes are powers of two, so every log<sub>2</sub> is a whole number:</p>
<pre>value:  1  2  4  8  16  32  64  128  256  512  1024  2048  4096  ...  32768
log2:   0  1  2  3   4   5   6    7    8    9    10    11    12  ...     15</pre>
<p>Special cases: <code>ways</code> = 1 is a <b>direct-mapped</b> cache. <code>ways</code> = number of lines
is <b>fully associative</b>: there is only 1 set, so 0 index bits.</p>
<h4>Examples</h4>
<table>
<tr><th>Address</th><th>Cache</th><th>Line</th><th>Ways</th><th>Lines</th><th>Sets</th><th>tag</th><th>index</th><th>offset</th></tr>
<tr><td>32 bits</td><td>32 KB = 32768</td><td>32 B</td><td>2</td><td>1024</td><td>512</td><td>18</td><td>9</td><td>5</td></tr>
<tr><td>16 bits</td><td>256 B</td><td>4 B</td><td>1 (direct-mapped)</td><td>64</td><td>64</td><td>8</td><td>6</td><td>2</td></tr>
<tr><td>32 bits</td><td>1 KB = 1024</td><td>16 B</td><td>64 (fully assoc.)</td><td>64</td><td>1</td><td>28</td><td>0</td><td>4</td></tr>
<tr><td>40 bits</td><td>4 KB = 4096</td><td>64 B</td><td>4</td><td>64</td><td>16</td><td>30</td><td>4</td><td>6</td></tr>
</table>
<p>First row in detail: offset = log<sub>2</sub>(32) = 5; sets = 32768 / 32 / 2 = 512, so index =
log<sub>2</sub>(512) = 9; tag = 32 &minus; 9 &minus; 5 = 18.</p>
<p>The tests use addresses of up to 40 bits, caches up to 2<sup>19</sup> bytes, lines of 4 to 128 bytes, and
any number of ways from 1 up to "fully associative".</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a small helper that returns log<sub>2</sub> of a power of two: count how many times you can halve
the number before it reaches 1.</li>
<li>Compute the number of sets first, then the three answers in the order offset, index, tag.</li>
</ol>
</details>""",
r"""void cache_bits(int addr_bits, int cache_bytes, int line_bytes, int ways,
                int *tag, int *index, int *offset)
{
    *tag = *index = *offset = 0;
}
""",
r"""static int log2i(int x)
{
    int k = 0;
    while (x > 1) {
        x >>= 1;
        k++;
    }
    return k;
}

void cache_bits(int addr_bits, int cache_bytes, int line_bytes, int ways,
                int *tag, int *index, int *offset)
{
    int sets = cache_bytes / line_bytes / ways;
    *offset = log2i(line_bytes);
    *index = log2i(sets);
    *tag = addr_bits - *index - *offset;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[128];
    int t = -1, i = -1, o = -1;
    cache_bits(32, 32768, 32, 2, &t, &i, &o);
    ck_int("32-bit, 32 KB, 2-way, 32 B: tag", t, 18);
    ck_int("32-bit, 32 KB, 2-way, 32 B: index", i, 9);
    ck_int("32-bit, 32 KB, 2-way, 32 B: offset", o, 5);
    for (int c = 0; c < 200; c++) {
        int lb = ck_range(2, 7), cb = lb + ck_range(0, 12), wb = ck_range(0, cb - lb), ab = ck_range(cb + 1, 40);
        cache_bits(ab, 1 << cb, 1 << lb, 1 << wb, &t, &i, &o);
        CK_FMT(d, "%d-bit address, %d B cache, %d B lines, %d ways: offset", ab, 1 << cb, 1 << lb, 1 << wb); ck_int(d, o, lb);
        CK_FMT(d, "%d-bit address, %d B cache, %d B lines, %d ways: index", ab, 1 << cb, 1 << lb, 1 << wb); ck_int(d, i, cb - lb - wb);
        CK_FMT(d, "%d-bit address, %d B cache, %d B lines, %d ways: tag", ab, 1 << cb, 1 << lb, 1 << wb); ck_int(d, t, ab - cb + wb);
    }
    return ck_done();
}
""",
"offset = log2(line_bytes); index = log2(cache_bytes / line_bytes / ways); tag = addr_bits - index - offset."))

add(P("cache_sim", S, "Cache simulator (set-associative, LRU)", "c", "func",
r"""<p><b>What to write.</b> A cache simulator that counts hits:</p>
<pre>int cache_hits(const uint32_t *addr, int n,
               int sets, int ways, int line_bytes);</pre>
<p>The cache starts empty. Feed it the <code>n</code> byte addresses in <code>addr</code>, one after another,
and return how many of them were <b>hits</b> (the data was already in the cache).</p>
<p><b>Why it matters.</b> OA papers give a short address trace and ask for the hit count or hit rate. Doing it
by hand is slow; writing the simulator once makes the rules clear.</p>
<h4>Where an address goes</h4>
<ul>
<li>line number = <code>addr / line_bytes</code> (which memory line the byte belongs to)</li>
<li>set = line number % <code>sets</code> (which set of the cache the line must go into)</li>
<li>tag = line number / <code>sets</code> (stored with the line, to recognise it later)</li>
</ul>
<pre>cache with 4 sets and 2 ways (each set holds up to 2 lines):

          way 0          way 1
set 0  [ tag | data ]  [ tag | data ]
set 1  [ tag | data ]  [ tag | data ]
set 2  [ tag | data ]  [ tag | data ]
set 3  [ tag | data ]  [ tag | data ]</pre>
<h4>The rules for each access</h4>
<ol>
<li>Work out the set and the tag.</li>
<li><b>Hit</b>: a valid line in that set has the same tag. Count a hit, and mark that line as the
<b>most recently used</b>.</li>
<li><b>Miss</b>: put the line into the set. Use an empty way if there is one. If the set is full, replace
the <b>least recently used</b> line (LRU): the one whose last access is the oldest. The new line is now the
most recently used.</li>
</ol>
<h4>Example 1: 4 sets, 1 way (direct-mapped), 16-byte lines, addresses 0 4 64 0</h4>
<table>
<tr><th>Address</th><th>Line</th><th>Set</th><th>Tag</th><th>Result</th><th>Set 0 holds</th></tr>
<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>miss (empty)</td><td>tag 0</td></tr>
<tr><td>4</td><td>0</td><td>0</td><td>0</td><td><b>hit</b> (same line as address 0)</td><td>tag 0</td></tr>
<tr><td>64</td><td>4</td><td>0</td><td>1</td><td>miss, replaces tag 0</td><td>tag 1</td></tr>
<tr><td>0</td><td>0</td><td>0</td><td>0</td><td>miss, replaces tag 1</td><td>tag 0</td></tr>
</table>
<p>Returns 1.</p>
<h4>Example 2: the same trace with 2 ways</h4>
<table>
<tr><th>Address</th><th>Set</th><th>Tag</th><th>Result</th><th>Set 0 holds (oldest use first)</th></tr>
<tr><td>0</td><td>0</td><td>0</td><td>miss</td><td>tag 0</td></tr>
<tr><td>4</td><td>0</td><td>0</td><td><b>hit</b></td><td>tag 0</td></tr>
<tr><td>64</td><td>0</td><td>1</td><td>miss, uses the empty way</td><td>tag 0, tag 1</td></tr>
<tr><td>0</td><td>0</td><td>0</td><td><b>hit</b></td><td>tag 1, tag 0</td></tr>
</table>
<p>Returns 2. The second way stops addresses 0 and 64 from throwing each other out.</p>
<h4>Example 3: LRU in action. 1 set, 2 ways, 16-byte lines, addresses 0 16 0 32 16</h4>
<table>
<tr><th>Address</th><th>Tag</th><th>Result</th><th>Set holds (oldest use first)</th></tr>
<tr><td>0</td><td>0</td><td>miss</td><td>0</td></tr>
<tr><td>16</td><td>1</td><td>miss</td><td>0, 1</td></tr>
<tr><td>0</td><td>0</td><td><b>hit</b>: tag 0 becomes the newest</td><td>1, 0</td></tr>
<tr><td>32</td><td>2</td><td>miss: evict tag 1 (the oldest use)</td><td>0, 2</td></tr>
<tr><td>16</td><td>1</td><td>miss: evict tag 0</td><td>2, 1</td></tr>
</table>
<p>Returns 1. If a hit did not update the "last used" time, address 32 would have evicted tag 0 instead.</p>
<h4>Inputs and limits</h4>
<ul>
<li><code>sets</code> &le; 1024, <code>ways</code> &le; 16, <code>sets</code> &times; <code>ways</code> &le;
4096. All are powers of two, as is <code>line_bytes</code>.</li>
<li>Addresses use all 32 bits (some are above 2<sup>31</sup>), so do the divisions with unsigned
numbers.</li>
<li>The tests call your function many times, with traces of 20,000 addresses. Every call must start with an
<b>empty</b> cache.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep, for every way of every set, three things: is it valid, its tag, and the time it was last used.
The access number <code>i</code> works as the time.</li>
<li>For each access, look only at the <code>ways</code> entries of its set. Search for the tag; if it is not
there, choose the victim: an invalid way first, otherwise the smallest "last used" time.</li>
<li>A static array of 4096 entries is big enough; clear the valid flags at the start of each call.</li>
</ol>
</details>""",
r"""#include <stdint.h>

int cache_hits(const uint32_t *addr, int n, int sets, int ways, int line_bytes)
{
    return 0;
}
""",
r"""#include <stdint.h>

static uint32_t tags[4096];
static int valid[4096];
static long last_use[4096];

int cache_hits(const uint32_t *addr, int n, int sets, int ways, int line_bytes)
{
    for (int i = 0; i < sets * ways; i++)
        valid[i] = 0;
    int hits = 0;
    for (int i = 0; i < n; i++) {
        uint32_t line = addr[i] / (uint32_t)line_bytes;
        int set = (int)(line % (uint32_t)sets);
        uint32_t tag = line / (uint32_t)sets;
        int base = set * ways, victim = base, hit = 0;
        for (int w = base; w < base + ways; w++) {
            if (valid[w] && tags[w] == tag) {
                hit = 1;
                victim = w;
                break;
            }
            if (!valid[w] || (valid[victim] && last_use[w] < last_use[victim]))
                victim = w;     /* an empty way, else the oldest one */
        }
        hits += hit;
        tags[victim] = tag;
        valid[victim] = 1;
        last_use[victim] = i;
    }
    return hits;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const uint32_t *a, int n, int sets, int ways, int lb)
{
    static uint32_t tg[4096]; static int stamp[4096];   /* stamp 0 = empty */
    memset(stamp, 0, sizeof stamp);
    int hits = 0;
    for (int i = 0; i < n; i++) {
        uint32_t line = a[i] / (uint32_t)lb, tag = line / (uint32_t)sets;
        int *st = stamp + (line % (uint32_t)sets) * ways; uint32_t *t = tg + (line % (uint32_t)sets) * ways;
        int w, best = 0;
        for (w = 0; w < ways; w++) if (st[w] && t[w] == tag) break;
        if (w < ways) hits++;
        else { for (int k = 1; k < ways; k++) if (st[k] < st[best]) best = k; w = best; t[w] = tag; }
        st[w] = i + 1;
    }
    return hits;
}
static uint32_t A[20000];
int main(void)
{
    char d[128];
    uint32_t ex[] = {0, 4, 64, 0};
    ck_int("example: 4 sets, 1 way", cache_hits(ex, 4, 4, 1, 16), 1);
    ck_int("example: 4 sets, 2 ways", cache_hits(ex, 4, 4, 2, 16), 2);
    for (int t = 0; t < 60; t++) {
        int sets = 1 << ck_range(0, 8), ways = 1 << ck_range(0, 4), lb = 1 << ck_range(2, 6), n = 20000;
        int pat = t % 3;
        uint32_t span = (uint32_t)(sets * ways * lb) * (uint32_t)ck_range(1, 3);
        for (int i = 0; i < n; i++) {
            if (pat == 0) A[i] = (uint32_t)(i * ck_range(1, 3) * 4) % span;              /* strided sweeps */
            else if (pat == 1) A[i] = ck_rand() % span;                                  /* random in a working set */
            else A[i] = (i & 1) ? ck_rand() : (uint32_t)(i * 4) % (span / 2 + 4);         /* mixed */
        }
        CK_FMT(d, "trace %d: %d sets, %d ways, %d B lines, %d accesses", t, sets, ways, lb, n);
        ck_int(d, cache_hits(A, n, sets, ways, lb), ref(A, n, sets, ways, lb));
    }
    return ck_done();
}
""",
"Keep per-way arrays: tag, valid, and the time of last use (the access index). For each access, search the set for the tag; on a miss pick an empty way or the one with the smallest last-use time. Remember to reset valid[] at the start of every call."))

add(P("vm_translate", S, "Two-level page table", "c", "func",
r"""<p><b>What to write.</b> <code>int64_t vm_translate(uint32_t *const *dir, uint32_t va);</code> It
translates the virtual address <code>va</code> into a physical address by walking a two-level page table.
Return the physical address, or &minus;1 for a page fault.</p>
<p><b>Why it matters.</b> This is exactly what the MMU (memory management unit) of a 32-bit processor does
on every memory access. Interviews ask "how is a virtual address split?" and "what happens on a page
fault?".</p>
<h4>How the 32-bit virtual address is split (4 KB pages)</h4>
<pre>bit:  31             22 21             12 11                     0
     +-----------------+-----------------+------------------------+
     |  directory idx  |   table index   |         offset         |
     |    (10 bits)    |    (10 bits)    |  (12 bits, 4096 bytes) |
     +-----------------+-----------------+------------------------+</pre>
<ul>
<li>directory index = <code>va &gt;&gt; 22</code> (0 to 1023)</li>
<li>table index = <code>(va &gt;&gt; 12) &amp; 0x3FF</code> (0 to 1023)</li>
<li>offset = <code>va &amp; 0xFFF</code> (0 to 4095)</li>
</ul>
<h4>The two levels</h4>
<pre>dir (1024 pointers)          page table (1024 uint32_t entries)
+---------+
| [0]     | --&gt; NULL          +----------------------------------+
| [1]     | ----------------&gt; | [0] ...                          |
|  ...    |                   | [3] 0x12345001                   |
+---------+                   |      frame 0x12345, present = 1  |
                              +----------------------------------+</pre>
<ul>
<li><code>dir</code> has 1024 entries. <code>dir[i] == NULL</code> means that page table is not present.</li>
<li>A page-table entry is a <code>uint32_t</code>:
<pre>bit:   31                        12 11          1   0
      +----------------------------+-------------+---+
      |    physical frame number   |  other flags| P |
      +----------------------------+-------------+---+
       P = bit 0 = present.  The flag bits 11..1 do not matter here.</pre></li>
<li>Physical address = (frame number &lt;&lt; 12) | offset. Since the frame number already sits in bits
31..12 of the entry, this is the same as <code>(entry &amp; 0xFFFFF000) | offset</code>.</li>
</ul>
<h4>The steps</h4>
<ol>
<li>Split <code>va</code> into the three fields.</li>
<li>If <code>dir[directory index]</code> is <code>NULL</code>: page fault, return &minus;1.</li>
<li>Read the entry at <code>table index</code> in that table. If its present bit is 0: page fault, return
&minus;1.</li>
<li>Otherwise return the physical address.</li>
</ol>
<h4>Examples</h4>
<table>
<tr><th>va</th><th>dir idx</th><th>table idx</th><th>offset</th><th>Entry</th><th>Returns</th></tr>
<tr><td>0x00403ABC</td><td>1</td><td>3</td><td>0xABC</td><td>0x12345001</td><td>0x12345ABC</td></tr>
<tr><td>0x00403ABC</td><td>1</td><td>3</td><td>0xABC</td><td>0x12345000 (present bit 0)</td><td>&minus;1</td></tr>
<tr><td>0x00003ABC</td><td>0</td><td>3</td><td>0xABC</td><td>(<code>dir[0]</code> is NULL)</td><td>&minus;1</td></tr>
<tr><td>0xC0801234</td><td>770</td><td>1</td><td>0x234</td><td>0x0ABCD003 (flag bit 1 also set)</td><td>0x0ABCD234</td></tr>
</table>
<p>Check the first row: 0x00403ABC = 0000 0000 01 | 00 0000 0011 | 1010 1011 1100 in binary, so the
directory index is 1, the table index is 3 and the offset is 0xABC.</p>
<div class="note">The return type is <code>int64_t</code> so that a physical address of 0x80000000 or more
stays positive and can never be confused with &minus;1. Build the address as an unsigned 32-bit value,
then convert it to <code>int64_t</code>.</div>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Each field is a shift followed by a mask. Check your three values against the first example.</li>
<li>There are exactly two ways to fault. Test for them in the order the hardware meets them.</li>
</ol>
</details>""",
r"""#include <stdint.h>
#include <stddef.h>

int64_t vm_translate(uint32_t *const *dir, uint32_t va)
{
    return -1;
}
""",
r"""#include <stdint.h>
#include <stddef.h>

int64_t vm_translate(uint32_t *const *dir, uint32_t va)
{
    uint32_t di = va >> 22, ti = (va >> 12) & 0x3FF, off = va & 0xFFF;
    const uint32_t *table = dir[di];
    if (table == NULL)
        return -1;
    uint32_t pte = table[ti];
    if (!(pte & 1))
        return -1;
    return (int64_t)((pte & 0xFFFFF000u) | off);
}
""",
r"""#include "check.h"
#include "solution.c"
static uint32_t tables[8][1024];
static uint32_t *dir[1024];
int main(void)
{
    char d[96];
    memset(dir, 0, sizeof dir);
    dir[1] = tables[0];
    tables[0][3] = 0x12345001u;
    ck_hex("example: va 0x00403ABC", (unsigned long long)vm_translate(dir, 0x00403ABCu), 0x12345ABCu);
    ck_int("va 0x00003ABC (no table)", vm_translate(dir, 0x00003ABCu), -1);
    tables[0][3] = 0x12345000u;
    ck_int("va 0x00403ABC with the present bit clear", vm_translate(dir, 0x00403ABCu), -1);
    for (int r = 0; r < 5; r++) {
        memset(dir, 0, sizeof dir);
        for (int k = 0; k < 8; k++) {
            dir[ck_range(0, 1023)] = tables[k];
            for (int e = 0; e < 1024; e++) tables[k][e] = ck_rand() & (ck_range(0, 3) ? 0xFFFFF001u : 0xFFFFF000u);
        }
        int used[8], nu = 0;
        for (int i = 0; i < 1024; i++) if (dir[i]) used[nu++] = i;
        for (int t = 0; t < 200; t++) {
            uint32_t va = (t & 1) ? ck_rand() : ((uint32_t)used[ck_range(0, nu - 1)] << 22 | (ck_rand() & 0x3FFFFF));
            const uint32_t *tb = dir[va >> 22];
            int64_t want = -1;
            if (tb && (tb[(va >> 12) & 0x3FF] & 1)) want = (int64_t)((tb[(va >> 12) & 0x3FF] & 0xFFFFF000u) | (va & 0xFFF));
            CK_FMT(d, "va 0x%08X", (unsigned)va); ck_int(d, vm_translate(dir, va), want);
        }
    }
    return ck_done();
}
""",
"di = va >> 22; ti = (va >> 12) & 0x3FF; off = va & 0xFFF. Check dir[di] != NULL, then the present bit of dir[di][ti], then combine (pte & 0xFFFFF000) | off."))

add(P("page_fifo_lru", S, "Page replacement: FIFO and LRU", "c", "func",
r"""<p><b>What to write.</b> Two functions that count <b>page faults</b> for a reference string (the list of
pages a program touches, in order):</p>
<pre>int faults_fifo(const int *refs, int n, int frames);
     // victim = the page that was loaded earliest
int faults_lru(const int *refs, int n, int frames);
     // victim = the page that was used longest ago</pre>
<p><b>Why it matters.</b> Page replacement tables are a standard OS question in OA papers: "how many page
faults with 3 frames under FIFO / LRU?".</p>
<h4>The setting</h4>
<ul>
<li>Memory has <code>frames</code> physical frames (1 to 16). Each frame holds one page. All frames start
empty.</li>
<li>For each page in <code>refs</code>: if it is already in a frame, it is a <b>hit</b>. Otherwise it is a
<b>fault</b>: the page is loaded into an empty frame, or, if all frames are full, it replaces a
<em>victim</em> page.</li>
</ul>
<h4>How the victim is chosen</h4>
<table>
<tr><th>Policy</th><th>Victim</th><th>What a hit does</th></tr>
<tr><td>FIFO (first in, first out)</td><td>the page that was <b>loaded</b> earliest</td><td>nothing</td></tr>
<tr><td>LRU (least recently used)</td><td>the page whose <b>last use</b> is the oldest</td><td>makes that page the most recently used</td></tr>
</table>
<h4>FIFO on 7 0 1 2 0 3 0 4 2 3 0 3 2 with 3 frames: 10 faults</h4>
<table>
<tr><th>Step</th><th>Page</th><th>Frame 0</th><th>Frame 1</th><th>Frame 2</th><th>Result</th></tr>
<tr><td>1</td><td>7</td><td>7</td><td>&ndash;</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>2</td><td>0</td><td>7</td><td>0</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>3</td><td>1</td><td>7</td><td>0</td><td>1</td><td><b>fault</b></td></tr>
<tr><td>4</td><td>2</td><td>2</td><td>0</td><td>1</td><td><b>fault</b>, evict 7</td></tr>
<tr><td>5</td><td>0</td><td>2</td><td>0</td><td>1</td><td>hit</td></tr>
<tr><td>6</td><td>3</td><td>2</td><td>3</td><td>1</td><td><b>fault</b>, evict 0</td></tr>
<tr><td>7</td><td>0</td><td>2</td><td>3</td><td>0</td><td><b>fault</b>, evict 1</td></tr>
<tr><td>8</td><td>4</td><td>4</td><td>3</td><td>0</td><td><b>fault</b>, evict 2</td></tr>
<tr><td>9</td><td>2</td><td>4</td><td>2</td><td>0</td><td><b>fault</b>, evict 3</td></tr>
<tr><td>10</td><td>3</td><td>4</td><td>2</td><td>3</td><td><b>fault</b>, evict 0</td></tr>
<tr><td>11</td><td>0</td><td>0</td><td>2</td><td>3</td><td><b>fault</b>, evict 4</td></tr>
<tr><td>12</td><td>3</td><td>0</td><td>2</td><td>3</td><td>hit</td></tr>
<tr><td>13</td><td>2</td><td>0</td><td>2</td><td>3</td><td>hit</td></tr>
</table>
<h4>LRU on the same string: 9 faults</h4>
<table>
<tr><th>Step</th><th>Page</th><th>Frame 0</th><th>Frame 1</th><th>Frame 2</th><th>Result</th></tr>
<tr><td>1</td><td>7</td><td>7</td><td>&ndash;</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>2</td><td>0</td><td>7</td><td>0</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>3</td><td>1</td><td>7</td><td>0</td><td>1</td><td><b>fault</b></td></tr>
<tr><td>4</td><td>2</td><td>2</td><td>0</td><td>1</td><td><b>fault</b>, evict 7</td></tr>
<tr><td>5</td><td>0</td><td>2</td><td>0</td><td>1</td><td>hit</td></tr>
<tr><td>6</td><td>3</td><td>2</td><td>0</td><td>3</td><td><b>fault</b>, evict 1</td></tr>
<tr><td>7</td><td>0</td><td>2</td><td>0</td><td>3</td><td>hit</td></tr>
<tr><td>8</td><td>4</td><td>4</td><td>0</td><td>3</td><td><b>fault</b>, evict 2</td></tr>
<tr><td>9</td><td>2</td><td>4</td><td>0</td><td>2</td><td><b>fault</b>, evict 3</td></tr>
<tr><td>10</td><td>3</td><td>4</td><td>3</td><td>2</td><td><b>fault</b>, evict 0</td></tr>
<tr><td>11</td><td>0</td><td>0</td><td>3</td><td>2</td><td><b>fault</b>, evict 4</td></tr>
<tr><td>12</td><td>3</td><td>0</td><td>3</td><td>2</td><td>hit</td></tr>
<tr><td>13</td><td>2</td><td>0</td><td>3</td><td>2</td><td>hit</td></tr>
</table>
<p>Compare step 6: FIFO throws out page 0 (loaded at step 2), although it was just used at step 5. LRU
remembers that use and throws out page 1 instead.</p>
<h4>More examples</h4>
<table>
<tr><th>Reference string</th><th>Frames</th><th>FIFO</th><th>LRU</th></tr>
<tr><td>7 0 1 2 0 3 0 4 2 3 0 3 2</td><td>3</td><td>10</td><td>9</td></tr>
<tr><td>1 2 3 4 1 2 5 1 2 3 4 5</td><td>3</td><td>9</td><td>10</td></tr>
<tr><td>1 2 3 4 1 2 5 1 2 3 4 5</td><td>4</td><td>10</td><td>8</td></tr>
<tr><td>1 1 2 1</td><td>1</td><td>3</td><td>3</td></tr>
</table>
<p>Rows 2 and 3 show <b>Belady's anomaly</b>: with FIFO, more frames gave <em>more</em> faults (9 &rarr;
10). LRU never does that.</p>
<p>The tests use strings of up to 300 references with page numbers 0 to 24.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep an array of the pages in the frames, and next to each one a "time" (the step number).</li>
<li>For FIFO the time is when the page was loaded; for LRU it is when the page was last used, so a hit
updates it.</li>
<li>On a fault with all frames full, the victim is the frame with the smallest time.</li>
</ol>
</details>""",
r"""int faults_fifo(const int *refs, int n, int frames)
{
    return 0;
}

int faults_lru(const int *refs, int n, int frames)
{
    return 0;
}
""",
r"""int faults_fifo(const int *refs, int n, int frames)
{
    int frame[16], used = 0, next = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int hit = 0;
        for (int f = 0; f < used; f++)
            if (frame[f] == refs[i])
                hit = 1;
        if (hit)
            continue;
        faults++;
        if (used < frames) {
            frame[used++] = refs[i];
        } else {
            frame[next] = refs[i];          /* frames fill in order, so a round-robin pointer is FIFO */
            next = (next + 1) % frames;
        }
    }
    return faults;
}

int faults_lru(const int *refs, int n, int frames)
{
    int frame[16], last[16], used = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int f = 0;
        while (f < used && frame[f] != refs[i])
            f++;
        if (f == used) {
            faults++;
            if (used < frames) {
                used++;
            } else {
                f = 0;
                for (int k = 1; k < used; k++)
                    if (last[k] < last[f])
                        f = k;
            }
            frame[f] = refs[i];
        }
        last[f] = i;
    }
    return faults;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const int *r, int n, int fr, int lru)
{
    int pg[16], t[16], used = 0, faults = 0;      /* t = load time (FIFO) or last use (LRU) */
    for (int i = 0; i < n; i++) {
        int f;
        for (f = 0; f < used; f++) if (pg[f] == r[i]) break;
        if (f < used) { if (lru) t[f] = i; continue; }
        faults++;
        if (used < fr) f = used++;
        else { f = 0; for (int k = 1; k < used; k++) if (t[k] < t[f]) f = k; }
        pg[f] = r[i]; t[f] = i;
    }
    return faults;
}
int main(void)
{
    char d[96];
    int s1[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2}, s2[] = {1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5};
    ck_int("FIFO, textbook string, 3 frames", faults_fifo(s1, 13, 3), 10);
    ck_int("LRU, textbook string, 3 frames", faults_lru(s1, 13, 3), 9);
    ck_int("FIFO, Belady string, 3 frames", faults_fifo(s2, 12, 3), 9);
    ck_int("FIFO, Belady string, 4 frames", faults_fifo(s2, 12, 4), 10);
    int r[300];
    for (int t = 0; t < 150; t++) {
        int n = ck_range(1, 300), fr = ck_range(1, 16), pages = ck_range(1, 25);
        for (int i = 0; i < n; i++) r[i] = ck_range(0, pages - 1);
        CK_FMT(d, "FIFO, random string %d (%d refs, %d frames)", t, n, fr); ck_int(d, faults_fifo(r, n, fr), ref(r, n, fr, 0));
        CK_FMT(d, "LRU, random string %d (%d refs, %d frames)", t, n, fr); ck_int(d, faults_lru(r, n, fr), ref(r, n, fr, 1));
    }
    return ck_done();
}
""",
"Keep an array of the pages in memory plus a time per frame: the time it was loaded (FIFO) or last used (LRU). On a fault with all frames full, replace the frame with the smallest time."))

add(P("page_opt", S, "Optimal page replacement", "c", "func",
r"""<p><b>What to write.</b> <code>int faults_opt(const int *refs, int n, int frames);</code> It counts the page
faults of the <b>optimal</b> replacement policy (also called OPT or Belady's MIN). <code>frames</code> is 1
to 16, and all frames start empty.</p>
<p><b>Why it matters.</b> No real OS can use this policy, because it needs to know the future. But it gives
the smallest possible number of faults, so OA questions use it as the yardstick for FIFO and LRU.</p>
<h4>The rule</h4>
<ul>
<li>A page already in memory is a hit. A missing page is a fault.</li>
<li>On a fault with a free frame, load the page there.</li>
<li>On a fault with all frames full, look <b>ahead</b> in <code>refs</code>. Evict the page whose next use is
<b>farthest in the future</b>. A page that is never used again is the best victim of all.</li>
</ul>
<p>If several pages are never used again, it does not matter which one you evict: none of them will be
asked for again, so the fault count is the same.</p>
<h4>Example: 7 0 1 2 0 3 0 4 2 3 0 3 2 with 3 frames: 7 faults</h4>
<table>
<tr><th>Step</th><th>Page</th><th>Frame 0</th><th>Frame 1</th><th>Frame 2</th><th>Result</th></tr>
<tr><td>1</td><td>7</td><td>7</td><td>&ndash;</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>2</td><td>0</td><td>7</td><td>0</td><td>&ndash;</td><td><b>fault</b></td></tr>
<tr><td>3</td><td>1</td><td>7</td><td>0</td><td>1</td><td><b>fault</b></td></tr>
<tr><td>4</td><td>2</td><td>2</td><td>0</td><td>1</td><td><b>fault</b>, evict 7<br><small>next use of 7: never; 0: step 5; 1: never</small></td></tr>
<tr><td>5</td><td>0</td><td>2</td><td>0</td><td>1</td><td>hit</td></tr>
<tr><td>6</td><td>3</td><td>2</td><td>0</td><td>3</td><td><b>fault</b>, evict 1<br><small>next use of 2: step 9; 0: step 7; 1: never</small></td></tr>
<tr><td>7</td><td>0</td><td>2</td><td>0</td><td>3</td><td>hit</td></tr>
<tr><td>8</td><td>4</td><td>2</td><td>4</td><td>3</td><td><b>fault</b>, evict 0<br><small>next use of 2: step 9; 0: step 11; 3: step 10</small></td></tr>
<tr><td>9</td><td>2</td><td>2</td><td>4</td><td>3</td><td>hit</td></tr>
<tr><td>10</td><td>3</td><td>2</td><td>4</td><td>3</td><td>hit</td></tr>
<tr><td>11</td><td>0</td><td>2</td><td>0</td><td>3</td><td><b>fault</b>, evict 4<br><small>next use of 2: step 13; 4: never; 3: step 12</small></td></tr>
<tr><td>12</td><td>3</td><td>2</td><td>0</td><td>3</td><td>hit</td></tr>
<tr><td>13</td><td>2</td><td>2</td><td>0</td><td>3</td><td>hit</td></tr>
</table>
<p>At step 8 (page 4), the pages in memory are 2, 0 and 3. Their next uses are at steps 9, 11 and 10.
Page 0 is needed last, so it is evicted.</p>
<p>For the same string, FIFO gives 10 faults and LRU gives 9, so OPT really is the best.</p>
<p>The tests use strings of up to 400 references with page numbers 0 to 24.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a helper: "starting after position <i>i</i>, where is page <i>p</i> used next?" Return
<code>n</code> if it is never used again, so that "never" counts as the farthest.</li>
<li>On a fault with full frames, call the helper for every page in memory and evict the one with the largest
answer.</li>
</ol>
</details>""",
r"""int faults_opt(const int *refs, int n, int frames)
{
    return 0;
}
""",
r"""static int next_use(const int *refs, int n, int from, int page)
{
    for (int j = from; j < n; j++)
        if (refs[j] == page)
            return j;
    return n;                       /* never used again: the best victim */
}

int faults_opt(const int *refs, int n, int frames)
{
    int frame[16], used = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int f = 0;
        while (f < used && frame[f] != refs[i])
            f++;
        if (f < used)
            continue;
        faults++;
        if (used < frames) {
            frame[used++] = refs[i];
            continue;
        }
        int victim = 0, far = -1;
        for (int k = 0; k < used; k++) {
            int nu = next_use(refs, n, i + 1, frame[k]);
            if (nu > far) {
                far = nu;
                victim = k;
            }
        }
        frame[victim] = refs[i];
    }
    return faults;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(const int *r, int n, int fr)
{
    int pg[16], used = 0, faults = 0;
    for (int i = 0; i < n; i++) {
        int f;
        for (f = 0; f < used; f++) if (pg[f] == r[i]) break;
        if (f < used) continue;
        faults++;
        if (used < fr) { pg[used++] = r[i]; continue; }
        int best = 0, bd = -1;
        for (int k = 0; k < used; k++) { int j = i + 1; while (j < n && r[j] != pg[k]) j++; if (j > bd) { bd = j; best = k; } }
        pg[best] = r[i];
    }
    return faults;
}
int main(void)
{
    char d[96];
    int s1[] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2};
    ck_int("OPT, textbook string, 3 frames", faults_opt(s1, 13, 3), 7);
    int r[400];
    for (int t = 0; t < 150; t++) {
        int n = ck_range(1, 400), fr = ck_range(1, 16), pages = ck_range(1, 25);
        for (int i = 0; i < n; i++) r[i] = ck_range(0, pages - 1);
        CK_FMT(d, "OPT, random string %d (%d refs, %d frames)", t, n, fr); ck_int(d, faults_opt(r, n, fr), ref(r, n, fr));
    }
    return ck_done();
}
""",
"On a fault with all frames full, for each page in memory find the index of its next use after i (n if never). Evict the one with the largest index."))

add(P("sched_fcfs_sjf", S, "Scheduling: FCFS and SJF waiting time", "c", "func",
r"""<p><b>What to write.</b> Two CPU-scheduling simulators that return the <b>total waiting time</b>:</p>
<pre>int fcfs_wait(const int *arrival, const int *burst, int n);
     // first come, first served
int sjf_wait(const int *arrival, const int *burst, int n);
     // shortest job first</pre>
<p><b>Why it matters.</b> "Draw the Gantt chart and find the average waiting time" is a standard OS question.
These two functions are that calculation.</p>
<h4>The setting</h4>
<ul>
<li>Process <i>i</i> arrives at time <code>arrival[i]</code> and needs <code>burst[i]</code> units of CPU
time. Processes are numbered in order of arrival (<code>arrival</code> never decreases).</li>
<li>Both policies are <b>non-preemptive</b>: once a process starts, it runs to the end without a break.</li>
<li>Waiting time of a process = the time it starts &minus; its arrival time. Return the <b>sum</b> over all
processes (the average is that sum divided by <code>n</code>).</li>
<li>If the CPU is free and no waiting process has arrived yet, time jumps forward to the next arrival (the
CPU is idle until then).</li>
</ul>
<h4>The two policies</h4>
<ul>
<li><b>FCFS</b>: run the processes in arrival order: 0, 1, 2, ...</li>
<li><b>SJF</b>: each time the CPU becomes free, choose, among the processes that have <b>already arrived</b>
and not yet run, the one with the <b>smallest burst</b>. Ties: earlier arrival first, then lower index.</li>
</ul>
<h4>Example 1: arrival 0 1 2 3, burst 8 4 9 5</h4>
<pre>FCFS
|       P0      |   P1  |        P2       |    P3   |
0               8       12                21        26

SJF   (at time 8, P1, P2 and P3 have all arrived: P1 has the
       shortest burst; then P3 (5) beats P2 (9))
|       P0      |   P1  |    P3   |        P2       |
0               8       12        17                26</pre>
<table>
<tr><th>Process</th><th>Arrival</th><th>Burst</th><th>FCFS start</th><th>FCFS wait</th><th>SJF start</th><th>SJF wait</th></tr>
<tr><td>P0</td><td>0</td><td>8</td><td>0</td><td>0</td><td>0</td><td>0</td></tr>
<tr><td>P1</td><td>1</td><td>4</td><td>8</td><td>7</td><td>8</td><td>7</td></tr>
<tr><td>P2</td><td>2</td><td>9</td><td>12</td><td>10</td><td>17</td><td>15</td></tr>
<tr><td>P3</td><td>3</td><td>5</td><td>21</td><td>18</td><td>12</td><td>9</td></tr>
<tr><td colspan="4"><b>Total</b> (average)</td><td><b>35</b> (8.75)</td><td></td><td><b>31</b> (7.75)</td></tr>
</table>
<p>Note that P0 runs first under SJF too: at time 0 it is the only process that has arrived. SJF does not
wait for shorter jobs that come later.</p>
<h4>Example 2: an idle gap and a tie. Arrival 0 5 5 5, burst 2 3 1 3</h4>
<pre>FCFS   total wait 0 + 0 + 3 + 4 = 7   (P0, P1, P2, P3)
|   P0  |    idle   |     P1    | P2|     P3    |
0       2           5           8   9           12

SJF    total wait 0 + 1 + 0 + 4 = 5   (P0, P1, P2, P3)
       At time 5, P2 goes first (burst 1). P1 and P3 both have burst 3
       and the same arrival, so the lower index, P1, goes next.
|   P0  |    idle   | P2|     P1    |     P3    |
0       2           5   6           9           12</pre>
<p>The tests use up to 200 processes, bursts of 1 to 10, and both small and large gaps between arrivals.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep a clock <code>t</code>. FCFS is one pass: before each process starts, if <code>t</code> is earlier
than its arrival, move <code>t</code> to the arrival.</li>
<li>For SJF, repeat <code>n</code> times: scan all processes that are not done and have arrival &le;
<code>t</code>, and keep the one with the smallest burst. Which comparison (&lt; or &le;) keeps the earlier
one on a tie?</li>
<li>If that scan finds nothing, move <code>t</code> to the earliest arrival among the processes not done,
and scan again.</li>
</ol>
</details>""",
r"""int fcfs_wait(const int *arrival, const int *burst, int n)
{
    return 0;
}

int sjf_wait(const int *arrival, const int *burst, int n)
{
    return 0;
}
""",
r"""int fcfs_wait(const int *arrival, const int *burst, int n)
{
    int t = 0, total = 0;
    for (int i = 0; i < n; i++) {
        if (t < arrival[i])
            t = arrival[i];             /* CPU idle until it arrives */
        total += t - arrival[i];
        t += burst[i];
    }
    return total;
}

int sjf_wait(const int *arrival, const int *burst, int n)
{
    int done[256] = {0};
    int t = 0, total = 0;
    for (int finished = 0; finished < n; finished++) {
        int pick = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && arrival[i] <= t && (pick < 0 || burst[i] < burst[pick]))
                pick = i;               /* strict < keeps the earlier arrival on ties */
        if (pick < 0) {                 /* nothing has arrived: jump ahead */
            for (int i = 0; i < n; i++)
                if (!done[i]) {
                    pick = i;
                    break;
                }
            t = arrival[pick];
            for (int i = pick + 1; i < n; i++)
                if (!done[i] && arrival[i] <= t && burst[i] < burst[pick])
                    pick = i;
        }
        total += t - arrival[pick];
        t += burst[pick];
        done[pick] = 1;
    }
    return total;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref_sjf(const int *a, const int *b, int n)
{
    int done[256] = {0}, t = 0, tot = 0;
    for (int k = 0; k < n; k++) {
        int p = -1;
        for (;;) {
            for (int i = 0; i < n; i++) if (!done[i] && a[i] <= t && (p < 0 || b[i] < b[p])) p = i;
            if (p >= 0) break;
            t++;
        }
        tot += t - a[p]; t += b[p]; done[p] = 1;
    }
    return tot;
}
static int ref_fcfs(const int *a, const int *b, int n)
{
    int t = 0, tot = 0;
    for (int i = 0; i < n; i++) { if (t < a[i]) t = a[i]; tot += t - a[i]; t += b[i]; }
    return tot;
}
int main(void)
{
    char d[96];
    int a0[] = {0, 1, 2, 3}, b0[] = {8, 4, 9, 5};
    ck_int("FCFS example", fcfs_wait(a0, b0, 4), 35);
    ck_int("SJF example", sjf_wait(a0, b0, 4), 31);
    int a[200], b[200];
    for (int t = 0; t < 200; t++) {
        int n = ck_range(1, 200), at = ck_range(0, 5);
        for (int i = 0; i < n; i++) { at += ck_range(0, t % 2 ? 12 : 3); a[i] = at; b[i] = ck_range(1, 10); }
        CK_FMT(d, "FCFS, random case %d (%d processes)", t, n); ck_int(d, fcfs_wait(a, b, n), ref_fcfs(a, b, n));
        CK_FMT(d, "SJF, random case %d (%d processes)", t, n); ck_int(d, sjf_wait(a, b, n), ref_sjf(a, b, n));
    }
    return ck_done();
}
""",
"FCFS: one pass, t = max(t, arrival[i]). SJF: n rounds; each round pick the unfinished process with arrival <= t and the smallest burst (strict < keeps the earliest on ties); if there is none, move t to the next unfinished arrival first. n is at most 200."))

add(P("sched_rr", S, "Scheduling: round robin", "c", "func",
r"""<p><b>What to write.</b> A round-robin CPU scheduler:</p>
<pre>void rr_finish(const int *arrival, const int *burst, int n,
               int quantum, int *finish);</pre>
<p>It writes the completion time of each process into <code>finish[i]</code>.</p>
<p><b>Why it matters.</b> Round robin is the time-sharing policy that OS questions ask about most ("draw the
Gantt chart for quantum 2").</p>
<h4>The setting</h4>
<ul>
<li>Process <i>i</i> arrives at <code>arrival[i]</code> and needs <code>burst[i]</code> &ge; 1 units of CPU.
Processes are numbered by arrival (<code>arrival</code> never decreases).</li>
<li>There is one FIFO <b>ready queue</b> (first in, first out).</li>
<li>The process at the front of the queue runs for at most <code>quantum</code> units (less if it needs less).</li>
</ul>
<h4>The rules, step by step</h4>
<ol>
<li>If the queue is empty, time jumps to the next arrival, and every process that has arrived by then joins
the queue (in index order).</li>
<li>Take the process at the front. Run it for min(remaining time, <code>quantum</code>). The clock moves
forward by that amount, to time <i>t</i>.</li>
<li><b>First</b> add every process with arrival &le; <i>t</i> that has not joined yet, in index order.</li>
<li><b>Then</b>, if the process that just ran still has work left, put it at the back of the queue.
Otherwise it is finished: <code>finish</code> = <i>t</i>.</li>
</ol>
<p>The order in steps 3 and 4 (new arrivals before the process that was just stopped) is the usual textbook
convention, and the tests check it.</p>
<h4>Example 1: arrival 0 0 0, burst 5 3 1, quantum 2 &rarr; finish 9 8 5</h4>
<pre>|   P0  |   P1  | P2|   P0  | P1| P0|
0       2       4   5       7   8   9</pre>
<table>
<tr><th>Slice</th><th>Runs</th><th>Time</th><th>Work left</th><th>Queue after the slice</th></tr>
<tr><td>1</td><td>P0</td><td>0&ndash;2</td><td>3</td><td>P1 P2 P0</td></tr>
<tr><td>2</td><td>P1</td><td>2&ndash;4</td><td>1</td><td>P2 P0 P1</td></tr>
<tr><td>3</td><td>P2</td><td>4&ndash;5</td><td>0: finish[2] = 5</td><td>P0 P1</td></tr>
<tr><td>4</td><td>P0</td><td>5&ndash;7</td><td>1</td><td>P1 P0</td></tr>
<tr><td>5</td><td>P1</td><td>7&ndash;8</td><td>0: finish[1] = 8</td><td>P0</td></tr>
<tr><td>6</td><td>P0</td><td>8&ndash;9</td><td>0: finish[0] = 9</td><td>(empty)</td></tr>
</table>
<h4>Example 2: new arrivals go in first. Arrival 0 1 2, burst 3 2 1, quantum 2 &rarr; finish 6 4 5</h4>
<pre>|   P0  |   P1  | P2| P0|
0       2       4   5   6</pre>
<p>At time 2, P0 stops with 1 unit left. P1 (arrived at 1) and P2 (arrived at 2) join the queue first, and
P0 goes behind them: the queue is P1 P2 P0.</p>
<h4>Example 3: an idle gap. Arrival 0 10, burst 1 2, quantum 2 &rarr; finish 1 12</h4>
<pre>|P0|           idle           |  P1 |
0  1                          10    12</pre>
<p>Useful formulas for OA questions: turnaround = finish &minus; arrival; waiting = turnaround &minus;
burst.</p>
<p>The tests use up to 200 processes, quantum 1 to 6, bursts 1 to 12.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>You need: a queue of process indices (a circular buffer of a little more than <code>n</code> entries is
enough, because each process is in it at most once), the remaining time of each process, the clock, and the
index of the next process that has not arrived yet.</li>
<li>Write the loop body exactly in the order of the four rules above. Stop when all <code>n</code> processes
are finished.</li>
<li>Check yourself with the slice table of example 1.</li>
</ol>
</details>""",
r"""void rr_finish(const int *arrival, const int *burst, int n, int quantum, int *finish)
{
}
""",
r"""void rr_finish(const int *arrival, const int *burst, int n, int quantum, int *finish)
{
    int rem[256], queue[257], head = 0, tail = 0, count = 0;
    int t = 0, next = 0, done = 0;
    for (int i = 0; i < n; i++)
        rem[i] = burst[i];
    while (done < n) {
        if (count == 0) {                           /* idle: jump to the next arrival */
            if (t < arrival[next])
                t = arrival[next];
            while (next < n && arrival[next] <= t) {
                queue[tail] = next++; tail = (tail + 1) % 257; count++;
            }
        }
        int p = queue[head]; head = (head + 1) % 257; count--;
        int run = rem[p] < quantum ? rem[p] : quantum;
        t += run;
        rem[p] -= run;
        while (next < n && arrival[next] <= t) {    /* new arrivals go in first */
            queue[tail] = next++; tail = (tail + 1) % 257; count++;
        }
        if (rem[p] > 0) {
            queue[tail] = p; tail = (tail + 1) % 257; count++;
        } else {
            finish[p] = t;
            done++;
        }
    }
}
""",
r"""#include "check.h"
#include "solution.c"
static void ref(const int *a, const int *b, int n, int q, int *f)
{
    int rem[256], qu[4096], h = 0, tl = 0, t = 0, nx = 0, done = 0;
    for (int i = 0; i < n; i++) rem[i] = b[i];
    while (done < n) {
        if (h == tl) { if (t < a[nx]) t = a[nx]; while (nx < n && a[nx] <= t) qu[tl++ % 4096] = nx++; }
        int p = qu[h++ % 4096], run = rem[p] < q ? rem[p] : q;
        t += run; rem[p] -= run;
        while (nx < n && a[nx] <= t) qu[tl++ % 4096] = nx++;
        if (rem[p]) qu[tl++ % 4096] = p; else { f[p] = t; done++; }
    }
}
int main(void)
{
    char d[96];
    int a0[] = {0, 0, 0}, b0[] = {5, 3, 1}, f[256] = {-1, -1, -1}, w[256];
    rr_finish(a0, b0, 3, 2, f);
    ck_int("example: finish[0]", f[0], 9);
    ck_int("example: finish[1]", f[1], 8);
    ck_int("example: finish[2]", f[2], 5);
    int a[200], b[200];
    for (int t = 0; t < 150; t++) {
        int n = ck_range(1, 200), q = ck_range(1, 6), at = 0;
        for (int i = 0; i < n; i++) { at += ck_range(0, t % 2 ? 9 : 2); a[i] = at; b[i] = ck_range(1, 12); }
        for (int i = 0; i < n; i++) f[i] = -1;
        rr_finish(a, b, n, q, f);
        ref(a, b, n, q, w);
        int k = 0;
        while (k < n && f[k] == w[k]) k++;
        CK_FMT(d, "random case %d (%d processes, quantum %d): finish[%d]", t, n, q, k < n ? k : 0);
        if (k < n) ck_int(d, f[k], w[k]); else ck_true(d, 1);
    }
    return ck_done();
}
""",
"Keep a circular queue of indices and a 'next arrival' index. Loop: if the queue is empty, move t to arrival[next] and enqueue arrivals; pop one, run min(remaining, quantum), enqueue new arrivals with arrival <= t, then re-enqueue the process if it still has work, else record finish = t."))

add(P("bankers", S, "Banker's algorithm (deadlock avoidance)", "c", "func",
r"""<p><b>What to write.</b> The safety check of the banker's algorithm:</p>
<pre>int bankers_safe(int n, int m, const int *avail, const int *max,
                 const int *alloc, int *order);</pre>
<p>Return 1 if the system is in a <b>safe state</b> and write the order in which the processes can finish
into <code>order[0..n-1]</code>. Return 0 if it is not safe.</p>
<p><b>Why it matters.</b> The banker's algorithm is the classic way to <em>avoid</em> deadlock: the OS only
grants a request if the system stays safe afterwards. OA papers give the tables and ask "is it safe, and in
which order?".</p>
<h4>The data</h4>
<ul>
<li><code>n</code> processes, <code>m</code> resource types (for example printers, tape drives,
buffers).</li>
<li><code>avail[j]</code>: free units of resource <i>j</i> right now.</li>
<li><code>max</code> and <code>alloc</code> are <code>n</code> &times; <code>m</code> tables stored
<b>row-major</b> in flat arrays: the entry for process <i>i</i>, resource <i>j</i> is at index
<code>i * m + j</code>. <code>max</code> = the most that process may ever ask for; <code>alloc</code> = what
it holds now.</li>
<li>need = max &minus; alloc: what it may still ask for.</li>
</ul>
<h4>The rule, step by step</h4>
<ol>
<li>Start with <b>work</b> = <code>avail</code> (a copy; do not change the inputs).</li>
<li>Scan the processes from index 0 upwards. Pick the <b>first</b> unfinished process whose need is &le;
work in <b>every</b> resource.</li>
<li>If there is none, the state is unsafe: return 0.</li>
<li>Otherwise that process can get everything it needs, finish, and give back what it holds:
work += its alloc. Mark it finished, append it to <code>order</code>, and go back to step 2 (scan from index
0 again).</li>
<li>When all <code>n</code> processes have finished, return 1.</li>
</ol>
<h4>Example (the textbook one): n = 5, m = 3, avail = 3 3 2</h4>
<table>
<tr><th>Process</th><th>alloc</th><th>max</th><th>need = max &minus; alloc</th></tr>
<tr><td>P0</td><td>0 1 0</td><td>7 5 3</td><td>7 4 3</td></tr>
<tr><td>P1</td><td>2 0 0</td><td>3 2 2</td><td>1 2 2</td></tr>
<tr><td>P2</td><td>3 0 2</td><td>9 0 2</td><td>6 0 0</td></tr>
<tr><td>P3</td><td>2 1 1</td><td>2 2 2</td><td>0 1 1</td></tr>
<tr><td>P4</td><td>0 0 2</td><td>4 3 3</td><td>4 3 1</td></tr>
</table>
<table>
<tr><th>Round</th><th>work before</th><th>Skipped (need too big)</th><th>Picked</th><th>work after (+ its alloc)</th></tr>
<tr><td>1</td><td>3 3 2</td><td>P0</td><td>P1 (need 1 2 2)</td><td>5 3 2</td></tr>
<tr><td>2</td><td>5 3 2</td><td>P0, P2</td><td>P3 (need 0 1 1)</td><td>7 4 3</td></tr>
<tr><td>3</td><td>7 4 3</td><td>&ndash;</td><td>P0 (need 7 4 3)</td><td>7 5 3</td></tr>
<tr><td>4</td><td>7 5 3</td><td>&ndash;</td><td>P2 (need 6 0 0)</td><td>10 5 5</td></tr>
<tr><td>5</td><td>10 5 5</td><td>&ndash;</td><td>P4 (need 4 3 1)</td><td>10 5 7</td></tr>
</table>
<p>Result: safe, returns 1, <code>order</code> = 1 3 0 2 4. Note round 2: P0 and P2 are checked again
(search restarts at 0) but still do not fit, so P3 is picked.</p>
<h4>Unsafe example</h4>
<p>n = 2, m = 1, avail = 1, alloc = 1 1, max = 3 3. Both processes need 2 more, but only 1 is free, so
nobody can finish: returns 0. (What you write into <code>order</code> for an unsafe state is not
checked.)</p>
<p>The tests use up to 40 processes and up to 6 resource types.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>You need a <code>work</code> array (size <code>m</code>) and a "finished" flag per process.</li>
<li>The outer loop runs at most <code>n</code> rounds, because each round finishes one process. Inside, scan
from index 0 and stop at the first process that fits.</li>
<li>"Fits" means: for every <i>j</i>, <code>max[i*m+j] &minus; alloc[i*m+j] &le; work[j]</code>. One
resource that does not fit is enough to skip the process.</li>
</ol>
</details>""",
r"""int bankers_safe(int n, int m, const int *avail, const int *max, const int *alloc, int *order)
{
    return 0;
}
""",
r"""int bankers_safe(int n, int m, const int *avail, const int *max, const int *alloc, int *order)
{
    int work[16], done[64] = {0};
    for (int j = 0; j < m; j++)
        work[j] = avail[j];
    for (int k = 0; k < n; k++) {
        int pick = -1;
        for (int i = 0; i < n && pick < 0; i++) {
            if (done[i])
                continue;
            int ok = 1;
            for (int j = 0; j < m; j++)
                if (max[i * m + j] - alloc[i * m + j] > work[j])
                    ok = 0;
            if (ok)
                pick = i;
        }
        if (pick < 0)
            return 0;                   /* nobody can finish: unsafe */
        for (int j = 0; j < m; j++)
            work[j] += alloc[pick * m + j];
        done[pick] = 1;
        order[k] = pick;
    }
    return 1;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int n, int m, const int *av, const int *mx, const int *al, int *ord)
{
    int w[16], dn[64] = {0};
    for (int j = 0; j < m; j++) w[j] = av[j];
    for (int k = 0; k < n; k++) {
        int i;
        for (i = 0; i < n; i++) {
            if (dn[i]) continue;
            int j; for (j = 0; j < m; j++) if (mx[i * m + j] - al[i * m + j] > w[j]) break;
            if (j == m) break;
        }
        if (i == n) return 0;
        for (int j = 0; j < m; j++) w[j] += al[i * m + j];
        dn[i] = 1; ord[k] = i;
    }
    return 1;
}
int main(void)
{
    char d[96];
    int av[] = {3, 3, 2}, al[] = {0, 1, 0, 2, 0, 0, 3, 0, 2, 2, 1, 1, 0, 0, 2}, mx[] = {7, 5, 3, 3, 2, 2, 9, 0, 2, 2, 2, 2, 4, 3, 3};
    int o[64] = {0}, wo[64] = {0};
    ck_int("textbook example: safe", bankers_safe(5, 3, av, mx, al, o), 1);
    int want[] = {1, 3, 0, 2, 4};
    for (int k = 0; k < 5; k++) { CK_FMT(d, "textbook example: order[%d]", k); ck_int(d, o[k], want[k]); }
    int A[16], MX[64 * 16], AL[64 * 16];
    for (int t = 0; t < 300; t++) {
        int n = ck_range(1, 40), m = ck_range(1, 6);
        for (int j = 0; j < m; j++) A[j] = ck_range(0, 4);
        for (int i = 0; i < n * m; i++) { AL[i] = ck_range(0, 3); MX[i] = AL[i] + ck_range(0, t % 2 ? 3 : 6); }
        for (int i = 0; i < n; i++) o[i] = -1;
        int sw = ref(n, m, A, MX, AL, wo), sg = bankers_safe(n, m, A, MX, AL, o);
        CK_FMT(d, "random case %d (%d processes, %d resources): safe?", t, n, m); ck_int(d, sg, sw);
        if (sw && sg) {
            int k = 0;
            while (k < n && o[k] == wo[k]) k++;
            CK_FMT(d, "random case %d: order[%d]", t, k < n ? k : 0);
            if (k < n) ck_int(d, o[k], wo[k]); else ck_true(d, 1);
        }
    }
    return ck_done();
}
""",
"Copy avail into work. n times: scan i from 0 for an unfinished process with max - alloc <= work in every column; if none, return 0; else add its alloc to work, mark it done, record it."))

add(P("mem_fit", S, "First fit, best fit, worst fit", "c", "func",
r"""<p><b>What to write.</b> The three classic memory allocation policies:</p>
<pre>void mem_fit(int *holes, int nh, const int *req, int nr,
             int policy, int *where);</pre>
<p>Free memory consists of <code>nh</code> <em>holes</em> (free blocks) of sizes
<code>holes[0..nh-1]</code>. The requests <code>req[0..nr-1]</code> arrive in order. Put each request into
one hole, which then gets smaller by that amount. Write the chosen hole index into <code>where[i]</code>.</p>
<p><b>Why it matters.</b> OA papers give exactly this table ("holes 100, 500, 200, 300, 600 KB; requests
212, 417, 112, 426 KB") and ask where each request goes under each policy.</p>
<h4>The policies</h4>
<p>A hole "fits" a request if its size is &ge; the request.</p>
<table>
<tr><th><code>policy</code></th><th>Name</th><th>Which hole</th></tr>
<tr><td>0</td><td>first fit</td><td>the first hole (lowest index) that fits</td></tr>
<tr><td>1</td><td>best fit</td><td>the <b>smallest</b> hole that fits (least space left over)</td></tr>
<tr><td>2</td><td>worst fit</td><td>the <b>largest</b> hole, if it fits (most space left over)</td></tr>
</table>
<ul>
<li>Ties (two holes of the same size) go to the <b>lower index</b>.</li>
<li>If no hole fits, <code>where[i] = &minus;1</code> (the request must wait) and nothing changes.</li>
<li>Update <code>holes</code> in place: subtract each request from its hole. The tests check the final
<code>holes</code> array too.</li>
</ul>
<h4>Example: holes 100 500 200 300 600, requests 212 417 112 426</h4>
<p><b>First fit</b> &rarr; <code>where</code> = 1 4 1 &minus;1</p>
<table>
<tr><th>Request</th><th>Chosen hole</th><th>Holes afterwards</th></tr>
<tr><td>(start)</td><td></td><td>100 500 200 300 600</td></tr>
<tr><td>212</td><td>hole 1</td><td>100 288 200 300 600</td></tr>
<tr><td>417</td><td>hole 4</td><td>100 288 200 300 183</td></tr>
<tr><td>112</td><td>hole 1</td><td>100 176 200 300 183</td></tr>
<tr><td>426</td><td>none fits: &minus;1</td><td>100 176 200 300 183</td></tr>
</table>
<p><b>Best fit</b> &rarr; <code>where</code> = 3 1 2 4</p>
<table>
<tr><th>Request</th><th>Chosen hole</th><th>Holes afterwards</th></tr>
<tr><td>(start)</td><td></td><td>100 500 200 300 600</td></tr>
<tr><td>212</td><td>hole 3</td><td>100 500 200 88 600</td></tr>
<tr><td>417</td><td>hole 1</td><td>100 83 200 88 600</td></tr>
<tr><td>112</td><td>hole 2</td><td>100 83 88 88 600</td></tr>
<tr><td>426</td><td>hole 4</td><td>100 83 88 88 174</td></tr>
</table>
<p><b>Worst fit</b> &rarr; <code>where</code> = 4 1 4 &minus;1</p>
<table>
<tr><th>Request</th><th>Chosen hole</th><th>Holes afterwards</th></tr>
<tr><td>(start)</td><td></td><td>100 500 200 300 600</td></tr>
<tr><td>212</td><td>hole 4</td><td>100 500 200 300 388</td></tr>
<tr><td>417</td><td>hole 1</td><td>100 83 200 300 388</td></tr>
<tr><td>112</td><td>hole 4</td><td>100 83 200 300 276</td></tr>
<tr><td>426</td><td>none fits: &minus;1</td><td>100 83 200 300 276</td></tr>
</table>
<p>Only best fit places all four requests here. Under first fit, the 426 request fails although the total
free memory is large: the free space is split into pieces that are all too small (this is called
<b>external fragmentation</b>).</p>
<h4>Tie example</h4>
<p>Holes 30 80 80, request 40: best fit and worst fit both choose hole 1, the first of the two equal
80s.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>For each request, scan all holes and ignore the ones that are too small.</li>
<li>First fit can stop at the first hole that fits. Best and worst fit must look at every hole and remember
the best one so far. Which comparison (&lt; or &le;) keeps the lower index on a tie?</li>
<li>After the scan, if a hole was chosen, subtract the request from it.</li>
</ol>
</details>""",
r"""void mem_fit(int *holes, int nh, const int *req, int nr, int policy, int *where)
{
    for (int i = 0; i < nr; i++)
        where[i] = -1;
}
""",
r"""void mem_fit(int *holes, int nh, const int *req, int nr, int policy, int *where)
{
    for (int i = 0; i < nr; i++) {
        int pick = -1;
        for (int h = 0; h < nh; h++) {
            if (holes[h] < req[i])
                continue;
            if (pick < 0 ||
                (policy == 1 && holes[h] < holes[pick]) ||
                (policy == 2 && holes[h] > holes[pick]))
                pick = h;
            if (policy == 0)
                break;              /* first fit stops at the first hole that fits */
        }
        where[i] = pick;
        if (pick >= 0)
            holes[pick] -= req[i];
    }
}
""",
r"""#include "check.h"
#include "solution.c"
static void ref(int *H, int nh, const int *r, int nr, int pol, int *w)
{
    for (int i = 0; i < nr; i++) {
        int p = -1;
        for (int h = 0; h < nh; h++) {
            if (H[h] < r[i]) continue;
            if (p < 0) { p = h; if (pol == 0) break; continue; }
            if ((pol == 1 && H[h] < H[p]) || (pol == 2 && H[h] > H[p])) p = h;
        }
        w[i] = p; if (p >= 0) H[p] -= r[i];
    }
}
int main(void)
{
    char d[96];
    static const char *pn[] = {"first fit", "best fit", "worst fit"};
    int want[3][4] = {{1, 4, 1, -1}, {3, 1, 2, 4}, {4, 1, 4, -1}}, rq[] = {212, 417, 112, 426};
    for (int pol = 0; pol < 3; pol++) {
        int h[] = {100, 500, 200, 300, 600}, w[4] = {-2, -2, -2, -2};
        mem_fit(h, 5, rq, 4, pol, w);
        for (int i = 0; i < 4; i++) { CK_FMT(d, "textbook example, %s: request %d", pn[pol], i); ck_int(d, w[i], want[pol][i]); }
    }
    int H1[40], H2[40], R[60], W1[60], W2[60];
    for (int t = 0; t < 300; t++) {
        int nh = ck_range(1, 40), nr = ck_range(1, 60), pol = t % 3;
        for (int i = 0; i < nh; i++) H1[i] = H2[i] = ck_range(1, 50) * 10;
        for (int i = 0; i < nr; i++) R[i] = ck_range(1, 30) * 10;
        for (int i = 0; i < nr; i++) W1[i] = -2;
        mem_fit(H1, nh, R, nr, pol, W1);
        ref(H2, nh, R, nr, pol, W2);
        int k = 0;
        while (k < nr && W1[k] == W2[k]) k++;
        CK_FMT(d, "random case %d, %s: request %d", t, pn[pol], k < nr ? k : 0);
        if (k < nr) ck_int(d, W1[k], W2[k]); else ck_true(d, 1);
        k = 0;
        while (k < nh && H1[k] == H2[k]) k++;
        CK_FMT(d, "random case %d, %s: holes[%d] afterwards", t, pn[pol], k < nh ? k : 0);
        if (k < nh) ck_int(d, H1[k], H2[k]); else ck_true(d, 1);
    }
    return ck_done();
}
""",
"For each request, scan the holes that are big enough: first fit takes the first; best fit keeps the smallest (strict <); worst fit keeps the largest (strict >). Then subtract the request from the chosen hole."))

# ---------------------------------------------------------------------------
S = "Sorting"

add(P("bubble_sort", S, "Bubble sort (count the swaps)", "c", "func",
r"""<p><b>What to write.</b> <code>long bubble_sort(int *a, int n)</code>. Sort the array in ascending order
with bubble sort and return the number of <b>swaps</b> you made.</p>
<p><b>Why it matters.</b> Bubble sort is the simplest sort, and OA questions ask how many swaps or passes it
needs, and what its complexity is.</p>
<h4>The idea</h4>
<ul>
<li>One <b>pass</b> walks from left to right and compares each pair of neighbours <code>a[i]</code>,
<code>a[i+1]</code>. If they are in the wrong order (<code>a[i] &gt; a[i+1]</code>), swap them.</li>
<li>After pass 1 the largest value has "bubbled" to the last place. After pass <i>k</i>, the <i>k</i>
largest values are in their final places, so the next pass can stop one place earlier.</li>
<li>If a pass makes <b>no swaps</b>, the array is sorted: stop early.</li>
</ul>
<h4>Example: {5, 1, 4, 2, 8}</h4>
<pre>pass 1 (compare up to the end):
  [5 1] 4 2 8   5 &gt; 1 swap  -&gt;  1 5 4 2 8
  1 [5 4] 2 8   5 &gt; 4 swap  -&gt;  1 4 5 2 8
  1 4 [5 2] 8   5 &gt; 2 swap  -&gt;  1 4 2 5 8
  1 4 2 [5 8]   ok          -&gt;  1 4 2 5 8      3 swaps, 8 is in place
pass 2 (stop before the 8):
  [1 4] 2 5 8   ok
  1 [4 2] 5 8   4 &gt; 2 swap  -&gt;  1 2 4 5 8
  1 2 [4 5] 8   ok                             1 swap
pass 3:
  [1 2] 4 5 8   ok
  1 [2 4] 5 8   ok                             0 swaps: stop

total: 4 swaps, result {1, 2, 4, 5, 8}</pre>
<h4>A neat fact: swaps = inversions</h4>
<p>An <b>inversion</b> is a pair of positions <code>i &lt; j</code> with <code>a[i] &gt; a[j]</code> (two values
in the wrong order). Each swap of neighbours fixes exactly one inversion. So the swap count is the number of
inversions, however you write the loops. {5, 1, 4, 2, 8} has 4 inversions: (5,1), (5,4), (5,2), (4,2).</p>
<h4>More examples</h4>
<table>
<tr><th>Input</th><th>Result</th><th>Returns</th></tr>
<tr><td>{3, 1, 2}</td><td>{1, 2, 3}</td><td>2</td></tr>
<tr><td>{1, 2, 3, 4} (already sorted)</td><td>unchanged</td><td>0 (one pass, then stop)</td></tr>
<tr><td>{} (n = 0) or one element</td><td>unchanged</td><td>0</td></tr>
</table>
<p>The tests use up to 2,000 values between &minus;1000 and 1000, some already sorted. The swap count can be
up to about 2 million, which is why the return type is <code>long</code>.</p>
<h4>OA facts</h4>
<p>Worst and average case O(n<sup>2</sup>). Best case O(n) on sorted input, thanks to the early stop. It is
<b>stable</b> (equal values keep their order, because equal neighbours are never swapped) and <b>in place</b>
(no extra array).</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Use two loops: the outer one counts passes and shrinks the unsorted part; the inner one walks over the
neighbour pairs of that part.</li>
<li>Keep a flag "did this pass swap anything?" and leave the outer loop when it stays false.</li>
<li>Swap only when <code>a[i] &gt; a[i+1]</code>, never when they are equal.</li>
</ol>
</details>""",
r"""long bubble_sort(int *a, int n)
{
    return 0;
}
""",
r"""long bubble_sort(int *a, int n)
{
    long swaps = 0;
    for (int end = n - 1; end > 0; end--) {
        int swapped = 0;
        for (int i = 0; i < end; i++)
            if (a[i] > a[i + 1]) {
                int t = a[i]; a[i] = a[i + 1]; a[i + 1] = t;
                swaps++;
                swapped = 1;
            }
        if (!swapped)
            break;
    }
    return swaps;
}
""",
r"""#include "check.h"
#include <stdlib.h>
#include "solution.c"
static int cmp(const void *x, const void *y) { int a = *(const int *)x, b = *(const int *)y; return (a > b) - (a < b); }
int main(void)
{
    char d[96];
    static int a[2000], s[2000];
    int ex[] = {3, 1, 2};
    ck_int("bubble_sort({3, 1, 2}) swaps", bubble_sort(ex, 3), 2);
    for (int t = 0; t < 60; t++) {
        int n = t < 3 ? t : ck_range(1, 2000), hi = ck_range(1, 1000);
        for (int i = 0; i < n; i++) a[i] = s[i] = (t % 10 == 9) ? i : ck_range(-hi, hi);
        long inv = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) inv += a[i] > a[j];
        qsort(s, (size_t)n, sizeof *s, cmp);
        CK_FMT(d, "case %d (n = %d): swaps", t, n); ck_int(d, bubble_sort(a, n), inv);
        CK_FMT(d, "case %d (n = %d): sorted", t, n); ck_true(d, n == 0 || memcmp(a, s, (size_t)n * sizeof *a) == 0);
    }
    return ck_done();
}
""",
"Outer loop shrinks the unsorted end; inner loop swaps a[i] and a[i+1] when a[i] > a[i+1] and counts it. Break when a pass swaps nothing."))

add(P("selection_sort", S, "Selection sort", "c", "func",
r"""<p><b>What to write.</b> <code>int selection_sort(int *a, int n)</code>. Sort the array in ascending order with
selection sort and return the number of <b>swaps</b> you made.</p>
<p><b>Why it matters.</b> Selection sort makes very few writes: at most n&minus;1 swaps. That is useful when
writing is expensive, for example in flash memory. OA questions ask for its number of comparisons and swaps.</p>
<h4>The rule, step by step</h4>
<p>For <i>i</i> = 0, 1, ..., n&minus;2:</p>
<ol>
<li>Find the <b>smallest</b> value in <code>a[i..n-1]</code>. If the smallest value appears more than once,
take the <b>first</b> one (compare with <code>&lt;</code>, not <code>&lt;=</code>). Call its index
<i>m</i>.</li>
<li>If <i>m</i> &ne; <i>i</i>, swap <code>a[i]</code> and <code>a[m]</code> and count one swap. If <i>m</i>
= <i>i</i>, the value is already in place: do not swap and do not count.</li>
</ol>
<h4>Example: {64, 25, 12, 22, 11}</h4>
<table>
<tr><th><i>i</i></th><th>Looks at</th><th>Smallest (index <i>m</i>)</th><th>Action</th><th>Array afterwards</th></tr>
<tr><td>0</td><td>64 25 12 22 11</td><td>11 (4)</td><td>swap a[0], a[4]</td><td>11 25 12 22 64</td></tr>
<tr><td>1</td><td>25 12 22 64</td><td>12 (2)</td><td>swap a[1], a[2]</td><td>11 12 25 22 64</td></tr>
<tr><td>2</td><td>25 22 64</td><td>22 (3)</td><td>swap a[2], a[3]</td><td>11 12 22 25 64</td></tr>
<tr><td>3</td><td>25 64</td><td>25 (3)</td><td>already in place</td><td>11 12 22 25 64</td></tr>
</table>
<p>Returns 3. The number of comparisons is always n(n&minus;1)/2, here 4 + 3 + 2 + 1 = 10, whatever the
input.</p>
<h4>More examples</h4>
<table>
<tr><th>Input</th><th>Result</th><th>Returns</th><th>Note</th></tr>
<tr><td>{4, 2, 3, 1}</td><td>{1, 2, 3, 4}</td><td>1</td><td>only 4 and 1 swap; 2 and 3 are already in place</td></tr>
<tr><td>{5, 5}</td><td>{5, 5}</td><td>0</td><td>with <code>&lt;=</code> you would wrongly swap the two 5s and return 1</td></tr>
<tr><td>{2, 1, 1}</td><td>{1, 1, 2}</td><td>2</td><td>with <code>&lt;=</code> you would pick the last 1 and return 1</td></tr>
</table>
<p>The tests use up to 1,500 values with many repeats, and compare your swap count with the rule above.</p>
<h4>Not stable</h4>
<p>Selection sort is <b>not stable</b>: a long-distance swap can jump a value over its equal twin. Mark two
equal 3s as 3a and 3b:</p>
<pre>{3a, 3b, 1}:  i = 0, smallest is 1 at index 2, swap a[0] and a[2]
           -&gt; {1, 3b, 3a}     3a is now behind 3b</pre>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The outer loop picks the position <i>i</i> to fill. The inner loop searches the rest of the array for the
index of the smallest value, starting with <i>m</i> = <i>i</i>.</li>
<li>Count a swap only when it actually moves something (<i>m</i> &ne; <i>i</i>).</li>
</ol>
</details>""",
r"""int selection_sort(int *a, int n)
{
    return 0;
}
""",
r"""int selection_sort(int *a, int n)
{
    int swaps = 0;
    for (int i = 0; i < n - 1; i++) {
        int m = i;
        for (int j = i + 1; j < n; j++)
            if (a[j] < a[m])
                m = j;
        if (m != i) {
            int t = a[i]; a[i] = a[m]; a[m] = t;
            swaps++;
        }
    }
    return swaps;
}
""",
r"""#include "check.h"
#include "solution.c"
static int ref(int *a, int n)
{
    int s = 0;
    for (int i = 0; i + 1 < n; i++) {
        int m = i;
        for (int j = i + 1; j < n; j++) if (a[j] < a[m]) m = j;
        if (m != i) { int t = a[i]; a[i] = a[m]; a[m] = t; s++; }
    }
    return s;
}
int main(void)
{
    char d[96];
    static int a[1500], b[1500];
    int ex[] = {4, 2, 3, 1};
    ck_int("selection_sort({4, 2, 3, 1}) swaps", selection_sort(ex, 4), 1);
    for (int t = 0; t < 60; t++) {
        int n = t < 3 ? t : ck_range(1, 1500), hi = ck_range(1, 50);
        for (int i = 0; i < n; i++) a[i] = b[i] = ck_range(-hi, hi);
        int sg = selection_sort(a, n), sw = ref(b, n);
        CK_FMT(d, "case %d (n = %d): swaps", t, n); ck_int(d, sg, sw);
        CK_FMT(d, "case %d (n = %d): sorted", t, n); ck_true(d, n == 0 || memcmp(a, b, (size_t)n * sizeof *a) == 0);
    }
    return ck_done();
}
""",
"For each i, scan j = i+1..n-1 keeping the index m of the smallest (a[j] < a[m]). Swap a[i] and a[m] only if m != i."))

add(P("insertion_sort", S, "Insertion sort", "c", "func",
r"""<p><b>What to write.</b> <code>long insertion_sort(int *a, int n)</code>. Sort the array in ascending order with
insertion sort and return the number of <b>shifts</b>: single moves of one element one place to the right.</p>
<p><b>Why it matters.</b> Insertion sort is O(n<sup>2</sup>) in general but very fast on nearly sorted data,
and it is stable. Fast library sorts use it for small pieces of the array.</p>
<h4>The idea</h4>
<p>The left part of the array is always sorted. Take the next element <code>x</code>. Move every element of
the sorted part that is <b>larger</b> than <code>x</code> one place to the right (each move is one shift),
then drop <code>x</code> into the gap.</p>
<pre>sorted part      next
[ 2  4  5  6 ] [ 1 ]  3          x = 1
[ 2  4  5  _ ]  6                6 &gt; 1: shift right  (1)
[ 2  4  _  5 ]  6                5 &gt; 1: shift right  (2)
[ 2  _  4  5 ]  6                4 &gt; 1: shift right  (3)
[ _  2  4  5 ]  6                2 &gt; 1: shift right  (4)
[ 1  2  4  5    6 ]  3           drop 1 into the gap: 4 shifts</pre>
<h4>Example: {5, 2, 4, 6, 1, 3}</h4>
<table>
<tr><th>Step (i)</th><th>x = a[i]</th><th>Shifts</th><th>Array afterwards</th></tr>
<tr><td>1</td><td>2</td><td>1</td><td>2 5 4 6 1 3</td></tr>
<tr><td>2</td><td>4</td><td>1</td><td>2 4 5 6 1 3</td></tr>
<tr><td>3</td><td>6</td><td>0</td><td>2 4 5 6 1 3</td></tr>
<tr><td>4</td><td>1</td><td>4</td><td>1 2 4 5 6 3</td></tr>
<tr><td>5</td><td>3</td><td>3</td><td>1 2 3 4 5 6</td></tr>
</table>
<p>Total: 9 shifts. Like the swaps of bubble sort, the shift count equals the number of <b>inversions</b>
(pairs <code>i &lt; j</code> with <code>a[i] &gt; a[j]</code>).</p>
<h4>More examples</h4>
<table>
<tr><th>Input</th><th>Result</th><th>Returns</th></tr>
<tr><td>{3, 1, 2}</td><td>{1, 2, 3}</td><td>2</td></tr>
<tr><td>{1, 2, 3} (sorted)</td><td>unchanged</td><td>0</td></tr>
<tr><td>n = 0</td><td>&ndash;</td><td>0</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>Shift only elements that are strictly larger than <code>x</code> (<code>&gt;</code>, not
<code>&gt;=</code>). An equal element stays in front of <code>x</code>: that keeps the sort stable and gives
the right count.</li>
<li>Stop shifting at the start of the array (index 0), even if every element was larger.</li>
<li>The tests use up to 2,000 values, some nearly sorted; the count can be about 2 million, so it is a
<code>long</code>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Save <code>x = a[i]</code> first, because the first shift overwrites <code>a[i]</code>.</li>
<li>Walk an index <code>j</code> from <code>i&minus;1</code> down while the element there is larger than
<code>x</code>, moving each one up by one place and counting.</li>
<li>Where the walk stops, the gap is just to the right of <code>j</code>.</li>
</ol>
</details>""",
r"""long insertion_sort(int *a, int n)
{
    return 0;
}
""",
r"""long insertion_sort(int *a, int n)
{
    long shifts = 0;
    for (int i = 1; i < n; i++) {
        int x = a[i], j = i - 1;
        while (j >= 0 && a[j] > x) {      /* > (not >=) keeps it stable */
            a[j + 1] = a[j];
            j--;
            shifts++;
        }
        a[j + 1] = x;
    }
    return shifts;
}
""",
r"""#include "check.h"
#include <stdlib.h>
#include "solution.c"
static int cmp(const void *x, const void *y) { int a = *(const int *)x, b = *(const int *)y; return (a > b) - (a < b); }
int main(void)
{
    char d[96];
    static int a[2000], s[2000];
    int ex[] = {3, 1, 2};
    ck_int("insertion_sort({3, 1, 2}) shifts", insertion_sort(ex, 3), 2);
    for (int t = 0; t < 60; t++) {
        int n = t < 3 ? t : ck_range(1, 2000), hi = ck_range(1, 1000);
        for (int i = 0; i < n; i++) a[i] = s[i] = (t % 10 == 9) ? i + (ck_range(0, 30) == 0 ? -5 : 0) : ck_range(-hi, hi);
        long inv = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) inv += a[i] > a[j];
        qsort(s, (size_t)n, sizeof *s, cmp);
        CK_FMT(d, "case %d (n = %d): shifts", t, n); ck_int(d, insertion_sort(a, n), inv);
        CK_FMT(d, "case %d (n = %d): sorted", t, n); ck_true(d, n == 0 || memcmp(a, s, (size_t)n * sizeof *a) == 0);
    }
    return ck_done();
}
""",
"for i = 1..n-1: x = a[i]; j = i-1; while (j >= 0 && a[j] > x) { a[j+1] = a[j]; j--; count++; } a[j+1] = x;"))

add(P("merge_sort", S, "Merge sort (stable)", "c", "func",
r"""<p><b>What to write.</b> A stable merge sort for records:</p>
<pre>struct Rec { int key; int id; };
void merge_sort(struct Rec *a, int n);   // sort by key; must be stable</pre>
<p><b>Why it matters.</b> Merge sort is O(n log n) in every case, and it is <b>stable</b>: records with equal
keys keep their original order. That matters when you sort by one field after another (for example by
name, then by age). The price is O(n) extra memory.</p>
<h4>The idea</h4>
<ol>
<li>An array of 0 or 1 records is already sorted.</li>
<li>Otherwise split it into two halves, sort each half (recursively), and <b>merge</b> them: repeatedly
compare the first remaining record of each half and take the smaller one into a temporary buffer. Then copy
the buffer back.</li>
<li><b>Stability rule:</b> when the two keys are equal, take the record from the <b>left</b> half.</li>
</ol>
<h4>Example: records written as key/id</h4>
<pre>input:            3/0  1/1  3/2  2/3  1/4

split:           [3/0  1/1] [3/2  2/3  1/4]
                 /      \    /     \
             [3/0]  [1/1] [3/2] [2/3  1/4]
                                /      \
                            [2/3]    [1/4]

merge [2/3] + [1/4]            -&gt; 1/4 2/3
merge [3/2] + [1/4 2/3]        -&gt; 1/4 2/3 3/2
merge [3/0] + [1/1]            -&gt; 1/1 3/0
merge [1/1 3/0] + [1/4 2/3 3/2]:</pre>
<table>
<tr><th>Left front</th><th>Right front</th><th>Take</th><th>Why</th></tr>
<tr><td>1/1</td><td>1/4</td><td>1/1</td><td>keys equal: take the left one</td></tr>
<tr><td>3/0</td><td>1/4</td><td>1/4</td><td>1 &lt; 3</td></tr>
<tr><td>3/0</td><td>2/3</td><td>2/3</td><td>2 &lt; 3</td></tr>
<tr><td>3/0</td><td>3/2</td><td>3/0</td><td>keys equal: take the left one</td></tr>
<tr><td>(empty)</td><td>3/2</td><td>3/2</td><td>copy what is left</td></tr>
</table>
<pre>output:           1/1  1/4  2/3  3/0  3/2</pre>
<p>Both 1s and both 3s are still in their original id order. If you took the right record on a tie, you
would get 1/4 before 1/1: sorted, but not stable.</p>
<h4>What the tests check</h4>
<ul>
<li>Sizes 0, 1, 2, 3, 10, 1,000, 77,777 and 100,000, with keys 0 to 1000 (some with only 4 different keys,
so many ties).</li>
<li>The result is sorted by key, equal keys keep their ids in increasing order, and the same records come
out as went in.</li>
</ul>
<div class="note">Allocate the temporary buffer <b>once</b> with <code>malloc</code> (n records) and pass it
to the recursive helper; free it at the end. Allocating inside every recursive call is slow, and a large
array on the stack could overflow it.</div>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a helper that sorts the range <code>a[lo..hi)</code> using the shared buffer. Split at
<code>mid = lo + (hi &minus; lo) / 2</code>.</li>
<li>During the merge, take from the right half only if its key is strictly smaller. When one half runs out,
copy the rest of the other.</li>
<li>Copy the merged range from the buffer back into <code>a</code> before returning.</li>
</ol>
</details>""",
r"""#include <stdlib.h>

struct Rec {
    int key;
    int id;
};

void merge_sort(struct Rec *a, int n)
{
}
""",
r"""#include <stdlib.h>
#include <string.h>

struct Rec {
    int key;
    int id;
};

static void sort_rec(struct Rec *a, struct Rec *tmp, int lo, int hi)    /* sorts a[lo, hi) */
{
    if (hi - lo < 2)
        return;
    int mid = lo + (hi - lo) / 2;
    sort_rec(a, tmp, lo, mid);
    sort_rec(a, tmp, mid, hi);
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi)
        tmp[k++] = (a[j].key < a[i].key) ? a[j++] : a[i++];    /* ties take the left one: stable */
    while (i < mid)
        tmp[k++] = a[i++];
    while (j < hi)
        tmp[k++] = a[j++];
    memcpy(a + lo, tmp + lo, (size_t)(hi - lo) * sizeof *a);
}

void merge_sort(struct Rec *a, int n)
{
    struct Rec *tmp = malloc((size_t)n * sizeof *tmp);
    if (tmp == NULL)
        return;
    sort_rec(a, tmp, 0, n);
    free(tmp);
}
""",
r"""#include "check.h"
#include "solution.c"
static struct Rec r[100000];
static int cnt[1001];
int main(void)
{
    char d[96];
    int sizes[] = {0, 1, 2, 3, 10, 1000, 100000, 77777};
    for (int t = 0; t < 8; t++) {
        int n = sizes[t], range = t == 6 ? 1000 : (t == 7 ? 3 : 50);
        memset(cnt, 0, sizeof cnt);
        for (int i = 0; i < n; i++) { r[i].key = ck_range(0, range); r[i].id = i; cnt[r[i].key]++; }
        merge_sort(r, n);
        int sorted = 1, stable = 1, kept = 1;
        for (int i = 1; i < n; i++) {
            if (r[i - 1].key > r[i].key) sorted = 0;
            if (r[i - 1].key == r[i].key && r[i - 1].id > r[i].id) stable = 0;
        }
        for (int i = 0; i < n; i++) if (r[i].key >= 0 && r[i].key <= 1000) cnt[r[i].key]--; else kept = 0;
        for (int k = 0; k <= 1000; k++) if (cnt[k]) kept = 0;
        CK_FMT(d, "n = %d: sorted by key", n); ck_true(d, sorted);
        CK_FMT(d, "n = %d: equal keys keep their order (stable)", n); ck_true(d, stable);
        CK_FMT(d, "n = %d: same records as the input", n); ck_true(d, kept);
    }
    return ck_done();
}
""",
"Write a recursive helper sort(a, tmp, lo, hi). Merge with 'take from the right only if right.key < left.key' so ties come from the left half. Copy tmp back into a."))

add(P("quick_sort", S, "Quicksort that survives sorted input", "c", "func",
r"""<p><b>What to write.</b> <code>void quick_sort(int *a, int n)</code>: sort the array in ascending order with a
quicksort that stays fast on every kind of input.</p>
<p><b>Why it matters.</b> Quicksort is the usual fastest in-place sort, but the textbook version has a weak
spot that interviewers like to ask about: on some inputs it becomes O(n<sup>2</sup>).</p>
<h4>The idea</h4>
<ol>
<li>Choose a <b>pivot</b> value.</li>
<li><b>Partition</b>: rearrange the array so that a left part holds values &le; pivot and a right part holds
values &ge; pivot.</li>
<li>Sort the two parts the same way.</li>
</ol>
<p>It averages O(n log n). But if the pivot is always the smallest or largest value, one part is empty and
the other has n&minus;1 elements. Then the time is O(n<sup>2</sup>) and the recursion is n levels deep.</p>
<h4>What the tests do</h4>
<p>They sort 100,000 values that are random, <b>already sorted</b>, <b>reversed</b>, <b>all equal</b>, only
4 different values, and "organ pipe" (rising, then falling), within the 5-second limit. The textbook
"last element as pivot" (Lomuto) version fails on sorted, reversed and all-equal input: the last element is
then always the largest (or equal to everything), so every split is n&minus;1 to 0.</p>
<h4>What works</h4>
<ul>
<li><b>Pivot = the middle element</b> of the range: on sorted or reversed input it is the median.</li>
<li><b>Hoare partitioning</b>: index <code>i</code> moves right while <code>a[i] &lt; pivot</code>, index
<code>j</code> moves left while <code>a[j] &gt; pivot</code>; if they have not crossed, swap
<code>a[i]</code> and <code>a[j]</code> and continue. Both stop on values <b>equal</b> to the pivot, so a run
of equal values is split evenly.</li>
<li><b>Recurse into the smaller part, loop on the larger part.</b> Then the recursion is at most about
log<sub>2</sub> n levels deep (about 17 for 100,000).</li>
</ul>
<h4>Hoare partition, traced on {5, 3, 8, 4, 2, 7, 1} (pivot = middle = 4)</h4>
<pre>index:   0  1  2  3  4  5  6
start:   5  3  8  4  2  7  1
         i stops at 0 (5 &ge; 4), j stops at 6 (1 &le; 4): swap
         1  3  8  4  2  7  5
         i moves to 2 (8 &ge; 4), j moves to 4 (2 &le; 4): swap
         1  3  2  4  8  7  5
         i moves to 3 (4), j moves to 3 (4): i &ge; j, stop with j = 3

parts:  [1  3  2  4] [8  7  5]      = a[0..j] and a[j+1..6]</pre>
<p>On all-equal input {2, 2, 2, 2, 2, 2}, <code>i</code> and <code>j</code> stop at every element, swap,
and meet in the middle (j = 2): two parts of 3. That is why equal values do no harm.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a helper that sorts <code>a[lo..hi]</code> (both ends included). In Hoare's scheme start with
<code>i = lo &minus; 1</code> and <code>j = hi + 1</code>, and move each index <b>before</b> testing it.</li>
<li>After partitioning, the two parts are <code>[lo, j]</code> and <code>[j+1, hi]</code>. Note:
<code>j</code>, not <code>i</code>, and the pivot is not necessarily at <code>j</code>.</li>
<li>To bound the stack: make the helper a <code>while (lo &lt; hi)</code> loop. Call it recursively for the
smaller part, then change <code>lo</code> or <code>hi</code> so that the loop continues with the larger
part.</li>
</ol>
</details>""",
r"""void quick_sort(int *a, int n)
{
}
""",
r"""static void qs(int *a, int lo, int hi)        /* sorts a[lo..hi] */
{
    while (lo < hi) {
        int pivot = a[lo + (hi - lo) / 2];
        int i = lo - 1, j = hi + 1;
        for (;;) {                                  /* Hoare partition */
            do i++; while (a[i] < pivot);
            do j--; while (a[j] > pivot);
            if (i >= j)
                break;
            int t = a[i]; a[i] = a[j]; a[j] = t;
        }
        if (j - lo < hi - j) {                      /* recurse into the smaller part */
            qs(a, lo, j);
            lo = j + 1;
        } else {
            qs(a, j + 1, hi);
            hi = j;
        }
    }
}

void quick_sort(int *a, int n)
{
    if (n > 1)
        qs(a, 0, n - 1);
}
""",
r"""#include "check.h"
#include <stdlib.h>
#include "solution.c"
static int cmp(const void *x, const void *y) { int a = *(const int *)x, b = *(const int *)y; return (a > b) - (a < b); }
static int a[100000], s[100000];
int main(void)
{
    char d[96];
    static const char *names[] = {"random", "already sorted", "reversed", "all equal", "few distinct values", "organ pipe"};
    int sizes[] = {0, 1, 2, 5, 100000};
    for (int z = 0; z < 5; z++)
        for (int kind = 0; kind < 6; kind++) {
            int n = sizes[z];
            for (int i = 0; i < n; i++) {
                switch (kind) {
                case 0: a[i] = (int)ck_rand(); break;
                case 1: a[i] = i * 3; break;
                case 2: a[i] = n - i; break;
                case 3: a[i] = 42; break;
                case 4: a[i] = ck_range(0, 3); break;
                default: a[i] = i < n / 2 ? i : n - i; break;
                }
                s[i] = a[i];
            }
            qsort(s, (size_t)n, sizeof *s, cmp);
            quick_sort(a, n);
            CK_FMT(d, "%s, n = %d", names[kind], n);
            ck_true(d, n == 0 || memcmp(a, s, (size_t)n * sizeof *a) == 0);
        }
    return ck_done();
}
""",
"Pivot = a[lo + (hi-lo)/2]. Hoare: i = lo-1, j = hi+1; do i++ while a[i] < pivot; do j-- while a[j] > pivot; if i >= j stop, else swap. The two parts are [lo, j] and [j+1, hi]."))

add(P("qsort_cmp", S, "qsort with a comparator", "c", "func",
r"""<p><b>What to write.</b> <code>void sort_tasks(struct Task *t, int n)</code>. It must call the C library's
<code>qsort</code> to order the tasks by <b>priority, highest first</b>, and for equal priorities by <b>id,
lowest first</b>.</p>
<pre>struct Task { int id; int priority; };

void qsort(void *base, size_t n, size_t size,
           int (*cmp)(const void *, const void *));</pre>
<p><b>Why it matters.</b> <code>qsort</code> can sort an array of any type, because you hand it a
<b>comparison function</b> through a function pointer. Writing that comparator correctly is a common C
interview task.</p>
<h4>How <code>qsort</code> uses your comparator</h4>
<ul>
<li><code>base</code> = the array, <code>n</code> = the number of elements, <code>size</code> = the size of
one element in bytes (<code>sizeof *t</code>), <code>cmp</code> = your function.</li>
<li><code>qsort</code> calls <code>cmp(p, q)</code> with pointers to two elements. They arrive as
<code>const void *</code>; cast them to <code>const struct Task *</code> to read the fields.</li>
</ul>
<table>
<tr><th><code>cmp(p, q)</code> returns</th><th>Meaning</th></tr>
<tr><td>a negative number</td><td>*p must come <b>before</b> *q</td></tr>
<tr><td>a positive number</td><td>*p must come <b>after</b> *q</td></tr>
<tr><td>0</td><td>they are equal (any order)</td></tr>
</table>
<h4>Example</h4>
<table>
<tr><th>Input (id, priority)</th><th>After <code>sort_tasks</code></th></tr>
<tr><td>(4, 2) (1, 5) (3, 2) (2, 5) (7, &minus;1)</td><td>(1, 5) (2, 5) (3, 2) (4, 2) (7, &minus;1)</td></tr>
</table>
<p>Priority 5 comes first; inside it, id 1 before id 2. Then priority 2 (ids 3, 4), then &minus;1.</p>
<h4>The overflow trap</h4>
<p>A common shortcut is <code>return b-&gt;priority - a-&gt;priority;</code>. Do not do this here. The tests
use priorities as large as <code>INT_MAX</code> (2,147,483,647) and as small as <code>INT_MIN</code>
(&minus;2,147,483,648). For example INT_MIN &minus; INT_MAX = &minus;4,294,967,295, which does not fit in an
<code>int</code>. That is signed overflow, undefined behaviour, and on this site it stops the program. Compare
with <code>&lt;</code> and <code>&gt;</code> instead, for example <code>(x &gt; y) - (x &lt; y)</code>
gives &minus;1, 0 or 1 safely.</p>
<h4>Things to watch out for</h4>
<ul>
<li>The ids are random 32-bit values, so they can be negative too. Compare them as <code>int</code>s.</li>
<li><code>qsort</code> is not stable, so the order of equal priorities is decided only by your id rule.</li>
<li>The tests use up to 3,000 tasks, including n = 0 and n = 1.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a <code>static int</code> comparator taking two <code>const void *</code>. First compare the
priorities. If they differ, the one with the <b>larger</b> priority goes first, so it must return a
negative number.</li>
<li>Only if the priorities are equal, compare the ids (smaller id first).</li>
<li><code>sort_tasks</code> is then a single call to <code>qsort</code>.</li>
</ol>
</details>""",
r"""#include <stdlib.h>

struct Task {
    int id;
    int priority;
};

void sort_tasks(struct Task *t, int n)
{
}
""",
r"""#include <stdlib.h>

struct Task {
    int id;
    int priority;
};

static int by_priority(const void *x, const void *y)
{
    const struct Task *a = x, *b = y;
    if (a->priority != b->priority)
        return a->priority > b->priority ? -1 : 1;     /* higher priority first */
    return (a->id > b->id) - (a->id < b->id);          /* then lower id first */
}

void sort_tasks(struct Task *t, int n)
{
    qsort(t, (size_t)n, sizeof *t, by_priority);
}
""",
r"""#include "check.h"
#include <limits.h>
#include "solution.c"
static struct Task T[3000];
int main(void)
{
    char d[96];
    for (int c = 0; c < 40; c++) {
        int n = c < 2 ? c : ck_range(2, 3000);
        for (int i = 0; i < n; i++) {
            T[i].id = (int)ck_rand();
            T[i].priority = c % 4 == 3 ? (ck_range(0, 1) ? INT_MAX : INT_MIN + ck_range(0, 2)) : ck_range(-5, 5);
        }
        sort_tasks(T, n);
        int ok = 1, bad = -1;
        for (int i = 1; i < n && ok; i++) {
            const struct Task *a = &T[i - 1], *b = &T[i];
            if (a->priority < b->priority || (a->priority == b->priority && a->id > b->id)) { ok = 0; bad = i; }
        }
        CK_FMT(d, "case %d (%d tasks): order (first problem at index %d)", c, n, bad); ck_true(d, ok);
    }
    return ck_done();
}
""",
"Comparator: cast the void pointers to const struct Task *. Compare priorities first (return -1 if a's is larger), then ids with (a > b) - (a < b). Pass it to qsort(t, n, sizeof *t, cmp)."))

# ---------------------------------------------------------------------------
S = "Interview classics"

add(P("print_upto", S, "Print 1 to n without loops", "c", "func",
r"""<p><b>What to write.</b> <code>void print_upto(int n)</code> that prints the numbers 1 to <code>n</code>
<b>without any loop</b>.</p>
<p><b>Why it matters.</b> This was asked in a 2026 Qualcomm interview. It checks whether you can replace a
loop with another way of repeating work.</p>
<h4>Exact output format</h4>
<ul>
<li>The numbers 1, 2, ..., <code>n</code> in increasing order, separated by <b>single spaces</b>.</li>
<li>After the last number: a newline <code>'\n'</code>, and no space before it.</li>
<li><code>n</code> is at least 1. The tests use n = 1, 2, 5, 100 and 1000.</li>
</ul>
<table>
<tr><th>Call</th><th>Prints exactly</th></tr>
<tr><td><code>print_upto(1)</code></td><td><code>"1\n"</code></td></tr>
<tr><td><code>print_upto(5)</code></td><td><code>"1 2 3 4 5\n"</code></td></tr>
</table>
<h4>The rules</h4>
<ul>
<li>The test program turns the words <code>for</code>, <code>while</code> and <code>goto</code> into compile
errors. (So <code>do ... while</code> is blocked too.)</li>
<li>Print with <code>printf</code> (or <code>putchar</code>): the test catches what these two print and
compares it. Other output functions such as <code>puts</code> are not caught.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>A function may call itself (this is called <b>recursion</b>). Each call can do one small piece of the job
and leave the rest to the next call.</li>
<li>Every recursive function needs a <b>stopping case</b>: when must a call print nothing and simply
return?</li>
<li>To print 1 to n in increasing order, it helps to have a helper with two parameters: the number to print
now, and <code>n</code>. Ask yourself: should a call print its number <b>before</b> or <b>after</b> the call
it makes?</li>
<li>Only the last number is followed by <code>'\n'</code> instead of a space. How does a call know that it is
the last one?</li>
</ol>
</details>""",
r"""#include <stdio.h>

void print_upto(int n)
{
}
""",
r"""#include <stdio.h>

static void count_from(int i, int n)
{
    if (i > n)
        return;
    printf(i < n ? "%d " : "%d\n", i);
    count_from(i + 1, n);
}

void print_upto(int n)
{
    count_from(1, n);
}
""",
r"""#include "check.h"
#include <stdarg.h>
static char cap[20000];
static int caplen;
static int cap_printf(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    int k = vsnprintf(cap + caplen, sizeof cap - (size_t)caplen, fmt, ap);
    va_end(ap);
    if (k > 0) { caplen += k; if (caplen > (int)sizeof cap - 1) caplen = (int)sizeof cap - 1; }
    return k;
}
__attribute__((unused)) static int cap_putchar(int c) { if (caplen < (int)sizeof cap - 1) { cap[caplen++] = (char)c; cap[caplen] = 0; } return c; }
#undef putchar
#define printf cap_printf
#define putchar cap_putchar
#define for NO_LOOPS_ALLOWED_for
#define while NO_LOOPS_ALLOWED_while
#define goto NO_GOTO_ALLOWED
#include "solution.c"
#undef printf
#undef putchar
#undef for
#undef while
#undef goto
int main(void)
{
    char d[64];
    static char want[20000];
    int ns[] = {1, 2, 5, 100, 1000};
    for (int t = 0; t < 5; t++) {
        int n = ns[t], w = 0;
        for (int i = 1; i <= n; i++) w += snprintf(want + w, sizeof want - (size_t)w, i < n ? "%d " : "%d\n", i);
        caplen = 0; cap[0] = 0;
        print_upto(n);
        CK_FMT(d, "print_upto(%d)", n);
        if (n <= 5) ck_str(d, cap, want);
        else {
            int k = 0;
            while (want[k] && cap[k] == want[k]) k++;
            if (want[k] || cap[k]) { printf("MISMATCH %s: first difference at character %d | expected \"%.20s...\" | got \"%.20s...\"\n", d, k, want + k, cap + k); ck_total++; ck_fail++; }
            else ck_true(d, 1);
        }
    }
    return ck_done();
}
""",
"Recursion replaces the loop: a helper count_from(i, n) prints i, then calls count_from(i + 1, n), and returns when i > n."))

add(P("bits_to_flip", S, "Bits to flip to turn a into b", "c", "func",
r"""<p><b>What to write.</b> <code>int bits_to_flip(uint32_t a, uint32_t b)</code>: how many bits must you flip to
turn <code>a</code> into <code>b</code>?</p>
<p><b>Why it matters.</b> This was asked in a 2026 Qualcomm interview. The same count is called the
<b>Hamming distance</b>; it tells you how many bit errors a received word has.</p>
<h4>The idea</h4>
<ul>
<li>XOR (<code>^</code>) gives 1 exactly where two bits differ. So the bits you must flip are the 1s of
<code>a ^ b</code>, and the answer is the number of 1s in it.</li>
<li>Counting the 1s, <b>Kernighan's trick</b>: <code>x &amp; (x - 1)</code> is <code>x</code> with its
<b>lowest</b> 1 cleared. Repeat until <code>x</code> is 0 and count the repeats. The loop runs once per 1
bit, not once per bit position.</li>
</ul>
<h4>Example: <code>bits_to_flip(29, 15)</code> = 2</h4>
<pre>a     = 29 = 1 1 1 0 1
b     = 15 = 0 1 1 1 1
a ^ b =      1 0 0 1 0      two 1s: bits 4 and 1 differ

Kernighan on x = 10010:
  x = 10010,  x - 1 = 10001,  x &amp; (x - 1) = 10000    count 1
  x = 10000,  x - 1 = 01111,  x &amp; (x - 1) = 00000    count 2, x is 0: stop</pre>
<h4>More examples</h4>
<table>
<tr><th>Call</th><th>a ^ b</th><th>Returns</th></tr>
<tr><td><code>bits_to_flip(7, 7)</code></td><td>0</td><td>0</td></tr>
<tr><td><code>bits_to_flip(0x0F, 0xF0)</code></td><td>0xFF</td><td>8</td></tr>
<tr><td><code>bits_to_flip(0, 0xFFFFFFFF)</code></td><td>0xFFFFFFFF</td><td>32</td></tr>
</table>
<p>The tests use random 32-bit values. Keep the work in an unsigned type (<code>uint32_t</code>), so bit 31
is just another bit.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>First reduce the problem to "count the 1 bits of one number".</li>
<li>Then either test each of the 32 bits with a shift and <code>&amp; 1</code>, or use Kernighan's trick in a
loop that runs while the number is not 0.</li>
</ol>
</details>""",
r"""#include <stdint.h>

int bits_to_flip(uint32_t a, uint32_t b)
{
    return 0;
}
""",
r"""#include <stdint.h>

int bits_to_flip(uint32_t a, uint32_t b)
{
    uint32_t x = a ^ b;
    int count = 0;
    while (x) {
        x &= x - 1;     /* clear the lowest set bit */
        count++;
    }
    return count;
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    ck_int("bits_to_flip(29, 15)", bits_to_flip(29, 15), 2);
    ck_int("bits_to_flip(0, 0xFFFFFFFF)", bits_to_flip(0, 0xFFFFFFFFu), 32);
    ck_int("bits_to_flip(7, 7)", bits_to_flip(7, 7), 0);
    for (int t = 0; t < 300; t++) {
        uint32_t a = ck_rand(), b = ck_rand() & ck_rand();
        CK_FMT(d, "bits_to_flip(0x%08X, 0x%08X)", (unsigned)a, (unsigned)b);
        ck_int(d, bits_to_flip(a, b), __builtin_popcount(a ^ b));
    }
    return ck_done();
}
""",
"x = a ^ b; then count with while (x) { x &= x - 1; count++; }"))

add(P("list_cycle", S, "Find the start of a loop in a list", "c", "func",
r"""<p><b>What to write.</b> <code>struct Node *cycle_start(struct Node *head)</code>. A linked list may end in a
<b>loop</b>: the last node points back to an earlier node instead of to <code>NULL</code>. Return a pointer
to the <b>first node of the loop</b>, or <code>NULL</code> if the list ends normally. Use O(1) extra memory
(a few pointers, no arrays, no marking of nodes).</p>
<pre>struct Node { int value; struct Node *next; };</pre>
<p><b>Why it matters.</b> This is one of the most asked linked-list interview questions. The same idea
detects loops in any "next" function, for example in a corrupted free list.</p>
<h4>Picture: 6 nodes, the last one points back to node 2</h4>
<pre>head
 |
 v
[0] --&gt; [1] --&gt; [2] --&gt; [3] --&gt; [4] --&gt; [5]
                 ^                        |
                 |                        |
                 +------------------------+
the answer is node 2</pre>
<h4>Floyd's method ("tortoise and hare")</h4>
<ol>
<li>Start two pointers at <code>head</code>. Each round, <code>slow</code> moves <b>one</b> step and
<code>fast</code> moves <b>two</b> steps.</li>
<li>If <code>fast</code> reaches <code>NULL</code> (or a node whose <code>next</code> is <code>NULL</code>),
there is no loop: return <code>NULL</code>.</li>
<li>If <code>slow</code> and <code>fast</code> land on the same node, there is a loop.</li>
<li>Then put one pointer back at <code>head</code>, leave the other at the meeting node, and move
<b>both one step</b> at a time. The node where they meet now is the start of the loop.</li>
</ol>
<h4>Trace for the picture above</h4>
<table>
<tr><th>Round</th><th>slow</th><th>fast</th><th></th></tr>
<tr><td>start</td><td>0</td><td>0</td><td></td></tr>
<tr><td>1</td><td>1</td><td>2</td><td></td></tr>
<tr><td>2</td><td>2</td><td>4</td><td></td></tr>
<tr><td>3</td><td>3</td><td>2</td><td>fast went 4 &rarr; 5 &rarr; 2 (round the loop)</td></tr>
<tr><td>4</td><td>4</td><td>4</td><td>they meet at node 4</td></tr>
</table>
<table>
<tr><th>Phase 2</th><th>pointer from head</th><th>pointer from meeting node</th></tr>
<tr><td>start</td><td>0</td><td>4</td></tr>
<tr><td>step 1</td><td>1</td><td>5</td></tr>
<tr><td>step 2</td><td>2</td><td>2 &larr; equal: return node 2</td></tr>
</table>
<h4>More cases</h4>
<table>
<tr><th>List</th><th>Returns</th></tr>
<tr><td>4 nodes, the last points back to node 0 (the whole list is a loop)</td><td>node 0 (the head)</td></tr>
<tr><td>3 nodes, the last points to <code>NULL</code></td><td><code>NULL</code></td></tr>
<tr><td><code>head == NULL</code> (empty list)</td><td><code>NULL</code></td></tr>
</table>
<p>The tests use lists of 1 to 3,000 nodes, with the loop going back to any node, or no loop. The answer is
checked by address, so return the node itself, not a copy.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Before each <code>fast</code> move you must know that <code>fast</code> and <code>fast-&gt;next</code>
are not <code>NULL</code>. Make that the loop condition.</li>
<li>Why phase 2 works: let <i>a</i> be the number of steps from <code>head</code> to the loop start. One can
show that the meeting node is also exactly <i>a</i> steps (plus whole laps) before the loop start, going
forward. In the picture: <i>a</i> = 2, and from node 4 two steps (4 &rarr; 5 &rarr; 2) reach the start.</li>
</ol>
</details>""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

struct Node *cycle_start(struct Node *head)
{
    return NULL;
}
""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

struct Node *cycle_start(struct Node *head)
{
    struct Node *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            slow = head;            /* distance head->start == distance meet->start (mod loop length) */
            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }
            return slow;
        }
    }
    return NULL;
}
""",
r"""#include "check.h"
#include "solution.c"
static struct Node pool[3000];
int main(void)
{
    char d[96];
    ck_true("cycle_start(NULL) is NULL", cycle_start(NULL) == NULL);
    for (int t = 0; t < 300; t++) {
        int n = ck_range(1, 3000), loop = ck_range(0, 2) ? ck_range(0, n - 1) : -1;
        for (int i = 0; i < n; i++) { pool[i].value = i; pool[i].next = i + 1 < n ? &pool[i + 1] : (loop >= 0 ? &pool[loop] : NULL); }
        struct Node *got = cycle_start(&pool[0]);
        CK_FMT(d, "%d nodes, last node points to %s%d", n, loop >= 0 ? "node " : "NULL ", loop);
        ck_int(d, got ? (int)(got - pool) : -1, loop);
    }
    return ck_done();
}
""",
"while (fast && fast->next) { slow = slow->next; fast = fast->next->next; if (slow == fast) { slow = head; walk both one step until equal; return slow; } } return NULL;"))

add(P("list_two_ptr", S, "Middle node and k-th from the end", "c", "func",
r"""<p><b>What to write.</b> Two classic one-pass linked-list functions that use two pointers:</p>
<pre>struct Node *list_middle(struct Node *head);         // the middle node
struct Node *kth_from_end(struct Node *head, int k); // k = 1: last node</pre>
<p><b>Why it matters.</b> Both are common interview questions, and both use the same trick: two pointers
that move at different speeds, or with a fixed gap, so you need only one pass and do not have to count the
length first.</p>
<h4>The rules</h4>
<ul>
<li><code>list_middle</code>: for an odd length, the middle node. For an even length, the <b>second</b> of the
two middle nodes.</li>
<li><code>kth_from_end</code>: <code>k</code> = 1 is the last node, <code>k</code> = 2 the one before it,
and so on. If <code>k</code> is larger than the length, return <code>NULL</code>.</li>
<li>Both return <code>NULL</code> for an empty list (<code>head == NULL</code>).</li>
</ul>
<h4>Middle: slow and fast</h4>
<p><code>fast</code> moves two steps for every one step of <code>slow</code>. When <code>fast</code> cannot
move two more steps, <code>slow</code> is in the middle.</p>
<pre>4 nodes:   [0] --&gt; [1] --&gt; [2] --&gt; [3] --&gt; NULL
start      s,f
round 1            s        f
round 2                     s                f = NULL: stop, answer node 2</pre>
<table>
<tr><th>Length</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr>
<tr><td>Middle node (counting from 0)</td><td>0</td><td>1</td><td>1</td><td>2</td><td>2</td><td>3</td></tr>
</table>
<h4>k-th from the end: a lead with a gap of k</h4>
<p>Move <code>lead</code> forward <code>k</code> steps first. Then move <code>lead</code> and
<code>trail</code> together until <code>lead</code> falls off the end (becomes <code>NULL</code>).
<code>trail</code> is then <code>k</code> nodes from the end.</p>
<pre>5 nodes, k = 2:   [0] --&gt; [1] --&gt; [2] --&gt; [3] --&gt; [4] --&gt; NULL
lead moves 2:      t                L
together:                  t                L
                                   t                L
                                           t                L = NULL
answer: node 3 (the 2nd from the end)</pre>
<table>
<tr><th>List</th><th>k</th><th>Returns</th></tr>
<tr><td>5 nodes (0..4)</td><td>1</td><td>node 4 (the last)</td></tr>
<tr><td>5 nodes</td><td>2</td><td>node 3</td></tr>
<tr><td>5 nodes</td><td>5</td><td>node 0 (the head)</td></tr>
<tr><td>5 nodes</td><td>6</td><td><code>NULL</code> (fewer than 6 nodes)</td></tr>
<tr><td>empty</td><td>1</td><td><code>NULL</code></td></tr>
</table>
<p>The tests use lists of 1 to 500 nodes and every k from 1 to length + 1 (some skipped in the middle).
Nodes are checked by address.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>For the middle, use the loop condition "<code>fast</code> is not NULL and <code>fast-&gt;next</code> is
not NULL". Check your stopping point with lengths 1, 2, 3 and 4 on paper.</li>
<li>For k-th from the end, while moving <code>lead</code> the first <code>k</code> steps, check for
<code>NULL</code> <b>before</b> each step: that is how you notice <code>k</code> &gt; length.</li>
</ol>
</details>""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

struct Node *list_middle(struct Node *head)
{
    return NULL;
}

struct Node *kth_from_end(struct Node *head, int k)
{
    return NULL;
}
""",
r"""#include <stddef.h>

struct Node {
    int value;
    struct Node *next;
};

struct Node *list_middle(struct Node *head)
{
    struct Node *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

struct Node *kth_from_end(struct Node *head, int k)
{
    struct Node *lead = head, *trail = head;
    for (int i = 0; i < k; i++) {
        if (lead == NULL)
            return NULL;            /* fewer than k nodes */
        lead = lead->next;
    }
    while (lead) {
        lead = lead->next;
        trail = trail->next;
    }
    return trail;
}
""",
r"""#include "check.h"
#include "solution.c"
static struct Node pool[500];
int main(void)
{
    char d[96];
    ck_true("list_middle(NULL)", list_middle(NULL) == NULL);
    ck_true("kth_from_end(NULL, 1)", kth_from_end(NULL, 1) == NULL);
    for (int n = 1; n <= 500; n += (n < 12 ? 1 : 37)) {
        for (int i = 0; i < n; i++) { pool[i].value = i; pool[i].next = i + 1 < n ? &pool[i + 1] : NULL; }
        struct Node *m = list_middle(&pool[0]);
        CK_FMT(d, "list_middle of %d nodes (index)", n); ck_int(d, m ? (int)(m - pool) : -1, n / 2);
        for (int k = 1; k <= n + 1; k += (k < 4 || k > n - 3 ? 1 : 11)) {
            struct Node *r = kth_from_end(&pool[0], k);
            CK_FMT(d, "kth_from_end(%d nodes, k = %d) (index)", n, k); ck_int(d, r ? (int)(r - pool) : -1, k <= n ? n - k : -1);
        }
    }
    return ck_done();
}
""",
"Middle: slow/fast loop while (fast && fast->next). k-th from end: advance lead k times (return NULL if it runs out), then advance both until lead is NULL; trail is the answer."))

add(P("reverse_words", S, "Reverse the words in place", "c", "func",
r"""<p><b>What to write.</b> <code>void reverse_words(char *s)</code>. Reverse the <b>order of the words</b> in the
string, in place (inside the same array, without a second string). The letters of each word stay in their
normal order.</p>
<p><b>Why it matters.</b> A favourite string question, because the clean solution uses a neat trick and no
extra memory.</p>
<h4>The input</h4>
<ul>
<li>Words are separated by <b>single spaces</b>. There are no spaces at the start or the end.</li>
<li>The string can be one word, or empty (<code>""</code>).</li>
<li>The tests use up to 25 words, each up to 10 characters.</li>
</ul>
<h4>The trick: two reversals</h4>
<ol>
<li>Reverse the <b>whole string</b>, character by character. Now the words are in the right order, but each
word is spelled backwards.</li>
<li>Reverse <b>each word</b> on its own. Now every word reads correctly again.</li>
</ol>
<pre>start:                 "the quick brown fox"
1. reverse everything: "xof nworb kciuq eht"
2. reverse each word:  "fox brown quick the"     &lt;- the answer</pre>
<h4>Examples</h4>
<table>
<tr><th>Before</th><th>After</th></tr>
<tr><td><code>"the quick brown fox"</code></td><td><code>"fox brown quick the"</code></td></tr>
<tr><td><code>"modem DSP"</code></td><td><code>"DSP modem"</code></td></tr>
<tr><td><code>"single"</code></td><td><code>"single"</code> (one word: nothing changes)</td></tr>
<tr><td><code>""</code></td><td><code>""</code></td></tr>
</table>
<h4>Picture of reversing a range in place</h4>
<pre>  l                 r      swap s[l] and s[r], then l moves right
  v                 v      and r moves left; stop when they meet
 [x][o][f][ ][n] ...       or cross</pre>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a small helper that reverses the characters between two positions (or two pointers).</li>
<li>Use it once on the whole string (you need its length).</li>
<li>Then walk through the string and remember where the current word started. When you reach a space or the
<code>'\0'</code> at the end, reverse that word. Do not forget the last word, which ends at
<code>'\0'</code>, not at a space.</li>
</ol>
</details>""",
r"""void reverse_words(char *s)
{
}
""",
r"""#include <string.h>

static void reverse_range(char *a, char *b)    /* reverses [a, b) */
{
    while (b - a > 1) {
        char t = *a;
        *a++ = *--b;
        *b = t;
    }
}

void reverse_words(char *s)
{
    size_t n = strlen(s);
    reverse_range(s, s + n);
    char *w = s;
    for (char *p = s;; p++) {
        if (*p == ' ' || *p == '\0') {
            reverse_range(w, p);
            if (*p == '\0')
                break;
            w = p + 1;
        }
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    static const char *dict[] = {"a", "to", "fox", "SoC", "modem", "Qualcomm", "Snapdragon", "x", "DSP", "bus"};
    char s[400], want[400], orig[400];
    strcpy(s, "the quick brown fox");
    reverse_words(s);
    ck_str("reverse_words(\"the quick brown fox\")", s, "fox brown quick the");
    strcpy(s, "single"); reverse_words(s); ck_str("reverse_words(\"single\")", s, "single");
    strcpy(s, ""); reverse_words(s); ck_str("reverse_words(\"\")", s, "");
    for (int t = 0; t < 200; t++) {
        int nw = ck_range(1, 25), idx[25];
        for (int i = 0; i < nw; i++) idx[i] = ck_range(0, 9);
        orig[0] = want[0] = 0;
        for (int i = 0; i < nw; i++) { if (i) strcat(orig, " "); strcat(orig, dict[idx[i]]); }
        for (int i = nw - 1; i >= 0; i--) { strcat(want, dict[idx[i]]); if (i) strcat(want, " "); }
        strcpy(s, orig);
        reverse_words(s);
        char what[480];
        CK_FMT(what, "reverse_words(\"%.60s%s\")", orig, strlen(orig) > 60 ? "..." : "");
        ck_str(what, s, want);
    }
    return ck_done();
}
""",
"Write a helper that reverses the characters between two pointers. Reverse the whole string, then walk it and reverse each run of characters between spaces."))

add(P("eval_postfix", S, "Evaluate a postfix expression", "c", "func",
r"""<p><b>What to write.</b> <code>int eval_postfix(const char *expr)</code>: evaluate an arithmetic expression
written in <b>postfix</b> notation and return its value.</p>
<p><b>Why it matters.</b> Postfix (also called reverse Polish notation) needs no brackets and no precedence
rules, so a computer can evaluate it with one simple stack. It is a classic stack question.</p>
<h4>How postfix works</h4>
<p>The operator comes <b>after</b> its two operands. "3 + 4" is written <code>3 4 +</code>, and
"(5 + 3) &times; (8 &minus; 2)" is written <code>5 3 + 8 2 - *</code>.</p>
<p>Read the tokens from left to right:</p>
<ul>
<li>A <b>number</b>: push it on the stack.</li>
<li>An <b>operator</b>: pop the top value (call it <i>b</i>), pop the next one (<i>a</i>), compute
<i>a</i> op <i>b</i>, and push the result. Note the order: the first value popped is the <b>right</b>
operand.</li>
<li>At the end, the single value left on the stack is the answer.</li>
</ul>
<h4>Trace of <code>"5 3 + 8 2 - *"</code></h4>
<table>
<tr><th>Token</th><th>Action</th><th>Stack afterwards (top on the right)</th></tr>
<tr><td>5</td><td>push</td><td>5</td></tr>
<tr><td>3</td><td>push</td><td>5 3</td></tr>
<tr><td>+</td><td>pop 3 and 5, push 5 + 3 = 8</td><td>8</td></tr>
<tr><td>8</td><td>push</td><td>8 8</td></tr>
<tr><td>2</td><td>push</td><td>8 8 2</td></tr>
<tr><td>-</td><td>pop 2 and 8, push 8 &minus; 2 = 6</td><td>8 6</td></tr>
<tr><td>*</td><td>pop 6 and 8, push 8 &times; 6 = 48</td><td>48</td></tr>
</table>
<h4>Examples</h4>
<table>
<tr><th>Expression</th><th>Returns</th><th>Note</th></tr>
<tr><td><code>"5 3 + 8 2 - *"</code></td><td>48</td><td>(5 + 3) &times; (8 &minus; 2)</td></tr>
<tr><td><code>"7 2 /"</code></td><td>3</td><td>integer division drops the fraction</td></tr>
<tr><td><code>"2 7 -"</code></td><td>&minus;5</td><td>2 &minus; 7, not 7 &minus; 2</td></tr>
<tr><td><code>"1 8 - 2 /"</code></td><td>&minus;3</td><td>&minus;7 / 2 = &minus;3.5, truncated towards zero</td></tr>
<tr><td><code>"42"</code></td><td>42</td><td>a single number</td></tr>
<tr><td><code>"1000000 3 /"</code></td><td>333333</td><td>numbers can have many digits</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li>Tokens are separated by single spaces. Numbers are non-negative integers written with digits only (a
negative value can only appear as a result).</li>
<li>Operators: <code>+ - * /</code>. <code>/</code> truncates towards zero, like C's <code>/</code>; the
divisor is never 0.</li>
<li>Every intermediate value fits in an <code>int</code>, and at most 64 values are on the stack. The input
is always a valid expression.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Use an <code>int</code> array of 64 entries as the stack, with a counter for its height.</li>
<li>Walk through the string one character at a time. A digit starts a number: keep reading digits and build
the value (value &times; 10 + next digit). A space is skipped. Anything else is an operator.</li>
<li>For an operator, be careful with the pop order: pop <i>b</i> first, then <i>a</i>.</li>
</ol>
</details>""",
r"""int eval_postfix(const char *expr)
{
    return 0;
}
""",
r"""int eval_postfix(const char *expr)
{
    int stack[64], top = 0;
    const char *p = expr;
    while (*p) {
        if (*p == ' ') {
            p++;
        } else if (*p >= '0' && *p <= '9') {
            int v = 0;
            while (*p >= '0' && *p <= '9')
                v = v * 10 + (*p++ - '0');
            stack[top++] = v;
        } else {
            int b = stack[--top], a = stack[--top];
            switch (*p++) {
            case '+': stack[top++] = a + b; break;
            case '-': stack[top++] = a - b; break;
            case '*': stack[top++] = a * b; break;
            default:  stack[top++] = a / b; break;
            }
        }
    }
    return stack[0];
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[700], e[600];
    ck_int("eval_postfix(\"5 3 + 8 2 - *\")", eval_postfix("5 3 + 8 2 - *"), 48);
    ck_int("eval_postfix(\"7 2 /\")", eval_postfix("7 2 /"), 3);
    ck_int("eval_postfix(\"2 7 -\")", eval_postfix("2 7 -"), -5);
    ck_int("eval_postfix(\"42\")", eval_postfix("42"), 42);
    ck_int("eval_postfix(\"1000000 3 /\")", eval_postfix("1000000 3 /"), 333333);
    for (int t = 0; t < 300; t++) {
        long long st[64]; int top = 0, len = 0, tokens = ck_range(1, 40);
        e[0] = 0;
        for (int k = 0; k < tokens || top > 1; k++) {
            int push = top < 2 || (k < tokens && top < 60 && ck_range(0, 2) == 0);
            if (len) e[len++] = ' ';
            if (push) { int v = ck_range(0, k % 5 == 0 ? 9999 : 20); st[top++] = v; len += snprintf(e + len, sizeof e - (size_t)len, "%d", v); }
            else {
                long long b = st[--top], a = st[--top], r;
                char op = "+-*/"[ck_range(0, 3)];
                if (op == '/' && b == 0) op = '+';
                if (op == '*' && (a * b > 1000000 || a * b < -1000000)) op = '-';
                r = op == '+' ? a + b : op == '-' ? a - b : op == '*' ? a * b : a / b;
                st[top++] = r;
                e[len++] = op; e[len] = 0;
            }
        }
        CK_FMT(d, "eval_postfix(\"%s\")", e);
        ck_int(d, eval_postfix(e), st[0]);
    }
    return ck_done();
}
""",
"An int array as the stack. Walk the string: skip spaces; read a number digit by digit and push it; for an operator pop b, then a, and push a op b. The answer is the last value left."))

add(P("find_substr", S, "Find a substring (strstr)", "c", "func",
r"""<p><b>What to write.</b> <code>int find_substr(const char *hay, const char *needle)</code>. Return the index of
the first place where the string <code>needle</code> occurs inside the string <code>hay</code>, or
&minus;1 if it does not occur. Do not call <code>strstr</code> (that is the library function you are
re-writing).</p>
<p><b>Why it matters.</b> A basic string question that tests careful loop limits and the empty-string
cases.</p>
<h4>The idea (the simple method)</h4>
<p>Try every starting position <code>i</code> in <code>hay</code>. At each one, compare
<code>needle[k]</code> with <code>hay[i + k]</code> for k = 0, 1, 2, ... If you reach the end of
<code>needle</code> without a mismatch, <code>i</code> is the answer. If a character differs, give up on this
<code>i</code> and try the next one.</p>
<h4>Picture: <code>find_substr("aaab", "aab")</code> = 1</h4>
<pre>i = 0:   hay:    a a a b
         needle: a a b      k=0 a=a, k=1 a=a, k=2 a vs b: differ, next i
i = 1:   hay:    a a a b
         needle:   a a b    k=0 a=a, k=1 a=a, k=2 b=b: needle ends, return 1</pre>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Returns</th><th>Why</th></tr>
<tr><td><code>find_substr("snapdragon", "drag")</code></td><td>4</td><td>s n a p <b>d r a g</b> o n: "drag" starts at index 4</td></tr>
<tr><td><code>find_substr("modem", "mode")</code></td><td>0</td><td>at the very start</td></tr>
<tr><td><code>find_substr("modem", "dems")</code></td><td>&minus;1</td><td>"dem" matches at index 2, but then <code>hay</code> ends before the "s"</td></tr>
<tr><td><code>find_substr("abc", "")</code></td><td>0</td><td>an empty needle matches at 0</td></tr>
<tr><td><code>find_substr("", "")</code></td><td>0</td><td>also an empty needle</td></tr>
<tr><td><code>find_substr("", "a")</code></td><td>&minus;1</td><td>nothing to search in</td></tr>
</table>
<p>The tests use random strings of up to 100 letters from a small alphabet (2 to 4 letters), so many
partial matches happen.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>When does the inner comparison stop? Either the needle has ended (success) or the characters differ.
Note that if <code>hay</code> ends first, its <code>'\0'</code> differs from the needle's next letter, so
that case stops by itself.</li>
<li>When should the outer loop give up? Once the starting position is at the <code>'\0'</code> of
<code>hay</code> and the needle did not match there, there are no more starting positions.</li>
<li>Check your code with the empty-needle cases.</li>
</ol>
</details>""",
r"""int find_substr(const char *hay, const char *needle)
{
    return -1;
}
""",
r"""int find_substr(const char *hay, const char *needle)
{
    for (int i = 0;; i++) {
        int k = 0;
        while (needle[k] && hay[i + k] == needle[k])
            k++;
        if (needle[k] == '\0')
            return i;
        if (hay[i] == '\0')     /* no more starting points */
            return -1;
    }
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[200], h[120], nd[20];
    ck_int("find_substr(\"snapdragon\", \"drag\")", find_substr("snapdragon", "drag"), 4);
    ck_int("find_substr(\"modem\", \"mode\")", find_substr("modem", "mode"), 0);
    ck_int("find_substr(\"modem\", \"dems\")", find_substr("modem", "dems"), -1);
    ck_int("find_substr(\"abc\", \"\")", find_substr("abc", ""), 0);
    ck_int("find_substr(\"\", \"\")", find_substr("", ""), 0);
    ck_int("find_substr(\"\", \"a\")", find_substr("", "a"), -1);
    ck_int("find_substr(\"aaab\", \"aab\")", find_substr("aaab", "aab"), 1);
    for (int t = 0; t < 400; t++) {
        int hn = ck_range(0, 100), nn = ck_range(1, 6), al = ck_range(2, 4);
        for (int i = 0; i < hn; i++) h[i] = (char)('a' + ck_range(0, al - 1));
        h[hn] = 0;
        for (int i = 0; i < nn; i++) nd[i] = (char)('a' + ck_range(0, al - 1));
        nd[nn] = 0;
        const char *r = strstr(h, nd);
        CK_FMT(d, "find_substr(\"%s\", \"%s\")", h, nd);
        ck_int(d, find_substr(h, nd), r ? (int)(r - h) : -1);
    }
    return ck_done();
}
""",
"For each start i, compare characters while needle[k] matches hay[i+k]. If you reach the end of needle, return i. Stop with -1 once hay[i] is the terminator."))

add(P("rotate_array", S, "Rotate an array in place", "c", "func",
r"""<p><b>What to write.</b> <code>void rotate_right(int *a, int n, int k)</code>. Move every element
<code>k</code> places to the right. Elements that fall off the end come back in at the start (they "wrap
around"). Use O(1) extra memory: a few variables, no second array.</p>
<p><b>Why it matters.</b> Rotating a buffer in place is common in embedded code (circular buffers), and the
reversal trick is a well-known interview answer.</p>
<h4>What "rotate right by k" means</h4>
<pre>index:        0  1  2  3  4
before:       1  2  3  4  5       k = 2
after:        4  5  1  2  3       (the element at index i moves
                                   to index (i + k) % n)</pre>
<h4>The trick: three reversals</h4>
<pre>start:                    1  2  3  4  5      k = 2
1. reverse the whole:     5  4  3  2  1
2. reverse the first k:   4  5 | 3  2  1
3. reverse the rest:      4  5 | 1  2  3      done</pre>
<p>Why it works: after step 1, the last <code>k</code> elements (4 5) are at the front, but backwards; the
other elements are behind them, also backwards. Steps 2 and 3 turn each group the right way round.</p>
<h4>Examples</h4>
<table>
<tr><th>Array</th><th>k</th><th>Result</th><th>Note</th></tr>
<tr><td>{1, 2, 3, 4, 5}</td><td>2</td><td>{4, 5, 1, 2, 3}</td><td></td></tr>
<tr><td>{1, 2, 3, 4, 5}</td><td>7</td><td>{4, 5, 1, 2, 3}</td><td>7 places = one full turn (5) + 2</td></tr>
<tr><td>{1, 2, 3, 4, 5}</td><td>5</td><td>{1, 2, 3, 4, 5}</td><td>a full turn changes nothing</td></tr>
<tr><td>{1, 2, 3, 4, 5}</td><td>0</td><td>{1, 2, 3, 4, 5}</td><td></td></tr>
<tr><td>{} (n = 0)</td><td>any</td><td>{}</td><td>must not crash</td></tr>
</table>
<h4>Inputs and limits</h4>
<ul>
<li><code>n</code> is 0 to 1000; <code>k</code> is 0 to 3000, so it can be larger than <code>n</code>.</li>
<li>Reduce <code>k</code> first with <code>k % n</code>. But <code>k % 0</code> is a division by zero, which
stops the program on this site, so handle <code>n == 0</code> before that.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write a helper that reverses <code>a[i..j]</code> by swapping the two ends and moving inwards.</li>
<li>Call it three times with the right ranges. Check the ranges on the example: what are they for
<code>n</code> = 5 and <code>k</code> = 2?</li>
<li>What happens to your ranges when <code>k</code> is 0 after reducing? Make sure an empty range does
nothing.</li>
</ol>
</details>""",
r"""void rotate_right(int *a, int n, int k)
{
}
""",
r"""static void rev(int *a, int i, int j)
{
    for (; i < j; i++, j--) {
        int t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
}

void rotate_right(int *a, int n, int k)
{
    if (n == 0)
        return;
    k %= n;
    rev(a, 0, n - 1);
    rev(a, 0, k - 1);
    rev(a, k, n - 1);
}
""",
r"""#include "check.h"
#include "solution.c"
int main(void)
{
    char d[96];
    static int a[1000], w[1000];
    int ex[] = {1, 2, 3, 4, 5}, exw[] = {4, 5, 1, 2, 3};
    rotate_right(ex, 5, 2);
    ck_true("rotate_right({1, 2, 3, 4, 5}, k = 2)", memcmp(ex, exw, sizeof ex) == 0);
    for (int t = 0; t < 300; t++) {
        int n = t < 2 ? t : ck_range(1, 1000), k = ck_range(0, 3000);
        for (int i = 0; i < n; i++) a[i] = i * 7 + 1;
        for (int i = 0; i < n; i++) w[(i + k) % n] = a[i];
        rotate_right(a, n, k);
        int i = 0;
        while (i < n && a[i] == w[i]) i++;
        CK_FMT(d, "rotate_right(n = %d, k = %d): element %d", n, k, i < n ? i : 0);
        if (i < n) ck_int(d, a[i], w[i]); else ck_true(d, 1);
    }
    return ck_done();
}
""",
"k %= n (watch n == 0). Reverse a[0..n-1], then a[0..k-1], then a[k..n-1]."))

add(P("missing_number", S, "The missing number", "c", "func",
r"""<p><b>What to write.</b> <code>int missing_number(const int *a, int n)</code>. The array <code>a</code> holds
<code>n</code> different numbers taken from 0, 1, 2, ..., <code>n</code>. That range has
<code>n</code>&nbsp;+&nbsp;1 numbers, so exactly one is missing. Return it, using one pass over the array
and O(1) extra memory.</p>
<p><b>Why it matters.</b> A classic interview question with two neat answers: one with a sum, one with XOR.</p>
<h4>Example: {3, 0, 1} (n = 3)</h4>
<p>The numbers should be 0, 1, 2, 3. The array has 3, 0 and 1, so the answer is 2.</p>
<h4>Method 1: sum</h4>
<p>0 + 1 + ... + n = n(n+1)/2. Subtract the sum of the array.</p>
<pre>n = 3:   0+1+2+3 = 6,   3+0+1 = 4,   6 - 4 = 2</pre>
<p>Watch out: the tests use <code>n</code> up to 200,000, and 200,000 &times; 200,001 / 2 = 20,000,100,000,
which is far more than the largest <code>int</code> (2,147,483,647). With this method you need a
<code>long long</code>.</p>
<h4>Method 2: XOR (no overflow possible)</h4>
<p>XOR facts: <code>x ^ x = 0</code>, <code>x ^ 0 = x</code>, and the order of XORs does not matter. XOR all
the numbers 0..n together with all the array values. Every number that is present appears twice and cancels;
only the missing one is left.</p>
<pre>should be:  0 ^ 1 ^ 2 ^ 3
array:      3 ^ 0 ^ 1
all of it:  0^0  1^1  3^3  2   -&gt;  0 ^ 0 ^ 0 ^ 2 = 2</pre>
<p>Handy detail: the indexes 0..n&minus;1 of the array plus the number <code>n</code> are exactly the numbers
0..n, so you can XOR them in the same loop.</p>
<h4>More examples</h4>
<table>
<tr><th>Array</th><th>n</th><th>Returns</th></tr>
<tr><td>{0}</td><td>1</td><td>1 (the largest number can be the missing one)</td></tr>
<tr><td>{1}</td><td>1</td><td>0 (so can 0)</td></tr>
<tr><td>{0, 1, 2, 4, 5, 6, 3, 8}</td><td>8</td><td>7</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Pick one method. For XOR: start a variable with one of the values you must include, then fold in the
rest inside a single loop over <code>i</code>.</li>
<li>Check with {3, 0, 1} on paper before running.</li>
</ol>
</details>""",
r"""int missing_number(const int *a, int n)
{
    return 0;
}
""",
r"""int missing_number(const int *a, int n)
{
    int x = n;
    for (int i = 0; i < n; i++)
        x ^= i ^ a[i];
    return x;
}
""",
r"""#include "check.h"
#include "solution.c"
static int a[200001];
int main(void)
{
    char d[96];
    int ex[] = {3, 0, 1};
    ck_int("missing_number({3, 0, 1})", missing_number(ex, 3), 2);
    for (int t = 0; t < 40; t++) {
        int n = t < 2 ? t + 1 : ck_range(1, t % 5 == 0 ? 200000 : 50), miss = ck_range(0, n);
        int k = 0;
        for (int v = 0; v <= n; v++) if (v != miss) a[k++] = v;
        for (int i = n - 1; i > 0; i--) { int j = ck_range(0, i), tmp = a[i]; a[i] = a[j]; a[j] = tmp; }
        CK_FMT(d, "n = %d (missing %d)", n, miss);
        ck_int(d, missing_number(a, n), miss);
    }
    return ck_done();
}
""",
"Start with x = n, then x ^= i ^ a[i] for every i. What is left is the missing value."))

add(P("int_to_str", S, "Integer to string (no printf)", "c", "func",
r"""<p><b>What to write.</b> <code>int int_to_str(int x, char *buf)</code>. Write <code>x</code> into
<code>buf</code> as decimal text: a <code>'-'</code> first if <code>x</code> is negative, then the digits,
then <code>'\0'</code>. Return the length of the text (the number of characters, not counting the
<code>'\0'</code>).</p>
<p><b>Why it matters.</b> Small firmware often has no full C library, so it must format numbers itself, for
example to print over a UART. In this problem <code>sprintf</code> and <code>snprintf</code> are blocked.</p>
<h4>The idea: peel off digits</h4>
<ul>
<li><code>u % 10</code> is the <b>last</b> digit of <code>u</code>, and <code>u / 10</code> removes that
digit.</li>
<li>So the digits come out <b>backwards</b> (last digit first). Store them in a small temporary array, then
copy them into <code>buf</code> in reverse order.</li>
<li>ASCII facts: the characters <code>'0'</code> to <code>'9'</code> have codes 48 to 57 in order, so the
character for digit <i>d</i> is <code>'0' + d</code>.</li>
</ul>
<h4>Example: <code>int_to_str(-307, buf)</code> returns 4, <code>buf</code> = "-307"</h4>
<table>
<tr><th>Step</th><th>u</th><th>u % 10</th><th>u / 10</th><th>Digits so far (backwards)</th></tr>
<tr><td>1</td><td>307</td><td>7</td><td>30</td><td>7</td></tr>
<tr><td>2</td><td>30</td><td>0</td><td>3</td><td>7 0</td></tr>
<tr><td>3</td><td>3</td><td>3</td><td>0 (stop)</td><td>7 0 3</td></tr>
</table>
<pre>buf:  [ '-' ][ '3' ][ '0' ][ '7' ][ '\0' ]      length 4
        0      1      2      3      4</pre>
<h4>Examples</h4>
<table>
<tr><th><code>x</code></th><th>Text</th><th>Returns</th></tr>
<tr><td>&minus;307</td><td>"-307"</td><td>4</td></tr>
<tr><td>0</td><td>"0"</td><td>1 (make sure zero still gives one digit)</td></tr>
<tr><td>2147483647 (<code>INT_MAX</code>)</td><td>"2147483647"</td><td>10</td></tr>
<tr><td>&minus;2147483648 (<code>INT_MIN</code>)</td><td>"-2147483648"</td><td>11</td></tr>
</table>
<div class="note"><b>Trap:</b> <code>INT_MIN</code> = &minus;2,147,483,648 has no positive <code>int</code>
partner (the largest <code>int</code> is 2,147,483,647). So <code>-x</code> overflows for it. That is
undefined behaviour, and on this site it stops the program. Work with an <code>unsigned</code> (or
<code>long long</code>) copy of the size of <code>x</code> instead.</div>
<p>The tests use the values above plus 7, 10, &minus;10, 1000000, &minus;1, INT_MIN + 1 and 300 random
values. <code>buf</code> has room for 32 characters.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>First get the size of <code>x</code> without its sign as an <code>unsigned</code> value, in a way that
never computes <code>-x</code> as an <code>int</code>. (Hint: convert to <code>unsigned</code> first, then
negate; unsigned arithmetic wraps around and never overflows.)</li>
<li>Peel digits until the value is 0. Which loop form makes sure that <code>x</code> = 0 still produces one
digit?</li>
<li>Write the <code>'-'</code>, then the digits in reverse, then <code>'\0'</code>, counting as you go.</li>
</ol>
</details>""",
r"""int int_to_str(int x, char *buf)
{
    buf[0] = '\0';
    return 0;
}
""",
r"""int int_to_str(int x, char *buf)
{
    unsigned u = x < 0 ? 0u - (unsigned)x : (unsigned)x;    /* safe even for INT_MIN */
    char tmp[12];
    int n = 0, len = 0;
    do {
        tmp[n++] = (char)('0' + u % 10);
        u /= 10;
    } while (u);
    if (x < 0)
        buf[len++] = '-';
    while (n)
        buf[len++] = tmp[--n];
    buf[len] = '\0';
    return len;
}
""",
r"""#include "check.h"
#include <limits.h>
#define sprintf NO_SPRINTF_IN_THIS_PROBLEM
#define snprintf NO_SNPRINTF_IN_THIS_PROBLEM
#include "solution.c"
#undef sprintf
#undef snprintf
int main(void)
{
    char d[96], buf[32], want[32];
    int v[] = {0, 7, -307, 10, -10, 1000000, INT_MAX, INT_MIN, INT_MIN + 1, -1};
    for (int i = 0; i < 10; i++) {
        int len = snprintf(want, sizeof want, "%d", v[i]);
        memset(buf, 'x', sizeof buf);
        CK_FMT(d, "int_to_str(%d) length", v[i]); ck_int(d, int_to_str(v[i], buf), len);
        buf[31] = 0;
        CK_FMT(d, "int_to_str(%d) text", v[i]); ck_str(d, buf, want);
    }
    for (int t = 0; t < 300; t++) {
        int x = (int)ck_rand() >> ck_range(0, 30);
        int len = snprintf(want, sizeof want, "%d", x);
        memset(buf, 'x', sizeof buf);
        int got = int_to_str(x, buf);
        buf[31] = 0;
        CK_FMT(d, "int_to_str(%d)", x); ck_str(d, buf, want);
        CK_FMT(d, "int_to_str(%d) length", x); ck_int(d, got, len);
    }
    return ck_done();
}
""",
"Take u = x < 0 ? 0u - (unsigned)x : x. Peel digits with u % 10 into a small buffer (they come out backwards), then copy them reversed after an optional '-'."))
