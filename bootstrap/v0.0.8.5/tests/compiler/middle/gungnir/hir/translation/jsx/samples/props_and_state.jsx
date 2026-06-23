// Props and State

function UserCard(props) {
  return (
    <div className="card">
      <h2>{props.name}</h2>
      <p>{props.email}</p>
      <button onClick={props.onDelete}>Delete</button>
    </div>
  );
}

function UserList() {
  const users = [
    { id: 1, name: "Alice", email: "alice@example.com" },
    { id: 2, name: "Bob", email: "bob@example.com" }
  ];

  return (
    <div>
      {users.map(user => (
        <UserCard
          key={user.id}
          name={user.name}
          email={user.email}
          onDelete={() => console.log("Delete", user.id)}
        />
      ))}
    </div>
  );
}
