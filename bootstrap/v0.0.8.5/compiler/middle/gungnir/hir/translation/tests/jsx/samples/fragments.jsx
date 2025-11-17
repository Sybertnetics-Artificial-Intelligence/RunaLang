// JSX Fragments

function Table() {
  return (
    <table>
      <tr>
        <Columns />
      </tr>
    </table>
  );
}

function Columns() {
  return (
    <>
      <td>Column 1</td>
      <td>Column 2</td>
      <td>Column 3</td>
    </>
  );
}

function FragmentWithKey() {
  const items = ["A", "B", "C"];

  return (
    <div>
      {items.map(item => (
        <>
          <h3>{item}</h3>
          <p>Description for {item}</p>
        </>
      ))}
    </div>
  );
}
