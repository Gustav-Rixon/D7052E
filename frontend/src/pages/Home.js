import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import UserNavBar from "../components/Navbar";
import { getCookie, setCookie } from "../utils/cookies";
// Json encoding
import jwt_decode from "jwt-decode";

function handleSignOut() {
  setCookie("jwt_cookie", {}, 1);
  window.location.replace("http://localhost:3000");
}

export default function Home() {
  // temp solv
  var obj = getCookie("jwt_cookie");
  var useObject;
  try {
    useObject = jwt_decode(obj);
  } catch (error) {
    useObject = false;
    console.log(error);
  }
  console.log(useObject);

  return (
    <>
      {!useObject && handleSignOut()}
      {useObject.email_verified && (
        <div className="">
          <UserNavBar
            handleSingOut={handleSignOut}
            objectValList={[
              useObject.picture,
              useObject.given_name,
              useObject.family_name,
            ]}
          />
        </div>
      )}
    </>
  );
}
