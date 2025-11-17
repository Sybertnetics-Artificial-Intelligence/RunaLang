// Control flow statements
using System;
using System.Collections.Generic;

namespace ControlFlowTest
{
    public class ControlFlow
    {
        public void TestIf(int x)
        {
            if (x > 0)
            {
                Console.WriteLine("Positive");
            }
            else if (x < 0)
            {
                Console.WriteLine("Negative");
            }
            else
            {
                Console.WriteLine("Zero");
            }
        }

        public void TestWhile(int max)
        {
            int i = 0;
            while (i < max)
            {
                Console.WriteLine(i);
                i++;
            }
        }

        public void TestFor(int count)
        {
            for (int i = 0; i < count; i++)
            {
                Console.WriteLine(i);
            }
        }

        public void TestForEach()
        {
            List<string> names = new List<string> { "Alice", "Bob", "Charlie" };
            foreach (string name in names)
            {
                Console.WriteLine(name);
            }
        }

        public void TestSwitch(int day)
        {
            switch (day)
            {
                case 1:
                    Console.WriteLine("Monday");
                    break;
                case 2:
                    Console.WriteLine("Tuesday");
                    break;
                default:
                    Console.WriteLine("Other day");
                    break;
            }
        }

        public void TestDoWhile(int n)
        {
            int i = 0;
            do
            {
                Console.WriteLine(i);
                i++;
            } while (i < n);
        }
    }
}
