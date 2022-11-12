import React, { useEffect, useState, useRef } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

// Json encoding
import jwt_decode from "jwt-decode";

// Json data.
import data from "../data/whitelist.json";

// Css
import "../styles/Home.css";

//Components
import UserNavBar from "../components/userNavbar";
import WhiteListContent from "../components/whiteListContent";
import GoogleAuth from "../components/googleAuth";

export default function App({ useObject }) {
  const [user, setUser] = useState({});

  function handleCallbackResponse(response, error) {
    var useObject = jwt_decode(response.credential);

    if (data.Whitelist.find((e) => e.email === useObject.email)) {
      document.getElementById("signInDiv").hidden = true;

      for (var i = 0; i < data.Whitelist.length; i++) {
        if (
          data.Whitelist[i].email === useObject.email &&
          data.Whitelist[i].admin === true
        ) {
          Object.assign(useObject, { admin: data.Whitelist[i].admin });
        }
      }
    } else alert("Not a Whitelisted user!");

    setUser(useObject);

    console.log("Error: " + error);
    console.log("Encoded JWT ID token: " + response);
    console.log("Credentials: " + response.credential);
    console.log(useObject);
  }

  //Signout click
  const handleSingOut = () => {
    setUser({});
    google.accounts.id.prompt();
    document.getElementById("signInDiv").hidden = false;
  };

  // Google login auth
  const divRef = useRef(null);
  useEffect(() => {
    /* global google */
    if (user.name === undefined) {
      google.accounts.id.prompt();
    }

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
  }, [divRef.current]);

  return (
    <div className="App">
      <GoogleAuth divRef={divRef} />

      {user.email_verified && (
        <UserNavBar
          handleSingOut={handleSingOut}
          objectVals={[user.picture, user.given_name, user.family_name]}
        />
      )}

      {user.admin && <WhiteListContent />}
    </div>
  );
}
