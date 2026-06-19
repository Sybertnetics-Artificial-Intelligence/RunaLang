// Namespaces and using directives
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Company.Product.Feature
{
    public class NamespaceDemo
    {
        public void UseSystemTypes()
        {
            string text = "Hello";
            List<int> numbers = new List<int>();
            StringBuilder builder = new StringBuilder();
            DateTime now = DateTime.Now;
        }

        public void UseLinq()
        {
            var numbers = new[] { 1, 2, 3, 4, 5 };
            var evens = numbers.Where(n => n % 2 == 0);
            var sum = numbers.Sum();
        }
    }
}

namespace Company.Product.AnotherFeature
{
    public class AnotherClass
    {
        public void DoWork()
        {
            Console.WriteLine("Working...");
        }
    }
}
