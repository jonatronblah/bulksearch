export default async function findUser() {
  await fetch('http://localhost/api/users/me', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
};