import React, { useEffect, useState, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// Json encoding
import jwt_decode from "jwt-decode";

import "../styles/app.css";
import { setCookie } from "../utils/cookies";

export default function Login() {
  // State for users callback response values from google oAuth 2.0
  const [user, setUser] = useState({});
  const [jwt, setWEBJWT] = useState("");

  //Decodes the response from google oAuth 2.0 and decodes it.
  function handleCallbackResponse(response, error) {
    var useObject = jwt_decode(response.credential);
    setUser(useObject);
    setWEBJWT(response.credential);

    setCookie("jwt_cookie", response.credential, 1);

    console.log("Error: ");
    console.log(error);
    console.log("Encoded JWT ID token: ");
    console.log(response);
    console.log("Decoded JWT credentials: ");
    console.log(useObject);
  }

  // Google login auth
  const divRef = useRef(null);
  useEffect(() => {
    /* global google */

    google.accounts.id.prompt();

    if (divRef.current) {
      window.google.accounts.id.initialize({
        client_id: process.env.REACT_APP_CLIENT_ID,
        callback: handleCallbackResponse,
      });
      window.google.accounts.id.renderButton(divRef.current, {
        theme: "outline",
        size: "large",
      });
    }
    // eslint-disable-next-line
  }, [divRef.current]);

  async function LoggedIn() {
    async function setJWT() {
      try {
        const response = await fetch("/set_jwt", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            jwt: jwt,
            email: user.email,
          }),
        });
        const data = await response.json();
        console.log(data);
      } catch (err) {
        console.log(err);
      }
    }

    await setJWT();
    window.location.replace("http://localhost:3000/home");
  }

  console.log(process.env);

  return (
    <div className="App">
      <div id="signInDiv" class="font-monospace">
        <center>
          <div ref={divRef} />
        </center>
      </div>
      {!process.env.REACT_APP_CLIENT_ID &&
        alert("Missing or Invalid Google OAuth 2 Key")}
      {user.email_verified && LoggedIn()}
    </div>
  );
}
