import React from "react";

const MultipleLiveStreaming = () => {
  return (
    <>
      <div className="col-lg-7">
        <h3 className="mt-3">Multiple Live Streaming</h3>
        <img
          src="{{ url_for('video_feed', id='0') }}"
          width="100%"
          alt=" camera 1"
        />
        <img
          src="{{ url_for('video_feed', id='1') }}"
          width="100%"
          alt=" camera 2"
        />
      </div>
      <img src="{{ url_for('video_feed', id='2') }}" width="100%" alt="" />"
    </>
  );
};

export default MultipleLiveStreaming;
