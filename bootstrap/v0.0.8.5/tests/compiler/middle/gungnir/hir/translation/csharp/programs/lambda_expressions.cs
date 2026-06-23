// Lambda expressions
using System;
using System.Collections.Generic;
using System.Linq;

namespace LambdaTest
{
    public class Calculator
    {
        // Single-parameter lambda
        public int Square(int x) => x * x;

        // Multi-parameter lambda
        public int Add(int x, int y) => x + y;

        public void TestLambdas()
        {
            // Expression lambda
            Func<int, int> double_value = x => x * 2;
            int result1 = double_value(5);

            // Statement lambda
            Func<int, int, int> multiply = (x, y) => { return x * y; };
            int result2 = multiply(3, 4);

            // Lambda with LINQ
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
            var evens = numbers.Where(n => n % 2 == 0);
            var squares = numbers.Select(n => n * n);

            // Lambda with multiple statements
            Action<string> greet = name =>
            {
                string message = "Hello, " + name;
                Console.WriteLine(message);
            };
        }
    }
}
