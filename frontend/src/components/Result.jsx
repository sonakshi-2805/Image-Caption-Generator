import React, { useEffect, useState } from 'react'
import Loader from './Loader';
import '../bgvid.mp4';
import { useSpeechSynthesis } from 'react-speech-kit'
import TransButton from './TransButton';
import Upload from './Upload';
import { Link } from "react-router-dom"
import { useNavigate } from 'react-router-dom';


const Result = (props) => {

  const [preview, setPreview] = useState();
  const [caption, setCaption] = useState("");
  const [cap, setCap] = useState("");
  const { speak } = useSpeechSynthesis();
  const [bool1, setBool] = useState(false);


  const handleListen = () => {
    speak({ text: caption })
  }


  const callback = (lang) => {
    setCaption(lang);
  }


  const fetchCaption = async () => {

    console.log("FETCH CAPTION FUNCTION CALLED");

    const formData = new FormData();
    formData.append('file', props.img);


    try {

      const url = "http://localhost:5000/after";

      console.log("Calling Flask:", url);


      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });


      console.log("Response Status:", response.status);


      const data = await response.json();


      console.log("Flask Data:", data);


      setCaption(data.caption);
      setCap(data.caption);


    } catch (err) {

      console.log("CAPTION ERROR:", err);

    }

  }



  useEffect(() => {

    console.log("IMAGE RECEIVED:", props.img);

    setPreview(URL.createObjectURL(props.img));

    fetchCaption();

  }, []);



  let navigate = useNavigate();


  const handleLogout = () => {

    localStorage.removeItem('token');

    navigate("/");

  }



  const handleClick = () => {

    setBool(true);

  }



  return (
    <>

      {!bool1 &&

      <div className="result-page">

        {
        localStorage.getItem('token') &&
        <button 
        onClick={handleLogout} 
        className='result-logout'
        style={{ position:'absolute', right:'118px', top:'27px' }}
        >
          Logout
        </button>
        }


        <div className="result-window" style={{position:'relative'}}>


          <button 
          style={{color:'black', marginLeft:"-31rem"}} 
          className='result-logout'
          onClick={handleClick}
          >
            Go back
          </button>


          <h1 className="result-heading">
            Result page
          </h1>


          {
          preview &&
          <img 
          className="result-image" 
          src={preview} 
          alt="image" 
          />
          }


          {
          caption ?

          <p className="result-caption">
            {caption}
          </p>

          :

          <Loader />

          }



          <div className='extra-button'>


          {
          localStorage.getItem('token') &&

          <button 
          className="text-to-speech-btn"
          onClick={handleListen}
          >
            Convert text to speech
          </button>

          }


          {
          localStorage.getItem('token') &&

          <TransButton 
          callback={callback}
          cap={cap}
          />

          }


          </div>



          {
          !localStorage.getItem('token') &&
          <Link to='/login'>
          Sign in to translate and hear the caption
          </Link>
          }


        </div>


      </div>

      }



      {
      bool1 &&
      <Upload />
      }


    </>
  );

}


export default Result;
