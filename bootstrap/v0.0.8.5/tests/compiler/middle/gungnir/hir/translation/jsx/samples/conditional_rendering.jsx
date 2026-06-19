// Conditional Rendering

function LoginButton({ isLoggedIn }) {
  return (
    <div>
      {isLoggedIn ? (
        <button>Logout</button>
      ) : (
        <button>Login</button>
      )}
    </div>
  );
}

function UserStatus({ user }) {
  return (
    <>
      {user && <div>Welcome, {user.name}</div>}
      {!user && <div>Please log in</div>}
    </>
  );
}

function MessageList({ messages }) {
  return (
    <div>
      {messages.length > 0 ? (
        <ul>
          {messages.map(msg => <li key={msg.id}>{msg.text}</li>)}
        </ul>
      ) : (
        <p>No messages</p>
      )}
    </div>
  );
}
