// Spread Attributes

function Button(props) {
  return <button {...props}>Click me</button>;
}

function Input({ type, ...rest }) {
  return <input type={type} {...rest} />;
}

function Card({ title, children, ...otherProps }) {
  return (
    <div className="card" {...otherProps}>
      <h2>{title}</h2>
      {children}
    </div>
  );
}

function App() {
  const buttonProps = {
    className: "btn",
    onClick: () => console.log("clicked"),
    disabled: false
  };

  return (
    <div>
      <Button {...buttonProps} />
      <Input type="text" placeholder="Enter name" required />
      <Card title="Profile" id="user-card">
        <p>User information</p>
      </Card>
    </div>
  );
}
