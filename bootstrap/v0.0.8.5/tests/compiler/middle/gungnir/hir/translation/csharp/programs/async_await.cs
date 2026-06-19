// Async/await patterns
using System;
using System.Threading.Tasks;

namespace AsyncTest
{
    public class AsyncOperations
    {
        public async Task<int> FetchDataAsync()
        {
            await Task.Delay(1000);
            return 42;
        }

        public async Task<string> GetMessageAsync()
        {
            string message = await FetchMessageAsync();
            return message;
        }

        private async Task<string> FetchMessageAsync()
        {
            await Task.Delay(500);
            return "Hello, Async!";
        }

        public async void ProcessDataAsync()
        {
            int result = await FetchDataAsync();
            Console.WriteLine(result);
        }

        public async Task<List<int>> GetNumbersAsync()
        {
            await Task.Delay(100);
            List<int> numbers = new List<int> { 1, 2, 3 };
            return numbers;
        }
    }
}
