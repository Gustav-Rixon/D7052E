import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import UserNavBar from "../components/Navbar";
import { getCookie, setCookie } from "../utils/cookies";
import jwt_decode from "jwt-decode";
import Whitelist from "../components/Whitelist";
import Footer from "../components/Footer";
import AddUserForm from "../components/AddUser";
import Camera from "../components/Camera";

function handleSignOut() {
  setCookie("jwt_cookie", "", 1);
  window.location.replace("http://localhost:3000");
}

// Load cookie value.
const obj = getCookie("jwt_cookie");
let useObject;
try {
  useObject = jwt_decode(obj);
} catch (error) {
  useObject = false;
  console.log(error);
}

export default function Home() {
  const [visible, setVisible] = useState(false);

  function toggleVisibility() {
    setVisible((prevVisible) => !prevVisible);
  }

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch("/whitelist");
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

  //console.log(useObject);
  //console.log(visible);

  return (
    <>
      {
        !useObject &&
          handleSignOut() /* checks if you have a jwt token, if not you get sent back to localhost/3000 */
      }
      {useObject.email_verified && (
        <div className="">
          <UserNavBar
            handleSingOut={handleSignOut}
            objectValList={[
              useObject.picture,
              useObject.given_name,
              useObject.family_name,
            ]}
            onToggle={toggleVisibility}
          />
          <div className="page-container">
            {!visible && (
              <>
                <aside>
                  <Whitelist data={data} />
                  <AddUserForm currentuser={useObject.email} />
                </aside>
              </>
            )}
          </div>
          <Camera />
          <Footer />
        </div>
      )}
    </>
  );
}
