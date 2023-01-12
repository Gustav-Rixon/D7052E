import React from "react";

const MultipleLiveStreaming = () => {
  return (
    <>
      <div className="CameraStreams">
        <h3 className="mx-auto mt-3">Multiple Live Streaming</h3>
        <img
          src={"http://127.0.0.1:5000/video_feed/0/"}
          width="100%"
          alt=" camera 1"
        />
        <img
          src={"http://127.0.0.1:5000/video_feed/1/"}
          width="100%"
          alt=" camera 2"
        />
      </div>
    </>
  );
};

export default MultipleLiveStreaming;
