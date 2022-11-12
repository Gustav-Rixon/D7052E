import React, { Component } from "react";
import data from "../data/whitelist.json";

class WhiteListContent extends Component {
  render() {
    return (
      <div id="Whitelist" class="font-monospace">
        {data.Whitelist.map((whitelist, i) => {
          var isAdmin = " ";
          whitelist.admin ? (isAdmin = " true") : (isAdmin = " false");
          return (
            <div>
              <div key={i}>
                {whitelist.admin ? (
                  <div>
                    {whitelist.email}
                    {isAdmin}
                  </div>
                ) : (
                  <div>
                    {whitelist.email}
                    {isAdmin}
                  </div>
                )}
              </div>
            </div>
          );
        })}
        <form>
          <label>
            Add User:
            <input type="email" placeholder="example@gmail.com" />
          </label>
          <input type="submit" />
        </form>
      </div>
    );
  }
}
export default WhiteListContent;
