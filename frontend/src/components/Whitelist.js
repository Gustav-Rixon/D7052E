import "../styles/app.css";

const Whitelist = ({ data }) => {
  return (
    <div>
      {data.length === 0 ? (
        <p>No data to display</p>
      ) : (
        <>
          <div className="whitelist">
            <h3 className="whitelistH3">Whitelist</h3>
            <div className="scrollable">
              <ul>
                {data.map((item) => (
                  <li key={item.email}>
                    <p>Email: {item.email}</p>
                    <p>Admin: {item.admin ? "Yes" : "No"}</p>
                    <p>Owner: {item.owner ? "Yes" : "No"}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Whitelist;
