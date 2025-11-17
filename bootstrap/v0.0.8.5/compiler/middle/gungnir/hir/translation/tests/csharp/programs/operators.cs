// Various operators
using System;

namespace OperatorTest
{
    public class Operators
    {
        public void TestArithmetic()
        {
            int a = 10;
            int b = 3;

            int sum = a + b;
            int diff = a - b;
            int prod = a * b;
            int quot = a / b;
            int rem = a % b;

            int x = 5;
            x++;
            ++x;
            x--;
            --x;
        }

        public void TestComparison()
        {
            int a = 10;
            int b = 20;

            bool eq = a == b;
            bool neq = a != b;
            bool lt = a < b;
            bool gt = a > b;
            bool lte = a <= b;
            bool gte = a >= b;
        }

        public void TestLogical()
        {
            bool p = true;
            bool q = false;

            bool and_result = p && q;
            bool or_result = p || q;
            bool not_result = !p;
        }

        public void TestBitwise()
        {
            int a = 5;
            int b = 3;

            int and_bits = a & b;
            int or_bits = a | b;
            int xor_bits = a ^ b;
            int not_bits = ~a;
            int left_shift = a << 2;
            int right_shift = a >> 1;
        }

        public void TestAssignment()
        {
            int x = 10;
            x += 5;
            x -= 3;
            x *= 2;
            x /= 4;
            x %= 3;
        }

        public void TestTernary(int x)
        {
            string result = x > 0 ? "Positive" : "Non-positive";
        }

        public void TestNullCoalescing()
        {
            string? name = null;
            string displayName = name ?? "Unknown";
        }
    }
}
