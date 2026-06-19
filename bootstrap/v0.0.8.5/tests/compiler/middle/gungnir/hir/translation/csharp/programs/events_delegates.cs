// Events and delegates
using System;

namespace EventTest
{
    public delegate void NotifyEventHandler(string message);

    public class Publisher
    {
        public event NotifyEventHandler Notify;

        public void RaiseEvent(string message)
        {
            if (Notify != null)
            {
                Notify(message);
            }
        }
    }

    public class Subscriber
    {
        public void OnNotify(string message)
        {
            Console.WriteLine("Received: " + message);
        }
    }

    public class EventDemo
    {
        public void TestEvents()
        {
            Publisher pub = new Publisher();
            Subscriber sub = new Subscriber();

            pub.Notify += sub.OnNotify;
            pub.RaiseEvent("Hello, Events!");
        }
    }
}
