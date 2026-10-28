# Problem bank, part E: embedded C, OS and architecture, sorting, interview classics.
# Topics follow the Qualcomm hardware-engineer study guide (OA programming section and the
# embedded / OS / C questions reported from interviews).
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "Embedded C"

add(P("uart_frame", S, "UART: build a frame", "c", "func",
r"""<p>A UART sends each byte as a <em>frame</em>. The line idles high (1). A frame is one start bit (0), the 8
data bits <b>least significant bit first</b>, an optional parity bit, then 1 or 2 stop bits (1).</p>
<p>Write <code>int uart_frame(uint8_t byte, int parity, int stop_bits, uint8_t bits[12])</code>. It writes the
line level for each bit time into <code>bits</code> and returns the frame length. <code>parity</code> is 0 for
none, 1 for odd, 2 for even. With even parity, the parity bit makes the number of 1s in data + parity even;
with odd parity, it makes it odd.</p>
<pre>uart_frame(0x41, 0, 1, bits) -> 10   bits = 0 1 0 0 0 0 0 1 0 1      ('A', 8N1)
uart_frame(0x41, 2, 1, bits) -> 11   bits = 0 1 0 0 0 0 0 1 0 0 1    (8E1: two 1s, so parity 0)</pre>
<p>Worth knowing for the OA: 8N1 at 115,200 baud sends 10 bit times per byte, so 11,520 bytes/s.</p>""",
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
r"""<p>Now the receiver. <code>line[]</code> holds the line level for <code>n</code> bit times (one sample per
bit). Decode 8N1 frames:</p>
<ol><li>While searching, skip 1s (idle). A 0 is a start bit.</li>
<li>The next 8 samples are the data bits, LSB first; the sample after them is the stop bit.</li>
<li>Stop bit 1: store the byte in <code>out</code> and search again right after the stop bit.</li>
<li>Stop bit 0: a <b>framing error</b>. Count it, drop the byte, and wait until the line is 1 again
(skip the 0s after the stop bit) before searching again.</li>
<li>A frame that would run past the end of <code>line</code> is ignored.</li></ol>
<p>Write <code>int uart_decode(const uint8_t *line, int n, uint8_t *out, int *framing_errors)</code>, which
returns the number of good bytes.</p>
<pre>line = 1 1 0 1 0 0 0 0 0 1 0 1 1      -> 1 byte, 0x41, no errors</pre>""",
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
r"""<p>I2C has two open-drain wires, SCL (clock) and SDA (data), both pulled up. Data may change only while
SCL is low, and the receiver samples SDA when SCL rises. Two patterns break that rule on purpose:</p>
<ul><li><b>START</b>: SDA falls while SCL stays high.</li>
<li><b>STOP</b>: SDA rises while SCL stays high.</li></ul>
<p>You get <code>n</code> samples of each wire. Write <code>int i2c_decode(const uint8_t *scl, const uint8_t *sda,
int n, char *out)</code>. For each <code>i</code> from 1 to <code>n &minus; 1</code>, check these rules in order:</p>
<ol><li>SCL rose (<code>scl[i-1] == 0</code>, <code>scl[i] == 1</code>): append <code>'0'</code> or
<code>'1'</code>, the value of <code>sda[i]</code>.</li>
<li>Otherwise, if SCL was high in both samples and SDA fell: append <code>'S'</code>.</li>
<li>Otherwise, if SCL was high in both samples and SDA rose: append <code>'P'</code>.</li></ol>
<p>End <code>out</code> with <code>'\0'</code> and return its length.</p>
<pre>scl: 1 1 0 1 0 1 0 1 1
sda: 1 0 0 1 1 0 0 0 1      -> "S100P"</pre>
<p>These simple rules also count the clock pulse just before a STOP as a bit (the last <code>0</code> in the
example); a real decoder knows the frame layout and drops it. In a real transfer, the first byte after START is the 7-bit address shifted left, plus R/W in bit 0
(0 = write), and every byte is followed by an ACK bit (0 = acknowledged).</p>""",
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
r"""<p>A CRC is the remainder of a polynomial division over bits. It protects UART packets, flash images and
radio frames. Write <code>uint16_t crc16_ccitt(const uint8_t *data, int n)</code> for CRC-16/CCITT-FALSE:</p>
<ul><li>polynomial 0x1021 (x<sup>16</sup> + x<sup>12</sup> + x<sup>5</sup> + 1), initial value 0xFFFF;</li>
<li>bytes are processed most significant bit first, with no reflection and no final XOR.</li></ul>
<p>Bit by bit: XOR the next byte into the <em>top</em> 8 bits of the CRC, then 8 times: if the top bit is 1,
shift left and XOR with 0x1021; otherwise just shift left.</p>
<pre>crc16_ccitt("123456789", 9) -> 0x29B1   (the standard check value)
crc16_ccitt(anything, 0)    -> 0xFFFF</pre>""",
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
r"""<p>ECC memory corrects single bit flips (the "EDAC" interview question). The smallest example is the Hamming
(7,4) code: 4 data bits plus 3 parity bits. Number the codeword positions 1 to 7; position <i>k</i> is bit
<i>k</i>&minus;1 of the byte.</p>
<ul><li>The data bits d1..d4 (bits 0..3 of the nibble) go to positions 3, 5, 6 and 7.</li>
<li>The parity bit at position 1 makes positions 1, 3, 5, 7 even; position 2 covers 2, 3, 6, 7; position 4
covers 4, 5, 6, 7. (Each parity bit covers the positions whose number has that bit set.)</li></ul>
<p>Decoding: XOR together the position numbers of all the 1 bits. That is the <b>syndrome</b>. 0 means no
error; otherwise it is the position of the flipped bit.</p>
<pre>uint8_t ham_encode(uint8_t nibble);               // ham_encode(0xB) -> 0x55
uint8_t ham_decode(uint8_t cw, int *fixed_pos);   // returns the nibble; *fixed_pos = 0 or the bit position corrected</pre>""",
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
r"""<p>A mechanical button bounces for a few milliseconds when pressed. Firmware samples it every millisecond
and accepts a new level only after it has been <b>stable for <code>n</code> samples</b>.</p>
<pre>struct Debounce { int state; int count; };
void debounce_init(struct Debounce *d, int initial);        // state = initial, count = 0
int  debounce_step(struct Debounce *d, int raw, int n);     // returns the debounced state</pre>
<p>Rule for each sample: if <code>raw</code> equals <code>state</code>, reset <code>count</code> to 0.
Otherwise increment <code>count</code>; when it reaches <code>n</code>, set <code>state = raw</code> and
<code>count = 0</code>.</p>
<pre>n = 3, state 0, raw: 1 0 1 1 1 0 0 1 1 1 1
output:              0 0 0 0 1 1 1 1 1 1 1</pre>""",
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
r"""<p>A watchdog timer resets the chip unless the software "kicks" it in time, so a hung program recovers by
itself. (It was asked in both 2026 Qualcomm interview rounds.) A <em>windowed</em> watchdog also resets the chip
if a kick comes <b>too early</b>, which catches code stuck in a tight loop that keeps kicking.</p>
<p>Write <code>int wdt_first_reset(const int *kicks, int nk, int timeout, int window, int end)</code>. Time 0
counts as the last kick. Then, for each kick time <code>t</code> in order (strictly increasing):</p>
<ul><li>if <code>t &minus; last &gt;= timeout</code>, the chip already reset at <code>last + timeout</code>;</li>
<li>else if <code>t &minus; last &lt; window</code>, the kick is too early: reset at <code>t</code>;</li>
<li>otherwise <code>last = t</code>.</li></ul>
<p>After the last kick, a reset happens at <code>last + timeout</code> if that is <code>&lt;= end</code>. Return
the time of the first reset, or &minus;1 if there is none.</p>
<pre>timeout 100, window 0,  kicks 50 120 250, end 1000 -> 220
timeout 100, window 30, kicks 50 60,      end 1000 -> 60   (too early)
timeout 100, window 30, kicks 50 90,      end 150  -> -1</pre>""",
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
r"""<p>An interrupt controller has a 32-bit <em>pending</em> register: bit <i>k</i> set means IRQ <i>k</i> is
waiting. The firmware keeps a vector table: an array of function pointers, one per IRQ.</p>
<pre>typedef void (*isr_t)(int irq);
void irq_register(int irq, isr_t handler);        // NULL removes a handler
int  irq_dispatch(volatile uint32_t *pending);    // returns how many handlers were called</pre>
<p><code>irq_dispatch</code> repeats until <code>*pending</code> is 0: take the <b>lowest</b> set bit (the
highest priority), clear it, then call its handler if there is one. A pending IRQ with no handler is just
cleared (a spurious interrupt). Read <code>*pending</code> again every time, because a handler may raise a new
interrupt. That is also why the register is <code>volatile</code>.</p>""",
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
r"""<p>Embedded and real-time code avoids <code>malloc</code>: it can be slow, it fragments the heap, and it can
fail at the worst moment. A common replacement is a pool of equal-sized blocks with a <b>free list</b>, where
each free block stores a pointer to the next free block inside itself. Allocation and free are O(1).</p>
<pre>#define BLOCK_SIZE 32
#define NUM_BLOCKS 16
void  pool_init(void);         // every block free
void *pool_alloc(void);        // NULL when all 16 are in use
void  pool_free(void *p);      // p came from pool_alloc</pre>
<p>Use a static array for the memory (no <code>malloc</code>). The tests write all 32 bytes of every block,
so blocks must not overlap.</p>""",
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
r"""<p>In Gray code, consecutive numbers differ in exactly one bit. Async FIFOs send their read and write
pointers across clock domains in Gray code, so a pointer sampled mid-change is either the old value or the new
one, never a mix.</p>
<pre>uint32_t bin_to_gray(uint32_t b);    // 5 (101) -> 7 (111)
uint32_t gray_to_bin(uint32_t g);    // 7 (111) -> 5 (101)</pre>
<p>Binary to Gray is one line. Going back, each binary bit is the XOR of all Gray bits at or above it.</p>""",
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
r"""<p>A cache splits an address into <b>tag | index | offset</b>. The offset picks a byte in the line, the index
picks a set, and the tag is everything left over.</p>
<pre>void cache_bits(int addr_bits, int cache_bytes, int line_bytes, int ways,
                int *tag, int *index, int *offset);</pre>
<p>All sizes are powers of two. Lines = cache_bytes / line_bytes, and sets = lines / ways. A fully associative
cache has ways = lines, so 1 set and 0 index bits.</p>
<pre>32-bit address, 32 KB, 2-way, 32-byte lines -> tag 18, index 9, offset 5</pre>""",
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
r"""<p>Simulate a cache on a list of byte addresses and count the hits.</p>
<pre>int cache_hits(const uint32_t *addr, int n, int sets, int ways, int line_bytes);</pre>
<ul><li>Line number = addr / line_bytes; set = line % sets; tag = line / sets.</li>
<li>The cache starts empty. On a miss in a full set, evict the <b>least recently used</b> line of that set.</li>
<li><code>sets</code> &le; 1024, <code>ways</code> &le; 16, sets &times; ways &le; 4096.</li></ul>
<pre>sets 4, ways 1, 16-byte lines, addresses 0 4 64 0  -> 1 hit   (64 maps to set 0 and evicts 0)
sets 4, ways 2, 16-byte lines, addresses 0 4 64 0  -> 2 hits</pre>""",
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
r"""<p>A 32-bit virtual address with 4 KB pages and a two-level page table is split as
<b>10 bits | 10 bits | 12 bits</b>: page-directory index, page-table index, offset.</p>
<pre>int64_t vm_translate(uint32_t *const *dir, uint32_t va);</pre>
<ul><li><code>dir</code> has 1024 entries. <code>dir[i] == NULL</code> means that page table is not present.</li>
<li>A page table has 1024 entries (<code>uint32_t</code>). Bit 0 is <em>present</em>; bits 31..12 are the
physical frame number.</li>
<li>Physical address = (frame &lt;&lt; 12) | offset. Return &minus;1 for a page fault (no table, or entry not
present).</li></ul>
<pre>va 0x00403ABC: directory 1, table 3, offset 0xABC.  If dir[1][3] = 0x12345001, pa = 0x12345ABC.</pre>""",
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
r"""<p>Count page faults for a reference string with <code>frames</code> physical frames (1 to 16), starting
empty.</p>
<pre>int faults_fifo(const int *refs, int n, int frames);   // evict the page loaded earliest
int faults_lru(const int *refs, int n, int frames);    // evict the page used longest ago</pre>
<pre>refs 7 0 1 2 0 3 0 4 2 3 0 3 2, 3 frames  -> FIFO 10, LRU 9
refs 1 2 3 4 1 2 5 1 2 3 4 5, FIFO         -> 3 frames: 9, 4 frames: 10   (Belady's anomaly)</pre>
<p>A hit changes nothing for FIFO, but for LRU it makes that page the most recently used.</p>""",
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
r"""<p>The optimal policy (Belady's MIN) evicts the page whose next use is <b>farthest in the future</b>, or one
that is never used again. No real OS can do it, since it needs the future, but it gives the lower bound
that other policies are compared with.</p>
<pre>int faults_opt(const int *refs, int n, int frames);    // frames 1..16, start empty
refs 7 0 1 2 0 3 0 4 2 3 0 3 2, 3 frames -> 7</pre>""",
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
r"""<p>Processes are numbered in order of arrival (<code>arrival</code> is non-decreasing). Each needs
<code>burst[i]</code> units of CPU. Both policies are non-preemptive: once a process starts, it runs to the
end. Waiting time = start time &minus; arrival time. Return the <b>total</b> waiting time.</p>
<pre>int fcfs_wait(const int *arrival, const int *burst, int n);   // run in arrival order
int sjf_wait(const int *arrival, const int *burst, int n);    // shortest job among those that have arrived</pre>
<p>For SJF, break ties by earlier arrival, then by lower index. If the CPU is idle and nothing has arrived,
time jumps to the next arrival.</p>
<pre>arrival 0 1 2 3, burst 8 4 9 5:  FCFS 0+7+10+18 = 35 (avg 8.75),  SJF 0+7+15+9 = 31 (avg 7.75)</pre>""",
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
r"""<p>Round robin keeps a FIFO ready queue and gives each process at most <code>quantum</code> units, then
moves it to the back of the queue.</p>
<pre>void rr_finish(const int *arrival, const int *burst, int n, int quantum, int *finish);</pre>
<ul><li>Processes are numbered by arrival (<code>arrival</code> is non-decreasing); bursts are &ge; 1.</li>
<li>When a slice ends at time <i>t</i>, first add every process with arrival &le; <i>t</i> to the queue (in
index order), <b>then</b> put the preempted process at the back. (This is the usual textbook convention.)</li>
<li>If the queue is empty, time jumps to the next arrival.</li>
<li>Write each process's completion time into <code>finish</code>.</li></ul>
<pre>arrival 0 0 0, burst 5 3 1, quantum 2 -> finish 9 8 5
(P0 0-2, P1 2-4, P2 4-5, P0 5-7, P1 7-8, P0 8-9)</pre>
<p>Turnaround = finish &minus; arrival; waiting = turnaround &minus; burst.</p>""",
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
r"""<p>The banker's algorithm checks whether the system is in a <b>safe state</b>: is there an order in which
every process can get its maximum demand and finish?</p>
<pre>int bankers_safe(int n, int m, const int *avail, const int *max, const int *alloc, int *order);</pre>
<ul><li><code>n</code> processes, <code>m</code> resource types; <code>max</code> and <code>alloc</code> are
n &times; m, row-major. need = max &minus; alloc.</li>
<li>Start with work = avail. Repeatedly pick the <b>lowest-index</b> unfinished process whose need &le; work in
every resource, finish it (work += its alloc), append it to <code>order</code>, and start the search again
from index 0.</li>
<li>Return 1 if every process finishes (safe), else 0.</li></ul>
<pre>avail 3 3 2; alloc P0 0 1 0, P1 2 0 0, P2 3 0 2, P3 2 1 1, P4 0 0 2;
max P0 7 5 3, P1 3 2 2, P2 9 0 2, P3 2 2 2, P4 4 3 3  -> safe, order 1 3 0 2 4</pre>""",
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
r"""<p>Memory holes of sizes <code>holes[0..nh-1]</code> receive requests in order. Each request goes into one
hole, which then shrinks by that amount.</p>
<pre>void mem_fit(int *holes, int nh, const int *req, int nr, int policy, int *where);</pre>
<ul><li>policy 0, <b>first fit</b>: the first hole that is big enough.</li>
<li>policy 1, <b>best fit</b>: the smallest hole that is big enough.</li>
<li>policy 2, <b>worst fit</b>: the largest hole (if it is big enough).</li>
<li>Ties go to the lower index. <code>where[i]</code> = the hole index, or &minus;1 if the request must wait.
Update <code>holes</code> in place.</li></ul>
<pre>holes 100 500 200 300 600, requests 212 417 112 426:
first fit -> 1 4 1 -1     best fit -> 3 1 2 4     worst fit -> 4 1 4 -1</pre>""",
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
r"""<p>Bubble sort walks the array and swaps neighbours that are out of order; after pass <i>k</i>, the
<i>k</i> largest values are in place. Stop early if a pass makes no swaps.</p>
<p>Write <code>long bubble_sort(int *a, int n)</code> that sorts ascending and returns the number of swaps.
(Each swap fixes exactly one <em>inversion</em>, a pair i &lt; j with a[i] &gt; a[j], so the count is the same
however you write it.)</p>
<pre>{3, 1, 2} -> {1, 2, 3}, 2 swaps</pre>
<p>OA facts: O(n<sup>2</sup>) worst and average, O(n) on sorted input with the early stop, stable, in place.</p>""",
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
r"""<p>Selection sort finds the smallest remaining element and swaps it into position <i>i</i>, for i = 0 to
n&minus;2. It always makes n(n&minus;1)/2 comparisons (5 elements: 10), but at most n&minus;1 swaps, which is
why it suits memory where writes are expensive (flash).</p>
<p>Write <code>int selection_sort(int *a, int n)</code>. Take the <b>first</b> smallest element (use
<code>&lt;</code>, not <code>&lt;=</code>), swap only if it is not already at <i>i</i>, and return the number of
swaps.</p>
<pre>{4, 2, 3, 1} -> {1, 2, 3, 4}, 1 swap (4 and 1)</pre>
<p>Selection sort is <b>not stable</b>: the long-distance swap can jump an element over its equal twin.</p>""",
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
r"""<p>Insertion sort grows a sorted prefix: take the next element, shift the larger elements of the prefix one
place right, and drop it into the gap. It is O(n<sup>2</sup>) in general but O(n) on nearly sorted data, it
is stable, and it is what fast library sorts use for small pieces.</p>
<p>Write <code>long insertion_sort(int *a, int n)</code> that sorts ascending and returns the number of
<b>shifts</b> (single moves of one element one place right). That equals the number of inversions.</p>
<pre>{3, 1, 2} -> {1, 2, 3}, 2 shifts</pre>""",
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
r"""<p>Merge sort splits the array in half, sorts each half, and merges them. It is O(n log n) always and
<b>stable</b> (equal keys keep their order), at the cost of O(n) extra memory.</p>
<pre>struct Rec { int key; int id; };
void merge_sort(struct Rec *a, int n);     // sort by key only; must be stable</pre>
<p>The tests use up to 100,000 records with many equal keys and check that equal keys keep their original
order. Allocate the temporary buffer once with <code>malloc</code>.</p>""",
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
r"""<p>Quicksort picks a pivot, partitions the array into "smaller" and "larger" parts, and recurses. It averages
O(n log n), but a bad pivot choice gives O(n<sup>2</sup>) time and O(n) recursion depth.</p>
<p>Write <code>void quick_sort(int *a, int n)</code>. The tests sort 100,000 values that are random, already
sorted, reversed and <b>all equal</b>, within the 5-second limit. The textbook "last element as pivot" Lomuto
version fails on the last three.</p>
<p>What works: take the middle element as the pivot, use <b>Hoare</b> partitioning (two indices moving towards
each other, which splits runs of equal keys evenly), and recurse into the smaller part while looping on the
larger part, so the stack stays O(log n).</p>""",
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
r"""<p>The C library's <code>qsort</code> sorts any array if you give it a comparison function through a
function pointer:</p>
<pre>void qsort(void *base, size_t n, size_t size, int (*cmp)(const void *, const void *));</pre>
<p>Write <code>void sort_tasks(struct Task *t, int n)</code> that calls <code>qsort</code> to order tasks by
<b>priority, highest first</b>, and by <b>id, lowest first</b> for equal priorities.</p>
<p>The comparator returns a negative number if the first argument goes first, positive if the second does, and 0
if they are equal. Do not return <code>a - b</code> for arbitrary ints: the subtraction can overflow.</p>""",
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
r"""<p>Asked in a 2026 Qualcomm interview: print the numbers 1 to <code>n</code> <b>without any loop</b>.</p>
<p>Write <code>void print_upto(int n)</code> that prints <code>1 2 3 ... n</code> with single spaces and a
newline at the end, for <code>n</code> &ge; 1. The test program turns <code>for</code>, <code>while</code> and
<code>goto</code> into compile errors, and it reads what you print with <code>printf</code>.</p>
<pre>print_upto(5) prints "1 2 3 4 5\n"</pre>""",
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
r"""<p>Asked in a 2026 Qualcomm interview: how many bits must you flip to turn <code>a</code> into
<code>b</code>?</p>
<p>Write <code>int bits_to_flip(uint32_t a, uint32_t b)</code>. The bits that differ are exactly the 1s of
<code>a ^ b</code>, so count them. <code>x &amp;= x - 1</code> clears the lowest 1 (Kernighan's trick).</p>
<pre>bits_to_flip(29, 15) -> 2     (11101 ^ 01111 = 10010)</pre>""",
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
r"""<p>A linked list may end in a loop: the last node points back to an earlier one. Write
<code>struct Node *cycle_start(struct Node *head)</code> that returns the first node of the loop, or
<code>NULL</code> if the list ends normally. Use O(1) extra memory.</p>
<p><b>Floyd's method:</b> move <code>slow</code> one step and <code>fast</code> two steps at a time. If they
meet, there is a loop. Then put one pointer back at <code>head</code> and move both one step at a time; they
meet at the start of the loop.</p>""",
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
r"""<p>Two classic one-pass problems with two pointers:</p>
<pre>struct Node *list_middle(struct Node *head);          // second middle when the length is even
struct Node *kth_from_end(struct Node *head, int k);  // k = 1 is the last node; NULL if k > length</pre>
<ul><li>Middle: <code>fast</code> moves two steps per step of <code>slow</code>; when <code>fast</code> reaches
the end, <code>slow</code> is in the middle. 1&rarr;2&rarr;3&rarr;4 gives 3.</li>
<li>k-th from the end: move <code>lead</code> k steps first, then move both until <code>lead</code> falls
off the end.</li></ul>
<p>Both return <code>NULL</code> for an empty list.</p>""",
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
r"""<p>Write <code>void reverse_words(char *s)</code> that reverses the order of the words, in place. Words are
separated by single spaces, with no leading or trailing spaces.</p>
<pre>"the quick brown fox" -> "fox brown quick the"</pre>
<p>Trick: reverse the whole string ("xof nworb kciuq eht"), then reverse each word back.</p>""",
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
r"""<p>Postfix (reverse Polish) notation needs no brackets: read tokens left to right, push numbers on a stack,
and for an operator pop two values, apply it, and push the result.</p>
<p>Write <code>int eval_postfix(const char *expr)</code>. Tokens are separated by single spaces; numbers are
non-negative integers; operators are <code>+ - * /</code> (<code>/</code> truncates towards zero, and the
divisor is never 0). Every intermediate value fits in an <code>int</code>, and at most 64 values are on the
stack.</p>
<pre>"5 3 + 8 2 - *" -> 48      ((5 + 3) * (8 - 2))
"7 2 /"         -> 3
"2 7 -"         -> -5      (the first value popped is the right operand)</pre>""",
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
r"""<p>Write <code>int find_substr(const char *hay, const char *needle)</code> that returns the index of the first
place <code>needle</code> occurs in <code>hay</code>, or &minus;1. An empty needle matches at 0. Do not call
<code>strstr</code>.</p>
<pre>find_substr("snapdragon", "drag") -> 4
find_substr("modem", "mode")      -> 0
find_substr("modem", "dems")      -> -1</pre>""",
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
r"""<p>Write <code>void rotate_right(int *a, int n, int k)</code> that moves every element <code>k</code> places
to the right, wrapping around, using O(1) extra memory. <code>k</code> may be larger than <code>n</code>.</p>
<pre>{1, 2, 3, 4, 5}, k = 2 -> {4, 5, 1, 2, 3}</pre>
<p>Trick: reverse the whole array, then reverse the first k elements and the rest separately.</p>""",
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
r"""<p><code>a</code> holds <code>n</code> distinct numbers taken from 0, 1, ..., n; exactly one is missing. Write
<code>int missing_number(const int *a, int n)</code> that finds it in one pass with O(1) memory.</p>
<pre>{3, 0, 1} -> 2</pre>
<p>Two ways: n(n+1)/2 minus the sum (watch for overflow with large n), or XOR all the indices and all the values
together. Every number that is present cancels out, because x ^ x = 0.</p>""",
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
r"""<p>Firmware without a full C library often has to format numbers itself. Write
<code>int int_to_str(int x, char *buf)</code> that writes <code>x</code> in decimal (with a <code>'-'</code> if
negative), ends it with <code>'\0'</code>, and returns the length. <code>sprintf</code> and
<code>snprintf</code> are blocked in this problem.</p>
<pre>int_to_str(-307, buf) -> 4, "-307"</pre>
<p><b>Trap:</b> <code>INT_MIN</code> = &minus;2,147,483,648 has no positive <code>int</code> partner, so
<code>-x</code> overflows. That is undefined behaviour, and on this site it stops the program. Work with an
<code>unsigned</code> or <code>long long</code> magnitude.</p>""",
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
