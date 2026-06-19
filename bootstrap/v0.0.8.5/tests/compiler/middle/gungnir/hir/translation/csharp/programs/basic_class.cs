// Basic class with fields and methods
using System;

namespace TestNamespace
{
    public class Person
    {
        private string name;
        private int age;

        public Person(string name, int age)
        {
            this.name = name;
            this.age = age;
        }

        public void Greet()
        {
            Console.WriteLine("Hello, " + name);
        }

        public int GetAge()
        {
            return age;
        }

        public static void Main(string[] args)
        {
            Person p = new Person("Alice", 30);
            p.Greet();
        }
    }
}
