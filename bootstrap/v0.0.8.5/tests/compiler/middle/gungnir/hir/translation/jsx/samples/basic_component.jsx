// Basic React Component

function Welcome() {
  return <h1>Hello, World!</h1>;
}

const Greeting = () => <div>Welcome to React</div>;

function App() {
  return (
    <div className="container">
      <Welcome />
      <Greeting />
    </div>
  );
}
