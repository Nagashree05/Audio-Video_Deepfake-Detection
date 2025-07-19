import axios from 'axios';
import React, { useState } from 'react';

function BackendStatus() {
  const [status, setStatus] = useState<string | null>(null);

  const checkBackend = async () => {
    try {
      const response = await axios.get('https://audio-videodeepfake-detection-production.up.railway.app/api/health');
      setStatus(response.data.status);
    } catch (error) {
      setStatus('Backend not reachable');
    }
  };

  return (
    <div>
      <button onClick={checkBackend}>Check Backend Connection</button>
      {status && <p>Status: {status}</p>}
    </div>
  );
}

export default BackendStatus;
