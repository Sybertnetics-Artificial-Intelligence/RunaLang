// Nullable value types
using System;

namespace NullableTest
{
    public class NullableTypes
    {
        public void TestNullableInts()
        {
            int? nullableInt = null;
            int? anotherInt = 42;

            if (nullableInt.HasValue)
            {
                int value = nullableInt.Value;
            }

            int definiteValue = nullableInt ?? 0;
        }

        public void TestNullableDoubles()
        {
            double? temperature = null;
            temperature = 98.6;

            if (temperature != null)
            {
                double t = temperature.Value;
            }
        }

        public void TestNullableBools()
        {
            bool? flag = null;
            flag = true;

            bool actualFlag = flag.GetValueOrDefault();
        }

        public int? GetNullableValue(bool shouldReturnNull)
        {
            if (shouldReturnNull)
            {
                return null;
            }
            return 100;
        }
    }
}
