# Problem bank, part C: C++ language and algorithms.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "C++ language"

add(P("cpp_hello", S, "Hello, C++", "cpp", "stdout",
r"""<p><b>What to write.</b> A complete C++ program (with its own <code>main()</code>) that prints
exactly this one line, using <code>std::cout</code>:</p>
<pre>Hello, C++!</pre>
<p><b>Why it matters.</b> This is the C++ version of the first C program. It shows the two things you
will use in every C++ problem here: the header <code>&lt;iostream&gt;</code> and the
<code>std::</code> prefix.</p>
<h4>The C++ way to print</h4>
<table>
<tr><th>Piece</th><th>What it means</th></tr>
<tr><td><code>#include &lt;iostream&gt;</code></td><td>Brings in C++ input and output. It plays the role
that <code>&lt;stdio.h&gt;</code> plays in C.</td></tr>
<tr><td><code>std::cout</code></td><td>The "console output" stream: text sent to it appears on the
screen. <code>std::</code> says it belongs to the standard library's <em>namespace</em> (a named group of
names).</td></tr>
<tr><td><code>&lt;&lt;</code></td><td>"Send this to the stream". You can chain it:
<code>std::cout &lt;&lt; "a" &lt;&lt; 5;</code> prints <code>a5</code>. No <code>%d</code> is needed: the
type decides how a value is printed.</td></tr>
<tr><td><code>"\n"</code></td><td>The newline character, the same as in C. (<code>std::endl</code> also
ends the line, and flushes the output; either is fine here.)</td></tr>
</table>
<h4>C and C++ side by side</h4>
<pre>C:    printf("x = %d\n", x);
C++:  std::cout &lt;&lt; "x = " &lt;&lt; x &lt;&lt; "\n";</pre>
<h4>Things to watch out for</h4>
<ul>
<li>The output must match character for character: capital <code>H</code>, the comma, one space, the
two plus signs and the exclamation mark.</li>
<li>End the line with a newline.</li>
<li>Keep <code>return 0;</code> at the end of <code>main()</code>.</li>
</ul>
<div class="note">A general fact for all C++ problems on this site: the C++ library here is built
<b>without exceptions</b>. Do not use <code>try</code>, <code>throw</code> or <code>catch</code>, and do not
rely on library functions that report errors by throwing.</div>""",
r"""#include <iostream>

int main()
{
    return 0;
}
""",
r"""#include <iostream>

int main()
{
    std::cout << "Hello, C++!\n";
    return 0;
}
""",
None,
"std::cout << \"Hello, C++!\\n\";",
expected="Hello, C++!\n"))

add(P("my_swap", S, "References and templates", "cpp", "func",
r"""<p><b>What to write.</b> A <em>function template</em> that swaps (exchanges) two values of any
type:</p>
<pre>template &lt;typename T&gt;
void my_swap(T&amp; a, T&amp; b);</pre>
<p>After the call, <code>a</code> holds the old value of <code>b</code>, and <code>b</code> holds the old
value of <code>a</code>.</p>
<h4>Feature 1: references (<code>T&amp;</code>)</h4>
<p>A <em>reference</em> is a second name for an existing variable. When a parameter is written
<code>int&amp; a</code>, the function does not get a copy. It works on the caller's own variable. So
the function can change the caller's variables without pointers, without <code>*</code> and without
<code>&amp;</code> at the call site.</p>
<pre>caller:    int x = 1, y = 2;        my_swap(x, y);

           x: [ 1 ]  &lt;---- a is another name for x
           y: [ 2 ]  &lt;---- b is another name for y

after:     x: [ 2 ]    y: [ 1 ]     (the caller's variables changed)</pre>
<p>Compare with C, where you must pass addresses: <code>swap(&amp;x, &amp;y)</code> and write
<code>*a</code> inside.</p>
<h4>Feature 2: templates (<code>template &lt;typename T&gt;</code>)</h4>
<p><code>T</code> is a placeholder for a type. You write the function once. When the program calls
<code>my_swap</code> with two <code>int</code>s, the compiler makes an <code>int</code> version (T =
<code>int</code>). For two <code>std::string</code>s it makes a string version, and so on.</p>
<h4>What the hidden test does</h4>
<table>
<tr><th>Type</th><th>Before</th><th>After <code>my_swap(a, b)</code></th></tr>
<tr><td><code>int</code></td><td>a = 1, b = 2</td><td>a = 2, b = 1</td></tr>
<tr><td><code>double</code></td><td>a = 0.5, b = &minus;3.25</td><td>a = &minus;3.25, b = 0.5</td></tr>
<tr><td><code>std::string</code></td><td>a = "left", b = "right channel"</td><td>a = "right channel", b = "left"</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>You need a temporary variable of type <code>T</code>. Without it, the first assignment destroys one
of the two values.</li>
<li>Optional: <code>std::move</code> (from <code>&lt;utility&gt;</code>) lets a string hand over its
memory instead of copying its letters. Plain copies also pass the test.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write the swap for two <code>int</code>s first, with a temporary variable.</li>
<li>Now replace every <code>int</code> with <code>T</code>. Nothing else changes.</li>
</ol>
</details>""",
r"""template <typename T>
void my_swap(T& a, T& b)
{
}
""",
r"""#include <utility>

template <typename T>
void my_swap(T& a, T& b)
{
    T t = std::move(a);
    a = std::move(b);
    b = std::move(t);
}
""",
r"""#include "check.h"
#include <string>
#include "solution.cpp"
int main()
{
    int a = 1, b = 2; my_swap(a, b);
    ck_true("my_swap(int 1, int 2)", a == 2 && b == 1);
    double x = 0.5, y = -3.25; my_swap(x, y);
    ck_true("my_swap(double 0.5, double -3.25)", x == -3.25 && y == 0.5);
    std::string s = "left", t = "right channel"; my_swap(s, t);
    ck_true("my_swap(std::string \"left\", \"right channel\")", s == "right channel" && t == "left");
    return ck_done();
}
""",
"Same three lines as the C swap, with T instead of int. std::move avoids copying big objects."))

add(P("overload", S, "Function overloading", "cpp", "func",
r"""<p><b>What to write.</b> Two functions that share the name <code>area</code>:</p>
<pre>int    area(int w, int h);  // rectangle: w * h
double area(double r);      // circle: pi * r * r</pre>
<p>Use pi = 3.14159265358979323846.</p>
<h4>The feature: function overloading</h4>
<p>In C every function needs its own name. In C++ two functions may have the <b>same name</b> if
their <b>parameter lists differ</b> (a different number of parameters, or different types). At each
call, the compiler looks at the arguments and picks the matching version. The choice is made when the
program is compiled, not when it runs.</p>
<pre>area(3, 4)  two ints   -&gt;  int    area(int w, int h)  -&gt;  12
area(2.0)   one double -&gt;  double area(double r)       -&gt;  12.566370614359172</pre>
<p>Note: the return type alone is not enough to tell two functions apart. The parameters must
differ.</p>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Version chosen</th><th>Result</th></tr>
<tr><td><code>area(3, 4)</code></td><td>rectangle</td><td>12</td></tr>
<tr><td><code>area(0, 1000)</code></td><td>rectangle</td><td>0</td></tr>
<tr><td><code>area(1.0)</code></td><td>circle</td><td>3.141592653589793</td></tr>
<tr><td><code>area(0.5)</code></td><td>circle</td><td>0.7853981633974483</td></tr>
</table>
<h4>What the hidden test does</h4>
<ul>
<li>50 rectangles with <code>w</code> and <code>h</code> from 0 to 1000. The answer must be exact.</li>
<li>50 circles with <code>r</code> from 0 up to (not including) 20. The answer must match
pi&middot;r&middot;r to about 12 significant digits, so use the full value of pi given above.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The rectangle version is already in the starter code. Leave it as it is, but make it return the
area.</li>
<li>Add a second function below it with the same name and one <code>double</code> parameter.</li>
</ol>
</details>""",
r"""int area(int w, int h)
{
    return 0;
}
""",
r"""int area(int w, int h)
{
    return w * h;
}

double area(double r)
{
    const double pi = 3.14159265358979323846;
    return pi * r * r;
}
""",
r"""#include "check.h"
#include "solution.cpp"
int main()
{
    char d[64];
    for (int i = 0; i < 50; i++) {
        int w = ck_range(0, 1000), h = ck_range(0, 1000);
        CK_FMT(d, "area(%d, %d)", w, h); ck_int(d, area(w, h), (long long)w * h);
        double r = (ck_unit() + 1) * 10;
        CK_FMT(d, "area(%.6f)", r); ck_dbl(d, area(r), 3.14159265358979323846 * r * r, 1e-12);
    }
    return ck_done();
}
""",
"Add a second function called area that takes one double."))

add(P("counter", S, "A first class", "cpp", "func",
r"""<p><b>What to write.</b> Finish the class <code>Counter</code> in the starter code. A Counter holds
one whole number:</p>
<ul>
<li>the constructor sets the start value (0 if you give no value);</li>
<li><code>inc()</code> adds 1;</li>
<li><code>add(n)</code> adds <code>n</code> (which can be negative);</li>
<li><code>value()</code> returns the current number.</li>
</ul>
<h4>The C++ features used here</h4>
<table>
<tr><th>Feature</th><th>Plain meaning</th></tr>
<tr><td><code>class</code> with <code>public:</code> and <code>private:</code></td><td>A struct whose
data can be hidden. Code outside the class can call the <code>public</code> functions, but cannot touch
<code>v_</code> directly.</td></tr>
<tr><td>Constructor <code>Counter(int start = 0)</code></td><td>A function that runs automatically when
an object is created. <code>= 0</code> is a <em>default argument</em>: <code>Counter c;</code> means
<code>Counter c(0);</code>.</td></tr>
<tr><td>Initialiser list <code>: v_(start)</code></td><td>Written between the <code>)</code> and the
<code>{</code> of a constructor. It sets the member <code>v_</code> to <code>start</code> as the object is
built.</td></tr>
<tr><td><code>explicit</code></td><td>Stops the compiler from turning a plain <code>int</code> into a Counter
by itself. You do not need to change it.</td></tr>
<tr><td><code>int value() const</code></td><td>The <code>const</code> after the brackets is a promise: this
function does not change the object. Only such functions can be called on a <code>const Counter</code>.</td></tr>
</table>
<h4>Picture of one object</h4>
<pre>Counter c(5);         c: +--------+
                         | v_ = 5 |   private: only Counter's own
                         +--------+   functions can read or write v_
c.inc();     -&gt; v_ = 6
c.add(-10);  -&gt; v_ = -4
c.value()    -&gt; returns -4, v_ unchanged</pre>
<h4>What the hidden test does</h4>
<table>
<tr><th>Code</th><th>Expected <code>value()</code></th></tr>
<tr><td><code>Counter c;</code></td><td>0</td></tr>
<tr><td><code>c.inc(); c.inc();</code></td><td>2</td></tr>
<tr><td><code>c.add(40);</code></td><td>42</td></tr>
<tr><td><code>const Counter k(-7);</code> then <code>k.value()</code></td><td>&minus;7</td></tr>
<tr><td><code>Counter m(100);</code> then 1000 calls <code>m.add(i % 3 - 1)</code> for i = 0 &hellip; 999
(adds &minus;1, 0, +1, &minus;1, 0, +1, &hellip;)</td><td>99</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>The starter's constructor does not set <code>v_</code>, so <code>v_</code> starts as garbage. Where
should <code>start</code> be stored?</li>
<li>Each of the other three functions needs only one short statement that reads or changes
<code>v_</code>.</li>
</ol>
</details>""",
r"""class Counter {
public:
    explicit Counter(int start = 0) { }
    void inc() { }
    void add(int n) { }
    int value() const { return 0; }
private:
    int v_;
};
""",
r"""class Counter {
public:
    explicit Counter(int start = 0) : v_(start) { }
    void inc() { ++v_; }
    void add(int n) { v_ += n; }
    int value() const { return v_; }
private:
    int v_;
};
""",
r"""#include "check.h"
#include "solution.cpp"
int main()
{
    Counter c;
    ck_int("Counter c; c.value()", c.value(), 0);
    c.inc(); c.inc();
    ck_int("after two inc()", c.value(), 2);
    c.add(40);
    ck_int("after add(40)", c.value(), 42);
    const Counter k(-7);
    ck_int("const Counter k(-7); k.value()", k.value(), -7);
    Counter m(100);
    for (int i = 0; i < 1000; i++) m.add(i % 3 - 1);
    ck_int("Counter(100) after 1000 add(i % 3 - 1)", m.value(), 100 - 1 * 334 + 333);
    return ck_done();
}
""",
"Initialise v_ in the constructor's initialiser list: Counter(int start = 0) : v_(start) {}"))

add(P("tracker", S, "Constructors and destructors", "cpp", "func",
r"""<p><b>What to write.</b> Finish the class <code>Tracker</code> so that its static member
<code>Tracker::live</code> always equals the number of Tracker objects that exist right now. Every
constructor adds 1; the destructor subtracts 1.</p>
<p><b>Why it matters.</b> C++ runs a constructor when an object is created and a destructor when it is
destroyed, <b>automatically</b>. Tying setup and clean-up to an object's life is called <b>RAII</b>
("Resource Acquisition Is Initialisation"). Lock guards, file handles and audio-device handles all use
it, so the clean-up can never be forgotten.</p>
<h4>Facts you need</h4>
<table>
<tr><th>Feature</th><th>Plain meaning</th></tr>
<tr><td><code>static int live;</code></td><td>One variable shared by the whole class, not one per object.
It is defined once outside the class: <code>int Tracker::live = 0;</code> (already in the starter).</td></tr>
<tr><td><code>Tracker()</code></td><td>Default constructor: runs for <code>Tracker a;</code>, for
<code>new Tracker</code>, and for each element of <code>std::vector&lt;Tracker&gt; v(3)</code>.</td></tr>
<tr><td><code>Tracker(const Tracker&amp; other)</code></td><td>Copy constructor: runs when a new
Tracker is made as a copy of another one, e.g. <code>Tracker b(a);</code> or
<code>v.push_back(a);</code>.</td></tr>
<tr><td><code>~Tracker()</code></td><td>Destructor: runs when a local object reaches the closing
<code>}</code> of its block, when a vector is destroyed (once per element), and on
<code>delete p;</code>.</td></tr>
</table>
<h4>What the hidden test does</h4>
<pre>                                          live must be
start                                          0
{ Tracker a;                                   1
  { Tracker b(a);                              2   (copy constructor)
    std::vector&lt;Tracker&gt; v(3);                 5   (3 default constructors)
    10 times v.push_back(a);                  15   (10 copies)
  }  b and v are destroyed here                1
}  a is destroyed here                         0
Tracker *p = new Tracker;                      1
delete p;                                      0</pre>
<h4>Things to watch out for</h4>
<ul>
<li>When a vector runs out of room during <code>push_back</code>, it moves to a bigger block of memory.
It copies the old elements there (copy constructor) and destroys the old ones (destructor). If you
count in <b>both</b> constructors and in the destructor, these extra calls cancel out.</li>
<li>Forgetting the copy constructor is the usual mistake: then copies are made but never counted, and
<code>live</code> goes negative.</li>
</ul>""",
r"""class Tracker {
public:
    static int live;   // how many Tracker objects exist right now

    Tracker();
    Tracker(const Tracker& other);
    ~Tracker();
};

int Tracker::live = 0;

Tracker::Tracker() { }
Tracker::Tracker(const Tracker&) { }
Tracker::~Tracker() { }
""",
r"""class Tracker {
public:
    static int live;

    Tracker();
    Tracker(const Tracker& other);
    ~Tracker();
};

int Tracker::live = 0;

Tracker::Tracker() { ++live; }
Tracker::Tracker(const Tracker&) { ++live; }
Tracker::~Tracker() { --live; }
""",
r"""#include "check.h"
#include <vector>
#include "solution.cpp"
int main()
{
    ck_int("live before any Tracker", Tracker::live, 0);
    {
        Tracker a;
        ck_int("after Tracker a;", Tracker::live, 1);
        {
            Tracker b(a);
            ck_int("after Tracker b(a);", Tracker::live, 2);
            std::vector<Tracker> v(3);
            ck_int("after std::vector<Tracker> v(3);", Tracker::live, 5);
            for (int i = 0; i < 10; i++) v.push_back(a);
            ck_int("after 10 x v.push_back(a)", Tracker::live, 15);
        }
        ck_int("after b and v go out of scope", Tracker::live, 1);
    }
    ck_int("after a goes out of scope", Tracker::live, 0);
    Tracker *p = new Tracker;
    ck_int("after new Tracker", Tracker::live, 1);
    delete p;
    ck_int("after delete", Tracker::live, 0);
    return ck_done();
}
""",
"Increment live in both constructors and decrement it in the destructor."))

