import React, { useState, useEffect } from "react";

function Whitelist() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("http://localhost:5000/whitelist");
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>An error occurred: {error.message}</p>;
  }

  return (
    <div
      style={{
        height: "450px",
        overflowY: "scroll",
        width: "fit-content",
        padding: "15px",
        border: "2px solid #ccc",
      }}
    >
      <style>
        {`
          div::-webkit-scrollbar {
            width: 8px;
          }

          div::-webkit-scrollbar-thumb {
            background-color: #ccc;
            border-radius: 10px;
          }
        `}
      </style>
      {data.length === 0 ? (
        <p>No data to display</p>
      ) : (
        <>
          <h3>Whitelist</h3>
          <ul>
            {data.map((item) => (
              <li key={item.email}>
                <p>Email: {item.email}</p>
                <p>Admin: {item.admin ? "Yes" : "No"}</p>
                <p>Owner: {item.owner ? "Yes" : "No"}</p>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default Whitelist;
