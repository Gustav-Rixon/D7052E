import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import UserNavBar from "../components/Navbar";
import { getCookie, setCookie } from "../utils/cookies";
import jwt_decode from "jwt-decode";
import Whitelist from "../components/Whitelist";
import Footer from "../components/Footer";
import { AddUserForm, RemoveUserForm } from "../components/UserForm";
import Camera from "../components/Camera";

function handleSignOut() {
  setCookie("jwt_cookie", "", 1);
  window.location.replace("http://localhost:3000");
}

// Load cookie value.
const obj = getCookie("jwt_cookie");
let jwt_decode_object;
try {
  jwt_decode_object = jwt_decode(obj);
} catch (error) {
  jwt_decode_object = false;
  console.log(error);
}

export default function Home() {
  const [visible, setVisible] = useState(false);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [jwt_api, setJWT] = useState(true);

  function toggleVisibility() {
    setVisible((prevVisible) => !prevVisible);
  }

  // JWT
  useEffect(() => {
    async function fetchJWT() {
      try {
        const response = await fetch("/get_jwt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: jwt_decode_object.email }),
        });
        const data = await response.json();
        setJWT(data.jwt);
      } catch (err) {
        console.log(err);
      }
    }

    fetchJWT();
  }, []);

  //Whitelist
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

  if (jwt_api !== obj) {
    new Promise((r) => setTimeout(r, 2000)); //Ful fix todo fixa idk.
    handleSignOut();
  }

  return (
    <>
      {
        !jwt_decode_object &&
          handleSignOut() /* checks if you have a jwt token, if not you get sent back to localhost/3000 */
      }
      {jwt_decode_object.email_verified && (
        <div>
          <UserNavBar
            handleSingOut={handleSignOut}
            objectValList={[
              jwt_decode_object.picture,
              jwt_decode_object.given_name,
              jwt_decode_object.family_name,
            ]}
            onToggle={toggleVisibility}
          />
          <div className="page-container">
            {visible && (
              <>
                <div className="whitelistContent">
                  <Whitelist data={data} />
                  <div className="containerAddRemove">
                    <AddUserForm />
                    <RemoveUserForm />
                  </div>
                </div>
              </>
            )}
            <Camera />
          </div>
          <Footer />
        </div>
      )}
    </>
  );
}
