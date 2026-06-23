// Generic types and methods
using System;
using System.Collections.Generic;

namespace GenericTest
{
    public class Box<T>
    {
        private T value;

        public Box(T value)
        {
            this.value = value;
        }

        public T GetValue()
        {
            return value;
        }

        public void SetValue(T newValue)
        {
            value = newValue;
        }
    }

    public class GenericMethods
    {
        public T Max<T>(T a, T b) where T : IComparable<T>
        {
            return a.CompareTo(b) > 0 ? a : b;
        }

        public void TestGenerics()
        {
            Box<int> intBox = new Box<int>(42);
            Box<string> stringBox = new Box<string>("Hello");

            List<int> numbers = new List<int> { 1, 2, 3 };
            Dictionary<string, int> ages = new Dictionary<string, int>();
            ages["Alice"] = 30;
            ages["Bob"] = 25;

            int maxValue = Max<int>(10, 20);
        }
    }
}
