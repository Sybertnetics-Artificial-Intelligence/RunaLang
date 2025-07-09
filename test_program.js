// Generated JavaScript code from Runa
// Natural language programming made executable

// Helper functions for Runa built-ins

function calculateInterest(principal, rate, years = 1) {
    return principal * rate * years;
}

function calculateSum(values, multiplier = 1) {
    return values.reduce((sum, val) => sum + val, 0) * multiplier;
}

function calculateAverage(numbers) {
    if (numbers.length === 0) return 0;
    return numbers.reduce((sum, num) => sum + num, 0) / numbers.length;
}

function main() {
    // Local variables
    let count;
    let message;
    let tmp_1;

    message = "Hello from Runa CLI!";
    console.log(message);
    count = 42;
    tmp_1 = count > 10;
    if (tmp_1) {
        console.log("Large number");
    } else {
        console.log("Small number");
    }
}

// Main execution
if (require.main === module) {
    main();
}
