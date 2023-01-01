import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { getCookie } from "../utils/cookies";
import jwt_decode from "jwt-decode";

// Load cookie value.
const obj = getCookie("jwt_cookie");
let useObject;
try {
  useObject = jwt_decode(obj);
} catch (error) {
  useObject = false;
  console.log(error);
}

const removeUserFromWhitelist = async (user) => {
  const response = await fetch("/whitelist/remove", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify([user, { email: useObject.email }]),
  });

  if (response.ok) {
    window.alert("User removed from whitelist successfully");
    return response;
  } else {
    window.alert("Error removing user from whitelist ");
    throw new Error(response);
  }
};

const RemoveUserForm = () => {
  const [email, setEmail] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Create the new user object with the form data
      const user = {
        email: email,
      };
      // Call the addUserToWhitelist function with the new user object
      const result = await removeUserFromWhitelist(user);
      console.log(result);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="apicontent mt-4">
        <h3 className="apicontenth3">Remove User</h3>
        <div className="adduser">
          <form onSubmit={handleSubmit} className="mb-3">
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                required
                onChange={(event) => setEmail(event.target.value)}
                className="form-control"
              />
            </div>
            <button type="submit" className="btn btn-primary mt-4">
              Remove User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default RemoveUserForm;
