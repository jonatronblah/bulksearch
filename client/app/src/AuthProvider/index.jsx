import React from 'react';
import { createContext, useContext, useState, useEffect, useMemo } from 'react';
import { useLocation } from "react-router-dom";

import { parseCookie } from '../utility/parseCookie';

const AuthContext = createContext({});

export function AuthProvider({ children, }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingInitial, setLoadingInitial] = useState(true);
  const [error, setError] = useState();

  const location = useLocation();

  async function findUser() {
    await fetch('http://localhost/api/users/me', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }).then((response) => response.json())
      .then(data =>
        setUser(data.email))
      .catch((_error) => { })
      .finally(() => setLoadingInitial(false));
  }

  useEffect(() => {
    if (error) setError(null);
  }, [location.pathname]);

  useEffect(() => {
    findUser();
  }, []);

  async function login(payload) {
    const response = await fetch('http://localhost/api/auth/jwt/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: payload
    }).then(findUser)
      .catch((error) => setError(error))
      .finally(() => setLoading(false))

  }




  async function logout() {
    return fetch('http://localhost/api/auth/jwt/logout', {
      method: 'POST'
    })
      .then(() => setUser(undefined));

  }

  const memoedValue = useMemo(
    () => ({
      user,
      loadingInitial,
      loading,
      error,
      login,
      logout
    }),
    [user, loading, error]
  );

  // We only want to render the underlying app after we
  // assert for the presence of a current user.
  return (
    <AuthContext.Provider value={memoedValue}>
      {!loadingInitial && children}
    </AuthContext.Provider>
  );
}

export default function useAuth() {
  return useContext(AuthContext);
}
