

export default function postData(path, payload) {
  try {
    return fetch(`/${path}`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })//.then((response) => response.json())

  } catch (error) {
    console.log("error", error);
  }
};