add(P("complex_ops", S, "Operator overloading", "cpp", "func",
r"""<p><b>What to write.</b> The starter code has a small complex-number type
<code>Cplx</code> with a real part <code>re</code> and an imaginary part <code>im</code>. Write three
functions, so that DSP code can be written like maths (<code>a + b</code>, <code>a * b</code>):</p>
<pre>Cplx   operator+(Cplx a, Cplx b);
Cplx   operator*(Cplx a, Cplx b);
double mag(Cplx a);</pre>
<h4>The feature: operator overloading</h4>
<p>A function named <code>operator+</code> is what the compiler calls when it sees <code>a + b</code>
with two <code>Cplx</code> values. So <code>a + b</code> really means <code>operator+(a, b)</code>. You
write it like any other function. It takes two Cplx values and returns a new Cplx.</p>
<p>You can build and return a Cplx with braces: <code>return {first_value, second_value};</code> sets
<code>re</code> and then <code>im</code>, in the order they are declared.</p>
<h4>The maths (with j&sup2; = &minus;1)</h4>
<table>
<tr><th>Operation</th><th>Real part</th><th>Imaginary part</th></tr>
<tr><td>a + b</td><td>a.re + b.re</td><td>a.im + b.im</td></tr>
<tr><td>a &times; b</td><td>a.re&middot;b.re &minus; a.im&middot;b.im</td><td>a.re&middot;b.im + a.im&middot;b.re</td></tr>
<tr><td>mag(a)</td><td colspan="2">&radic;(re&sup2; + im&sup2;), the length of the arrow from 0 to a</td></tr>
</table>
<h4>Examples</h4>
<table>
<tr><th>Expression</th><th>Working</th><th>Result</th></tr>
<tr><td>(1 + 2j) + (3 &minus; 1j)</td><td>(1 + 3) and (2 + (&minus;1))</td><td>4 + 1j</td></tr>
<tr><td>(1 + 2j) &times; (3 &minus; 1j)</td><td>re: 1&middot;3 &minus; 2&middot;(&minus;1) = 5;
im: 1&middot;(&minus;1) + 2&middot;3 = 5</td><td>5 + 5j</td></tr>
<tr><td>j &times; j = (0 + 1j) &times; (0 + 1j)</td><td>re: 0 &minus; 1 = &minus;1; im: 0 + 0 = 0</td><td>&minus;1 + 0j</td></tr>
<tr><td>mag(3 + 4j)</td><td>&radic;(9 + 16)</td><td>5</td></tr>
</table>
<h4>What the hidden test does</h4>
<ul>
<li>100 random pairs with both parts between &minus;5 and 5. Each result must match the formulas
above within 10<sup>&minus;12</sup>, so use exactly these formulas.</li>
<li><code>j * j</code> must be exactly &minus;1 + 0j.</li>
<li><code>std::sqrt</code> comes from <code>&lt;cmath&gt;</code>, already included.</li>
</ul>""",
r"""#include <cmath>

struct Cplx {
    double re;
    double im;
};

Cplx operator+(Cplx a, Cplx b) { return a; }
Cplx operator*(Cplx a, Cplx b) { return a; }
double mag(Cplx a) { return 0.0; }
""",
r"""#include <cmath>

struct Cplx {
    double re;
    double im;
};

Cplx operator+(Cplx a, Cplx b) { return {a.re + b.re, a.im + b.im}; }
Cplx operator*(Cplx a, Cplx b) { return {a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re}; }
double mag(Cplx a) { return std::sqrt(a.re * a.re + a.im * a.im); }
""",
r"""#include "check.h"
#include "solution.cpp"
int main()
{
    char d[128];
    for (int i = 0; i < 100; i++) {
        Cplx a{ck_unit() * 5, ck_unit() * 5}, b{ck_unit() * 5, ck_unit() * 5};
        Cplx s = a + b, p = a * b;
        CK_FMT(d, "(%.3f%+.3fj) + (%.3f%+.3fj)", a.re, a.im, b.re, b.im);
        ck_true(d, std::fabs(s.re - (a.re + b.re)) < 1e-12 && std::fabs(s.im - (a.im + b.im)) < 1e-12);
        CK_FMT(d, "(%.3f%+.3fj) * (%.3f%+.3fj)", a.re, a.im, b.re, b.im);
        ck_true(d, std::fabs(p.re - (a.re * b.re - a.im * b.im)) < 1e-12 && std::fabs(p.im - (a.re * b.im + a.im * b.re)) < 1e-12);
        CK_FMT(d, "mag(%.3f%+.3fj)", a.re, a.im); ck_dbl(d, mag(a), std::hypot(a.re, a.im), 1e-12);
    }
    Cplx j{0, 1};
    Cplx jj = j * j;
    ck_true("j * j == -1", jj.re == -1 && jj.im == 0);
    return ck_done();
}
""",
"Return a new Cplx built with braces: return {a.re + b.re, a.im + b.im};"))

add(P("clamp_to", S, "A generic clamp", "cpp", "func",
r"""<p><b>What to write.</b> A function template that <em>clamps</em> a value: it forces
<code>x</code> into the range from <code>lo</code> to <code>hi</code>.</p>
<pre>template &lt;typename T&gt;
T clamp_to(T x, T lo, T hi);</pre>
<h4>The rule</h4>
<pre>        lo                         hi
  ------[===========================]------&gt;
   x here: return lo   x inside: return x   x here: return hi</pre>
<ul>
<li>If <code>x</code> is smaller than <code>lo</code>, return <code>lo</code>.</li>
<li>If <code>x</code> is bigger than <code>hi</code>, return <code>hi</code>.</li>
<li>Otherwise return <code>x</code> unchanged. In the tests <code>lo</code> is never bigger than
<code>hi</code>.</li>
</ul>
<h4>The important restriction: use only <code>&lt;</code></h4>
<p>A template works with any type, but only if the type supports every operation you use. The test
calls your template with a type <code>Db</code> that defines <code>operator&lt;</code> and nothing
else: no <code>&gt;</code>, no <code>&lt;=</code>, no <code>==</code>. So every comparison you write must
use <code>&lt;</code>.</p>
<p>Useful fact: "x is bigger than hi" is the same question as "hi is smaller than x".</p>
<p>Also: all three arguments must have the same type, because they are all <code>T</code>. That is why
the test writes <code>-1.0f</code> (a float) and not <code>-1.0</code> (a double) next to a float.</p>
<h4>Examples (these types are all used by the test)</h4>
<table>
<tr><th>Call</th><th>Result</th><th>Why</th></tr>
<tr><td><code>clamp_to(5, -10, 10)</code></td><td>5</td><td>inside the range</td></tr>
<tr><td><code>clamp_to(-37, -10, 10)</code></td><td>&minus;10</td><td>below lo</td></tr>
<tr><td><code>clamp_to(1.75f, -1.0f, 1.0f)</code></td><td>1.0f</td><td>above hi (float)</td></tr>
<tr><td><code>clamp_to(std::string("zebra"), std::string("apple"), std::string("mango"))</code></td><td>"mango"</td><td>strings compare alphabetically; "zebra" comes after
"mango"</td></tr>
<tr><td><code>clamp_to(Db{-80}, Db{-60}, Db{0})</code></td><td><code>Db{-60}</code></td><td>&minus;80 is
below &minus;60 (a level in dB clamped to a floor)</td></tr>
</table>
<p>The test also runs 100 random <code>int</code> values from &minus;50 to 50 with range [&minus;10, 10],
and 100 random <code>float</code>s with range [&minus;1, 1].</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Two questions, asked in order: is x below lo? is x above hi?</li>
<li>Write the second question using only <code>&lt;</code>, by swapping the two sides.</li>
</ol>
</details>""",
r"""template <typename T>
T clamp_to(T x, T lo, T hi)
{
    return x;
}
""",
r"""template <typename T>
T clamp_to(T x, T lo, T hi)
{
    if (x < lo) return lo;
    if (hi < x) return hi;
    return x;
}
""",
r"""#include "check.h"
#include <string>
#include "solution.cpp"
struct Db { double v; };
bool operator<(Db a, Db b) { return a.v < b.v; }
int main()
{
    char d[96];
    for (int i = 0; i < 100; i++) {
        int x = ck_range(-50, 50);
        CK_FMT(d, "clamp_to<int>(%d, -10, 10)", x); ck_int(d, clamp_to(x, -10, 10), x < -10 ? -10 : (x > 10 ? 10 : x));
        float f = (float)(ck_unit() * 2);
        CK_FMT(d, "clamp_to<float>(%.5f, -1, 1)", f); ck_dbl(d, clamp_to(f, -1.0f, 1.0f), f < -1 ? -1 : (f > 1 ? 1 : f), 0);
    }
    ck_true("clamp_to<std::string>(\"zebra\", \"apple\", \"mango\") == \"mango\"", clamp_to(std::string("zebra"), std::string("apple"), std::string("mango")) == "mango");
    ck_dbl("clamp_to<Db>({-80}, {-60}, {0}).v  (Db has only operator<)", clamp_to(Db{-80}, Db{-60}, Db{0}).v, -60, 0);
    return ck_done();
}
""",
"Write 'hi < x' instead of 'x > hi', because the type may not have operator>."))

add(P("keep_even", S, "std::vector", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>std::vector&lt;int&gt; keep_even(const std::vector&lt;int&gt;&amp; v);</pre>
<p>It returns a <b>new</b> vector that holds only the even numbers of <code>v</code>, in the same order.
<code>v</code> itself is not changed.</p>
<h4>The feature: <code>std::vector</code></h4>
<p>A <code>std::vector&lt;int&gt;</code> is an array of ints that grows by itself and remembers its own
length. The parts you need:</p>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>std::vector&lt;int&gt; out;</code></td><td>an empty vector (size 0)</td></tr>
<tr><td><code>out.push_back(x);</code></td><td>add <code>x</code> at the end (size grows by 1)</td></tr>
<tr><td><code>v.size()</code></td><td>number of elements</td></tr>
<tr><td><code>for (int x : v)</code></td><td>"range-for": visit every element of <code>v</code> in order</td></tr>
<tr><td><code>return out;</code></td><td>returning a vector is cheap: its memory is handed over, not copied</td></tr>
</table>
<p>The parameter is <code>const std::vector&lt;int&gt;&amp;</code>: a reference, so the caller's vector is
not copied, and <code>const</code>, so you promise not to change it.</p>
<h4>Example</h4>
<pre>v   = { 1,  2,  3,  4, -6, -7 }
even?   no yes  no yes yes  no
out = { 2, 4, -6 }</pre>
<h4>Things to watch out for</h4>
<ul>
<li>Negative numbers: in C and C++, <code>%</code> keeps the sign of the left side. So
<code>-6 % 2</code> is 0, but <code>-7 % 2</code> is <b>&minus;1</b>, not 1. A test like
<code>x % 2 == 0</code> works for every sign; <code>x % 2 == 1</code> does not find negative odd
numbers.</li>
<li>Zero is even.</li>
</ul>
<h4>What the hidden test does</h4>
<ul>
<li><code>keep_even({})</code> must return an empty vector.</li>
<li><code>keep_even({1, 2, 3, 4, -6, -7})</code> must return <code>{2, 4, -6}</code>.</li>
<li>20 random vectors of 0 to 500 values between &minus;1000 and 1000.</li>
</ul>""",
r"""#include <vector>

std::vector<int> keep_even(const std::vector<int>& v)
{
    return {};
}
""",
r"""#include <vector>

std::vector<int> keep_even(const std::vector<int>& v)
{
    std::vector<int> out;
    for (int x : v)
        if (x % 2 == 0)
            out.push_back(x);
    return out;
}
""",
r"""#include "check.h"
#include <vector>
#include "solution.cpp"
int main()
{
    char d[96];
    ck_true("keep_even({}) is empty", keep_even({}).empty());
    ck_true("keep_even({1, 2, 3, 4, -6, -7}) == {2, 4, -6}", keep_even({1, 2, 3, 4, -6, -7}) == std::vector<int>({2, 4, -6}));
    for (int t = 0; t < 20; t++) {
        std::vector<int> v(ck_range(0, 500)), want;
        for (int& x : v) { x = ck_range(-1000, 1000); if (x % 2 == 0) want.push_back(x); }
        CK_FMT(d, "keep_even(random vector of %zu)", v.size()); ck_true(d, keep_even(v) == want);
    }
    return ck_done();
}
""",
"Create an empty vector, push_back the even values, return it."))

add(P("sort_by_abs", S, "std::sort with a lambda", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>void sort_by_abs(std::vector&lt;int&gt;&amp; v);</pre>
<p>It sorts <code>v</code> in place by <b>absolute value</b> (the size of the number without its sign),
smallest first. If two values have the same absolute value, the <b>negative one comes first</b>. Use
<code>std::sort</code> with a lambda as the comparison.</p>
<h4>Example</h4>
<pre>before:     {  3, -1,  2, -3,  1,  0 }
abs value:  {  3,  1,  2,  3,  1,  0 }
after:      {  0, -1,  1,  2, -3,  3 }
                  ^^^^^        ^^^^^   ties: negative first</pre>
<h4>The feature: <code>std::sort</code> with a lambda</h4>
<p><code>std::sort(v.begin(), v.end(), cmp)</code> sorts the whole vector. The third argument
<code>cmp</code> is a function that receives two elements <code>a</code> and <code>b</code> and returns
<code>true</code> if <b>a must come before b</b>.</p>
<p>A <em>lambda</em> is a small function written right where you need it:</p>
<pre>[](int a, int b) { return a &lt; b; }      // this one sorts normally</pre>
<p>The <code>[]</code> starts the lambda, then the parameters, then the body.</p>
<h4>The rules your comparison must follow</h4>
<ul>
<li>It must answer "strictly before". For two equal elements it must return <code>false</code>. Using
<code>&lt;=</code> instead of <code>&lt;</code> breaks <code>std::sort</code>: it can then read outside the
vector or crash.</li>
<li>It must be consistent: if a is before b and b is before c, then a is before c.</li>
<li><code>std::abs</code> is in <code>&lt;cstdlib&gt;</code>.</li>
</ul>
<h4>What the hidden test does</h4>
<p>The example above, then 20 random vectors of 0 to 300 values between &minus;50 and 50 (so there are
many ties and many equal values).</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Compare the absolute values first. If they differ, that alone decides the order.</li>
<li>If they are equal, which plain comparison of <code>a</code> and <code>b</code> puts &minus;3 before
3?</li>
</ol>
</details>""",
r"""#include <vector>
#include <algorithm>

void sort_by_abs(std::vector<int>& v)
{
    std::sort(v.begin(), v.end());
}
""",
r"""#include <vector>
#include <algorithm>
#include <cstdlib>

void sort_by_abs(std::vector<int>& v)
{
    std::sort(v.begin(), v.end(), [](int a, int b) {
        int aa = std::abs(a), bb = std::abs(b);
        if (aa != bb)
            return aa < bb;
        return a < b;
    });
}
""",
r"""#include "check.h"
#include <vector>
#include <algorithm>
#include <cstdlib>
#include "solution.cpp"
int main()
{
    std::vector<int> v{3, -1, 2, -3, 1, 0};
    sort_by_abs(v);
    ck_true("sort_by_abs({3, -1, 2, -3, 1, 0}) == {0, -1, 1, 2, -3, 3}", v == std::vector<int>({0, -1, 1, 2, -3, 3}));
    char d[96];
    for (int t = 0; t < 20; t++) {
        std::vector<int> a(ck_range(0, 300));
        for (int& x : a) x = ck_range(-50, 50);
        std::vector<int> w = a;
        std::stable_sort(w.begin(), w.end(), [](int p, int q) { return std::abs(p) != std::abs(q) ? std::abs(p) < std::abs(q) : p < q; });
        sort_by_abs(a);
        CK_FMT(d, "sort_by_abs(random vector of %zu)", a.size()); ck_true(d, a == w);
    }
    return ck_done();
}
""",
"The lambda gets (a, b) and returns true if a must come before b. Compare abs values first, then the values."))

