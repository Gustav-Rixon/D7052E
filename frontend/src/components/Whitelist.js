import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/app.css";

const Whitelist = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/whitelist");
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  //Whitelist
  useEffect(() => {
    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 30000); // update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>An error occurred: {error.message}</p>;
  }

  return (
    <div>
      {data.length === 0 ? (
        <p>No data to display</p>
      ) : (
        <>
          <div className="apicontent">
            <h3 className="apicontenth3">Whitelist</h3>
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
