import React from "react";
import { Routes, Route, Link, Outlet, NavLink, Navigate, useNavigate } from 'react-router-dom';
import { Box, Grid } from "@chakra-ui/react"

import useAuth from '../AuthProvider';
import SignIn from "../SignIn";


export default function Router() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Landing />} />
        <Route path="landing" element={<Landing />} />
        <Route
          path="home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="signin" element={<SignIn />} />
        <Route path="*" element={<NoMatch />} />
      </Route>
    </Routes>
  )
}

function Layout() {

  const style = ({ isActive }) => ({
    fontWeight: isActive ? 'bold' : 'normal',
  });

  return (
    <>
      <nav
        style={{
          borderBottom: 'solid 1px',
          paddingBottom: '1rem',
        }}
      >


        <Grid templateColumns='repeat(6, 1fr)' gap={1} height='20px'>

          <NavLink to="/home" style={style}>Home</NavLink>
          <NavLink to="/signin" style={style}>Sign In</NavLink>
        </Grid>

      </nav>
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        width: '100vw'
      }}>


        <Outlet />

      </div>
    </>
  );

}

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (!user) {
    return <Navigate to="/landing" />;
  }

  return children;
}

function Landing() {
  return <h2>Landing (Public: anyone can access this page)</h2>;
};


function NoMatch() {
  return (<p>There's nothing here: 404!</p>);
};


//////////
function Home() {
  const { user, logout } = useAuth();

  return (
    <div>
      <p>Hello {user}</p>

      <button type="button" onClick={logout}>
        Logout
      </button>
    </div>
  );
}