add(P("count_words", S, "std::string", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>int count_words(const std::string&amp; s);</pre>
<p>It returns how many words <code>s</code> contains. A <b>word</b> is a run of one or more characters
that are not whitespace. Words are separated by one or more whitespace characters.</p>
<h4>Whitespace in this problem (only these three)</h4>
<table>
<tr><th>Character</th><th>Written in C++</th><th>ASCII code</th></tr>
<tr><td>space</td><td><code>' '</code></td><td>32</td></tr>
<tr><td>tab</td><td><code>'\t'</code></td><td>9</td></tr>
<tr><td>newline</td><td><code>'\n'</code></td><td>10</td></tr>
</table>
<p>Everything else (letters, digits, punctuation) is part of a word.</p>
<h4>Picture</h4>
<pre>s = "  real time   audio\n"

     . . r e a l . t i m e . . . a u d i o \n      (. = space)
         ^         ^             ^
         a word starts at each ^  --&gt;  3 words</pre>
<p>Spaces at the start, at the end, or several in a row do not create extra words.</p>
<h4>What the hidden test checks</h4>
<table>
<tr><th>Input</th><th>Answer</th></tr>
<tr><td><code>""</code> (empty)</td><td>0</td></tr>
<tr><td><code>"one"</code></td><td>1</td></tr>
<tr><td><code>"  real time   audio\n"</code></td><td>3</td></tr>
<tr><td><code>"a b c d e"</code></td><td>5</td></tr>
<tr><td><code>"\t\ttab\tseparated\n\nlines "</code></td><td>3</td></tr>
<tr><td><code>"     "</code> (only spaces)</td><td>0</td></tr>
</table>
<p><code>for (char c : s)</code> visits every character of a <code>std::string</code> in order.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Count the moments where a word <em>starts</em>, not the spaces. A word starts at a non-whitespace
character whose previous character was whitespace, or which is the very first character.</li>
<li>To know the previous character's kind, keep one <code>bool</code> that remembers "am I inside a
word right now?".</li>
</ol>
</details>""",
r"""#include <string>

int count_words(const std::string& s)
{
    return 0;
}
""",
r"""#include <string>

int count_words(const std::string& s)
{
    int n = 0;
    bool in_word = false;
    for (char c : s) {
        bool space = (c == ' ' || c == '\t' || c == '\n');
        if (!space && !in_word)
            n++;
        in_word = !space;
    }
    return n;
}
""",
r"""#include "check.h"
#include <string>
#include "solution.cpp"
int main()
{
    const char *in[] = {"", "one", "  real time   audio\n", "a b c d e", "\t\ttab\tseparated\n\nlines ", "     "};
    int want[] = {0, 1, 3, 5, 3, 0};
    char d[96];
    for (int i = 0; i < 6; i++) { CK_FMT(d, "count_words(test %d)", i); ck_int(d, count_words(in[i]), want[i]); }
    return ck_done();
}
""",
"Count the moments when you move from whitespace into a word."))

add(P("char_freq", S, "std::map", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>std::map&lt;char, int&gt; char_freq(const std::string&amp; s);</pre>
<p>It counts how many times each character appears in <code>s</code> and returns the counts in a map.
The space character <code>' '</code> is <b>not</b> counted. Every other character is counted: letters,
digits, punctuation.</p>
<h4>The feature: <code>std::map</code></h4>
<p>A <code>std::map&lt;char, int&gt;</code> stores pairs <em>key &rarr; value</em>; here character
&rarr; count. Each key appears at most once.</p>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>std::map&lt;char, int&gt; m;</code></td><td>an empty map</td></tr>
<tr><td><code>m[c]</code></td><td>the value stored for key <code>c</code>. <b>If <code>c</code> is not
in the map yet, it is added with value 0 first.</b></td></tr>
<tr><td><code>m[c]++</code></td><td>so this works both for a new and for an old key</td></tr>
</table>
<p>A map keeps its keys sorted, here by their ASCII codes (for example <code>'!'</code> = 33,
<code>'1'</code> = 49, <code>'a'</code> = 97). You do not need to sort anything yourself.</p>
<h4>Examples</h4>
<table>
<tr><th>Input</th><th>Returned map</th></tr>
<tr><td><code>"aab b"</code></td><td>{'a': 2, 'b': 2}</td></tr>
<tr><td><code>"hello world"</code></td><td>{'d': 1, 'e': 1, 'h': 1, 'l': 3, 'o': 2, 'r': 1, 'w': 1}</td></tr>
<tr><td><code>"   "</code></td><td>{} (empty: only spaces)</td></tr>
</table>
<p>The hidden test checks the three kinds of input: <code>"aab b"</code>, <code>"   "</code>, and a long
sentence that also contains digits and <code>!!</code>. The whole map must be equal to the expected
one, so a wrong extra key (such as <code>' '</code> with any count) makes the test fail.</p>""",
r"""#include <map>
#include <string>

std::map<char, int> char_freq(const std::string& s)
{
    return {};
}
""",
r"""#include <map>
#include <string>

std::map<char, int> char_freq(const std::string& s)
{
    std::map<char, int> m;
    for (char c : s)
        if (c != ' ')
            m[c]++;
    return m;
}
""",
r"""#include "check.h"
#include <map>
#include <string>
#include "solution.cpp"
int main()
{
    std::map<char, int> w{{'a', 2}, {'b', 2}};
    ck_true("char_freq(\"aab b\") == {a:2, b:2}", char_freq("aab b") == w);
    ck_true("char_freq(\"   \") is empty", char_freq("   ").empty());
    std::string s = "the quick brown fox jumps over the lazy dog 1234 !!";
    std::map<char, int> r; for (char c : s) if (c != ' ') r[c]++;
    ck_true("char_freq(pangram with digits)", char_freq(s) == r);
    return ck_done();
}
""",
"m[c]++ creates the entry with 0 the first time, then adds 1."))

add(P("move_buffer", S, "Move semantics", "cpp", "func",
r"""<p><b>What to write.</b> Finish the class <code>Buffer</code>: an audio buffer that owns a
block of <code>float</code>s on the heap. Copying such a buffer would be slow, so the class is
<b>move-only</b>: copying is forbidden (the starter already says <code>= delete</code> for the copy
operations), but <em>moving</em> is allowed. Moving hands the memory over to another Buffer and leaves
the source empty.</p>
<h4>What each part must do</h4>
<ul>
<li><code>Buffer(n)</code>: allocate <code>n</code> floats, all set to 0
(<code>new float[n]()</code> does that: the <code>()</code> means "set to zero").</li>
<li>Move constructor <code>Buffer(Buffer&amp;&amp; other)</code>: take <code>other</code>'s pointer and
size. Then set <code>other</code>'s pointer to <code>nullptr</code> and its size to 0.</li>
<li>Move assignment <code>operator=(Buffer&amp;&amp; other)</code>: same, but this object may already
own memory. That memory must be freed first, or it leaks. Return <code>*this</code>.</li>
<li>Destructor: free the memory with <code>delete[]</code>. (<code>delete[] nullptr</code> is allowed
and does nothing.)</li>
</ul>
<h4>Facts you need</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>Buffer&amp;&amp;</code></td><td>an <em>rvalue reference</em>: a reference to an object that
is about to be thrown away, so it is safe to steal from it</td></tr>
<tr><td><code>std::move(a)</code></td><td>does not move anything by itself. It only marks <code>a</code> as
"you may steal from me", so that the move constructor or move assignment is chosen</td></tr>
<tr><td><code>noexcept</code></td><td>a promise that the function never throws (already written for you)</td></tr>
</table>
<h4>Picture</h4>
<pre>before  Buffer b(std::move(a)):

  a: [ data_ = 0x1000 | size_ = 256 ] ----&gt; [ 256 floats on the heap ]

after:

  a: [ data_ = nullptr | size_ = 0 ]
  b: [ data_ = 0x1000  | size_ = 256 ] ---&gt; [ the same 256 floats ]

  No new memory, no copying of floats: only the pointer changed owner.

c = std::move(b), when c already owns 16 floats:
  1. delete[] c's own 16 floats      (otherwise they leak)
  2. take b's pointer and size
  3. set b to (nullptr, 0)</pre>
<h4>What the hidden test does</h4>
<p>It replaces <code>new</code> and <code>delete</code> with versions that count live allocations, then:</p>
<table>
<tr><th>Step</th><th>Check</th></tr>
<tr><td><code>Buffer a(256);</code></td><td>size 256, all 256 values 0</td></tr>
<tr><td><code>a[10] = 0.5f;</code> then <code>Buffer b(std::move(a));</code></td><td>b has a's old pointer,
size 256 and b[10] == 0.5; a has size 0 and data nullptr</td></tr>
<tr><td><code>Buffer c(16);</code> then <code>c = std::move(b);</code></td><td>c has the same pointer and
size 256; b is empty; exactly <b>1</b> allocation is alive</td></tr>
<tr><td>all three destroyed</td><td>0 allocations alive (no leaks, nothing freed twice)</td></tr>
</table>
<p>Also good practice (not tested): in move assignment, do nothing if <code>this == &amp;other</code>
(moving an object into itself).</p>""",
r"""#include <cstddef>

class Buffer {
public:
    explicit Buffer(std::size_t n) : data_(nullptr), size_(0) { }
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&& other) noexcept : data_(nullptr), size_(0) { }
    Buffer& operator=(Buffer&& other) noexcept { return *this; }
    ~Buffer() { }

    std::size_t size() const { return size_; }
    float* data() { return data_; }
    float& operator[](std::size_t i) { return data_[i]; }

private:
    float* data_;
    std::size_t size_;
};
""",
r"""#include <cstddef>

class Buffer {
public:
    explicit Buffer(std::size_t n) : data_(new float[n]()), size_(n) { }
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
    Buffer(Buffer&& other) noexcept : data_(other.data_), size_(other.size_)
    {
        other.data_ = nullptr;
        other.size_ = 0;
    }
    Buffer& operator=(Buffer&& other) noexcept
    {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }
    ~Buffer() { delete[] data_; }

    std::size_t size() const { return size_; }
    float* data() { return data_; }
    float& operator[](std::size_t i) { return data_[i]; }

private:
    float* data_;
    std::size_t size_;
};
""",
r"""#include "check.h"
#include <cstdlib>
#include <new>
#include <utility>
static long ck_live_allocs = 0;
void* operator new(std::size_t n) { ck_live_allocs++; return std::malloc(n ? n : 1); }
void* operator new[](std::size_t n) { ck_live_allocs++; return std::malloc(n ? n : 1); }
void operator delete(void* p) noexcept { if (p) { ck_live_allocs--; std::free(p); } }
void operator delete[](void* p) noexcept { if (p) { ck_live_allocs--; std::free(p); } }
void operator delete(void* p, std::size_t) noexcept { if (p) { ck_live_allocs--; std::free(p); } }
void operator delete[](void* p, std::size_t) noexcept { if (p) { ck_live_allocs--; std::free(p); } }
#include "solution.cpp"
int main()
{
    long base = ck_live_allocs;
    {
        Buffer a(256);
        ck_int("Buffer a(256): a.size()", (long long)a.size(), 256);
        bool zero = a.data() != nullptr;
        for (std::size_t i = 0; zero && i < 256; i++) zero = a[i] == 0.0f;
        ck_true("Buffer a(256) holds 256 zeros", zero);
        a[10] = 0.5f;
        float* p = a.data();
        Buffer b(std::move(a));
        ck_true("Buffer b(std::move(a)): b took a's memory", b.data() == p && b.size() == 256 && b[10] == 0.5f);
        ck_true("after the move, a is empty (size 0, data nullptr)", a.size() == 0 && a.data() == nullptr);
        Buffer c(16);
        c = std::move(b);
        ck_true("c = std::move(b): c took b's memory", c.data() == p && c.size() == 256);
        ck_true("after the move assignment, b is empty", b.size() == 0 && b.data() == nullptr);
        ck_int("live allocations while c owns one buffer", ck_live_allocs - base, 1);
    }
    ck_int("live allocations after everything is destroyed (leaks)", ck_live_allocs - base, 0);
    return ck_done();
}
""",
"Move = steal the pointer and size, then set the other's pointer to nullptr. In move assignment, delete[] your own memory first."))

