import React from 'react';

import Router from '../Router';
import { AuthProvider } from '../AuthProvider';




export default function App() {

  return (
    <AuthProvider>
      <Router />
    </AuthProvider>
  );
};

