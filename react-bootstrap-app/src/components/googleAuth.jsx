function GoogleAuth({ divRef }) {
  return (
      <div id="signInDiv" class="font-monospace">
        <center>
          <span style={{ marginRight: ".5rem" }}>Login: </span>
          <div ref={divRef} />
        </center>
      </div>
  );
}

export default GoogleAuth;