add(P("constexpr_pow2", S, "constexpr", "cpp", "func",
r"""<p><b>What to write.</b> The starter function already gives the right answers. Your job is to
make it usable <b>at compile time</b> by marking it <code>constexpr</code>.</p>
<pre>uint32_t next_pow2_c(uint32_t x);
// returns the smallest power of two that is &gt;= x  (x is at least 1)</pre>
<p><b>Why it matters.</b> If the compiler computes a value while it builds the program, the program
does no work for it when it runs. Tables of window functions or filter coefficients can be made this
way at zero run-time cost, and stored in read-only memory.</p>
<h4>Facts you need</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>constexpr</code> before a function's return type</td><td>"This function may be run by the
compiler when its arguments are known at compile time." It can still be called normally at run time
too. Since C++14 such a function may contain local variables and loops.</td></tr>
<tr><td><code>static_assert(cond, "msg");</code></td><td>A check done by the compiler. If <code>cond</code>
is false, or cannot be computed at compile time, the program does not compile.</td></tr>
<tr><td><code>constexpr std::array&lt;...&gt; table{...};</code></td><td>A constant table whose values must
all be known at compile time.</td></tr>
</table>
<h4>The values (powers of two: 1, 2, 4, 8, 16, &hellip;)</h4>
<table>
<tr><th>x</th><th>1</th><th>2</th><th>3</th><th>5</th><th>8</th><th>17</th><th>100</th><th>1024</th><th>1025</th><th>4097</th></tr>
<tr><td>next_pow2_c(x)</td><td>1</td><td>2</td><td>4</td><td>8</td><td>8</td><td>32</td><td>128</td><td>1024</td><td>2048</td><td>8192</td></tr>
</table>
<h4>What the hidden test does</h4>
<ul>
<li>At compile time: <code>static_assert</code>s for x = 1, 5 and 1024, and a <code>constexpr</code> table
built from x = 3, 17, 100, 4097 (it must hold 4, 32, 128, 8192). Without <code>constexpr</code> the test
<b>does not compile</b>: the compiler reports that the expression is not a constant
expression.</li>
<li>At run time: 100 random x from 1 up to 2<sup>31</sup>.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Nothing in the loop needs to change.</li>
<li>One keyword goes in front of the return type.</li>
</ol>
</details>""",
r"""#include <cstdint>

std::uint32_t next_pow2_c(std::uint32_t x)
{
    std::uint32_t p = 1;
    while (p < x)
        p <<= 1;
    return p;
}
""",
r"""#include <cstdint>

constexpr std::uint32_t next_pow2_c(std::uint32_t x)
{
    std::uint32_t p = 1;
    while (p < x)
        p <<= 1;
    return p;
}
""",
r"""#include "check.h"
#include <array>
#include <cstdint>
#include "solution.cpp"
static_assert(next_pow2_c(1) == 1, "next_pow2_c(1) must be 1");
static_assert(next_pow2_c(5) == 8, "next_pow2_c(5) must be 8");
static_assert(next_pow2_c(1024) == 1024, "next_pow2_c(1024) must be 1024");
constexpr std::array<std::uint32_t, 4> table{next_pow2_c(3), next_pow2_c(17), next_pow2_c(100), next_pow2_c(4097)};
int main()
{
    ck_true("compile-time table {4, 32, 128, 8192}", table[0] == 4 && table[1] == 32 && table[2] == 128 && table[3] == 8192);
    char d[64];
    for (int i = 0; i < 100; i++) {
        std::uint32_t x = (ck_rand() >> ck_range(1, 31)) + 1, p = 1;
        while (p < x) p <<= 1;
        CK_FMT(d, "next_pow2_c(%u)", x); ck_int(d, next_pow2_c(x), p);
    }
    return ck_done();
}
""",
"Add the keyword constexpr in front of the return type. Loops are allowed in constexpr functions since C++14."))

add(P("shapes", S, "Virtual functions", "cpp", "func",
r"""<p><b>What to write.</b> The starter code has an <em>abstract base class</em>
<code>Shape</code>. Add:</p>
<ul>
<li><code>class Rect</code>, built as <code>Rect(double w, double h)</code>, area = w &times; h;</li>
<li><code>class Circle</code>, built as <code>Circle(double r)</code>, area = &pi; &times; r &times; r,
with &pi; = 3.14159265358979323846;</li>
<li><code>double total_area(const std::vector&lt;std::unique_ptr&lt;Shape&gt;&gt;&amp; shapes)</code>,
the sum of the areas of all shapes in the list.</li>
</ul>
<h4>The features used here</h4>
<table>
<tr><th>Code</th><th>Plain meaning</th></tr>
<tr><td><code>class Rect : public Shape</code></td><td>Rect <em>is a</em> Shape (inheritance). A
<code>Shape*</code> may point to a Rect.</td></tr>
<tr><td><code>virtual double area() const = 0;</code></td><td>A <em>pure virtual</em> function: Shape only
names it and every derived class must write its own version. You cannot create a plain Shape.</td></tr>
<tr><td><code>virtual</code></td><td>The version is chosen <b>at run time</b> from the real type of the
object, even when you call it through a <code>Shape*</code> or <code>Shape&amp;</code>.</td></tr>
<tr><td><code>override</code></td><td>Written after your <code>area() const</code>. The compiler then
checks that it really replaces a virtual function of the base (catches typos such as a missing
<code>const</code>).</td></tr>
<tr><td><code>std::unique_ptr&lt;Shape&gt;</code></td><td>A pointer that owns its object and deletes it
automatically. Use <code>p-&gt;area()</code> as with a plain pointer.</td></tr>
<tr><td><code>virtual ~Shape()</code></td><td>Makes sure deleting through a <code>Shape*</code> runs the
right destructor (already in the starter).</td></tr>
</table>
<h4>Picture: one list, different shapes</h4>
<pre>shapes:  [ ptr ] --&gt; Rect   { w_ = 2, h_ = 3 }   area() -&gt; Rect's
         [ ptr ] --&gt; Circle { r_ = 1 }           area() -&gt; Circle's
         ...
Every element has type unique_ptr&lt;Shape&gt;, yet p-&gt;area() runs the
version that belongs to the object's real class.</pre>
<h4>What the hidden test does</h4>
<table>
<tr><th>Check</th><th>Expected</th></tr>
<tr><td><code>Rect(2, 3)</code>, area through a Shape pointer</td><td>6</td></tr>
<tr><td><code>Circle(1)</code>, area through a Shape pointer</td><td>3.141592653589793</td></tr>
<tr><td><code>total_area</code> of those two</td><td>9.141592653589793</td></tr>
<tr><td><code>total_area</code> after adding 50 more shapes (sides and radii between 0.5 and 2.5)</td>
<td>the sum of all 52 areas</td></tr>
</table>
<p>The test creates the shapes with <code>std::make_unique&lt;Rect&gt;(a, b)</code> and
<code>std::make_unique&lt;Circle&gt;(a)</code>, so the constructors must take exactly these
arguments.</p>""",
r"""#include <memory>
#include <vector>

struct Shape {
    virtual ~Shape() = default;
    virtual double area() const = 0;
};

// write class Rect and class Circle here

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes)
{
    return 0.0;
}
""",
r"""#include <memory>
#include <vector>

struct Shape {
    virtual ~Shape() = default;
    virtual double area() const = 0;
};

class Rect : public Shape {
public:
    Rect(double w, double h) : w_(w), h_(h) { }
    double area() const override { return w_ * h_; }
private:
    double w_, h_;
};

class Circle : public Shape {
public:
    explicit Circle(double r) : r_(r) { }
    double area() const override { return 3.14159265358979323846 * r_ * r_; }
private:
    double r_;
};

double total_area(const std::vector<std::unique_ptr<Shape>>& shapes)
{
    double s = 0.0;
    for (const auto& p : shapes)
        s += p->area();
    return s;
}
""",
r"""#include "check.h"
#include <memory>
#include <vector>
#include "solution.cpp"
int main()
{
    std::vector<std::unique_ptr<Shape>> v;
    v.push_back(std::make_unique<Rect>(2.0, 3.0));
    v.push_back(std::make_unique<Circle>(1.0));
    ck_dbl("Rect(2, 3).area() through Shape*", v[0]->area(), 6.0, 1e-12);
    ck_dbl("Circle(1).area() through Shape*", v[1]->area(), 3.14159265358979323846, 1e-12);
    ck_dbl("total_area({Rect(2,3), Circle(1)})", total_area(v), 6.0 + 3.14159265358979323846, 1e-12);
    double want = 6.0 + 3.14159265358979323846;
    for (int i = 0; i < 50; i++) {
        double a = ck_unit() + 1.5, b = ck_unit() + 1.5;
        if (i % 2) { v.push_back(std::make_unique<Rect>(a, b)); want += a * b; }
        else { v.push_back(std::make_unique<Circle>(a)); want += 3.14159265358979323846 * a * a; }
    }
    ck_dbl("total_area of 52 mixed shapes", total_area(v), want, 1e-9);
    return ck_done();
}
""",
"class Rect : public Shape { ... double area() const override { ... } }; The override keyword makes the compiler check that you really override."))

add(P("ring_template", S, "Class template: ring buffer", "cpp", "func",
r"""<p><b>What to write.</b> A fixed-size FIFO queue ("first in, first out": the oldest value
leaves first) as a <b>class template</b>, stored in a <code>std::array</code>, with no heap memory:</p>
<pre>template &lt;typename T, std::size_t N&gt;
class RingBuffer {
public:
    bool push(const T&amp; v);   // add v at the back;
                              //   if full: change nothing, return false
    bool pop(T&amp; out);        // move the oldest value into out;
                              //   if empty: return false
    std::size_t size() const; // how many values are stored now
    bool empty() const;       // size() == 0
    bool full() const;        // size() == N
};</pre>
<h4>The template parameters</h4>
<p><code>T</code> is the element type. <code>N</code> is a <em>number</em> fixed at compile time: the
capacity. <code>RingBuffer&lt;int, 5&gt;</code> holds up to 5 ints, inside a
<code>std::array&lt;int, 5&gt;</code>. <code>N</code> can be any value from 1 up. It does <b>not</b> have
to be a power of two, so use <code>% N</code> to wrap, not a bit mask.</p>
<h4>The idea: indices that wrap around</h4>
<p>Keep the index of the oldest value (<code>head</code>) and how many values are stored
(<code>count</code>). The next free slot is <code>(head + count) % N</code>. When an index reaches
<code>N</code>, it wraps back to 0, so the array is used like a circle.</p>
<h4>Trace with N = 3</h4>
<pre>operation    returns       array [0] [1] [2]   head  count
start                            -   -   -      0     0
push(10)     true                10  -   -      0     1
push(20)     true                10  20  -      0     2
push(30)     true                10  20  30     0     3   full
push(40)     false               10  20  30     0     3   unchanged
pop          true, out=10        10  20  30     1     2   (10 is now stale)
push(40)     true                40  20  30     1     3   slot (1+2)%3 = 0
pop          true, out=20        40  20  30     2     2
pop          true, out=30        40  20  30     0     1   head wrapped
pop          true, out=40        40  20  30     1     0   empty
pop          false               40  20  30     1     0</pre>
<h4>What the hidden test does</h4>
<p>For <code>RingBuffer&lt;int, 5&gt;</code>, <code>RingBuffer&lt;float, 8&gt;</code> and
<code>RingBuffer&lt;std::string, 1&gt;</code>: 2000 random push/pop steps, compared with a
<code>std::deque</code>. After every step it checks the return value, the popped value, and
<code>size()</code>, <code>empty()</code> and <code>full()</code>.</p>""",
r"""#include <array>
#include <cstddef>

template <typename T, std::size_t N>
class RingBuffer {
public:
    bool push(const T& v) { return false; }
    bool pop(T& out) { return false; }
    std::size_t size() const { return 0; }
    bool empty() const { return true; }
    bool full() const { return false; }

private:
    std::array<T, N> buf_{};
};
""",
r"""#include <array>
#include <cstddef>

template <typename T, std::size_t N>
class RingBuffer {
public:
    bool push(const T& v)
    {
        if (count_ == N)
            return false;
        buf_[(head_ + count_) % N] = v;
        ++count_;
        return true;
    }
    bool pop(T& out)
    {
        if (count_ == 0)
            return false;
        out = buf_[head_];
        head_ = (head_ + 1) % N;
        --count_;
        return true;
    }
    std::size_t size() const { return count_; }
    bool empty() const { return count_ == 0; }
    bool full() const { return count_ == N; }

private:
    std::array<T, N> buf_{};
    std::size_t head_ = 0;
    std::size_t count_ = 0;
};
""",
r"""#include "check.h"
#include <deque>
#include <string>
#include "solution.cpp"
template <typename T, std::size_t N, typename Gen>
static void run(const char* name, Gen gen)
{
    RingBuffer<T, N> r;
    std::deque<T> q;
    char d[160];
    for (int step = 0; step < 2000; step++) {
        if (ck_rand() % 2) {
            T v = gen(step);
            bool ok = r.push(v), want = q.size() < N;
            if (want) q.push_back(v);
            CK_FMT(d, "%s: step %d push returns %d", name, step, (int)want); ck_int(d, ok, want);
        } else {
            T v{};
            bool ok = r.pop(v), want = !q.empty();
            CK_FMT(d, "%s: step %d pop returns %d", name, step, (int)want); ck_int(d, ok, want);
            if (want) { CK_FMT(d, "%s: step %d pop gives the oldest value", name, step); ck_true(d, v == q.front()); q.pop_front(); }
        }
        CK_FMT(d, "%s: step %d size/empty/full", name, step);
        ck_true(d, r.size() == q.size() && r.empty() == q.empty() && r.full() == (q.size() == N));
    }
}
int main()
{
    run<int, 5>("RingBuffer<int, 5>", [](int s) { return s * 3; });
    run<float, 8>("RingBuffer<float, 8>", [](int s) { return s * 0.5f; });
    run<std::string, 1>("RingBuffer<std::string, 1>", [](int s) { return std::to_string(s); });
    return ck_done();
}
""",
"Keep a read index and a count. The write slot is (head + count) % N."))

