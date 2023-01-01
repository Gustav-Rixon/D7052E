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

const addUserToWhitelist = async (newUser) => {
  const response = await fetch("/whitelist/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify([newUser, { email: useObject.email }]),
  });

  if (response.ok) {
    window.alert("User added to whitelist successfully");
    return response;
  } else {
    window.alert("Error adding user to whitelist ");
    throw new Error(response);
  }
};

const AddUserForm = () => {
  const [email, setEmail] = useState("");
  const [admin, setAdmin] = useState(false);
  const [owner, setOwner] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Create the new user object with the form data
      const newUser = {
        email: email,
        admin: admin,
        owner: owner,
      };
      // Call the addUserToWhitelist function with the new user object
      const result = await addUserToWhitelist(newUser);
      console.log(result);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="apicontent">
        <h3 className="apicontenth3">Add User</h3>
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
            <div className="form-group">
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="admin"
                  checked={admin}
                  onChange={(event) => setAdmin(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="admin" className="form-check-label">
                  Admin
                </label>
              </div>
              <div className="form-check form-check-inline">
                <input
                  type="checkbox"
                  id="owner"
                  alt=""
                  checked={owner}
                  onChange={(event) => setOwner(event.target.checked)}
                  className="form-check-input"
                />
                <label htmlFor="owner" className="form-check-label">
                  Owner
                </label>
              </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Add User
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default AddUserForm;
