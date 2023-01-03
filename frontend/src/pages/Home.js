import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import UserNavBar from "../components/Navbar";
import { getCookie, setCookie, sleep } from "../utils/utils";
import jwt_decode from "jwt-decode";
import Whitelist from "../components/Whitelist";
import Footer from "../components/Footer";
import {
  AddUserForm,
  DemoteUserForm,
  PromoteUserForm,
  RemoveUserForm,
} from "../components/UserForm";
import Camera from "../components/Camera";
import { CSSTransition } from "react-transition-group";

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
  const [jwt_api, setJWT] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function toggleVisibility() {
    setVisible((prevVisible) => !prevVisible);
  }

  // JWT
  useEffect(() => {
    async function fetchJWT() {
      setLoading(true); // set loading to true before making the request
      try {
        const response = await fetch("/get_jwt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: jwt_decode_object.email }),
        });
        const data = await response.json();
        setJWT(data.jwt);
      } catch (err) {
        setError(err); // set error if there is an error
      }
      setLoading(false); // set loading to false after request is complete
    }

    fetchJWT();
  }, []);

  // Check if web jwt and api jwt are the same
  useEffect(() => {
    const interval = setInterval(() => {
      if (jwt_api !== obj) {
        handleSignOut();
      }
    }, 6000); // 300000 milliseconds = 5 minutes
    return () => clearInterval(interval);
  }, [jwt_api]);

  // State loading and error
  if (loading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>An error occurred: {error.message}</p>;
  }

  sleep(2000).then(() => {
    if (jwt_api !== obj) {
      //handleSignOut();
    }
  });

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
            <CSSTransition
              in={visible}
              timeout={400}
              classNames="list-transition"
              unmountOnExit
              appear
            >
              <div className="whitelistContent">
                <div className="formContainer">
                  <PromoteUserForm />
                  <DemoteUserForm />
                </div>
                <Whitelist />
                <div className="formContainer">
                  <AddUserForm />
                  <RemoveUserForm />
                </div>
              </div>
            </CSSTransition>
            <Camera />
          </div>
          <Footer />
        </div>
      )}
    </>
  );
}
