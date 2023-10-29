import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import { Input, Button, VStack } from '@chakra-ui/react'

import useAuth from '../AuthProvider';
import UploadForm from "../UploadForm";






export default function Login() {
  const { user, loading, error, login, loadingInitial } = useAuth();


  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new URLSearchParams(new FormData(e.currentTarget)).toString()
    // const username = formData.get("username");
    // const password = formData.get("password");
    // formData.append()
    const token = await login(
      formData
    );
  }

  if (loadingInitial) {
    return <section>Loading...</section>
  }
  if (!user) {
    return (
      <form onSubmit={handleSubmit}>
        <VStack spacing='24px'>
          <Input placeholder='Username' name="username" />
          <Input placeholder='Password' name="password" type="password" />
          <Button type='submit'>Submit</Button>
        </VStack>
        {/* {user && <p>OK</p>} */}
        {error && <p>Bad login/password</p>}
      </form>
    )
  }
  else {
    return <UploadForm></UploadForm>
  }

}