add(P("span_sum", S, "std::span", "cpp", "func",
r"""<p><b>What to write.</b> Two functions that read samples through a
<code>std::span</code>:</p>
<pre>float sum_span(std::span&lt;const float&gt; s);              // sum of all samples
float mean_of_last(std::span&lt;const float&gt; s, std::size_t k);
                 // mean (average) of the last k samples</pre>
<p>For <code>mean_of_last</code>, <code>k</code> is always at least 1 and at most
<code>s.size()</code>.</p>
<h4>The feature: <code>std::span</code> (C++20)</h4>
<p>A span is a <b>view</b> of someone else's array: a pointer to the first element plus a length. It
does not own or copy the samples. A <code>std::vector&lt;float&gt;</code>, a
<code>std::array&lt;float, N&gt;</code> or a plain <code>float[]</code> array all turn into a span
automatically when passed. <code>const float</code> means you can read the samples but not change
them.</p>
<pre>std::array&lt;float, 4&gt; a = {1, 2, 3, 4};

a:       [ 1 ][ 2 ][ 3 ][ 4 ]
s:       ptr --^             size = 4
s.last(2):         ptr --^   size = 2      (a view of {3, 4})
s.first(2): {1, 2}           s.subspan(1, 2): {2, 3}</pre>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>s.size()</code></td><td>number of samples in the view</td></tr>
<tr><td><code>s[i]</code></td><td>sample i</td></tr>
<tr><td><code>for (float v : s)</code></td><td>visit every sample in the view</td></tr>
<tr><td><code>s.last(k)</code></td><td>a smaller span: the last <code>k</code> samples (no copying)</td></tr>
</table>
<h4>Examples</h4>
<table>
<tr><th>Call</th><th>Working</th><th>Result</th></tr>
<tr><td><code>sum_span({1, 2, 3, 4})</code></td><td>1 + 2 + 3 + 4</td><td>10</td></tr>
<tr><td><code>mean_of_last({1, 2, 3, 4}, 2)</code></td><td>(3 + 4) / 2</td><td>3.5</td></tr>
<tr><td><code>mean_of_last({1, 2, 3, 4}, 4)</code></td><td>10 / 4</td><td>2.5</td></tr>
</table>
<h4>What the hidden test does</h4>
<p>The <code>std::array</code> example above, then 20 random <code>std::vector&lt;float&gt;</code>s of
1 to 512 samples between &minus;1 and 1 with a random <code>k</code>. Answers must be within about
10<sup>&minus;4</sup> of the exact value, so a plain <code>float</code> sum is accurate enough.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Write <code>sum_span</code> first, with a range-for loop.</li>
<li>The mean of the last k samples is (sum of those k samples) / k. Which span holds exactly those
samples, and which function already sums a span?</li>
</ol>
</details>""",
r"""#include <span>
#include <cstddef>

float sum_span(std::span<const float> s)
{
    return 0.0f;
}

float mean_of_last(std::span<const float> s, std::size_t k)
{
    return 0.0f;
}
""",
r"""#include <span>
#include <cstddef>

float sum_span(std::span<const float> s)
{
    float acc = 0.0f;
    for (float v : s)
        acc += v;
    return acc;
}

float mean_of_last(std::span<const float> s, std::size_t k)
{
    return sum_span(s.last(k)) / static_cast<float>(k);
}
""",
r"""#include "check.h"
#include <vector>
#include <array>
#include <span>
#include "solution.cpp"
int main()
{
    std::array<float, 4> a{1.0f, 2.0f, 3.0f, 4.0f};
    ck_dbl("sum_span(std::array {1,2,3,4})", sum_span(a), 10.0, 1e-6);
    ck_dbl("mean_of_last({1,2,3,4}, 2)", mean_of_last(a, 2), 3.5, 1e-6);
    char d[96];
    for (int t = 0; t < 20; t++) {
        std::vector<float> v(ck_range(1, 512));
        double s = 0; for (float& x : v) { x = (float)ck_unit(); s += x; }
        std::size_t k = (std::size_t)ck_range(1, (int)v.size());
        double m = 0; for (std::size_t i = v.size() - k; i < v.size(); i++) m += v[i];
        CK_FMT(d, "sum_span(vector of %zu)", v.size()); ck_dbl(d, sum_span(v), s, 1e-4);
        CK_FMT(d, "mean_of_last(vector of %zu, %zu)", v.size(), k); ck_dbl(d, mean_of_last(v, k), m / k, 1e-4);
    }
    return ck_done();
}
""",
"A range-for loop works on a span. s.last(k) is the sub-span of the last k elements."))

add(P("parse_uint", S, "std::optional", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>std::optional&lt;unsigned&gt; parse_uint(std::string_view s);</pre>
<p>It turns text such as <code>"48000"</code> into the number 48000. It succeeds only when
<b>both</b> rules hold:</p>
<ol>
<li><code>s</code> is not empty and every character is a digit <code>'0'</code> &hellip; <code>'9'</code>
(no sign, no spaces, no other characters);</li>
<li>the value is at most 1,000,000,000.</li>
</ol>
<p>On success return the value. Otherwise return <code>std::nullopt</code> ("no value").</p>
<p><b>Why it matters.</b> Reading numbers from a configuration file, a command line or a serial
port: bad input must be rejected, never turned into a wrong number.</p>
<h4>The features used here</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>std::optional&lt;unsigned&gt;</code></td><td>A box that either holds an <code>unsigned</code> or
is empty. <code>return 48000u;</code> fills it; <code>return std::nullopt;</code> returns it empty. This
replaces "magic" error values such as &minus;1.</td></tr>
<tr><td><code>std::string_view</code></td><td>A read-only view of text (a pointer plus a length; no copy).
<code>s.empty()</code>, <code>s.size()</code>, <code>s[i]</code> and <code>for (char c : s)</code> all
work.</td></tr>
</table>
<h4>Data you need</h4>
<ul>
<li>ASCII codes: <code>'0'</code> = 48, <code>'1'</code> = 49, &hellip;, <code>'9'</code> = 57. So the
digit value of a character <code>c</code> is <code>c - '0'</code>.</li>
<li>Reading digits left to right: value = value &times; 10 + digit.
<code>"482"</code>: 0 &rarr; 4 &rarr; 48 &rarr; 482.</li>
<li>On this site <code>unsigned</code> is 32 bits: largest value 4,294,967,295. <code>unsigned long
long</code> is 64 bits: about 1.8 &times; 10<sup>19</sup>.</li>
</ul>
<h4>Examples (all of these are in the hidden test)</h4>
<table>
<tr><th>Input</th><th>Result</th><th>Why</th></tr>
<tr><td><code>"48000"</code></td><td>48000</td><td></td></tr>
<tr><td><code>"0"</code></td><td>0</td><td>zero is a valid value</td></tr>
<tr><td><code>"007"</code></td><td>7</td><td>leading zeros are allowed</td></tr>
<tr><td><code>"1000000000"</code></td><td>1000000000</td><td>exactly the limit</td></tr>
<tr><td><code>"1000000001"</code></td><td>nullopt</td><td>one above the limit</td></tr>
<tr><td><code>"4294967296"</code></td><td>nullopt</td><td>too big; this is 2<sup>32</sup>, which would wrap to 0 in an
<code>unsigned</code></td></tr>
<tr><td><code>"99999999999999999999"</code></td><td>nullopt</td><td>20 digits: too big even for 64 bits</td></tr>
<tr><td><code>""</code></td><td>nullopt</td><td>empty</td></tr>
<tr><td><code>"12a"</code>, <code>"-5"</code>, <code>" 5"</code></td><td>nullopt</td><td>a character that is not
a digit</td></tr>
</table>
<h4>Things to watch out for</h4>
<ul>
<li>Overflow: the 20-digit input does not fit in any integer type. Check the limit <b>while</b> you read
the digits, and stop as soon as the value is too big.</li>
<li>Library functions such as <code>std::stoul</code> report bad input by throwing an exception, and
this site is built without exceptions. Do the conversion yourself.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Reject the empty string first.</li>
<li>Walk through the characters. For each one: is it a digit? Then add it to the value. Is the value
now above the limit?</li>
<li>Which type can hold "limit &times; 10 + 9" without overflowing?</li>
</ol>
</details>""",
r"""#include <optional>
#include <string_view>

std::optional<unsigned> parse_uint(std::string_view s)
{
    return std::nullopt;
}
""",
r"""#include <optional>
#include <string_view>

std::optional<unsigned> parse_uint(std::string_view s)
{
    if (s.empty())
        return std::nullopt;
    unsigned long long v = 0;
    for (char c : s) {
        if (c < '0' || c > '9')
            return std::nullopt;
        v = v * 10 + static_cast<unsigned>(c - '0');
        if (v > 1000000000ULL)
            return std::nullopt;
    }
    return static_cast<unsigned>(v);
}
""",
r"""#include "check.h"
#include <optional>
#include <string_view>
#include <string>
#include "solution.cpp"
int main()
{
    struct T { const char* s; long long v; } t[] = {
        {"48000", 48000}, {"", -1}, {"12a", -1}, {"0", 0}, {"007", 7}, {"1000000000", 1000000000},
        {"1000000001", -1}, {"99999999999999999999", -1}, {"-5", -1}, {" 5", -1}, {"4294967296", -1}};
    char d[96];
    for (const auto& c : t) {
        std::optional<unsigned> r = parse_uint(c.s);
        long long got = r ? (long long)*r : -1;
        CK_FMT(d, "parse_uint(\"%s\")  (-1 means nullopt)", c.s); ck_int(d, got, c.v);
    }
    return ck_done();
}
""",
"Check each character; accumulate in a 64-bit value and stop as soon as it exceeds the limit."))

add(P("rbj_lowpass", S, "Biquad class: RBJ low-pass", "cpp", "func",
r"""<p><b>What to write.</b> A class <code>Biquad</code> (a second-order IIR filter) that designs
its own coefficients and then filters samples. Everything is in <code>double</code>.</p>
<ul>
<li><code>setLowpass(fs, f0, Q)</code>: compute the five coefficients of a low-pass filter. fs = sample
rate in Hz, f0 = cut-off frequency in Hz, Q = how sharp the corner is (0.7071 gives the flattest
response).</li>
<li><code>process(x)</code>: take one input sample, return one output sample, using Transposed Direct
Form II.</li>
<li><code>reset()</code>: set the two state variables to 0, but <b>keep</b> the coefficients.</li>
</ul>
<h4>Step 1: the design formulas (Audio EQ Cookbook, Robert Bristow-Johnson)</h4>
<pre>w0    = 2 * pi * f0 / fs          pi = 3.14159265358979323846
alpha = sin(w0) / (2 * Q)

b0 = (1 - cos w0) / 2     a0 = 1 + alpha
b1 =  1 - cos w0          a1 = -2 * cos w0
b2 = (1 - cos w0) / 2     a2 = 1 - alpha

then divide b0, b1, b2, a1 and a2 by a0 (so the a0 term becomes 1)</pre>
<h4>Step 2: Transposed Direct Form II, for each sample</h4>
<p>The filter keeps two state numbers, <code>s1</code> and <code>s2</code> (both 0 at the start). For
each input x:</p>
<pre>y  = b0*x + s1
s1 = b1*x - a1*y + s2      (uses the OLD s2)
s2 = b2*x - a2*y
return y</pre>
<h4>Worked example: fs = 48000, f0 = 1000, Q = 0.7071</h4>
<table>
<tr><th>Value</th><th>Number</th></tr>
<tr><td>w0</td><td>0.1308997</td></tr>
<tr><td>cos w0</td><td>0.9914449</td></tr>
<tr><td>alpha</td><td>0.0922968</td></tr>
<tr><td>a0</td><td>1.0922968</td></tr>
<tr><td>b0, b1, b2 (after dividing)</td><td>0.00391612, 0.00783225, 0.00391612</td></tr>
<tr><td>a1, a2 (after dividing)</td><td>&minus;1.8153396, 0.8310041</td></tr>
<tr><td>output for input 1, 0, 0, 0 (the <em>impulse response</em>)</td><td>0.00391612, 0.0149413, 0.0277854, 0.0380237, &hellip;</td></tr>
</table>
<p>Check: the first output is always b0. And the sum of the whole impulse response is the gain at
0 Hz, which is 1 for a low-pass filter.</p>
<h4>What the hidden test does</h4>
<p>For four settings (fs, f0, Q) = (48000, 1000, 0.7071), (44100, 200, 0.5), (48000, 8000, 2.0) and
(96000, 20000, 0.7071):</p>
<ul>
<li>feeds an impulse (1 then 3999 zeros) and compares every output with a reference filter, within
10<sup>&minus;9</sup>;</li>
<li>checks that those 4000 outputs add up to 1 (within 10<sup>&minus;6</sup>);</li>
<li>calls <code>process(0.7)</code>, then <code>reset()</code>, then <code>process(1.0)</code>, which must
return exactly b0.</li>
</ul>""",
r"""#include <cmath>

class Biquad {
public:
    void setLowpass(double fs, double f0, double Q) { }
    double process(double x) { return x; }
    void reset() { }

private:
    double b0_ = 1, b1_ = 0, b2_ = 0, a1_ = 0, a2_ = 0;
    double s1_ = 0, s2_ = 0;
};
""",
r"""#include <cmath>

class Biquad {
public:
    void setLowpass(double fs, double f0, double Q)
    {
        const double pi = 3.14159265358979323846;
        double w0 = 2 * pi * f0 / fs, alpha = std::sin(w0) / (2 * Q), c = std::cos(w0);
        double a0 = 1 + alpha;
        b0_ = (1 - c) / 2 / a0;
        b1_ = (1 - c) / a0;
        b2_ = (1 - c) / 2 / a0;
        a1_ = -2 * c / a0;
        a2_ = (1 - alpha) / a0;
    }
    double process(double x)
    {
        double y = b0_ * x + s1_;
        s1_ = b1_ * x - a1_ * y + s2_;
        s2_ = b2_ * x - a2_ * y;
        return y;
    }
    void reset() { s1_ = s2_ = 0; }

private:
    double b0_ = 1, b1_ = 0, b2_ = 0, a1_ = 0, a2_ = 0;
    double s1_ = 0, s2_ = 0;
};
""",
r"""#include "check.h"
#include <cmath>
#include "solution.cpp"
int main()
{
    char d[128];
    double cfg[][3] = {{48000, 1000, 0.7071}, {44100, 200, 0.5}, {48000, 8000, 2.0}, {96000, 20000, 0.7071}};
    for (auto& c : cfg) {
        const double pi = 3.14159265358979323846;
        double w0 = 2 * pi * c[1] / c[0], al = std::sin(w0) / (2 * c[2]), cs = std::cos(w0), a0 = 1 + al;
        double b0 = (1 - cs) / 2 / a0, b1 = (1 - cs) / a0, b2 = b0, a1 = -2 * cs / a0, a2 = (1 - al) / a0;
        Biquad q; q.setLowpass(c[0], c[1], c[2]);
        double x1 = 0, x2 = 0, y1 = 0, y2 = 0, sum = 0; int bad = -1;
        for (int n = 0; n < 4000; n++) {
            double x = n == 0 ? 1.0 : 0.0;
            double y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
            x2 = x1; x1 = x; y2 = y1; y1 = y;
            double g = q.process(x); sum += g;
            if (bad < 0 && std::fabs(g - y) > 1e-9) bad = n;
        }
        CK_FMT(d, "impulse response, fs=%.0f f0=%.0f Q=%.4f: first wrong sample %d", c[0], c[1], c[2], bad); ck_true(d, bad < 0);
        CK_FMT(d, "DC gain (sum of the impulse response) for f0=%.0f is 1", c[1]); ck_dbl(d, sum, 1.0, 1e-6);
        q.process(0.7); q.reset();
        CK_FMT(d, "after reset(), an impulse gives b0 again (f0=%.0f)", c[1]); ck_dbl(d, q.process(1.0), b0, 1e-12);
    }
    return ck_done();
}
""",
"Compute the six numbers, divide five of them by a0, and reuse your TDF-II process code."))

add(P("process_blocks", S, "Callbacks with std::function", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>void process_blocks(std::vector&lt;float&gt;&amp; x, std::size_t block,
                    const std::function&lt;void(float*, std::size_t)&gt;&amp; cb);</pre>
<p>Cut <code>x</code> into consecutive blocks of <code>block</code> samples and call
<code>cb(pointer_to_first_sample_of_the_block, number_of_samples_in_the_block)</code> once per block,
from the start of the vector to the end. The last block may be shorter.</p>
<p><b>Why it matters.</b> Audio APIs work this way: the driver calls <em>your</em> function
(a <em>callback</em>) for every block of samples, and your function processes them in place.</p>
<h4>The features used here</h4>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>std::function&lt;void(float*, std::size_t)&gt;</code></td><td>"Any function, lambda or
callable object that takes a <code>float*</code> and a <code>size_t</code> and returns nothing." You call
it like a normal function: <code>cb(p, n);</code></td></tr>
<tr><td><code>x.data()</code></td><td>pointer to the first sample of the vector</td></tr>
<tr><td><code>x.data() + i</code></td><td>pointer to sample number i (pointer arithmetic)</td></tr>
<tr><td><code>std::min(a, b)</code></td><td>the smaller of two values (in <code>&lt;algorithm&gt;</code>)</td></tr>
</table>
<h4>Picture: 10 samples, block = 4</h4>
<pre>index:  0   1   2   3 | 4   5   6   7 | 8   9
       [ ][ ][ ][ ]   [ ][ ][ ][ ]   [ ][ ]
        call 1         call 2         call 3
   cb(x.data()+0, 4)  cb(x.data()+4, 4)  cb(x.data()+8, 2)</pre>
<h4>Examples</h4>
<table>
<tr><th>x.size()</th><th>block</th><th>Calls (start index, count)</th></tr>
<tr><td>10</td><td>4</td><td>(0, 4) (4, 4) (8, 2)</td></tr>
<tr><td>8</td><td>4</td><td>(0, 4) (4, 4) &mdash; no empty third call</td></tr>
<tr><td>3</td><td>5</td><td>(0, 3) &mdash; one short block</td></tr>
<tr><td>0</td><td>4</td><td>no calls at all</td></tr>
</table>
<h4>What the hidden test does</h4>
<p>30 cases with 0 to 2000 samples and <code>block</code> from 1 to 300. Its callback doubles every
sample it receives. It checks that:</p>
<ul>
<li>blocks come in order, start right where the previous one ended, and only the last one is short;</li>
<li>no call has count 0, and the number of calls is size &divide; block rounded up;</li>
<li>every sample was doubled exactly once.</li>
</ul>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Let an index i start at 0 and jump forward by <code>block</code> while it is inside the vector.</li>
<li>How many samples are left from i to the end? The count for this call is the smaller of that and
<code>block</code>.</li>
</ol>
</details>""",
r"""#include <vector>
#include <functional>
#include <cstddef>

void process_blocks(std::vector<float>& x, std::size_t block,
                    const std::function<void(float*, std::size_t)>& cb)
{
}
""",
r"""#include <vector>
#include <functional>
#include <cstddef>
#include <algorithm>

void process_blocks(std::vector<float>& x, std::size_t block,
                    const std::function<void(float*, std::size_t)>& cb)
{
    for (std::size_t i = 0; i < x.size(); i += block)
        cb(x.data() + i, std::min(block, x.size() - i));
}
""",
r"""#include "check.h"
#include <vector>
#include <functional>
#include "solution.cpp"
int main()
{
    char d[128];
    for (int t = 0; t < 30; t++) {
        std::vector<float> x(ck_range(0, 2000));
        for (std::size_t i = 0; i < x.size(); i++) x[i] = (float)i;
        std::size_t block = (std::size_t)ck_range(1, 300), expect_off = 0;
        bool order_ok = true; int calls = 0;
        process_blocks(x, block, [&](float* p, std::size_t n) {
            if (p != x.data() + expect_off || n == 0 || n > block || expect_off + n > x.size()) order_ok = false;
            if (expect_off + n < x.size() && n != block) order_ok = false;
            for (std::size_t i = 0; i < n; i++) p[i] *= 2.0f;
            expect_off += n; calls++;
        });
        bool data_ok = expect_off == x.size();
        for (std::size_t i = 0; i < x.size(); i++) if (x[i] != 2.0f * i) data_ok = false;
        std::size_t want_calls = (x.size() + block - 1) / block;
        CK_FMT(d, "size %zu, block %zu: blocks are consecutive and full except the last", x.size(), block); ck_true(d, order_ok);
        CK_FMT(d, "size %zu, block %zu: number of callback calls", x.size(), block); ck_int(d, calls, (long long)want_calls);
        CK_FMT(d, "size %zu, block %zu: every sample processed exactly once", x.size(), block); ck_true(d, data_ok);
    }
    return ck_done();
}
""",
"Step i by block and pass std::min(block, x.size() - i) as the count."))

