// TypeScript JSX

interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

function Button({ label, onClick, disabled = false }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}

interface User {
  id: number;
  name: string;
  email: string;
}

function UserCard({ user }: { user: User }) {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
}

type Theme = "light" | "dark";

interface AppProps {
  theme: Theme;
  children: React.ReactNode;
}

function App({ theme, children }: AppProps) {
  return (
    <div className={`app-${theme}`}>
      {children}
    </div>
  );
}
