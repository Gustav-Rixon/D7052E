import React from "react";

const MultipleLiveStreaming = () => {
  const cameras = [
    "http://127.0.0.1:1337/video_feed/0/",
    "http://127.0.0.1:1337/video_feed/1/",
    "http://127.0.0.1:1337/video_feed/2/",
    "http://127.0.0.1:1337/video_feed/3/",
    "http://127.0.0.1:1337/video_feed/4/",
    "http://127.0.0.1:1337/video_feed/5/",
    "http://127.0.0.1:1337/video_feed/6/"
  ];

  return (
    <><h3 className="mx-auto mt-3">Multiple Live Streaming</h3><div className="cameras-container">
      {cameras.map((camera, index) => (
        <img src={camera} alt={`camera ${index}`} key={index} className="camera-unit" />
      ))}
    </div></>
  );
};

export default MultipleLiveStreaming;