# ---------------------------------------------------------------------------
S = "Algorithms"

add(P("lower_bound", S, "Binary search", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>int lower_bound_idx(const std::vector&lt;int&gt;&amp; a, int x);</pre>
<p>The vector <code>a</code> is sorted from small to large. Return the <b>first index i with
<code>a[i] &gt;= x</code></b>. If no element is &gt;= x, return <code>a.size()</code>. It must run in
O(log n) steps (binary search), and you may not use <code>std::lower_bound</code>.</p>
<p><b>Why it matters.</b> This is "where would x go?" in a sorted list. It finds x if it is there,
and it is also the insert position if it is not. It is the safest form of binary search to learn,
because it handles duplicates and "not found" with no special cases.</p>
<h4>Examples with a = {1, 3, 3, 3, 7, 9}</h4>
<pre>index:   0  1  2  3  4  5
a:     { 1, 3, 3, 3, 7, 9 }</pre>
<table>
<tr><th>x</th><th>Answer</th><th>Why</th></tr>
<tr><td>0</td><td>0</td><td>every element is &gt;= 0</td></tr>
<tr><td>3</td><td>1</td><td>the <b>first</b> of the three 3s</td></tr>
<tr><td>4</td><td>4</td><td>4 is missing; 7 at index 4 is the first element &gt;= 4</td></tr>
<tr><td>9</td><td>5</td><td>the last element</td></tr>
<tr><td>10</td><td>6</td><td>nothing is &gt;= 10, so return a.size()</td></tr>
</table>
<h4>The idea: shrink a range that always contains the answer</h4>
<p>Keep two indices lo and hi such that the answer is always somewhere in lo &hellip; hi (hi = a.size()
is allowed, it means "past the end"). Look at the middle element:</p>
<ul>
<li>if <code>a[mid] &lt; x</code>, then mid and everything left of it are too small: the answer is right
of mid;</li>
<li>otherwise <code>a[mid] &gt;= x</code>: mid could be the answer, or the answer is further left.</li>
</ul>
<p>Stop when lo == hi. Trace for x = 4:</p>
<pre>lo  hi  mid  a[mid]  decision
 0   6    3     3    3 &lt; 4   -&gt; answer is right of 3: lo = 4
 4   6    5     9    9 &gt;= 4  -&gt; answer is 5 or left:  hi = 5
 4   5    4     7    7 &gt;= 4  -&gt; answer is 4 or left:  hi = 4
 4   4    stop: the answer is 4</pre>
<h4>What the hidden test does</h4>
<p>An empty vector (the answer is 0), then 30 sorted vectors of 0 to 3000 values between &minus;500 and
500 (many duplicates), with 20 values of x from &minus;520 to 520 each (some below, some above every
element).</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>What should lo and hi be at the start, so that "past the end" is a possible answer?</li>
<li>In each case of the rule above, which one of lo and hi moves, and to where? Make sure the range
gets smaller every time, or the loop never ends.</li>
<li>Compute mid as <code>lo + (hi - lo) / 2</code>.</li>
</ol>
</details>""",
r"""#include <vector>

int lower_bound_idx(const std::vector<int>& a, int x)
{
    return 0;
}
""",
r"""#include <vector>

int lower_bound_idx(const std::vector<int>& a, int x)
{
    int lo = 0, hi = static_cast<int>(a.size());   // answer is in [lo, hi]
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x)
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo;
}
""",
r"""#include "check.h"
#include <vector>
#include <algorithm>
#include "solution.cpp"
int main()
{
    char d[96];
    ck_int("lower_bound_idx({}, 5)", lower_bound_idx({}, 5), 0);
    for (int t = 0; t < 30; t++) {
        std::vector<int> a(ck_range(0, 3000));
        for (int& v : a) v = ck_range(-500, 500);
        std::sort(a.begin(), a.end());
        for (int k = 0; k < 20; k++) {
            int x = ck_range(-520, 520);
            CK_FMT(d, "lower_bound_idx(sorted vector of %zu, %d)", a.size(), x);
            ck_int(d, lower_bound_idx(a, x), std::lower_bound(a.begin(), a.end(), x) - a.begin());
        }
    }
    return ck_done();
}
""",
"Keep a half-open range [lo, hi). If a[mid] < x the answer is right of mid; otherwise it is mid or to its left."))

add(P("two_sum", S, "Two sum", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>std::pair&lt;int, int&gt; two_sum(const std::vector&lt;int&gt;&amp; a, int target);</pre>
<p>Find two <b>different positions</b> i &lt; j with <code>a[i] + a[j] == target</code>, and return
<code>{i, j}</code>. The input always has exactly one such pair. The two values may be equal to each
other, but you may not use the same position twice.</p>
<p><b>Why it matters.</b> One of the most common interview questions. The point is to trade memory for
speed: the hidden test has 20,000 elements, so trying every pair (about 200 million pairs) is far too
slow. Aim for one pass, O(n), using a hash map.</p>
<h4>The feature: <code>std::unordered_map</code></h4>
<p>A hash map from <code>&lt;unordered_map&gt;</code>. It stores key &rarr; value pairs and finds a key in
roughly constant time, however many keys it holds.</p>
<table>
<tr><th>Code</th><th>Meaning</th></tr>
<tr><td><code>std::unordered_map&lt;int, int&gt; seen;</code></td><td>empty map; here value &rarr; index</td></tr>
<tr><td><code>seen[v] = j;</code></td><td>store "value v is at index j"</td></tr>
<tr><td><code>auto it = seen.find(k);</code></td><td><code>it == seen.end()</code> if key k is not there;
otherwise <code>it-&gt;second</code> is its stored index</td></tr>
<tr><td><code>return {i, j};</code></td><td>builds the <code>std::pair</code></td></tr>
</table>
<h4>The idea</h4>
<p>When you reach <code>a[j]</code>, the partner it needs is <code>target - a[j]</code>. If that partner
appeared earlier, you are done.</p>
<h4>Trace: a = {3, 8, 5, 1}, target = 6</h4>
<pre>j  a[j]  needs 6-a[j]   seen before this step     found?
0    3        3         {}                        no -&gt; store 3:0
1    8       -2         {3:0}                     no -&gt; store 8:1
2    5        1         {3:0, 8:1}                no -&gt; store 5:2
3    1        5         {3:0, 8:1, 5:2}           yes, at 2 -&gt; {2, 3}</pre>
<p>Notice step 0: 3 needs another 3. Because the map is searched <b>before</b> a[0] is stored, the
single 3 cannot pair with itself.</p>
<h4>What the hidden test does</h4>
<ul>
<li><code>two_sum({2, 7, 11, 15}, 9)</code> must return <code>{0, 1}</code>.</li>
<li>5 vectors of 20,000 values, each with exactly one valid pair at random positions. The pair must
be returned with the smaller index first.</li>
</ul>""",
r"""#include <vector>
#include <utility>

std::pair<int, int> two_sum(const std::vector<int>& a, int target)
{
    return {0, 0};
}
""",
r"""#include <vector>
#include <utility>
#include <unordered_map>

std::pair<int, int> two_sum(const std::vector<int>& a, int target)
{
    std::unordered_map<int, int> seen;   // value -> index
    for (int j = 0; j < static_cast<int>(a.size()); j++) {
        auto it = seen.find(target - a[j]);
        if (it != seen.end())
            return {it->second, j};
        seen[a[j]] = j;
    }
    return {-1, -1};
}
""",
r"""#include "check.h"
#include <vector>
#include <utility>
#include <set>
#include "solution.cpp"
int main()
{
    char d[96];
    auto p = two_sum({2, 7, 11, 15}, 9);
    ck_true("two_sum({2, 7, 11, 15}, 9) == {0, 1}", p.first == 0 && p.second == 1);
    for (int t = 0; t < 5; t++) {
        int n = 20000;
        std::vector<int> a; std::set<int> used;
        while ((int)a.size() < n) { int v = ck_range(0, 500000000) * 4 + 1; if (used.insert(v).second) a.push_back(v); }   /* all 1 mod 4: any two sum to 2 mod 4 */
        int i = ck_range(0, n - 1), j = ck_range(0, n - 1); if (i == j) j = (j + 1) % n;
        if (i > j) { int s = i; i = j; j = s; }
        a[i] = 4 * ck_range(-1000000, 1000000); a[j] = 4 * ck_range(-1000000, 1000000);   /* the only pair summing to 0 mod 4 */
        int target = a[i] + a[j];
        auto r = two_sum(a, target);
        CK_FMT(d, "two_sum(20000 values) == {%d, %d}", i, j); ck_true(d, r.first == i && r.second == j);
    }
    return ck_done();
}
""",
"For each a[j], look up target - a[j] among the values you have already seen."))

