import React from 'react'

import { Helmet } from 'react-helmet'

import Header from '../components/header'
import './home.css'

const Home = (props) => {
  return (
    <div className="home-container">
      <Helmet>
        <title>Narrow Determined Seahorse</title>
        <meta property="og:title" content="Narrow Determined Seahorse" />
      </Helmet>
      <Header></Header>
    </div>
  )
}

export default Home
