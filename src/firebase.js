// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB3JI0fSUEhgIL-EQ-a3K1drzlzf6j-Pd4",
  authDomain: "bdrestaurantes.firebaseapp.com",
  projectId: "bdrestaurantes",
  storageBucket: "bdrestaurantes.firebasestorage.app",
  messagingSenderId: "42699445654",
  appId: "1:42699445654:web:156bd9a7213e0b682db9b7",
  measurementId: "G-MPKS1BG250"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);