add(P("balanced", S, "Balanced brackets", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>bool balanced(std::string_view s);</pre>
<p>Return <code>true</code> if the brackets <code>( )</code>, <code>[ ]</code> and <code>{ }</code> in
<code>s</code> are correctly matched and nested. All other characters are ignored.</p>
<p><b>Why it matters.</b> Compilers, JSON and XML parsers and code editors all do this check. It is
the standard first example of a <em>stack</em>.</p>
<h4>The rules</h4>
<ul>
<li>Every closing bracket must close the <b>most recent</b> bracket that is still open, and it must be
the same kind: <code>)</code> closes <code>(</code>, <code>]</code> closes <code>[</code>,
<code>}</code> closes <code>{</code>.</li>
<li>A closing bracket with nothing open is an error.</li>
<li>At the end, nothing may still be open.</li>
</ul>
<h4>Picture: a stack of open brackets</h4>
<p>A stack is a pile: you add on top (push) and take from the top (pop). In C++ a
<code>std::vector&lt;char&gt;</code> works: <code>push_back</code>, <code>back()</code>,
<code>pop_back()</code>, <code>empty()</code>.</p>
<pre>s = "{[()()]}"                    s = "{[(])}"
char  stack after it              char  stack after it
 {    {                            {    {
 [    {[                           [    {[
 (    {[(                          (    {[(
 )    {[      ( closed             ]    top is ( but ] needs [
 (    {[(                                -&gt; false
 )    {[
 ]    {
 }    (empty) -&gt; at the end: true</pre>
<h4>What the hidden test checks</h4>
<table>
<tr><th>Input</th><th>Answer</th><th>Why</th></tr>
<tr><td><code>"f(a[1]) { }"</code></td><td>true</td><td>letters and spaces ignored</td></tr>
<tr><td><code>"{[()()]}"</code></td><td>true</td><td>nested correctly</td></tr>
<tr><td><code>"x[i] = y[(j + 1) % n];"</code></td><td>true</td><td>real code</td></tr>
<tr><td><code>""</code> and <code>"no brackets"</code></td><td>true</td><td>nothing to match</td></tr>
<tr><td><code>"(]"</code></td><td>false</td><td>wrong kind</td></tr>
<tr><td><code>"{[(])}"</code></td><td>false</td><td>crossed, not nested</td></tr>
<tr><td><code>"(("</code></td><td>false</td><td>still open at the end</td></tr>
<tr><td><code>")("</code> and <code>"}"</code></td><td>false</td><td>closes with nothing open</td></tr>
</table>""",
r"""#include <string_view>

bool balanced(std::string_view s)
{
    return false;
}
""",
r"""#include <string_view>
#include <vector>

bool balanced(std::string_view s)
{
    std::vector<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push_back(c);
        } else if (c == ')' || c == ']' || c == '}') {
            char open = c == ')' ? '(' : (c == ']' ? '[' : '{');
            if (st.empty() || st.back() != open)
                return false;
            st.pop_back();
        }
    }
    return st.empty();
}
""",
r"""#include "check.h"
#include <string_view>
#include "solution.cpp"
int main()
{
    struct T { const char* s; bool b; } t[] = {
        {"f(a[1]) { }", true}, {"(]", false}, {"((", false}, {"", true}, {"no brackets", true},
        {"{[()()]}", true}, {"{[(])}", false}, {")(", false}, {"x[i] = y[(j + 1) % n];", true}, {"}", false}};
    char d[96];
    for (const auto& c : t) { CK_FMT(d, "balanced(\"%s\")", c.s); ck_int(d, balanced(c.s), c.b); }
    return ck_done();
}
""",
"Push opening brackets on a stack. A closing bracket must match the top of the stack. At the end the stack must be empty."))

add(P("max_subarray", S, "Maximum subarray", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>long long max_subarray(const std::vector&lt;int&gt;&amp; a);</pre>
<p>Return the <b>largest sum</b> you can get by adding a run of <b>consecutive</b> elements. The run
must contain at least one element. The vector is never empty. Use Kadane's algorithm, which needs
one pass: O(n).</p>
<h4>Examples</h4>
<pre>{-2, 1, -3, 4, -1, 2, 1, -5, 4}  -&gt;  6      the run 4, -1, 2, 1
{-3, -1, -2}                      -&gt;  -1     all negative: the best run
                                             is the single largest element</pre>
<p>The second example is why the answer is not simply "0 if everything is negative": an empty run
is not allowed.</p>
<h4>The idea</h4>
<p>For each position i, think about the best run that <b>ends exactly at i</b> (call it cur). There
are only two choices for it:</p>
<ul>
<li>start a new run at i: the sum is just <code>a[i]</code>;</li>
<li>extend the best run that ended at i&minus;1: the sum is <code>cur + a[i]</code>.</li>
</ul>
<p>Take the larger. The answer (best) is the largest cur seen at any position.</p>
<h4>Trace for the first example</h4>
<pre> i   a[i]   cur = max(a[i], cur + a[i])   best
 0    -2    -2  (start)                    -2
 1     1     1  (start new: 1 &gt; -2+1)       1
 2    -3    -2  (extend: 1-3)               1
 3     4     4  (start new: 4 &gt; -2+4)       4
 4    -1     3  (extend)                    4
 5     2     5  (extend)                    5
 6     1     6  (extend)                    6
 7    -5     1  (extend)                    6
 8     4     5  (extend)                    6   -&gt; answer 6</pre>
<h4>Things to watch out for</h4>
<ul>
<li>Overflow: the test uses values up to &plusmn;1,000,000,000 and up to 300 of them, so a sum can reach
3 &times; 10<sup>11</sup>. An <code>int</code> holds only about &plusmn;2.1 &times; 10<sup>9</sup>. Keep
your sums in <code>long long</code>.</li>
<li>Start cur and best from the first element, not from 0.</li>
</ul>
<p>The hidden test checks both examples above and 30 random vectors of 1 to 300 values against a
slow "try every run" answer.</p>""",
r"""#include <vector>

long long max_subarray(const std::vector<int>& a)
{
    return 0;
}
""",
r"""#include <vector>
#include <algorithm>

long long max_subarray(const std::vector<int>& a)
{
    long long best = a[0], cur = a[0];
    for (std::size_t i = 1; i < a.size(); i++) {
        cur = std::max<long long>(a[i], cur + a[i]);
        best = std::max(best, cur);
    }
    return best;
}
""",
r"""#include "check.h"
#include <vector>
#include "solution.cpp"
static long long ref_max(const std::vector<int>& a) { long long b = a[0]; for (size_t i = 0; i < a.size(); i++) { long long s = 0; for (size_t j = i; j < a.size(); j++) { s += a[j]; if (s > b) b = s; } } return b; }
int main()
{
    ck_int("max_subarray({-2, 1, -3, 4, -1, 2, 1, -5, 4})", max_subarray({-2, 1, -3, 4, -1, 2, 1, -5, 4}), 6);
    ck_int("max_subarray({-3, -1, -2})", max_subarray({-3, -1, -2}), -1);
    char d[96];
    for (int t = 0; t < 30; t++) {
        std::vector<int> a(ck_range(1, 300));
        for (int& v : a) v = ck_range(-1000000000, 1000000000) / (t % 2 ? 1 : 1000);
        CK_FMT(d, "max_subarray(random vector of %zu)", a.size()); ck_int(d, max_subarray(a), ref_max(a));
    }
    return ck_done();
}
""",
"Track the best sum of a run ending at i: either a[i] alone, or the previous run plus a[i]. Use long long."))

add(P("count_primes", S, "Sieve of Eratosthenes", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>int count_primes(int n);</pre>
<p>Return how many prime numbers are <b>smaller than n</b> (not equal to n). n is from 0 to
2,000,000. A prime is a whole number greater than 1 whose only divisors are 1 and itself: 2, 3, 5, 7,
11, &hellip;</p>
<p><b>Why it matters.</b> Testing each number separately is too slow for 2,000,000 numbers. The
<b>Sieve of Eratosthenes</b> finds all primes below n at once, in about n&middot;log(log n) steps. It is
a classic example of trading memory (one flag per number) for speed.</p>
<h4>The sieve, step by step</h4>
<ol>
<li>Make a list of flags for 0 &hellip; n&minus;1, all saying "maybe prime". 0 and 1 are not prime.</li>
<li>Go up from 2. When you reach a number still marked "maybe prime", it <b>is</b> prime. Count it.
Then cross out all its multiples.</li>
<li>For a prime p you can start crossing out at p&times;p: the smaller multiples (2p, 3p, &hellip;) were
already crossed out by smaller primes.</li>
</ol>
<h4>Picture for n = 20</h4>
<pre>number:     2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
p = 2:            x     x     x     x     x     x     x     x
p = 3:                           x                 x
p = 5:    5*5 = 25 is not below 20: nothing more to cross out
left:       2  3     5     7          11    13          17    19

p = 3 starts at 3*3 = 9 and would also hit 12 and 18,
but those were already crossed out by p = 2.   Result: 8 primes</pre>
<h4>Values to check against (all in the hidden test, except 20)</h4>
<table>
<tr><th>n</th><th>0</th><th>1</th><th>2</th><th>3</th><th>10</th><th>20</th><th>100</th><th>1000</th><th>7919</th><th>7920</th><th>1,000,000</th><th>2,000,000</th></tr>
<tr><td>count</td><td>0</td><td>0</td><td>0</td><td>1</td><td>4</td><td>8</td><td>25</td><td>168</td><td>999</td><td>1000</td><td>78498</td><td>148933</td></tr>
</table>
<p>7919 is itself prime (the 1000th prime). That is why n = 7919 gives 999 and n = 7920 gives 1000:
"smaller than n" matters.</p>
<h4>Things to watch out for</h4>
<ul>
<li>p&times;p overflows an <code>int</code> when p is above 46,340 (46,341&sup2; &gt; 2,147,483,647). Compute it
in <code>long long</code>, or only start crossing out while p&times;p &lt; n.</li>
<li>A <code>std::vector&lt;bool&gt;</code> of 2,000,000 flags is small (it uses one bit per flag).</li>
</ul>""",
r"""int count_primes(int n)
{
    return 0;
}
""",
r"""#include <vector>

int count_primes(int n)
{
    if (n < 3)
        return 0;
    std::vector<bool> composite(n, false);
    int count = 0;
    for (long long i = 2; i < n; i++) {
        if (composite[i])
            continue;
        count++;
        for (long long j = i * i; j < n; j += i)
            composite[j] = true;
    }
    return count;
}
""",
r"""#include "check.h"
#include "solution.cpp"
int main()
{
    int n[] = {0, 1, 2, 3, 10, 100, 1000, 7919, 7920, 1000000, 2000000};
    int want[] = {0, 0, 0, 1, 4, 25, 168, 999, 1000, 78498, 148933};
    char d[64];
    for (int i = 0; i < 11; i++) { CK_FMT(d, "count_primes(%d)", n[i]); ck_int(d, count_primes(n[i]), want[i]); }
    return ck_done();
}
""",
"Mark multiples of each prime p starting at p*p. Use long long for p*p."))

add(P("fib_mod", S, "Fibonacci with dynamic programming", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>int fib_mod(int n);</pre>
<p>Return F(n) mod 1,000,000,007 for n from 0 up to 10,000,000. The Fibonacci numbers are</p>
<pre>F(0) = 0,  F(1) = 1,  F(n) = F(n-1) + F(n-2)

n:     0  1  2  3  4  5  6   7   8   9  10
F(n):  0  1  1  2  3  5  8  13  21  34  55</pre>
<p>"mod 1,000,000,007" means: return the remainder after dividing by 1,000,000,007.</p>
<h4>Why the starter code fails</h4>
<p>The starter calls itself twice for every n. The calls form a tree that roughly doubles with each
level:</p>
<pre>                fib(5)
            /           \
       fib(4)           fib(3)
       /     \          /    \
   fib(3)  fib(2)   fib(2)  fib(1)      fib(3) is computed twice,
   /   \     ...      ...               fib(2) three times, ...</pre>
<p>That is about 1.6<sup>n</sup> calls: hopeless for n = 50, impossible for 10,000,000. The fix
(<em>dynamic programming</em>): compute F(0), F(1), F(2), &hellip; in order, and remember only the last two
values. That is n steps and two variables.</p>
<h4>Why the "mod" is needed</h4>
<ul>
<li>F(46) = 1,836,311,903 still fits in an <code>int</code> (largest 2,147,483,647). F(47) =
2,971,215,073 does not.</li>
<li>Rule: (x + y) mod M = ((x mod M) + (y mod M)) mod M. So you may take the remainder after every
addition and the result is still right.</li>
<li>If both numbers are below M = 1,000,000,007, their sum is below 2,000,000,014, which still fits in
an <code>int</code>.</li>
</ul>
<h4>Examples (in the hidden test)</h4>
<table>
<tr><th>n</th><th>F(n) mod 1,000,000,007</th></tr>
<tr><td>0</td><td>0</td></tr>
<tr><td>1</td><td>1</td></tr>
<tr><td>2</td><td>1</td></tr>
<tr><td>10</td><td>55</td></tr>
<tr><td>50</td><td>586268941 (F(50) = 12,586,269,025, and 12,586,269,025 mod 1,000,000,007 = 586,268,941)</td></tr>
<tr><td>1000</td><td>517691607</td></tr>
<tr><td>10,000,000</td><td>(checked by the test)</td></tr>
</table>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>Keep two variables a = F(i) and b = F(i+1), starting at i = 0.</li>
<li>One step moves both forward: what are the new a and b, in terms of the old ones?</li>
<li>After n steps, which of the two variables holds F(n)? Check with n = 0 and n = 1.</li>
</ol>
</details>""",
r"""int fib_mod(int n)
{
    if (n < 2)
        return n;
    return fib_mod(n - 1) + fib_mod(n - 2);
}
""",
r"""int fib_mod(int n)
{
    const int MOD = 1000000007;
    int a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        int c = (a + b) % MOD;   // a + b < 2^31 because both are < MOD
        a = b;
        b = c;
    }
    return a;
}
""",
r"""#include "check.h"
#include "solution.cpp"
int main()
{
    int n[] = {0, 1, 2, 10, 50, 1000, 10000000};
    long long want[] = {0, 1, 1, 55, 12586269025LL % 1000000007, 517691607, 0};
    { long long a = 0, b = 1; for (int i = 0; i < 10000000; i++) { long long c = (a + b) % 1000000007; a = b; b = c; } want[6] = a; }
    char d[64];
    for (int i = 0; i < 7; i++) { CK_FMT(d, "fib_mod(%d)", n[i]); ck_int(d, fib_mod(n[i]), want[i]); }
    return ck_done();
}
""",
"Iterate: (a, b) -> (b, (a + b) % MOD), n times."))

add(P("merge_sorted", S, "Merge two sorted vectors", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>std::vector&lt;int&gt; merge_sorted(const std::vector&lt;int&gt;&amp; a,
                              const std::vector&lt;int&gt;&amp; b);</pre>
<p>Both inputs are already sorted from small to large. Return one sorted vector that contains every
element of both (duplicates kept). It must run in O(n + m) steps, where n and m are the two
sizes: one pass, no sorting.</p>
<p><b>Why it matters.</b> This is the core step of <em>merge sort</em>, and the same idea merges sorted
files, sorted event lists or timestamped packets from two sources.</p>
<h4>The idea: two fingers</h4>
<p>Put one finger (index i) on the front of a and one (index j) on the front of b. The smallest
remaining value is always under one of the two fingers. Take the smaller one, move that finger, and
repeat. When one vector runs out, copy the rest of the other.</p>
<h4>Trace: a = {1, 4, 9}, b = {2, 3, 10, 11}</h4>
<pre>a[i]  b[j]   take      out
  1     2    1 (a)     1
  4     2    2 (b)     1 2
  4     3    3 (b)     1 2 3
  4    10    4 (a)     1 2 3 4
  9    10    9 (a)     1 2 3 4 9
  a is used up: copy the rest of b -&gt;  1 2 3 4 9 10 11</pre>
<h4>Edge cases</h4>
<table>
<tr><th>a</th><th>b</th><th>Result</th></tr>
<tr><td>{}</td><td>{}</td><td>{}</td></tr>
<tr><td>{}</td><td>{5, 6}</td><td>{5, 6}</td></tr>
<tr><td>{1, 3, 3}</td><td>{2, 3}</td><td>{1, 2, 3, 3, 3} (all three 3s kept)</td></tr>
</table>
<p>The hidden test merges 30 pairs of sorted vectors, each with 0 to 500 values between &minus;100 and
100 (so empty inputs and many equal values occur), and compares with the fully sorted answer.</p>
<p>Tip: <code>out.reserve(a.size() + b.size())</code> sets aside room once, so <code>push_back</code> never
has to grow the vector.</p>""",
r"""#include <vector>

std::vector<int> merge_sorted(const std::vector<int>& a, const std::vector<int>& b)
{
    return {};
}
""",
r"""#include <vector>

std::vector<int> merge_sorted(const std::vector<int>& a, const std::vector<int>& b)
{
    std::vector<int> out;
    out.reserve(a.size() + b.size());
    std::size_t i = 0, j = 0;
    while (i < a.size() && j < b.size())
        out.push_back(a[i] <= b[j] ? a[i++] : b[j++]);
    while (i < a.size()) out.push_back(a[i++]);
    while (j < b.size()) out.push_back(b[j++]);
    return out;
}
""",
r"""#include "check.h"
#include <vector>
#include <algorithm>
#include "solution.cpp"
int main()
{
    char d[96];
    for (int t = 0; t < 30; t++) {
        std::vector<int> a(ck_range(0, 500)), b(ck_range(0, 500));
        for (int& v : a) v = ck_range(-100, 100);
        for (int& v : b) v = ck_range(-100, 100);
        std::sort(a.begin(), a.end()); std::sort(b.begin(), b.end());
        std::vector<int> w(a); w.insert(w.end(), b.begin(), b.end()); std::sort(w.begin(), w.end());
        CK_FMT(d, "merge_sorted(%zu values, %zu values)", a.size(), b.size()); ck_true(d, merge_sorted(a, b) == w);
    }
    return ck_done();
}
""",
"Two indices; always take the smaller front element; then copy what is left."))

add(P("palindrome", S, "Palindrome", "cpp", "func",
r"""<p><b>What to write.</b></p>
<pre>bool is_palindrome(std::string_view s);</pre>
<p>A <em>palindrome</em> reads the same forwards and backwards. Here you look only at <b>letters and
digits</b>: skip spaces and punctuation, and treat upper and lower case as the same
(<code>'A'</code> equals <code>'a'</code>). Return whether what is left is a palindrome.</p>
<h4>Facts you need (from <code>&lt;cctype&gt;</code>)</h4>
<table>
<tr><th>Function</th><th>Meaning</th></tr>
<tr><td><code>std::isalnum(c)</code></td><td>non-zero if c is a letter <code>A</code>&hellip;<code>Z</code>,
<code>a</code>&hellip;<code>z</code> or a digit <code>0</code>&hellip;<code>9</code></td></tr>
<tr><td><code>std::tolower(c)</code></td><td>the lower-case version of a letter (<code>'P'</code> &rarr;
<code>'p'</code>); any other character is returned unchanged</td></tr>
</table>
<p>Pass these functions an <code>unsigned char</code> value, e.g.
<code>std::isalnum((unsigned char)c)</code>. On this site <code>char</code> is signed, and a negative
value other than EOF is not allowed for them.</p>
<h4>Examples</h4>
<table>
<tr><th>Input</th><th>Letters and digits, lower case</th><th>Answer</th></tr>
<tr><td><code>"A man, a plan, a canal: Panama"</code></td><td>amanaplanacanalpanama</td><td>true</td></tr>
<tr><td><code>"race a car"</code></td><td>raceacar</td><td>false</td></tr>
<tr><td><code>"Ab, 2 b-a!"</code></td><td>ab2ba</td><td>true</td></tr>
<tr><td><code>"0P"</code></td><td>0p</td><td>false (a digit is not a letter)</td></tr>
<tr><td><code>""</code> and <code>".,"</code></td><td>(nothing)</td><td>true: nothing left reads the same both ways</td></tr>
</table>
<h4>Picture: two indices moving inwards</h4>
<pre>s = "Ab, 2 b-a!"   (. = space)
index:    0  1  2  3  4  5  6  7  8  9
s:        A  b  ,  .  2  .  b  -  a  !
          i                          j   '!' skipped: j moves left
          i                       j      'A' vs 'a': same, both move
             i                 j         '-' skipped: j moves left
             i              j            'b' vs 'b': same, both move
                i        j               ',' skipped: i moves right
                   i     j               ' ' skipped: i moves right
                      i  j               ' ' skipped: j moves left
                     ij                  i is not left of j: stop, true</pre>
<p>Comparing in place this way needs no copy of the string. (Building a cleaned copy and comparing it
with its reverse also passes.)</p>
<p>The hidden test checks the examples above plus <code>"Was it a car or a cat I saw?"</code> (true),
<code>"ab2ba"</code> (true) and <code>"ab"</code> (false).</p>""",
r"""#include <string_view>

bool is_palindrome(std::string_view s)
{
    return false;
}
""",
r"""#include <string_view>
#include <cctype>

bool is_palindrome(std::string_view s)
{
    if (s.empty())
        return true;
    std::size_t i = 0, j = s.size() - 1;
    while (i < j) {
        unsigned char a = static_cast<unsigned char>(s[i]), b = static_cast<unsigned char>(s[j]);
        if (!std::isalnum(a)) { i++; continue; }
        if (!std::isalnum(b)) { j--; continue; }
        if (std::tolower(a) != std::tolower(b))
            return false;
        i++;
        j--;
    }
    return true;
}
""",
r"""#include "check.h"
#include <string_view>
#include "solution.cpp"
int main()
{
    struct T { const char* s; bool b; } t[] = {
        {"A man, a plan, a canal: Panama", true}, {"race a car", false}, {"", true}, {".,", true},
        {"0P", false}, {"Was it a car or a cat I saw?", true}, {"ab2ba", true}, {"ab", false}};
    char d[96];
    for (const auto& c : t) { CK_FMT(d, "is_palindrome(\"%s\")", c.s); ck_int(d, is_palindrome(c.s), c.b); }
    return ck_done();
}
""",
"Two indices moving inwards; skip characters that are not letters or digits; compare with tolower."))

add(P("matmul", S, "Matrix multiply", "cpp", "func",
r"""<p><b>What to write.</b> With</p>
<pre>using Matrix = std::vector&lt;std::vector&lt;double&gt;&gt;;   // a list of rows</pre>
<p>write <code>Matrix matmul(const Matrix&amp; A, const Matrix&amp; B)</code>. A has n rows and k
columns; B has k rows and m columns. Return C = A&middot;B, which has <b>n rows and m columns</b>.</p>
<h4>The rule</h4>
<p>Each entry is "row i of A times column j of B": multiply the pairs and add them up.</p>
<pre>C[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + ... + A[i][k-1]*B[k-1][j]</pre>
<h4>Worked example (2&times;3 times 3&times;2 gives 2&times;2)</h4>
<pre>    A           B              C
| 1 2 3 |   |  7  8 |     |  58  64 |
| 4 5 6 | x |  9 10 |  =  | 139 154 |
            | 11 12 |

C[0][0] = 1*7 + 2*9 + 3*11  = 7 + 18 + 33  = 58
C[0][1] = 1*8 + 2*10 + 3*12 = 8 + 20 + 36  = 64
C[1][0] = 4*7 + 5*9 + 6*11  = 28 + 45 + 66 = 139
C[1][1] = 4*8 + 5*10 + 6*12 = 32 + 50 + 72 = 154</pre>
<h4>Facts you need</h4>
<ul>
<li>n = <code>A.size()</code> (number of rows), k = <code>B.size()</code>, m = <code>B[0].size()</code>
(length of a row of B).</li>
<li><code>Matrix C(n, std::vector&lt;double&gt;(m, 0.0));</code> makes n rows of m zeros.</li>
<li>Each row of a <code>std::vector&lt;std::vector&lt;double&gt;&gt;</code> is stored separately, and the
numbers inside one row sit next to each other in memory. Loops that walk along a row are faster than
loops that jump down a column.</li>
</ul>
<h4>What the hidden test does</h4>
<p>15 random cases with n, k and m each from 1 to 30 (so 1&times;1 and long thin shapes occur) and
values between &minus;1 and 1. It checks that C has exactly n rows of m values each, and that every
value is within 10<sup>&minus;9</sup> of the exact sum.</p>
<details><summary>How to think about it (open if you are stuck)</summary>
<ol>
<li>One loop over the rows i of C, one over the columns j, and one over p = 0 &hellip; k&minus;1 for the
sum.</li>
<li>Optional speed-up: the three loops can be put in any order. Which order makes the innermost loop
walk along a row of B and a row of C?</li>
</ol>
</details>""",
r"""#include <vector>

using Matrix = std::vector<std::vector<double>>;

Matrix matmul(const Matrix& A, const Matrix& B)
{
    return {};
}
""",
r"""#include <vector>

using Matrix = std::vector<std::vector<double>>;

Matrix matmul(const Matrix& A, const Matrix& B)
{
    std::size_t n = A.size(), k = B.size(), m = B[0].size();
    Matrix C(n, std::vector<double>(m, 0.0));
    for (std::size_t i = 0; i < n; i++)
        for (std::size_t p = 0; p < k; p++)
            for (std::size_t j = 0; j < m; j++)
                C[i][j] += A[i][p] * B[p][j];
    return C;
}
""",
r"""#include "check.h"
#include <vector>
#include "solution.cpp"
int main()
{
    char d[96];
    for (int t = 0; t < 15; t++) {
        int n = ck_range(1, 30), k = ck_range(1, 30), m = ck_range(1, 30);
        Matrix A(n, std::vector<double>(k)), B(k, std::vector<double>(m));
        for (auto& r : A) for (double& v : r) v = ck_unit();
        for (auto& r : B) for (double& v : r) v = ck_unit();
        Matrix C = matmul(A, B);
        bool ok = (int)C.size() == n;
        for (int i = 0; ok && i < n; i++) {
            if ((int)C[i].size() != m) { ok = false; break; }
            for (int j = 0; j < m; j++) { double s = 0; for (int p = 0; p < k; p++) s += A[i][p] * B[p][j]; if (std::fabs(C[i][j] - s) > 1e-9) ok = false; }
        }
        CK_FMT(d, "matmul(%dx%d, %dx%d)", n, k, k, m); ck_true(d, ok);
    }
    return ck_done();
}
""",
"Create C with n rows of m zeros, then three nested loops. The i-p-j loop order reads memory row by row, which is faster."))

add(P("gcd_lcm", S, "GCD and LCM", "c", "func",
r"""<p><b>What to write</b> (in C, for inputs &ge; 0):</p>
<pre>long long gcd_ll(long long a, long long b);  // greatest common divisor
long long lcm_ll(long long a, long long b);  // least common multiple</pre>
<ul>
<li>gcd(a, b) is the largest number that divides both. Special case: gcd(0, 0) = 0, and
gcd(a, 0) = a.</li>
<li>lcm(a, b) is the smallest positive number that both divide. Special case: lcm(x, 0) = 0.</li>
</ul>
<p><b>Why it matters.</b> Example from audio: converting between 44,100 Hz and 48,000 Hz. gcd = 300,
so the ratio is 147 : 160, and lcm = 7,056,000 Hz is the smallest rate that both divide.</p>
<h4>Euclid's algorithm for the GCD</h4>
<p>Rule: gcd(a, b) = gcd(b, a % b). Repeat until b is 0; then a is the answer.</p>
<pre>  a        b        a % b
44100    48000     44100      (a &lt; b: the first step just swaps them)
48000    44100      3900
44100     3900      1200
 3900     1200       300
 1200      300         0
  300        0               -&gt; gcd = 300</pre>
<p>Another one: gcd(12, 18): (12, 18) &rarr; (18, 12) &rarr; (12, 6) &rarr; (6, 0) &rarr; 6.</p>
<h4>The LCM from the GCD</h4>
<p>lcm(a, b) = a &times; b / gcd(a, b). But compute it as <b>a / gcd &times; b</b>: divide first.
a / gcd is a whole number, so nothing is lost, and the value in between stays small.</p>
<pre>lcm(44100, 48000) = 44100 / 300 * 48000 = 147 * 48000 = 7056000
lcm(4, 6)         = 4 / 2 * 6           = 12</pre>
<p>Why divide first: a <code>long long</code> holds up to 9,223,372,036,854,775,807 (about 9.2
&times; 10<sup>18</sup>). For a = b = 4,000,000,000 the product a &times; b = 1.6 &times; 10<sup>19</sup>
overflows, even though lcm(a, b) is only 4,000,000,000.</p>
<h4>What the hidden test checks</h4>
<table>
<tr><th>Call</th><th>Answer</th></tr>
<tr><td><code>gcd_ll(0, 0)</code></td><td>0</td></tr>
<tr><td><code>gcd_ll(12, 18)</code></td><td>6</td></tr>
<tr><td><code>lcm_ll(4, 6)</code></td><td>12</td></tr>
<tr><td><code>lcm_ll(7, 0)</code></td><td>0 (also make sure you never divide by a gcd of 0)</td></tr>
<tr><td><code>lcm_ll(44100, 48000)</code></td><td>7056000</td></tr>
</table>
<p>Then 200 random pairs with a and b from 0 to 2,000,000,000 (a value can be 0).</p>""",
r"""long long gcd_ll(long long a, long long b)
{
    return 1;
}

long long lcm_ll(long long a, long long b)
{
    return a * b;
}
""",
r"""long long gcd_ll(long long a, long long b)
{
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

long long lcm_ll(long long a, long long b)
{
    if (a == 0 || b == 0)
        return 0;
    return a / gcd_ll(a, b) * b;
}
""",
r"""#include "check.h"
#include "solution.c"
static long long g_(long long a, long long b) { while (b) { long long t = a % b; a = b; b = t; } return a; }
int main(void)
{
    char d[96];
    ck_int("gcd_ll(0, 0)", gcd_ll(0, 0), 0);
    ck_int("gcd_ll(12, 18)", gcd_ll(12, 18), 6);
    ck_int("lcm_ll(4, 6)", lcm_ll(4, 6), 12);
    ck_int("lcm_ll(7, 0)", lcm_ll(7, 0), 0);
    ck_int("lcm_ll(44100, 48000)", lcm_ll(44100, 48000), 7056000);
    for (int i = 0; i < 200; i++) {
        long long a = ck_range(0, 2000000000), b = ck_range(0, 2000000000), g = g_(a, b);
        CK_FMT(d, "gcd_ll(%lld, %lld)", a, b); ck_int(d, gcd_ll(a, b), g);
        if (g && a / g <= 4000000000LL) { CK_FMT(d, "lcm_ll(%lld, %lld)", a, b); ck_int(d, lcm_ll(a, b), a / g * b); }
    }
    return ck_done();
}
""",
"Euclid: gcd(a, b) = gcd(b, a % b) until b is 0."))
