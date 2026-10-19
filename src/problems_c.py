# Problem bank, part C: C++ language and algorithms.
from common import P

PROBLEMS = []
add = PROBLEMS.append

S = "C++ language"

add(P("cpp_hello", S, "Hello, C++", "cpp", "stdout",
r"""<p>Write a C++ program that prints this line with <code>std::cout</code>:</p>
<pre>Hello, C++!</pre>""",
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
r"""<p>In C++ a function can take its arguments <em>by reference</em> (<code>T&amp;</code>), so it
changes the caller's variables without pointers. Write a function template</p>
<pre>template &lt;typename T&gt;
void my_swap(T&amp; a, T&amp; b);</pre>
<p>that swaps two values of any type. The test uses <code>int</code>, <code>double</code> and
<code>std::string</code>.</p>""",
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
r"""<p>C++ lets two functions share a name if their parameter types differ. Write both:</p>
<pre>int    area(int w, int h);  // rectangle: w * h
double area(double r);      // circle: pi * r * r, pi = 3.14159265358979323846</pre>""",
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
r"""<p>Complete the class <code>Counter</code>. It starts at the value given to the constructor
(default 0), <code>inc()</code> adds 1, <code>add(n)</code> adds n, and <code>value()</code>
returns the current value. <code>value()</code> is <code>const</code>: it must not change the
object.</p>""",
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
r"""<p>Complete <code>Tracker</code> so that the static member <code>live</code> always holds how
many Tracker objects exist: the constructors add 1 and the destructor subtracts 1. This is
<b>RAII</b>: code that runs automatically when an object is created and destroyed. Lock guards,
file handles and audio-device handles all use it.</p>
<p>The test creates Trackers on the stack, copies them, puts them in a
<code>std::vector</code>, and uses <code>new</code>/<code>delete</code>.</p>""",
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
r"""<p>The starter code defines a small complex-number type. Write the operators, so that DSP
code can be written as maths:</p>
<pre>Cplx   operator+(Cplx a, Cplx b);
Cplx   operator*(Cplx a, Cplx b);   // (a.re*b.re - a.im*b.im, a.re*b.im + a.im*b.re)
double mag(Cplx a);                 // sqrt(re^2 + im^2)</pre>""",
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
r"""<p>Write a function template that clamps a value of any ordered type:</p>
<pre>template &lt;typename T&gt;
T clamp_to(T x, T lo, T hi);</pre>
<p>Use only <code>&lt;</code> to compare (the test also uses a type that only has
<code>operator&lt;</code>).</p>""",
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
r"""<p>Write <code>std::vector&lt;int&gt; keep_even(const std::vector&lt;int&gt;&amp; v)</code> that
returns a new vector with only the even numbers of <code>v</code>, in the same order.</p>
<p>Passing by <code>const&amp;</code> avoids copying the input.</p>""",
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
r"""<p>Write <code>void sort_by_abs(std::vector&lt;int&gt;&amp; v)</code> that sorts by absolute value,
smallest first. When two values have the same absolute value, the negative one comes first.</p>
<pre>{3, -1, 2, -3, 1, 0} -> {0, -1, 1, 2, -3, 3}</pre>
<p>Use <code>std::sort</code> with a lambda as the comparison.</p>""",
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
r"""<p>Write <code>int count_words(const std::string&amp; s)</code> that counts words separated by
one or more spaces, tabs or newlines.</p>
<pre>count_words("  real time   audio\n") -> 3</pre>""",
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
r"""<p>Write <code>std::map&lt;char, int&gt; char_freq(const std::string&amp; s)</code> that counts
how many times each character appears, ignoring spaces.</p>
<pre>char_freq("aab b") -> {'a': 2, 'b': 2}</pre>""",
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
r"""<p>An audio buffer owns a block of memory. Copying it would be slow, so make it
<b>move-only</b>: moving hands the memory over and leaves the source empty. Complete the class:</p>
<ul><li><code>Buffer(n)</code> allocates n floats set to 0;</li>
<li>the move constructor and move assignment take the other buffer's memory; the other buffer
ends with <code>size() == 0</code> and <code>data() == nullptr</code>;</li>
<li>the destructor frees the memory. Nothing may leak: the test counts every
<code>new</code> and <code>delete</code>.</li></ul>""",
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
r"""<p>The starter code works, but the test uses it in <code>static_assert</code> and to fill a
constant table, so it must run <b>at compile time</b>. Make it <code>constexpr</code>.</p>
<pre>uint32_t next_pow2_c(uint32_t x);  // smallest power of two >= x, for x >= 1</pre>
<p>Computing tables at compile time (window functions, filter coefficients) costs nothing at
run time.</p>""",
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
r"""<p>The starter code has an abstract base class <code>Shape</code>. Add two derived classes and
a function:</p>
<ul><li><code>Rect(double w, double h)</code> with area w&middot;h;</li>
<li><code>Circle(double r)</code> with area &pi;r&sup2; (&pi; = 3.14159265358979323846);</li>
<li><code>double total_area(const std::vector&lt;std::unique_ptr&lt;Shape&gt;&gt;&amp; shapes)</code>.</li></ul>
<p>The test calls <code>area()</code> through <code>Shape</code> pointers, so the right version
must be chosen at run time.</p>""",
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
r"""<p>Write a fixed-capacity FIFO as a class template, with no heap allocation (use a
<code>std::array</code>):</p>
<pre>template &lt;typename T, std::size_t N&gt;
class RingBuffer {
public:
    bool push(const T&amp; v);   // false if full
    bool pop(T&amp; out);        // false if empty
    std::size_t size() const;
    bool empty() const;
    bool full() const;        // size() == N
};</pre>
<p><code>N</code> can be any capacity from 1 up, not only a power of two.</p>""",
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
r"""<p><code>std::span</code> (C++20) is a pointer plus a length: a safe view of someone else's
array, perfect for audio blocks. Write</p>
<pre>float sum_span(std::span&lt;const float&gt; s);
float mean_of_last(std::span&lt;const float&gt; s, std::size_t k); // mean of the last k samples, k >= 1, k <= size</pre>
<p>Hint: <code>s.last(k)</code> gives a smaller span.</p>""",
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
r"""<p>Write <code>std::optional&lt;unsigned&gt; parse_uint(std::string_view s)</code>. Return the
value if <code>s</code> is a non-empty string of digits only, with a value of at most
1,000,000,000. Otherwise return <code>std::nullopt</code>.</p>
<pre>"48000" -> 48000      "" -> nullopt      "12a" -> nullopt
"99999999999999999999" -> nullopt (too big; don't overflow)</pre>""",
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
r"""<p>Put it together: a biquad class that designs its own coefficients with the
<em>Audio EQ Cookbook</em> (Robert Bristow-Johnson) low-pass formulas, in <code>double</code>:</p>
<pre>w0 = 2 pi f0 / fs,   alpha = sin(w0) / (2 Q)
b0 = (1 - cos w0)/2,  b1 = 1 - cos w0,  b2 = (1 - cos w0)/2
a0 = 1 + alpha,       a1 = -2 cos w0,   a2 = 1 - alpha
divide b0, b1, b2, a1, a2 by a0</pre>
<p>Process with Transposed Direct Form II. <code>reset()</code> clears the state but keeps the
coefficients. Use &pi; = 3.14159265358979323846.</p>""",
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
r"""<p>Audio APIs call <em>your</em> function for every block of samples. Write</p>
<pre>void process_blocks(std::vector&lt;float&gt;&amp; x, std::size_t block,
                    const std::function&lt;void(float*, std::size_t)&gt;&amp; cb);</pre>
<p>It calls <code>cb(pointer, count)</code> for consecutive blocks of <code>block</code>
samples, in order. The last block may be shorter. <code>block</code> is at least 1. The callback
can change the samples through the pointer.</p>""",
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
r"""<p>Write <code>int lower_bound_idx(const std::vector&lt;int&gt;&amp; a, int x)</code>. The vector
is sorted. Return the first index i with <code>a[i] &gt;= x</code>, or <code>a.size()</code> if
there is none. Do it in O(log n), without <code>std::lower_bound</code>.</p>""",
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
r"""<p>Write <code>std::pair&lt;int, int&gt; two_sum(const std::vector&lt;int&gt;&amp; a, int target)</code>
that returns indices i &lt; j with a[i] + a[j] == target. Exactly one such pair exists. The
test has 20,000 elements, so aim for O(n) with a hash map.</p>""",
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
r"""<p>Write <code>bool balanced(std::string_view s)</code> that checks that the brackets
<code>() [] {}</code> are correctly nested. Ignore all other characters.</p>
<pre>"f(a[1]) { }" -> true      "(]" -> false      "((" -> false</pre>""",
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
r"""<p>Write <code>long long max_subarray(const std::vector&lt;int&gt;&amp; a)</code> that returns the
largest sum of a non-empty run of consecutive elements (Kadane's algorithm, O(n)).</p>
<pre>{-2, 1, -3, 4, -1, 2, 1, -5, 4} -> 6   (4, -1, 2, 1)
{-3, -1, -2} -> -1</pre>""",
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
r"""<p>Write <code>int count_primes(int n)</code> that returns how many primes are smaller than
<code>n</code> (0 &le; n &le; 2,000,000).</p>
<pre>count_primes(10) -> 4   (2, 3, 5, 7)</pre>""",
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
r"""<p>Write <code>int fib_mod(int n)</code> returning F(n) mod 1,000,000,007, with F(0) = 0 and
F(1) = 1, for n up to 10,000,000. Plain recursion takes forever; keep only the last two
values.</p>""",
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
r"""<p>Write <code>std::vector&lt;int&gt; merge_sorted(const std::vector&lt;int&gt;&amp; a,
const std::vector&lt;int&gt;&amp; b)</code> for two sorted inputs, in O(n + m), without sorting again.
This is the core step of merge sort.</p>""",
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
r"""<p>Write <code>bool is_palindrome(std::string_view s)</code> that looks only at letters and
digits, ignores case, and returns whether they read the same backwards.</p>
<pre>"A man, a plan, a canal: Panama" -> true      "race a car" -> false</pre>""",
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
r"""<p>With <code>using Matrix = std::vector&lt;std::vector&lt;double&gt;&gt;;</code>, write
<code>Matrix matmul(const Matrix&amp; A, const Matrix&amp; B)</code> for an n&times;k matrix A and a
k&times;m matrix B. The result is n&times;m with C[i][j] = &Sigma;<sub>p</sub> A[i][p]&middot;B[p][j].</p>""",
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
r"""<p>Write, in C, for non-negative inputs:</p>
<pre>long long gcd_ll(long long a, long long b);  // gcd(0, 0) = 0
long long lcm_ll(long long a, long long b);  // lcm(x, 0) = 0; the result fits in long long</pre>
<p>Compute the LCM as a / gcd &middot; b (divide first, so the intermediate does not overflow).</p>""",
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
